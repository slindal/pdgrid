from pdgrid import aggrid_values
from unittest import mock
import pandas as pd
import json
import itertools
import numpy

from timeit import default_timer as timer


import cProfile, pstats
from pstats import SortKey
import io

def test_1():

    groupkeys = ["".join(p) for p in itertools.product("AAABBCDEFGHKK", repeat=6)]
    values = range(len(groupkeys))
    df = pd.DataFrame()
    df['a'] = groupkeys
    df['b'] = values
    df['c'] = values
    df['d'] = values
    df['f'] = values
    
    print(df.index.size)
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
            },
            {
                "id": "c",
                "aggFunc": "mean",
                "displayName": "C",
                "field": "c"
            },
            {
                "id": "d",
                "aggFunc": "min",
                "displayName": "D",
                "field": "d"
            },
        ],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {},
        "sortModel": [{'colId': 'b', 'sort': 'desc'}]
    }

    start = timer()


    with cProfile.Profile() as pr:
        result = aggrid_values(df, group_model)
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    print (timer() - start)
    assert(len(result['rows'])) == 100
    print (result['rows'][0])


def test_2():
    groupkeys = numpy.random.randint(0, 100, 10000000)
    values = numpy.random.normal(5, 3, 10000000)
    df = pd.DataFrame()
    df['a'] = groupkeys
    df['b'] = values
    df['c'] = values
    df['d'] = values
    df['f'] = values
    
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
            },
            {
                "id": "c",
                "aggFunc": "mean",
                "displayName": "C",
                "field": "c"
            },
            {
                "id": "d",
                "aggFunc": "min",
                "displayName": "D",
                "field": "d"
            },
        ],
        "pivotCols": [],
        "pivotMode": False,
        "groupKeys": [],
        "filterModel": {},
        "sortModel": [{'colId': 'b', 'sort': 'desc'}]
    }

    start = timer()
    result = aggrid_values(df, group_model)
    print (timer() - start)
    assert(len(result['rows'])) == 100
    print (result['rows'][0])
