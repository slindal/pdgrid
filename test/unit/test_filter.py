from pdgrid import unique_values, grid_values
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

    response = grid_values(df, group_model)
    rows = response['rows']
    assert(len(rows)) == 5
    assert(rows ==  [{'country': 'Australia', 'gold': '0'}, {'country': 'China', 'gold': '3'}, {'country': 'Romania', 'gold': '5'}, {'country': 'South Korea', 'gold': '1'}, {'country': 'United States', 'gold': '4'}]
)



def test_filterendpoint():
    df = pandas.read_json("/home/slindal/dev/pdgrid/test/manual/olympic-winners.json")
    response = unique_values(df, 'age')
    assert(response == ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '37', '41'])
    
