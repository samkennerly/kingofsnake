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


# Copyright © 2020 Sam Kennerly
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
