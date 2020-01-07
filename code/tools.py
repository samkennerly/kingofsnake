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


def nycenergy(path=DATADIR/'examples/energy.csv', start=2000):
    """ DataFrame: New York state energy sources. """
    data = read_csv(path)
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')
    data = data.loc[lambda df: df['year'].ge(start)].drop(columns = ['total'])
    data['hydro'] = data.pop('conv._hydro') + data.pop('ps_hydro')
    data['year'] = to_datetime(data['year'], format='%Y')
    data['gas'] = data.pop('lfg') + data.pop('natural_gas')
    data = data.set_index('year').sort_index().sort_index(axis=1)

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
