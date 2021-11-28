import pandas as pd


def unique_values(df, filter_field):
    return df[filter_field].drop_duplicates().sort_values().astype(str).tolist()


def process_aggrid_request(df, request):
    groupby_columns = [f.get('field') for f in request.get('rowGroupCols', [])]
    aggregation_params = {f.get('field'): f.get('aggFunc') for f in request.get('valueCols') if f.get('aggFunc') is not None and f.get('field') is not None}

    selected_groups = request.get('groupKeys', [])
    sort_fields = [f.get('colId') for f in request.get('sortModel', []) if f.get('colId') not in groupby_columns[:len(selected_groups)]]
    sort_ascending = [f.get('sort') == 'asc' for f in request.get('sortModel', []) if f.get('colId') not in groupby_columns[:len(selected_groups)]]
    filter_model = request.get('filterModel', {})
    start_row = request.get('startRow') or 0
    end_row = request.get('endRow') or 200
    
    return grid_values(df,
                       groupby_columns,
                       selected_groups,
                       aggregation_params,
                       filter_model,
                       sort_fields,
                       sort_ascending,
                       start_row,
                       end_row)
    

def grid_values(df, groupby_columns, selected_groups, aggregation_params, filter_model, sort_fields, sort_ascending, start_row, end_row):
    df = process_filters(df, filter_model)
    df = expand_selected(df, groupby_columns, selected_groups)
    df, last_row = sort_and_aggregate(df, groupby_columns, selected_groups, aggregation_params, sort_fields, sort_ascending, start_row, end_row)
    df = df[df.columns].astype(str) ## Looks like this is what is returned by laravel. Dubious. FIXME
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
    for field, filter_options in  filter_model.items():
        if filter_options.get('filterType') == 'set':
            df = df[df[field].astype(str).isin(filter_options.get('values'))] ## This is a potential error source here! Why send it as string? FIXME
        else:
            raise Exception("Unimplemented filter type")
        
    return df

        
def expand_selected(df, groupby_columns, selected_groups):
    for groupby_column, selected_group in zip(groupby_columns, selected_groups):
        df = df.loc[df[groupby_column] == selected_group]
    return df


def aggregate(df, request):
    group_keys = request.get('groupKeys') or []
    rowGroups = request.get('rowGroupCols') or []
    if len(group_keys) < len(rowGroups):


        aggFields = {f.get('field'): f.get('aggFunc') for f in request.get('valueCols')}

        df = df.groupby(rowGroups[len(group_keys)].get('field')).agg(aggFields).reset_index(drop=False)
    return df
    

def expand_nodes_query(df, request):
    '''uses df.query for filtering. Slower on simple operations?!
    
    also needs strings to be backticked
    '''
    if request.get('groupKeys'):
        group_filters = " and ".join("{} == {}".format(rowGroup, value) for rowGroup,value in zip((f.get('field') for f in request.get('rowGroupCols')), request.get('groupKeys')))
        df = df.query(group_filters)
    return df
