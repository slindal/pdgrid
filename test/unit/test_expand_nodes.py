import pandas as pd
from src.pdgrid import expand_nodes


def test_expand_nodes1():
    df = pd.DataFrame(columns=["a", "b", "c"], data=[[1,2,'a'], [1,2,'a'], [1,3, 'b'], [1,4,'c']])
    df = expand_nodes(df, {'groupKeys': [2], "rowGroupCols": [{"field": "b"}]})
    assert df.index.size == 2
    assert (df['b'] == 2).all()
    
def test_expand_nodes2():
    df = pd.DataFrame(columns=["a", "b", "c"], data=[[1,2,'a'], [1,2,'a'], [1,3, 'b'], [1,4,'c']])
    df = expand_nodes(df, {'groupKeys': ["a"], "rowGroupCols": [{"field": "c"}]})
    assert df.index.size == 2

def test_expand_nodes3():
    df = pd.DataFrame(columns=["a", "b", "c"], data=[[1,2,'a'], [1,2,'b'], [1,3, 'a'], [1,4,'c']])
    df = expand_nodes(df, {'groupKeys': ["a", 2], "rowGroupCols": [{"field": "c"}, {'field': "b"}]})
    assert df.index.size == 1
