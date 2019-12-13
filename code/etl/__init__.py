"""
Extract, Transform, and/or Load data.
"""
from pathlib import Path

from pandas import DataFrame

from .ergast_tables import ErgastTables

def show(data, n=5):
    """ None: Show DataFrame size and schema. """
    print(f"{len(data)} rows")
    print(data.dtypes, "", "nulls", data.isnull().sum(), sep="\n")

    return data.head(n)
