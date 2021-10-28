import pandas as pd
from src.pdgrid import unique_values, expand_nodes

def test_unique_values():
    df = pd.DataFrame(columns=["a", "b"], data=[[1,2], [1,2], [1,3], [1,4]])
    
    uv = unique_values(df, "a")
    assert(unique_values(df, "a") == {"a": [1]})
    assert(unique_values(df, "b") == {"b": [2,3,4]})

    assert(unique_values(df, ["a", "b"]) == { "a": [1],
                                              "b": [2,3,4] })
    
