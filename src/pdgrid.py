import pandas as pd


def unique_values(df, columns):
    return {column : df[column].drop_duplicates().to_json(orient='records') for column in columns}
