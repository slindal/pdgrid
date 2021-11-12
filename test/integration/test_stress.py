from pdgrid.server import load_dataframe
from pdgrid.server import app
from unittest import mock
import pandas as pd
import json
import itertools


@mock.patch('pdgrid.server.load_dataframe')
def test_1(load_dataframe):

    groupkeys = ["".join(p) for p in itertools.product("AAABBCDE", repeat=6)]
    values = range(len(groupkeys))
    df = pd.DataFrame()
    df['a'] = groupkeys
    df['b'] = values
    
    
    load_dataframe.return_value = df
                                    
    
    with app.test_client() as client:
        group_model = '''{
            "startRow": 0,
            "endRow": 100,
            "rowGroupCols": [{"id":"a", "field":"a"}],
            "valueCols": [
                {
                    "id": "b",
                    "aggFunc": "sum",
                    "displayName": "B",
                    "field": "b"
                }
            ],
            "pivotCols": [],
            "pivotMode": false,
            "groupKeys": [],
            "filterModel": {},
            "sortModel": []
        }'''

        response = client.post('/api/olympicWinners/', data= group_model)
        rows = json.loads(response.data)['rows']
        assert(len(rows)) == 100
#        assert(rows ==  [{'a': '1', 'b': '10', 'c': 'a'}, {'a': '3', 'b': '20', 'c': 'a'}])



