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
    return data.loc[random.choice(data.index, n)]


def irisdata():
    """ DataFrame: Fisher's iris dataset with covfefe removed. """
    data = load_iris()
    cols = [x.rstrip("(cm)").strip().replace(" ", "_") for x in data.feature_names]
    cats = Categorical.from_codes(data.target, data.target_names)

    return DataFrame(data.data, columns=cols).assign(species=cats)


def zscores(data, robust=False):
    """ DataFrame: Data with each column standardized. """
    data = DataFrame(data).copy()
    for col in data.columns:
        data[col] -= data[col].median() if robust else data[col].mean()
        data[col] /= data[col].mad() if robust else data[col].std()

    return data
