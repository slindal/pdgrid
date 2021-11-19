import pandas as pd


def unique_values(df, filter_field):
    return df[filter_field].drop_duplicates().sort_values().astype(str).tolist()


def grid_values(df, request):
    df = process_filters(df, request)
    df = expand_nodes(df, request)
    df = aggregate(df, request)
    lastRow = df.index.size
    df = sort_and_paginate(df, request)
    df = df[df.columns].astype(str) ## Looks like this is what is returned by laravel. Dubious. FIXME
    return {'rows': df.to_dict(orient='records'),
            'lastRow': lastRow
            }


def process_filters(df, request):
    for field, filter_options in request.get('filterModel', {}).items():
        if filter_options.get('filterType') == 'set':
            df = df[df[field].astype(str).isin(filter_options.get('values'))] ## This is a potential error source here! Why send it as string? FIXME
        else:
            raise Exception("Unimplemented filter type")
        
    return df

        
def expand_nodes(df, request):
    for rowGroup, groupKey in zip((f.get('field') for f in request.get('rowGroupCols')), request.get('groupKeys')):
        df = df.loc[df[rowGroup] == groupKey]
    return df


def aggregate(df, request):
    group_keys = request.get('groupKeys') or []
    rowGroups = request.get('rowGroupCols') or []
    aggFields = {f.get('field'): f.get('aggFunc') for f in request.get('valueCols')}
    
    if len(group_keys) < len(rowGroups):
        df = df.groupby(rowGroups[len(group_keys)].get('field')).agg(aggFields).reset_index(drop=False)
    return df
    

def sort_and_paginate(df, request):
    if (sortModel := request.get('sortModel')):
        df = df.sort_values(by=[f.get('colId') for f in sortModel], ascending=[f.get('sort') == 'asc' for f in sortModel])
    start_row = request.get('startRow', 0)
    end_row = request.get('endRow', 1000)
    df = df.iloc[start_row:end_row]
    return df


def expand_nodes_query(df, request):
    '''uses df.query for filtering. Slower on simple operations?!
    
    also needs strings to be backticked
    '''
    if request.get('groupKeys'):
        group_filters = " and ".join("{} == {}".format(rowGroup, value) for rowGroup,value in zip((f.get('field') for f in request.get('rowGroupCols')), request.get('groupKeys')))
        df = df.query(group_filters)
    return df
