"""
Constants and convenience functions.
"""
from pathlib import Path

from numpy import cov, random
from numpy.linalg import eigh
from pandas import Categorical, DataFrame, Series, read_csv, to_datetime
from sklearn.datasets import load_iris


REPO = Path(__file__).resolve().parent.parent
DATADIR = REPO / "data"


def afew(data, n=5):
    """DataFrame view: Distinct random rows from a DataFrame."""
    return data.loc[random.choice(data.index, size=n, replace=False)].copy()


def irisdata():
    """DataFrame: Fisher's iris dataset from scikit-learn."""
    raw = load_iris()
    cols = [x.rstrip("(cm)").strip().replace(" ", "_") for x in raw.feature_names]
    cats = Categorical.from_codes(raw.target, raw.target_names)
    data = DataFrame(raw.data, columns=cols).assign(species=cats)

    return data


def princols(data, ncols=2):
    """
    DataFrame: DataFrame with numerical columns replaced by principal components.

    Inputs:
        data    DataFrame   features are columns and rows are observations
        ncols   int > 0     output will have this many columns
    """
    feats = data[data.select_dtypes("number").columns]
    notfeats = data[data.columns.drop(feats.columns)]

    # Find eigenvectors of covariance matrix with largest eigenvalues
    eigvals, eigvecs = eigh(cov(feats, rowvar=False))
    eigvecs = eigvecs[:, -1 : -(1 + ncols) : -1]

    # Transform features to new coordinates
    pcols = DataFrame(feats @ eigvecs)
    pcols.columns = [f"pc{n}" for n in range(ncols)]

    return pcols.join(notfeats)


def zscores(data, robust=False):
    """DataFrame: Data with each numeric column standardized."""
    data = DataFrame(data).copy()

    for c in data.select_dtypes("number").columns:
        data[c] -= data[c].median() if robust else data[c].mean()
        data[c] /= data[c].abs().mean() if robust else data[c].std()

    return data
