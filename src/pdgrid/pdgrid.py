import pandas as pd
import operator
import functools


PDGRID_FILTERS = {
    ('set', None): lambda column, filter_value: column.astype(str).isin(filter_value),
    ('text', 'contains'): lambda column, filter_value: column.str.contains(filter_value),
    ('text', 'notContains'): lambda column, filter_value: ~column.str.contains(filter_value),
    ('text', 'equals'): operator.eq,
    ('text', 'notEquals'): operator.ne,
    ('text', 'startsWith'): lambda column, filter_value: column.str.startswith(filter_value),
    ('text', 'endsWith'): lambda column, filter_value: column.str.endswith(filter_value),
    ('number', 'lessThanOrEqual'): operator.le,
    ('number', 'lessThan'): operator.lt,
    ('number', 'equals'): operator.eq,
    ('number', 'notEquals'): operator.ne,
    ('number', 'greaterThan'): operator.gt,
    ('number', 'greaterThanOrEqual'): operator.ge,
}


def unique_values(df, filter_field):
    return df[filter_field].drop_duplicates().sort_values().tolist()


class column_filter(functools.partial):
    '''Like partial, but allow to pass in leftmost argument last'''
    def __call__(self, column):
        return self.func(column, *self.args)


def operator_processor(column, operator_func, filter1, filter2):
    '''Combine the output of two column filters using the operator (OR, AND) passed in'''
    return operator_func(filter1(column), filter2(column))


def grid_values(df, groupby_columns, selected_groups, aggregation_params, filter_model, sort_fields, sort_ascending, start_row, end_row):
    df = process_filters(df, filter_model)
    df, last_row = sort_and_aggregate(df, groupby_columns, selected_groups, aggregation_params, sort_fields, sort_ascending, start_row, end_row)
    df = df[df.columns]
    return {'rows': df.to_dict(orient='records'),
            'lastRow': last_row
            }


def sort_and_aggregate(df, groupby_columns, selected_groups, aggregation_params, sort_fields, sort_ascending, start_row, end_row):
    aggregation_group = groupby_columns[len(selected_groups)] if len(selected_groups) < len(groupby_columns) else None

    #do we need to aggregate?
    if aggregation_group:
        df = df.set_index(aggregation_group)
        last_row = df.index.nunique()

        sort_agg_params = {f: ('min' if asc else 'max') for f, asc in zip(sort_fields, sort_ascending) if f not in aggregation_params and f != aggregation_group}
        #Do we need to paginate or sort on non aggregated field?
        if pagination := end_row < last_row or start_row > 0 or sort_agg_params:

            if not sort_fields or sort_fields[0] == aggregation_group:
                #only sort by group by column
                ascending = True if not sort_fields else sort_ascending[0]
                sorted_keys = df.index.drop_duplicates().sort_values(ascending=ascending)
            else:
                sort_agg_params.update({k:v for k,v in aggregation_params.items() if k in sort_fields})
                sorted_keys = (df.groupby(level=0)
                               .agg(sort_agg_params)
                               .sort_values(by=sort_fields,
                                            ascending=sort_ascending)
                               ).index

            sorted_keys = sorted_keys[start_row:end_row]
            df = df.loc[sorted_keys] #Filter out unneded groups


        df = df.groupby(level=0).agg(aggregation_params)
        if pagination:
            df = df.loc[sorted_keys] #Group by scrambles order, resort
        df = df.reset_index(drop=False)

    if not aggregation_group or not pagination:
        df = df.sort_values(by=sort_fields, ascending=sort_ascending)
        last_row = df.index.size
        df = df.iloc[start_row:end_row]

    return df, last_row


def process_filters(df, filter_model):
    '''This could possibly be done with df.query, but unclear if it would be faster'''
    for field, filter_function in filter_model.items():
        df = df.loc[filter_function(df[field])]
    return df


def process_aggrid_request(df, request):
    '''AG-Grid specific transform function
    Take in json from aggrid and extract parameters needed to decide how to transform'''
    operator_map = {'OR': operator.or_,
                    'AND': operator.and_}

    agg_lookup = {
        'avg': 'mean'
    }

    def agfilter_to_func(f):
        if 'operator' in f:
            return column_filter(operator_processor,
                            operator_map[f['operator']],
                            agfilter_to_func(f.get('condition1')),
                            agfilter_to_func(f.get('condition2'))
                            )
        elif f.get('filterType') == 'number' and f.get('type') == 'inRange':
            return column_filter(operator_processor,
                            operator_map['AND'],
                            column_filter(PDGRID_FILTERS[('number', 'greaterThanOrEqual')], f.get('filter')),
                            column_filter(PDGRID_FILTERS[('number', 'lessThan')], f.get('filterTo'))
                            )
        else:
            return column_filter(PDGRID_FILTERS[(f['filterType'], f.get('type'))], f.get('values' if f['filterType'] == 'set' else 'filter'))
        
    groupby_columns = [f.get('field') for f in request.get('rowGroupCols', [])]
    aggregation_params = {f.get('field'): agg_lookup.get(f.get('aggFunc'), f.get('aggFunc')) for f in request.get('valueCols') if f.get('aggFunc') is not None and f.get('field') is not None}

    selected_groups = request.get('groupKeys', [])
    sort_fields = [f.get('colId') for f in request.get('sortModel', []) if f.get('colId') not in groupby_columns[:len(selected_groups)]]
    sort_ascending = [f.get('sort') == 'asc' for f in request.get('sortModel', []) if f.get('colId') not in groupby_columns[:len(selected_groups)]]
    filter_model = {}

    for field, f in request.get('filterModel', {}).items():
        filter_model[field] = agfilter_to_func(f)

    #Expanding a group is essentially a single value filter
    for field, filter_value in zip(groupby_columns, selected_groups):
        filter_model[field] = column_filter(operator.eq, filter_value)
        
    start_row = request.get('startRow') or 0
    end_row = request.get('endRow') or 100

    return grid_values(df,
                       groupby_columns,
                       selected_groups,
                       aggregation_params,
                       filter_model,
                       sort_fields,
                       sort_ascending,
                       start_row,
                       end_row)

