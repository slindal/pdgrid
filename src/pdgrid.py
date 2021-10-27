import pandas as pd


def unique_values(df, columns):
    return {column : df[column].drop_duplicates().to_json(orient='records') for column in columns}


def grid_values(df, request):
    df = expand_nodes(df, request)
    return {'rows': df.to_dict(orient='records')}


def expand_nodes(df, request):
    for rowGroup, groupKey in zip((f.get('field') for f in request.get('rowGroupCols')), request.get('groupKeys')):
        df = df.loc[df[rowGroup] == groupKey]
    return df



def expand_nodes_query(df, request):
    '''uses df.query for filtering. Slower on simple operations?!
    
    also needs strings to be backticked
    '''
    if request.get('groupKeys'):
        group_filters = " and ".join("{} == {}".format(rowGroup, value) for rowGroup,value in zip((f.get('field') for f in request.get('rowGroupCols')), request.get('groupKeys')))
        df = df.query(group_filters)
    return df
