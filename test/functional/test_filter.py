from pdgrid import unique_values, aggrid_values
import pandas
import json
import itertools

def test_1():

    df = pandas.read_json("/home/slindal/dev/pdgrid/test/manual/olympic-winners.json")

    group_model = {
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [{"id":"country", "field":"country"}],
            "valueCols": [
                {
                    "id": "gold",
                    "aggFunc": "sum",
                    "displayName": "gold",
                    "field": "gold"
                }
            ],
            "pivotCols": [],
            "pivotMode": False,
            "groupKeys": [],
            "filterModel": {"age": {"values": ["16", "15"], "filterType": "set"}},
            "sortModel": []
    }

    response = aggrid_values(df, group_model)
    rows = response['rows']
    assert(len(rows)) == 5
    assert(rows ==  [{'country': 'Australia', 'gold': 0}, {'country': 'China', 'gold': 3}, {'country': 'Romania', 'gold': 5}, {'country': 'South Korea', 'gold': 1}, {'country': 'United States', 'gold': 4}]
)


def test_filterendpoint():
    df = pandas.read_json("/home/slindal/dev/pdgrid/test/manual/olympic-winners.json")
    response = unique_values(df, 'age')
    assert(response == [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 41])
    

def test_text_filter_contains():
    df = pandas.DataFrame(columns=['a', 'b', 'c'], data = [['aaa', 'bbb', 'ccc'],
                                                             ['aba', 'bba', 'cca'],
                                                             ['abb', 'baa', 'cbb']])

    request = {
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [],
            "valueCols": [],
            "pivotCols": [],
            "pivotMode": False,
            "groupKeys": [],
            "filterModel": {"a": {"filterType": "text", "type": "contains", "filter": "ab"}},
            "sortModel": []
    }

    response = aggrid_values(df, request)
    assert(response == {'rows': [{'a': 'aba', 'b': 'bba', 'c': 'cca'}, {'a': 'abb', 'b': 'baa', 'c': 'cbb'}], 'lastRow': 2})
 
    
def test_text_filter_not_contains():
    df = pandas.DataFrame(columns=['a', 'b', 'c'], data = [['aaa', 'bbb', 'ccc'],
                                                             ['aba', 'bba', 'cca'],
                                                             ['abb', 'baa', 'cbb']])

    request = {
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [],
            "valueCols": [],
            "pivotCols": [],
            "pivotMode": False,
            "groupKeys": [],
            "filterModel": {"a": {"filterType": "text", "type": "notContains", "filter": "ab"}},
            "sortModel": []
    }

    response = aggrid_values(df, request)
    assert(response == {'rows': [{'a': 'aaa', 'b': 'bbb', 'c': 'ccc'}], 'lastRow': 1})

 
def test_text_filter_equals():
    df = pandas.DataFrame(columns=['a', 'b', 'c'], data = [['aaa', 'bbb', 'ccc'],
                                                             ['aba', 'bba', 'cca'],
                                                             ['abb', 'baa', 'cbb']])

    request = {
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [],
            "valueCols": [],
            "pivotCols": [],
            "pivotMode": False,
            "groupKeys": [],
            "filterModel": {"a": {"filterType": "text", "type": "equals", "filter": "abb"}},
            "sortModel": []
    }

    response = aggrid_values(df, request)
    assert(response == {'rows': [{'a': 'abb', 'b': 'baa', 'c': 'cbb'}], 'lastRow': 1})
    
def test_text_filter_not_equals():
    df = pandas.DataFrame(columns=['a', 'b', 'c'], data = [['aaa', 'bbb', 'ccc'],
                                                             ['aba', 'bba', 'cca'],
                                                             ['abb', 'baa', 'cbb']])

    request = {
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [],
            "valueCols": [],
            "pivotCols": [],
            "pivotMode": False,
            "groupKeys": [],
            "filterModel": {"a": {"filterType": "text", "type": "notEquals", "filter": "abb"}},
            "sortModel": []
    }

    response = aggrid_values(df, request)
    assert(response == {'rows': [{'a': 'aaa', 'b': 'bbb', 'c': 'ccc'}, {'a': 'aba', 'b': 'bba', 'c': 'cca'}], 'lastRow': 2})

    
def test_text_filter_startwith():
    df = pandas.DataFrame(columns=['a', 'b', 'c'], data = [['aaa', 'bbb', 'ccc'],
                                                             ['aba', 'bba', 'cca'],
                                                             ['abb', 'baa', 'cbb']])

    request = {
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [],
            "valueCols": [],
            "pivotCols": [],
            "pivotMode": False,
            "groupKeys": [],
            "filterModel": {"a": {"filterType": "text", "type": "startsWith", "filter": "ab"}},
            "sortModel": []
    }

    response = aggrid_values(df, request)
    assert(response == {'rows': [{'a': 'aba', 'b': 'bba', 'c': 'cca'}, {'a': 'abb', 'b': 'baa', 'c': 'cbb'}], 'lastRow': 2})

def test_text_filter_endswith():
    df = pandas.DataFrame(columns=['a', 'b', 'c'], data = [['aaa', 'bbb', 'ccc'],
                                                             ['aba', 'bba', 'cca'],
                                                             ['abb', 'baa', 'cbb']])

    request = {
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [],
            "valueCols": [],
            "pivotCols": [],
            "pivotMode": False,
            "groupKeys": [],
            "filterModel": {"a": {"filterType": "text", "type": "endsWith", "filter": "bb"}},
            "sortModel": []
    }

    response = aggrid_values(df, request)
    assert(response == {'rows': [{'a': 'abb', 'b': 'baa', 'c': 'cbb'}], 'lastRow': 1})


def test_multi_filter():

    df = pandas.DataFrame(columns=['a', 'b', 'c'], data = [['aaa', 'bbb', 'ccc'],
                                                             ['aba', 'bba', 'cca'],
                                                             ['abb', 'baa', 'cbb']])

    request = {
        "startRow": 0,
        "endRow": 100,
        "rowGroupCols": [],
        "valueCols": [],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {
            "a": {
                "filterType":"text",
                "operator":"OR",
                "condition1": {"filterType": "text", "type": "endsWith", "filter": "ba"},
                "condition2": {"filterType": "text", "type": "endsWith", "filter": "aa"},
            }
        },                                  
        "sortModel": []
    }

    response = aggrid_values(df, request)
    assert(response == {'rows': [{'a': 'aaa', 'b': 'bbb', 'c': 'ccc'}, {'a': 'aba', 'b': 'bba', 'c': 'cca'}], 'lastRow': 2})



def test_number_filter():

    df = pandas.DataFrame(columns=['a', 'b', 'c'], data = [[1, 'bbb', 'ccc'],
                                                             [21, 'bba', 'cca'],
                                                             [22, 'baa', 'cbb']])

    request = {
        "startRow": 0,
        "endRow": 100,
        "rowGroupCols": [],
        "valueCols": [],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {
            "b": {
                "filterType":"text",
                "operator":"OR",
                "condition1": {"filterType": "text", "type": "endsWith", "filter": "ba"},
                "condition2": {"filterType": "text", "type": "endsWith", "filter": "aa"},
            },
            "a": {"filterType": "number", "type": "lessThanOrEqual", "filter": 21}

        },                                  
        "sortModel": []
    }

    response = aggrid_values(df, request)
    assert(response == {"rows": [{"a": 21, "b": "bba", "c": "cca"}], "lastRow": 1})

    

def test_number_inRange_filter():

    df = pandas.DataFrame(columns=['a', 'b', 'c'], data = [[1, 'bbb', 'ccc'],
                                                           [2, 'bba', 'cca'],
                                                           [3, 'baa', 'cbb'],
                                                           [4, 'bb', 'bb']
                                                           ])

    request = {
        "startRow": 0,
        "endRow": 100,
        "rowGroupCols": [],
        "valueCols": [],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {
            "a": {"filterType": "number", "type": "inRange", "filter": 1, "filterTo": 3}
        },                                  
        "sortModel": []
    }

    response = aggrid_values(df, request)
    assert(response == {"rows": [{"a": 1, "b": "bbb", "c": "ccc"}, {"a": 2, "b": "bba", "c": "cca"}], "lastRow": 2})
