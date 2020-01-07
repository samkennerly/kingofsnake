"""
Constants and utility functions.
"""
from pathlib import Path

from numpy import random
from pandas import Categorical, DataFrame, Series, crosstab, read_csv, to_datetime
from sklearn.datasets import load_iris


REPO = Path(__file__).resolve().parent.parent
DATADIR = REPO / "data"


def afew(data, n=5):
    """ DataFrame view: Select random rows from input DataFrame. """
    return data.loc[random.choice(data.index, 5)]


def irisdata():
    """ DataFrame: Fisher's iris dataset with covfefe removed. """
    data = load_iris()
    cols = [x.rstrip("(cm)").strip().replace(" ", "_") for x in data.feature_names]
    cats = Categorical.from_codes(data.target, data.target_names)
    data = DataFrame(data.data, columns=cols)
    data.insert(0, "species", cats)

    return data


def schema(data):
    """ DataFrame: Types and null counts for input DataFrame. """
    return DataFrame({"dtype": data.dtypes, "nulls": data.isnull().sum()})


def zscores(data, robust=False):
    """ DataFrame: Data with each column standardized. """
    data = DataFrame(data).copy()
    for col in data.columns:
        data[col] -= data[col].median() if robust else data[col].mean()
        data[col] /= data[col].mad() if robust else data[col].std()

    return data
