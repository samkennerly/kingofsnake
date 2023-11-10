"""
Constants and convenience functions.
"""
from pathlib import Path

from numpy import random
from pandas import Categorical, DataFrame, Series, read_csv, to_datetime
from sklearn.datasets import load_iris


REPO = Path(__file__).resolve().parent.parent
DATADIR = REPO / "data"


def afew(data, n=5):
    """ DataFrame view: Distinct random rows from a DataFrame. """
    return data.loc[random.choice(data.index, size=n, replace=False)].copy()


def datasplit(data, nrows=0):
    """ (DataFrame, DataFrame): Partition rows into 2 disjoint DataFrames. """
    nrows = nrows or len(data) // 2

    trainrows = afew(data, nrows).sort_index()
    testrows = data.drop(index = trainrows.index)

    return trainrows, testrows


def irisdata():
    """ DataFrame: Fisher's iris dataset from scikit-learn. """
    raw = load_iris()
    cols = [x.rstrip("(cm)").strip().replace(" ", "_") for x in raw.feature_names]
    cats = Categorical.from_codes(raw.target, raw.target_names)
    data = DataFrame(raw.data, columns=cols).assign(species=cats)

    return data


def zscores(data, robust=False):
    """ DataFrame: Data with each numeric column standardized. """
    data = DataFrame(data).copy()

    for c in data.select_dtypes('number').columns:
        data[c] -= (data[c].median() if robust else data[c].mean())
        data[c] /= (data[c].abs().mean() if robust else data[c].std())

    return data


# Copyright © 2023 Sam Kennerly
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
