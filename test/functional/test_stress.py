from pdgrid import aggrid_values
from unittest import mock
import pandas as pd
import json
import itertools


def test_1():

    groupkeys = ["".join(p) for p in itertools.product("AAABBCDE", repeat=6)]
    values = range(len(groupkeys))
    df = pd.DataFrame()
    df['a'] = groupkeys
    df['b'] = values
    
    group_model = {
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
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {},
        "sortModel": []
    }
    
    result = aggrid_values(df, group_model)
    assert(len(result['rows'])) == 100



