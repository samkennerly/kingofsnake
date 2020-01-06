"""
Constants and utility functions.
"""
from pathlib import Path

from pandas import Categorical, DataFrame, Series
from sklearn.datasets import load_iris

from graph import Graph
from plot import Plot


REPO = Path(__file__).resolve().parent.parent
DATADIR = REPO / "data"


def afew(data, n=5):
    """ DataFrame: Print DataFrame metadata and return a few rows. """
    schema = DataFrame({"dtype": data.dtypes, "nulls": data.isnull().sum()})
    print(f"[{len(data)} rows x {len(schema)} columns]", schema, sep="\n")

    return data.tail(n)


def iris():
    """ DataFrame: Fisher's iris dataset with covfefe removed. """
    data = load_iris()
    cols = [ x.rstrip('(cm)').strip().replace(' ', '_') for x in data.feature_names ]
    cats = Categorical.from_codes(data.target, data.target_names)
    data = DataFrame(data.data, columns=cols)
    data.insert(0, 'species', cats)

    return data


def zscores(data, robust=False):
    """ DataFrame: Data with each column standardized. """
    data = DataFrame(data).copy()
    for col in data.columns:
        data[col] -= data[col].median() if robust else data[col].mean()
        data[col] /= data[col].mad() if robust else data[col].std()

    return data
