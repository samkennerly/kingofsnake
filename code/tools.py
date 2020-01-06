"""
Constants and utility functions.
"""
from pathlib import Path

from pandas import DataFrame, Series

REPO = Path(__file__).resolve().parent.parent
DATADIR = REPO / "data"

def afew(data, n=5):
    """ DataFrame: Print DataFrame metadata and return a few rows. """
    schema = DataFrame({"dtype": data.dtypes, "nulls": data.isnull().sum()})
    print(f"[{len(data)} rows x {len(schema)} columns]", schema, sep="\n")

    return data.tail(n)

