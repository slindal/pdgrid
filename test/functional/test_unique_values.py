import pandas as pd
from pdgrid import unique_values

def test_unique_values():
    df = pd.DataFrame(columns=["a", "b"], data=[[1,2], [1,2], [1,3], [1,4]])
    
    assert(unique_values(df, "a") == [1])
    assert(unique_values(df, "b") == [2,3,4])
