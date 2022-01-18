import functools
import operator

from .pdgrid import grid_values

class GridRequest():

    def __init__(self, request):
        self.request = request

    @property
    def aggregation_group(self):
        '''The column to group the data by (first unexpanded groupby column)'''
        if len(self.selected_groups) < len(self.groupby_columns):
            return self.groupby_columns[len(self.selected_groups)]
        return None


class column_filter(functools.partial):
    '''Like partial, but allow to pass in leftmost argument last'''
    def __call__(self, column):
        return self.func(column, *self.args)


def operator_processor(column, operator_func, filter1, filter2):
    '''Combine the output of two column filters using the operator (OR, AND) passed in'''
    return operator_func(filter1(column), filter2(column))

operator_map = {'OR': operator.or_,
                'AND': operator.and_}



class AgGridRequest(GridRequest):

    agg_lookup = {
        'avg': 'mean'
    }

    FILTER_OPERATORS = {
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


    def filter_to_func(self, f):
        if 'operator' in f:
            return column_filter(operator_processor,
                                 operator_map[f['operator']],
                                 self.filter_to_func(f.get('condition1')),
                                 self.filter_to_func(f.get('condition2'))
                                 )
        elif f.get('filterType') == 'number' and f.get('type') == 'inRange':
            return column_filter(operator_processor,
                                 operator_map['AND'],
                                 column_filter(self.FILTER_OPERATORS[('number', 'greaterThanOrEqual')], f.get('filter')),
                                 column_filter(self.FILTER_OPERATORS[('number', 'lessThan')], f.get('filterTo'))
                                 )
        else:
            return column_filter(self.FILTER_OPERATORS[(f['filterType'], f.get('type'))], f.get('values' if f['filterType'] == 'set' else 'filter'))
        
    @property
    def groupby_columns(self):
        '''The grouped columns in the grid'''
        return [f.get('field') for f in self.request.get('rowGroupCols', [])]

    @property
    def selected_groups(self):
        '''The groups that have been expanded'''
        return self.request.get('groupKeys', [])

    @property
    def aggregation_params(self):
        return {f.get('field'): self.agg_lookup.get(f.get('aggFunc'), f.get('aggFunc'))
                for f in self.request.get('valueCols')
                if f.get('aggFunc') is not None
                and f.get('field') is not None}
            
    @property
    def sort_columns(self):
        return {f.get('colId'):f.get('sort') == 'asc' for f in self.request.get('sortModel', [])
                if f.get('colId') not in self.groupby_columns[:len(self.selected_groups)]}

    @property
    def start_row(self):
        return self.request.get('startRow')

    @property
    def end_row(self):
        return self.request.get('endRow')

    @property
    def filter_model(self):
        return { field: self.filter_to_func(f) for field, f in self.request.get('filterModel', {}).items()}

    @property
    def expanded_column_filters(self):
        return { field: column_filter(operator.eq, filter_value) for field, filter_value in zip(self.groupby_columns, self.selected_groups)}
    
    @property
    def filters(self):
        return {**self.filter_model,  **self.expanded_column_filters}

    @property
    def pivot_mode(self):
        return self.request.get('pivotMode', False)

    @property
    def pivot_columns(self):
        return [f.get('field') for f in self.request.get('pivotCols', [])][:1]

    @property
    def do_pivot(self):
        return self.pivot_mode and self.pivot_columns
    
    @property
    def sort_agg_params(self):
        '''Columns needed for sorting but not being aggregated'''
        return {f: ('min' if asc else 'max') for f, asc in self.sort_columns.items()
                if f not in self.aggregation_params and f != self.aggregation_group}

    @property
    def sort_fields(self):
        return list(self.sort_columns.keys())

    @property
    def sort_ascending(self):
        return list(self.sort_columns.values())

    @property
    def display_names(self):
        return {f['field']: f['displayName'] for f in self.request['valueCols']}



def aggrid_values(df, request):
    '''Entry point for aggrid request'''
    return grid_values(df, AgGridRequest(request))
