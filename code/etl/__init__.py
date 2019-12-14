"""
Extract, transform, and load raw data.
"""
from pathlib import Path

from pandas import DataFrame

from .ergast import ErgastF1

REPO = Path(__file__).resolve().parent.parent.parent
DATADIR = REPO / "data"


def afew(data, n=5):
    """ DataFrame: Print DataFrame metadata and return a few rows. """
    schema = DataFrame()
    schema["dtype"] = data.dtypes
    schema["nulls"] = data.isnull().sum()
    print(f"{len(data)} rows", schema, sep="\n")

    return data.sample(n)
