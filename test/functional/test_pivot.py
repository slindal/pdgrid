from pdgrid.pdgrid import grid_values
from pdgrid.aggrid import AgGridRequest
import pandas as pd
import os


def test_pivot_mode_off_has_pivot_cols():

    df = pd.DataFrame(columns=['a', 'b', 'c', 'd'],
                      data= [['a', 1, 10, True],
                             ['b', 2, 20, True],
                             ['b', 3, 30, False]]
                      )

    
    request = {
        'startRow': 0,
        'endRow': 10,
        'rowGroupCols': [{'field': 'a'}],
        'valueCols': [
            {
                'field': 'b',
                'displayName': 'BB',
                'aggFunc': 'mean',
            },
            {
                'field': 'c',
                'displayName': 'C',
                'aggFunc': 'sum',
            },
        ],
            
        'pivotMode': False,
        'pivotCols': [{'field': 'd'}],
    }


    response = grid_values(df, AgGridRequest(request))


    assert(response['rows'] == [{'a': 'a', 'b': 1.0, 'c': 10}, {'a': 'b', 'b': 2.5, 'c': 50}])
    assert(response['secondaryColDefs'] == {})
    assert(response['lastRow'] == 2)


def test_pivot_mode_on_has_pivot_cols():

    df = pd.DataFrame(columns=['a', 'b', 'c', 'd'],
                      data= [['a', 1, 10, True],
                             ['b', 2, 20, True],
                             ['b', 3, 30, False],
                             ['b', 4, 40, False]]
                      )

    
    request = {
        'startRow': 0,
        'endRow': 10,
        'rowGroupCols': [{'field': 'a'}],
        'valueCols': [
            {
                'field': 'b',
                'displayName': 'BB',
                'aggFunc': 'mean',
            },
            {
                'field': 'c',
                'displayName': 'C',
                'aggFunc': 'sum',
            },
        ],
            
        'pivotMode': True,
        'pivotCols': [{'field': 'd'}],
    }


    response = grid_values(df, AgGridRequest(request))

    assert(response['rows'] == [{'a': 'a', 'False|b': None, 'True|b': 1.0, 'False|c': None, 'True|c': 10.0},
                                {'a': 'b', 'False|b': 3.5, 'True|b': 2.0, 'False|c': 70.0, 'True|c': 20.0}])

    assert(response['secondaryColDefs'] ==
           [{'groupId': 'False', 'headerName': 'False', 'children': [
               {'colId': 'False|b', 'field': 'False|b', 'headerName': 'mean(BB)'},
               {'colId': 'False|c', 'field': 'False|c', 'headerName': 'sum(C)'}]},
            {'groupId': 'True', 'headerName': 'True', 'children': [
                {'colId': 'True|b', 'field': 'True|b', 'headerName': 'mean(BB)'},
                {'colId': 'True|c', 'field': 'True|c', 'headerName': 'sum(C)'}]}
            ]
           )

    assert(response['lastRow'] == 2)



def test_pivot_mode_on_has_pivot_cols_no_group_cols():

    df = pd.DataFrame(columns=['a', 'b', 'c', 'd'],
                      data= [['a', 1, 10, True],
                             ['b', 2, 20, True],
                             ['b', 3, 30, False],
                             ['b', 4, 40, False]]
                      )

    
    request = {
        'startRow': 0,
        'endRow': 10,
        'rowGroupCols': [],
        'valueCols': [
            {
                'field': 'b',
                'displayName': 'BB',
                'aggFunc': 'mean',
            },
            {
                'field': 'c',
                'displayName': 'C',
                'aggFunc': 'sum',
            },
        ],
            
        'pivotMode': True,
        'pivotCols': [{'field': 'd'}],
    }


    response = grid_values(df, AgGridRequest(request))

    assert(response['rows'] == [{'False|b': 3.5, 'False|c': 70.0, 'True|b': 1.5, 'True|c': 30.0}])
    assert(response['secondaryColDefs'] ==
           [{'groupId': 'False', 'headerName': 'False', 'children': [
               {'colId': 'False|b', 'field': 'False|b', 'headerName': 'mean(BB)'},
               {'colId': 'False|c', 'field': 'False|c', 'headerName': 'sum(C)'}]},
            {'groupId': 'True', 'headerName': 'True', 'children': [
                {'colId': 'True|b', 'field': 'True|b', 'headerName': 'mean(BB)'},
                {'colId': 'True|c', 'field': 'True|c', 'headerName': 'sum(C)'}]}
            ]
           )

    assert(response['lastRow'] == 1)


def test_pivot_mode_on_no_pivot_cols():

    df = pd.DataFrame(columns=['a', 'b', 'c', 'd'],
                      data= [['a', 1, 10, True],
                             ['b', 2, 20, True],
                             ['b', 3, 30, False],
                             ['b', 4, 40, False]]
                      )

    
    request = {
        'startRow': 0,
        'endRow': 10,
        'rowGroupCols': [{'field': 'a'}],
        'valueCols': [
            {
                'field': 'b',
                'displayName': 'BB',
                'aggFunc': 'mean',
            },
            {
                'field': 'c',
                'displayName': 'C',
                'aggFunc': 'sum',
            },
        ],
            
        'pivotMode': True,
        'pivotCols': []
    }


    response = grid_values(df, AgGridRequest(request))

    assert(response['rows'] == [{'a': 'a', 'b': 1.0, 'c': 10}, {'a': 'b', 'b': 3.0, 'c': 90}])
    assert(response['secondaryColDefs'] == {})
    assert(response['lastRow'] == 2)

    

def test_1():

    dirname = os.path.dirname(__file__)
    df = pd.read_json(os.path.join(dirname, "olympic-winners.json"))

    request = {
        "startRow": 0,
        "endRow": 5,
        "rowGroupCols": [{"id":"country", "field":"country"}],
        "valueCols": [
            {
                "id": "gold",
                "aggFunc": "sum",
                "displayName": "Gold",
                "field": "gold"
            },
            {
                "id": "silver",
                "aggFunc": "sum",
                "displayName": "Silver",
                "field": "silver"
            },
            {
                "id": "bronze",
                "aggFunc": "sum",
                "displayName": "Bronze",
                "field": "bronze"
            },

        ],
        "pivotCols": [
            {
                "id": "year",
                "displayName": "Year",
                "field": "year"
            },
        ],
        "pivotMode": True,
        "groupKeys": [],
        "filterModel": {},
        "sortModel": []
    }

    response = grid_values(df, AgGridRequest(request))
    rows = response['rows']
    assert(len(rows)) == 5
    assert(response  == {'secondaryColDefs': [{'groupId': '2000', 'headerName': '2000', 'children': [{'colId': '2000|bronze', 'field': '2000|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2000|gold', 'field': '2000|gold', 'headerName': 'sum(Gold)'}, {'colId': '2000|silver', 'field': '2000|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2002', 'headerName': '2002', 'children': [{'colId': '2002|bronze', 'field': '2002|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2002|gold', 'field': '2002|gold', 'headerName': 'sum(Gold)'}, {'colId': '2002|silver', 'field': '2002|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2004', 'headerName': '2004', 'children': [{'colId': '2004|bronze', 'field': '2004|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2004|gold', 'field': '2004|gold', 'headerName': 'sum(Gold)'}, {'colId': '2004|silver', 'field': '2004|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2006', 'headerName': '2006', 'children': [{'colId': '2006|bronze', 'field': '2006|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2006|gold', 'field': '2006|gold', 'headerName': 'sum(Gold)'}, {'colId': '2006|silver', 'field': '2006|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2008', 'headerName': '2008', 'children': [{'colId': '2008|bronze', 'field': '2008|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2008|gold', 'field': '2008|gold', 'headerName': 'sum(Gold)'}, {'colId': '2008|silver', 'field': '2008|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2010', 'headerName': '2010', 'children': [{'colId': '2010|bronze', 'field': '2010|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2010|gold', 'field': '2010|gold', 'headerName': 'sum(Gold)'}, {'colId': '2010|silver', 'field': '2010|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2012', 'headerName': '2012', 'children': [{'colId': '2012|bronze', 'field': '2012|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2012|gold', 'field': '2012|gold', 'headerName': 'sum(Gold)'}, {'colId': '2012|silver', 'field': '2012|silver', 'headerName': 'sum(Silver)'}]}], 'lastRow': 35, 'rows': [{'country': 'Australia', '2000|bronze': 3.0, '2002|bronze': None, '2004|bronze': 3.0, '2006|bronze': None, '2008|bronze': 17.0, '2010|bronze': None, '2012|bronze': 5.0, '2000|gold': 11.0, '2002|gold': None, '2004|gold': 14.0, '2006|gold': None, '2008|gold': 12.0, '2010|gold': None, '2012|gold': 4.0, '2000|silver': 17.0, '2002|silver': None, '2004|silver': 6.0, '2006|silver': None, '2008|silver': 10.0, '2010|silver': None, '2012|silver': 13.0}, {'country': 'Austria', '2000|bronze': None, '2002|bronze': 4.0, '2004|bronze': 0.0, '2006|bronze': 0.0, '2008|bronze': None, '2010|bronze': 3.0, '2012|bronze': None, '2000|gold': None, '2002|gold': 1.0, '2004|gold': 0.0, '2006|gold': 5.0, '2008|gold': None, '2010|gold': 2.0, '2012|gold': None, '2000|silver': None, '2002|silver': 1.0, '2004|silver': 2.0, '2006|silver': 2.0, '2008|silver': None, '2010|silver': 0.0, '2012|silver': None}, {'country': 'Belarus', '2000|bronze': 1.0, '2002|bronze': None, '2004|bronze': None, '2006|bronze': None, '2008|bronze': None, '2010|bronze': None, '2012|bronze': 1.0, '2000|gold': 0.0, '2002|gold': None, '2004|gold': None, '2006|gold': None, '2008|gold': None, '2010|gold': None, '2012|gold': 1.0, '2000|silver': 1.0, '2002|silver': None, '2004|silver': None, '2006|silver': None, '2008|silver': None, '2010|silver': None, '2012|silver': 2.0}, {'country': 'Brazil', '2000|bronze': None, '2002|bronze': None, '2004|bronze': None, '2006|bronze': None, '2008|bronze': 1.0, '2010|bronze': None, '2012|bronze': None, '2000|gold': None, '2002|gold': None, '2004|gold': None, '2006|gold': None, '2008|gold': 1.0, '2010|gold': None, '2012|gold': None, '2000|silver': None, '2002|silver': None, '2004|silver': None, '2006|silver': None, '2008|silver': 0.0, '2010|silver': None, '2012|silver': None}, {'country': 'Bulgaria', '2000|bronze': None, '2002|bronze': 1.0, '2004|bronze': 1.0, '2006|bronze': None, '2008|bronze': None, '2010|bronze': None, '2012|bronze': None, '2000|gold': None, '2002|gold': 0.0, '2004|gold': 1.0, '2006|gold': None, '2008|gold': None, '2010|gold': None, '2012|gold': None, '2000|silver': None, '2002|silver': 1.0, '2004|silver': 0.0, '2006|silver': None, '2008|silver': None, '2010|silver': None, '2012|silver': None}]})


def test_2():

    dirname = os.path.dirname(__file__)
    df = pd.read_json(os.path.join(dirname, "olympic-winners.json"))

    
    request = {"startRow":0,"endRow":10,"rowGroupCols":[{"id":"country","displayName":"Country","field":"country"},{"id":"sport","displayName":"Sport","field":"sport"}],"valueCols":[{"id":"gold","aggFunc":"sum","displayName":"Gold","field":"gold"},{"id":"silver","aggFunc":"sum","displayName":"Silver","field":"silver"},{"id":"bronze","aggFunc":"sum","displayName":"Bronze","field":"bronze"}],"pivotCols":[{"id":"year","displayName":"Year","field":"year"}],"pivotMode":True,"groupKeys":[],"filterModel":{},"sortModel":[{"colId":"2000|silver","sort":"desc"}]}

    response = grid_values(df, AgGridRequest(request))
    rows = response['rows']
    assert(len(rows)) == 10
    assert(response == {'secondaryColDefs': [{'groupId': '2000', 'headerName': '2000', 'children': [{'colId': '2000|bronze', 'field': '2000|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2000|gold', 'field': '2000|gold', 'headerName': 'sum(Gold)'}, {'colId': '2000|silver', 'field': '2000|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2002', 'headerName': '2002', 'children': [{'colId': '2002|bronze', 'field': '2002|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2002|gold', 'field': '2002|gold', 'headerName': 'sum(Gold)'}, {'colId': '2002|silver', 'field': '2002|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2004', 'headerName': '2004', 'children': [{'colId': '2004|bronze', 'field': '2004|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2004|gold', 'field': '2004|gold', 'headerName': 'sum(Gold)'}, {'colId': '2004|silver', 'field': '2004|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2006', 'headerName': '2006', 'children': [{'colId': '2006|bronze', 'field': '2006|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2006|gold', 'field': '2006|gold', 'headerName': 'sum(Gold)'}, {'colId': '2006|silver', 'field': '2006|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2008', 'headerName': '2008', 'children': [{'colId': '2008|bronze', 'field': '2008|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2008|gold', 'field': '2008|gold', 'headerName': 'sum(Gold)'}, {'colId': '2008|silver', 'field': '2008|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2010', 'headerName': '2010', 'children': [{'colId': '2010|bronze', 'field': '2010|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2010|gold', 'field': '2010|gold', 'headerName': 'sum(Gold)'}, {'colId': '2010|silver', 'field': '2010|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': '2012', 'headerName': '2012', 'children': [{'colId': '2012|bronze', 'field': '2012|bronze', 'headerName': 'sum(Bronze)'}, {'colId': '2012|gold', 'field': '2012|gold', 'headerName': 'sum(Gold)'}, {'colId': '2012|silver', 'field': '2012|silver', 'headerName': 'sum(Silver)'}]}], 'lastRow': 35, 'rows': [{'country': 'Australia', '2000|bronze': 3.0, '2002|bronze': None, '2004|bronze': 3.0, '2006|bronze': None, '2008|bronze': 17.0, '2010|bronze': None, '2012|bronze': 5.0, '2000|gold': 11.0, '2002|gold': None, '2004|gold': 14.0, '2006|gold': None, '2008|gold': 12.0, '2010|gold': None, '2012|gold': 4.0, '2000|silver': 17.0, '2002|silver': None, '2004|silver': 6.0, '2006|silver': None, '2008|silver': 10.0, '2010|silver': None, '2012|silver': 13.0}, {'country': 'United States', '2000|bronze': 6.0, '2002|bronze': 2.0, '2004|bronze': 15.0, '2006|bronze': 3.0, '2008|bronze': 12.0, '2010|bronze': 7.0, '2012|bronze': 9.0, '2000|gold': 28.0, '2002|gold': 2.0, '2004|gold': 25.0, '2006|gold': 4.0, '2008|gold': 23.0, '2010|gold': 3.0, '2012|gold': 36.0, '2000|silver': 10.0, '2002|silver': 2.0, '2004|silver': 21.0, '2006|silver': 3.0, '2008|silver': 23.0, '2010|silver': 9.0, '2012|silver': 14.0}, {'country': 'Russia', '2000|bronze': 6.0, '2002|bronze': 1.0, '2004|bronze': 0.0, '2006|bronze': 2.0, '2008|bronze': 2.0, '2010|bronze': 1.0, '2012|bronze': 2.0, '2000|gold': 10.0, '2002|gold': 1.0, '2004|gold': 6.0, '2006|gold': 1.0, '2008|gold': 4.0, '2010|gold': 0.0, '2012|gold': 5.0, '2000|silver': 7.0, '2002|silver': 1.0, '2004|silver': 2.0, '2006|silver': 0.0, '2008|silver': 0.0, '2010|silver': 1.0, '2012|silver': 1.0}, {'country': 'Netherlands', '2000|bronze': 2.0, '2002|bronze': 0.0, '2004|bronze': 2.0, '2006|bronze': 6.0, '2008|bronze': None, '2010|bronze': 2.0, '2012|bronze': 1.0, '2000|gold': 8.0, '2002|gold': 2.0, '2004|gold': 2.0, '2006|gold': 1.0, '2008|gold': None, '2010|gold': 2.0, '2012|gold': 2.0, '2000|silver': 6.0, '2002|silver': 1.0, '2004|silver': 3.0, '2006|silver': 1.0, '2008|silver': None, '2010|silver': 0.0, '2012|silver': 2.0}, {'country': 'Japan', '2000|bronze': 1.0, '2002|bronze': None, '2004|bronze': 4.0, '2006|bronze': None, '2008|bronze': 1.0, '2010|bronze': None, '2012|bronze': 6.0, '2000|gold': 0.0, '2002|gold': None, '2004|gold': 2.0, '2006|gold': None, '2008|gold': 2.0, '2010|gold': None, '2012|gold': 1.0, '2000|silver': 5.0, '2002|silver': None, '2004|silver': 5.0, '2006|silver': None, '2008|silver': 0.0, '2010|silver': None, '2012|silver': 6.0}, {'country': 'China', '2000|bronze': 1.0, '2002|bronze': 3.0, '2004|bronze': 0.0, '2006|bronze': 1.0, '2008|bronze': 8.0, '2010|bronze': 0.0, '2012|bronze': 5.0, '2000|gold': 5.0, '2002|gold': 2.0, '2004|gold': 2.0, '2006|gold': 1.0, '2008|gold': 15.0, '2010|gold': 5.0, '2012|gold': 12.0, '2000|silver': 4.0, '2002|silver': 4.0, '2004|silver': 0.0, '2006|silver': 1.0, '2008|silver': 4.0, '2010|silver': 0.0, '2012|silver': 7.0}, {'country': 'Slovakia', '2000|bronze': 0.0, '2002|bronze': None, '2004|bronze': None, '2006|bronze': None, '2008|bronze': None, '2010|bronze': None, '2012|bronze': None, '2000|gold': 0.0, '2002|gold': None, '2004|gold': None, '2006|gold': None, '2008|gold': None, '2010|gold': None, '2012|gold': None, '2000|silver': 2.0, '2002|silver': None, '2004|silver': None, '2006|silver': None, '2008|silver': None, '2010|silver': None, '2012|silver': None}, {'country': 'Sweden', '2000|bronze': 1.0, '2002|bronze': None, '2004|bronze': None, '2006|bronze': 2.0, '2008|bronze': None, '2010|bronze': 2.0, '2012|bronze': None, '2000|gold': 0.0, '2002|gold': None, '2004|gold': None, '2006|gold': 1.0, '2008|gold': None, '2010|gold': 1.0, '2012|gold': None, '2000|silver': 2.0, '2002|silver': None, '2004|silver': None, '2006|silver': 0.0, '2008|silver': None, '2010|silver': 0.0, '2012|silver': None}, {'country': 'Belarus', '2000|bronze': 1.0, '2002|bronze': None, '2004|bronze': None, '2006|bronze': None, '2008|bronze': None, '2010|bronze': None, '2012|bronze': 1.0, '2000|gold': 0.0, '2002|gold': None, '2004|gold': None, '2006|gold': None, '2008|gold': None, '2010|gold': None, '2012|gold': 1.0, '2000|silver': 1.0, '2002|silver': None, '2004|silver': None, '2006|silver': None, '2008|silver': None, '2010|silver': None, '2012|silver': 2.0}, {'country': 'France', '2000|bronze': 0.0, '2002|bronze': None, '2004|bronze': 1.0, '2006|bronze': None, '2008|bronze': 3.0, '2010|bronze': None, '2012|bronze': 1.0, '2000|gold': 2.0, '2002|gold': None, '2004|gold': 1.0, '2006|gold': None, '2008|gold': 1.0, '2010|gold': None, '2012|gold': 6.0, '2000|silver': 1.0, '2002|silver': None, '2004|silver': 1.0, '2006|silver': None, '2008|silver': 3.0, '2010|silver': None, '2012|silver': 5.0}]})
    

def test_3():
    dirname = os.path.dirname(__file__)
    df = pd.read_json(os.path.join(dirname, "olympic-winners.json"))
    
    request = {"startRow":2,"endRow":12,"rowGroupCols":[{"id":"country","displayName":"Country","field":"country"},{"id":"sport","displayName":"Sport","field":"sport"}],"valueCols":[{"id":"gold","aggFunc":"sum","displayName":"Gold","field":"gold"},{"id":"silver","aggFunc":"sum","displayName":"Silver","field":"silver"},{"id":"bronze","aggFunc":"sum","displayName":"Bronze","field":"bronze"}],"pivotCols":[{"id":"country","displayName":"Country","field":"country"}],"pivotMode":True,"groupKeys":[],"filterModel":{},"sortModel":[]}

    response = grid_values(df, AgGridRequest(request))

    assert(response == {'secondaryColDefs': [{'groupId': 'Belarus', 'headerName': 'Belarus', 'children': [{'colId': 'Belarus|bronze', 'field': 'Belarus|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'Belarus|gold', 'field': 'Belarus|gold', 'headerName': 'sum(Gold)'}, {'colId': 'Belarus|silver', 'field': 'Belarus|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': 'Brazil', 'headerName': 'Brazil', 'children': [{'colId': 'Brazil|bronze', 'field': 'Brazil|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'Brazil|gold', 'field': 'Brazil|gold', 'headerName': 'sum(Gold)'}, {'colId': 'Brazil|silver', 'field': 'Brazil|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': 'Bulgaria', 'headerName': 'Bulgaria', 'children': [{'colId': 'Bulgaria|bronze', 'field': 'Bulgaria|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'Bulgaria|gold', 'field': 'Bulgaria|gold', 'headerName': 'sum(Gold)'}, {'colId': 'Bulgaria|silver', 'field': 'Bulgaria|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': 'Canada', 'headerName': 'Canada', 'children': [{'colId': 'Canada|bronze', 'field': 'Canada|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'Canada|gold', 'field': 'Canada|gold', 'headerName': 'sum(Gold)'}, {'colId': 'Canada|silver', 'field': 'Canada|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': 'Chile', 'headerName': 'Chile', 'children': [{'colId': 'Chile|bronze', 'field': 'Chile|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'Chile|gold', 'field': 'Chile|gold', 'headerName': 'sum(Gold)'}, {'colId': 'Chile|silver', 'field': 'Chile|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': 'China', 'headerName': 'China', 'children': [{'colId': 'China|bronze', 'field': 'China|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'China|gold', 'field': 'China|gold', 'headerName': 'sum(Gold)'}, {'colId': 'China|silver', 'field': 'China|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': 'Costa Rica', 'headerName': 'Costa Rica', 'children': [{'colId': 'Costa Rica|bronze', 'field': 'Costa Rica|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'Costa Rica|gold', 'field': 'Costa Rica|gold', 'headerName': 'sum(Gold)'}, {'colId': 'Costa Rica|silver', 'field': 'Costa Rica|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': 'Croatia', 'headerName': 'Croatia', 'children': [{'colId': 'Croatia|bronze', 'field': 'Croatia|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'Croatia|gold', 'field': 'Croatia|gold', 'headerName': 'sum(Gold)'}, {'colId': 'Croatia|silver', 'field': 'Croatia|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': 'Czech Republic', 'headerName': 'Czech Republic', 'children': [{'colId': 'Czech Republic|bronze', 'field': 'Czech Republic|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'Czech Republic|gold', 'field': 'Czech Republic|gold', 'headerName': 'sum(Gold)'}, {'colId': 'Czech Republic|silver', 'field': 'Czech Republic|silver', 'headerName': 'sum(Silver)'}]}, {'groupId': 'Finland', 'headerName': 'Finland', 'children': [{'colId': 'Finland|bronze', 'field': 'Finland|bronze', 'headerName': 'sum(Bronze)'}, {'colId': 'Finland|gold', 'field': 'Finland|gold', 'headerName': 'sum(Gold)'}, {'colId': 'Finland|silver', 'field': 'Finland|silver', 'headerName': 'sum(Silver)'}]}], 'lastRow': 35, 'rows': [{'country': 'Belarus', 'Belarus|bronze': 2.0, 'Brazil|bronze': None, 'Bulgaria|bronze': None, 'Canada|bronze': None, 'Chile|bronze': None, 'China|bronze': None, 'Costa Rica|bronze': None, 'Croatia|bronze': None, 'Czech Republic|bronze': None, 'Finland|bronze': None, 'Belarus|gold': 1.0, 'Brazil|gold': None, 'Bulgaria|gold': None, 'Canada|gold': None, 'Chile|gold': None, 'China|gold': None, 'Costa Rica|gold': None, 'Croatia|gold': None, 'Czech Republic|gold': None, 'Finland|gold': None, 'Belarus|silver': 3.0, 'Brazil|silver': None, 'Bulgaria|silver': None, 'Canada|silver': None, 'Chile|silver': None, 'China|silver': None, 'Costa Rica|silver': None, 'Croatia|silver': None, 'Czech Republic|silver': None, 'Finland|silver': None}, {'country': 'Brazil', 'Belarus|bronze': None, 'Brazil|bronze': 1.0, 'Bulgaria|bronze': None, 'Canada|bronze': None, 'Chile|bronze': None, 'China|bronze': None, 'Costa Rica|bronze': None, 'Croatia|bronze': None, 'Czech Republic|bronze': None, 'Finland|bronze': None, 'Belarus|gold': None, 'Brazil|gold': 1.0, 'Bulgaria|gold': None, 'Canada|gold': None, 'Chile|gold': None, 'China|gold': None, 'Costa Rica|gold': None, 'Croatia|gold': None, 'Czech Republic|gold': None, 'Finland|gold': None, 'Belarus|silver': None, 'Brazil|silver': 0.0, 'Bulgaria|silver': None, 'Canada|silver': None, 'Chile|silver': None, 'China|silver': None, 'Costa Rica|silver': None, 'Croatia|silver': None, 'Czech Republic|silver': None, 'Finland|silver': None}, {'country': 'Bulgaria', 'Belarus|bronze': None, 'Brazil|bronze': None, 'Bulgaria|bronze': 2.0, 'Canada|bronze': None, 'Chile|bronze': None, 'China|bronze': None, 'Costa Rica|bronze': None, 'Croatia|bronze': None, 'Czech Republic|bronze': None, 'Finland|bronze': None, 'Belarus|gold': None, 'Brazil|gold': None, 'Bulgaria|gold': 1.0, 'Canada|gold': None, 'Chile|gold': None, 'China|gold': None, 'Costa Rica|gold': None, 'Croatia|gold': None, 'Czech Republic|gold': None, 'Finland|gold': None, 'Belarus|silver': None, 'Brazil|silver': None, 'Bulgaria|silver': 1.0, 'Canada|silver': None, 'Chile|silver': None, 'China|silver': None, 'Costa Rica|silver': None, 'Croatia|silver': None, 'Czech Republic|silver': None, 'Finland|silver': None}, {'country': 'Canada', 'Belarus|bronze': None, 'Brazil|bronze': None, 'Bulgaria|bronze': None, 'Canada|bronze': 7.0, 'Chile|bronze': None, 'China|bronze': None, 'Costa Rica|bronze': None, 'Croatia|bronze': None, 'Czech Republic|bronze': None, 'Finland|bronze': None, 'Belarus|gold': None, 'Brazil|gold': None, 'Bulgaria|gold': None, 'Canada|gold': 9.0, 'Chile|gold': None, 'China|gold': None, 'Costa Rica|gold': None, 'Croatia|gold': None, 'Czech Republic|gold': None, 'Finland|gold': None, 'Belarus|silver': None, 'Brazil|silver': None, 'Bulgaria|silver': None, 'Canada|silver': 12.0, 'Chile|silver': None, 'China|silver': None, 'Costa Rica|silver': None, 'Croatia|silver': None, 'Czech Republic|silver': None, 'Finland|silver': None}, {'country': 'Chile', 'Belarus|bronze': None, 'Brazil|bronze': None, 'Bulgaria|bronze': None, 'Canada|bronze': None, 'Chile|bronze': 1.0, 'China|bronze': None, 'Costa Rica|bronze': None, 'Croatia|bronze': None, 'Czech Republic|bronze': None, 'Finland|bronze': None, 'Belarus|gold': None, 'Brazil|gold': None, 'Bulgaria|gold': None, 'Canada|gold': None, 'Chile|gold': 3.0, 'China|gold': None, 'Costa Rica|gold': None, 'Croatia|gold': None, 'Czech Republic|gold': None, 'Finland|gold': None, 'Belarus|silver': None, 'Brazil|silver': None, 'Bulgaria|silver': None, 'Canada|silver': None, 'Chile|silver': 0.0, 'China|silver': None, 'Costa Rica|silver': None, 'Croatia|silver': None, 'Czech Republic|silver': None, 'Finland|silver': None}, {'country': 'China', 'Belarus|bronze': None, 'Brazil|bronze': None, 'Bulgaria|bronze': None, 'Canada|bronze': None, 'Chile|bronze': None, 'China|bronze': 18.0, 'Costa Rica|bronze': None, 'Croatia|bronze': None, 'Czech Republic|bronze': None, 'Finland|bronze': None, 'Belarus|gold': None, 'Brazil|gold': None, 'Bulgaria|gold': None, 'Canada|gold': None, 'Chile|gold': None, 'China|gold': 42.0, 'Costa Rica|gold': None, 'Croatia|gold': None, 'Czech Republic|gold': None, 'Finland|gold': None, 'Belarus|silver': None, 'Brazil|silver': None, 'Bulgaria|silver': None, 'Canada|silver': None, 'Chile|silver': None, 'China|silver': 20.0, 'Costa Rica|silver': None, 'Croatia|silver': None, 'Czech Republic|silver': None, 'Finland|silver': None}, {'country': 'Costa Rica', 'Belarus|bronze': None, 'Brazil|bronze': None, 'Bulgaria|bronze': None, 'Canada|bronze': None, 'Chile|bronze': None, 'China|bronze': None, 'Costa Rica|bronze': 2.0, 'Croatia|bronze': None, 'Czech Republic|bronze': None, 'Finland|bronze': None, 'Belarus|gold': None, 'Brazil|gold': None, 'Bulgaria|gold': None, 'Canada|gold': None, 'Chile|gold': None, 'China|gold': None, 'Costa Rica|gold': 0.0, 'Croatia|gold': None, 'Czech Republic|gold': None, 'Finland|gold': None, 'Belarus|silver': None, 'Brazil|silver': None, 'Bulgaria|silver': None, 'Canada|silver': None, 'Chile|silver': None, 'China|silver': None, 'Costa Rica|silver': 0.0, 'Croatia|silver': None, 'Czech Republic|silver': None, 'Finland|silver': None}, {'country': 'Croatia', 'Belarus|bronze': None, 'Brazil|bronze': None, 'Bulgaria|bronze': None, 'Canada|bronze': None, 'Chile|bronze': None, 'China|bronze': None, 'Costa Rica|bronze': None, 'Croatia|bronze': 0.0, 'Czech Republic|bronze': None, 'Finland|bronze': None, 'Belarus|gold': None, 'Brazil|gold': None, 'Bulgaria|gold': None, 'Canada|gold': None, 'Chile|gold': None, 'China|gold': None, 'Costa Rica|gold': None, 'Croatia|gold': 3.0, 'Czech Republic|gold': None, 'Finland|gold': None, 'Belarus|silver': None, 'Brazil|silver': None, 'Bulgaria|silver': None, 'Canada|silver': None, 'Chile|silver': None, 'China|silver': None, 'Costa Rica|silver': None, 'Croatia|silver': 1.0, 'Czech Republic|silver': None, 'Finland|silver': None}, {'country': 'Czech Republic', 'Belarus|bronze': None, 'Brazil|bronze': None, 'Bulgaria|bronze': None, 'Canada|bronze': None, 'Chile|bronze': None, 'China|bronze': None, 'Costa Rica|bronze': None, 'Croatia|bronze': None, 'Czech Republic|bronze': 1.0, 'Finland|bronze': None, 'Belarus|gold': None, 'Brazil|gold': None, 'Bulgaria|gold': None, 'Canada|gold': None, 'Chile|gold': None, 'China|gold': None, 'Costa Rica|gold': None, 'Croatia|gold': None, 'Czech Republic|gold': 3.0, 'Finland|gold': None, 'Belarus|silver': None, 'Brazil|silver': None, 'Bulgaria|silver': None, 'Canada|silver': None, 'Chile|silver': None, 'China|silver': None, 'Costa Rica|silver': None, 'Croatia|silver': None, 'Czech Republic|silver': 1.0, 'Finland|silver': None}, {'country': 'Finland', 'Belarus|bronze': None, 'Brazil|bronze': None, 'Bulgaria|bronze': None, 'Canada|bronze': None, 'Chile|bronze': None, 'China|bronze': None, 'Costa Rica|bronze': None, 'Croatia|bronze': None, 'Czech Republic|bronze': None, 'Finland|bronze': 1.0, 'Belarus|gold': None, 'Brazil|gold': None, 'Bulgaria|gold': None, 'Canada|gold': None, 'Chile|gold': None, 'China|gold': None, 'Costa Rica|gold': None, 'Croatia|gold': None, 'Czech Republic|gold': None, 'Finland|gold': 3.0, 'Belarus|silver': None, 'Brazil|silver': None, 'Bulgaria|silver': None, 'Canada|silver': None, 'Chile|silver': None, 'China|silver': None, 'Costa Rica|silver': None, 'Croatia|silver': None, 'Czech Republic|silver': None, 'Finland|silver': 3.0}]})
    

    assert(len(response['rows'])) == 10
