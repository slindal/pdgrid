from pdgrid.server import app
from unittest import mock
import pandas as pd
import json
import itertools

def test_1():

    with app.test_client() as client:
        group_model = '''{
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
            "pivotMode": false,
            "groupKeys": [],
            "filterModel": {"age": {"values": ["16", "15"], "filterType": "set"}},
            "sortModel": []
        }'''

        response = client.post('/api/olympicWinners/', data=group_model)
        rows = json.loads(response.data)['rows']
        assert(len(rows)) == 5
        assert(rows ==  [{'country': 'Australia', 'gold': '0'}, {'country': 'China', 'gold': '3'}, {'country': 'Romania', 'gold': '5'}, {'country': 'South Korea', 'gold': '1'}, {'country': 'United States', 'gold': '4'}]
)



def test_filterendpoint():
    with app.test_client() as client:
        response = client.get('/api/olympicWinners/age/')
        print(json.loads(response.data))
        assert(json.loads(response.data) == ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '37', '41'])
