import pandas as pd


def unique_values(df, columns):
    return {column : df[column].drop_duplicates().to_json(orient='records') for column in columns}


def grid_values(df, request):
    df = expand_nodes(df, request)
    return {'rows': df.to_json(orient='records')}




def expand_nodes(df, request):
    if request.get('groupKeys'):
        group_filters = " and ".join("{} == {}".format(rowGroup, value) for rowGroup,value in zip((f.get('field') for f in request.get('rowGroupCols')), request.get('groupKeys')))
        df = df.query(group_filters)
    return df
