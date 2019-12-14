"""
Extract, transform, and load raw data.
"""
from pandas import DataFrame

from .ergast_tables import ErgastTables

def afew(data, n=5):
    """ DataFrame: Print DataFrame metadata and return a few rows. """
    schema = DataFrame()
    schema['dtype'] = data.dtypes
    schema['nulls'] = data.isnull().sum()
    print(f"{len(data)} rows", schema, sep="\n")

    return data.sample(n)
