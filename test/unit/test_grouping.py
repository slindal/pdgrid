from unittest import mock
from pdgrid import grid_values
import pandas as pd
import json


def test_1():
    df = pd.DataFrame(columns=['a', 'b', 'c'], data = [[1, 10, 'a'],
                                                       [2, 20, 'b'],
                                                       [3, 30, 'c'],
                                                       [3, 20, 'a']
                                                       ])
    
    
    request = {
        "startRow": 0,
        "endRow": 100,
        "rowGroupCols": [{"id":"c", "field":"c"}],
        "valueCols": [
            {
                "id": "b",
                "aggFunc": "sum",
                "displayName": "B",
                "field": "b"
            },
            {
                "id": "a",
                "aggFunc": "sum",
                "displayName": "A",
                "field": "a"
            }
        ],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {},
        "sortModel": []
    }

    response = grid_values(df, request)
    rows = response['rows']
    assert(len(rows)) == 3
    assert(rows == [{'a': '4', 'b': '30', 'c': 'a'},
                    {'a': '2', 'b': '20', 'c': 'b'},
                    {'a': '3', 'b': '30', 'c': 'c'}])
    
    
def test_2():
    df = pd.DataFrame(columns=['a', 'b', 'c'], data = [[1, 10, 'a'],
                                                       [2, 20, 'b'],
                                                       [3, 30, 'c'],
                                                       [3, 20, 'a']
                                                       ])
    
    
    request = {
        "startRow": 0,
        "endRow": 100,
        "rowGroupCols": [{"id":"c", "field":"c"}],
        "valueCols": [
            {
                "id": "b",
                "aggFunc": "sum",
                "displayName": "B",
                "field": "b"
            },
            {
                "id": "a",
                "aggFunc": "sum",
                "displayName": "A",
                "field": "a"
            }
        ],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": ["b"],
        "filterModel": {},
        "sortModel": []
    }
    
    response = grid_values(df, request)
    rows = response['rows']
    assert(len(rows)) == 1
    assert(rows == [{'a': '2', 'b': '20', 'c': 'b'}])
    


def test_3():
    df = pd.DataFrame(columns=['a', 'b', 'c'], data = [[1, 10, 'a'],
                                                       [2, 20, 'b'],
                                                       [3, 30, 'c'],
                                                       [3, 20, 'a']
                                                       ])
    
    
    request = {
        "startRow": 0,
        "endRow": 100,
        "rowGroupCols": [{"id":"c", "field":"c"}],
        "valueCols": [
            {
                "id": "b",
                "aggFunc": "sum",
                "displayName": "B",
                "field": "b"
            },
            {
                "id": "a",
                "aggFunc": "sum",
                "displayName": "A",
                "field": "a"
            }
        ],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": ["a"],
        "filterModel": {},
        "sortModel": []
    }

    response = grid_values(df, request)
    rows = response['rows']
    assert(len(rows)) == 2
    assert(rows ==  [{'a': '1', 'b': '10', 'c': 'a'}, {'a': '3', 'b': '20', 'c': 'a'}])
    

def test_4():
    df = pd.DataFrame(columns=['a', 'b', 'c', 'd'],
                      data = [[1, 10, 'a', "aa"],
                              [2, 20, 'b', "aa"],
                              [3, 30, 'c', "bb"],
                              [3, 20, 'a', "aa"]
                              ])
    
    
    request = {
        "startRow": 0,
        "endRow": 100,
        "rowGroupCols": [{"id":"c", "field":"c"}, {"field": "d"}],
        "valueCols": [
            {
                "id": "b",
                "aggFunc": "sum",
                "displayName": "B",
                "field": "b"
            },
            {
                "id": "a",
                "aggFunc": "sum",
                "displayName": "A",
                "field": "a"
            }
        ],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": ["a"],
        "filterModel": {},
        "sortModel": []
    }

    response = grid_values(df, request)
    rows = response['rows']
    assert(len(rows)) == 1
    assert(rows ==  [{'a': '4', 'b': '30', 'd': 'aa'}])


def test_5():
    df = pd.DataFrame(columns=['a', 'b', 'c', 'd'],
                      data = [[1, 10, 'a', "aa"],
                              [2, 20, 'b', "aa"],
                              [3, 30, 'c', "bb"],
                              [3, 20, 'a', "aa"]
                              ])
    
    
    request = {
        "startRow": 0,
        "endRow": 100,
        "rowGroupCols": [{"id":"c", "field":"c"}, {"field": "d"}],
        "valueCols": [
            {
                "id": "b",
                "aggFunc": "sum",
                "displayName": "B",
                "field": "b"
            },
            {
                "id": "a",
                "aggFunc": "sum",
                "displayName": "A",
                "field": "a"
            }
        ],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": ["a", "aa"],
        "filterModel": {},
        "sortModel": []
    }

    response = grid_values(df, request)
    rows = response['rows']
    assert(len(rows)) == 2
    assert(rows ==  [{'a': '1', 'b': '10', 'c': 'a', 'd': 'aa'},
                     {'a': '3', 'b': '20', 'c': 'a', 'd': 'aa'}])
    
