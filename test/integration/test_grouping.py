from src.server import load_dataframe
from src.server import app
from unittest import mock
import pandas as pd
import json

@mock.patch('src.server.load_dataframe')
def test_1(load_dataframe):
    load_dataframe.return_value = pd.DataFrame(columns=['a', 'b', 'c'], data = [[1, 10, 'a'],
                                                                                [2, 20, 'b'],
                                                                                [3, 30, 'c'],
                                                                                [3, 20, 'a']
                                                                                ])

    
    with app.test_client() as client:
        group_model = '''{
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
            "pivotMode": false,
            "groupKeys": [],
            "filterModel": {},
            "sortModel": []
        }'''

        response = client.get('/api/olympicWinners', data= group_model)
        rows = json.loads(response.data)['data']['rows']
        assert(len(rows)) == 3
        assert(rows == [{'a': '4', 'b': '30', 'c': 'a'},
                        {'a': '2', 'b': '20', 'c': 'b'},
                        {'a': '3', 'b': '30', 'c': 'c'}])


@mock.patch('src.server.load_dataframe')
def test_2(load_dataframe):
    load_dataframe.return_value = pd.DataFrame(columns=['a', 'b', 'c'], data = [[1, 10, 'a'],
                                                                                [2, 20, 'b'],
                                                                                [3, 30, 'c'],
                                                                                [3, 20, 'a']
                                                                                ])

    
    with app.test_client() as client:
        group_model = '''{
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
            "pivotMode": false,
            "groupKeys": ["b"],
            "filterModel": {},
            "sortModel": []
        }'''

        response = client.get('/api/olympicWinners', data= group_model)
        rows = json.loads(response.data)['data']['rows']
        assert(len(rows)) == 1
        assert(rows == [{'a': '2', 'b': '20', 'c': 'b'}])



@mock.patch('src.server.load_dataframe')
def test_3(load_dataframe):
    load_dataframe.return_value = pd.DataFrame(columns=['a', 'b', 'c'], data = [[1, 10, 'a'],
                                                                                [2, 20, 'b'],
                                                                                [3, 30, 'c'],
                                                                                [3, 20, 'a']
                                                                                ])

    
    with app.test_client() as client:
        group_model = '''{
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
            "pivotMode": false,
            "groupKeys": ["a"],
            "filterModel": {},
            "sortModel": []
        }'''

        response = client.get('/api/olympicWinners', data= group_model)
        rows = json.loads(response.data)['data']['rows']
        assert(len(rows)) == 2
        assert(rows ==  [{'a': '1', 'b': '10', 'c': 'a'}, {'a': '3', 'b': '20', 'c': 'a'}])


@mock.patch('src.server.load_dataframe')
def test_4(load_dataframe):
    load_dataframe.return_value = pd.DataFrame(columns=['a', 'b', 'c', 'd'],
                                               data = [[1, 10, 'a', "aa"],
                                                       [2, 20, 'b', "aa"],
                                                       [3, 30, 'c', "bb"],
                                                       [3, 20, 'a', "aa"]
                                                       ])
    
    
    with app.test_client() as client:
        group_model = '''{
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
            "pivotMode": false,
            "groupKeys": ["a"],
            "filterModel": {},
            "sortModel": []
        }'''

        response = client.get('/api/olympicWinners', data= group_model)
        rows = json.loads(response.data)['data']['rows']
        assert(len(rows)) == 1
        assert(rows ==  [{'a': '4', 'b': '30', 'd': 'aa'}])


@mock.patch('src.server.load_dataframe')
def test_5(load_dataframe):
    load_dataframe.return_value = pd.DataFrame(columns=['a', 'b', 'c', 'd'],
                                               data = [[1, 10, 'a', "aa"],
                                                       [2, 20, 'b', "aa"],
                                                       [3, 30, 'c', "bb"],
                                                       [3, 20, 'a', "aa"]
                                                       ])
    
    
    with app.test_client() as client:
        group_model = '''{
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
            "pivotMode": false,
            "groupKeys": ["a", "aa"],
            "filterModel": {},
            "sortModel": []
        }'''

        response = client.get('/api/olympicWinners', data= group_model)
        rows = json.loads(response.data)['data']['rows']
        assert(len(rows)) == 2
        assert(rows ==  [{'a': '1', 'b': '10', 'c': 'a', 'd': 'aa'},
                         {'a': '3', 'b': '20', 'c': 'a', 'd': 'aa'}])
