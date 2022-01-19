import pandas as pd
import operator
import functools
import itertools

import numpy as np



def unique_values(df, filter_field):
    '''Endpoint that provides a distinct list of values in a column, used by the front end for filtering'''
    return df[filter_field].drop_duplicates().sort_values().tolist()

def grid_values(df, request):

    response = {'secondaryColDefs': {}}
    df = process_filters(df, request)
    df = sort_and_aggregate(df, request, response)

    response['rows'] = df.to_dict(orient='records')

    return response


def pivot(df, request, response):

    df = df.pivot_table(
        index = request.aggregation_group,
        columns = request.pivot_columns,
        values = list(request.aggregation_params),
        aggfunc=request.aggregation_params)

    if not request.aggregation_group:
        df = df.unstack()
        df = pd.DataFrame(columns=df.index, data=[df.values])
    else:
        df.columns = df.columns.swaplevel(0,1)
    
    secondaryColDefs = [
]
    for group, cols in itertools.groupby(sorted(df.columns, key=lambda k: k[0]), key=lambda k: k[0]):
        secondaryColDefs.append({'groupId': str(group),
                                 'headerName': str(group),
                                 'children': [
                                     {'colId': "|".join(str(f) for f in col),
                                      'field': "|".join(str(f) for f in col),
                                      'headerName': f"{request.aggregation_params[col[-1]]}({request.display_names[col[-1]]})"}
                                     for col in cols]
                                 }
                                )
    df.columns = ["|".join(str(f) for f in col) for col in df.columns] 
    
    df = df.replace({np.nan: None})

    response['secondaryColDefs'] = secondaryColDefs
    return df
    
def sort_and_aggregate(df, request, response):

    if request.aggregation_group:
        df = df.set_index(request.aggregation_group)

        groups = df.groupby(request.aggregation_group)
        last_row = groups.ngroups

        #Do we need to paginate or sort on non aggregated field? If so, paginate before aggregating all columns. Huge speed up in some cases!!
        if pagination := request.end_row < last_row or request.start_row > 0 or request.sort_agg_params:

            if not request.sort_fields or request.sort_fields[0] == request.aggregation_group:
                #only sort by group by column
                ascending = True if not request.sort_fields else request.sort_ascending[0]
                sorted_keys = df.index.drop_duplicates().sort_values(ascending=ascending)
            elif request.do_pivot:
                pivot_sort_column = next(iter(request.sort_agg_params.keys()))
                pre_pivot_column = pivot_sort_column.split('|')[-1]
                sorted_keys = df.pivot_table(index=df.index, columns=request.pivot_columns, values=[pre_pivot_column], aggfunc=request.aggregation_params.get(pre_pivot_column))
                sorted_keys.columns = ["|".join(str(f) for f in col[::-1]) for col in sorted_keys.columns] 
                sorted_keys = sorted_keys.sort_values(by=request.sort_fields, ascending=request.sort_ascending).index

            else:    
                agg_params = {**request.sort_agg_params, **{k:v for k,v in request.aggregation_params.items() if k in request.sort_fields}}
                sorted_keys = (groups
                               .agg(agg_params)
                               .sort_values(by=list(request.sort_columns.keys()),
                                            ascending=list(request.sort_columns.values()))
                               ).index
                
            sorted_keys = sorted_keys[request.start_row:request.end_row]
            df = df.loc[sorted_keys] #Filter out unneded groups before aggregating

        if request.do_pivot:
            df = pivot(df, request, response)
        else:
            df = df.groupby(level=0).agg(request.aggregation_params)
        if pagination:
            df = df.loc[sorted_keys] #Group by scrambles order, resort
        df = df.reset_index(drop=False)

    #Pivot without aggregation group
    elif request.do_pivot:
        df = pivot(df, request, response)
        
    if (not request.aggregation_group or not pagination):
        df = df.sort_values(by=request.sort_fields, ascending=request.sort_ascending)
        last_row = df.index.size
        df = df.iloc[request.start_row:request.end_row]

    response['lastRow'] = last_row
    return df


def process_filters(df, request):
    '''This could possibly be done with df.query, but unclear if it would be faster'''
    for field, filter_function in request.filters.items():
        df = df.loc[filter_function(df[field])]
    return df

