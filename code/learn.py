"""
Machine learning examples with SciPy and scikit-learn.
"""
from pandas import Categorical, DataFrame, Series
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn import linear_model


class Classify:
    """
    Train, use, and re-use an automatic classifier.
    Input training data, then call with new data to return a Series.

    Constructor inputs:
        clues       DataFrame: Training data with numeric columns.
        answers     Iterable: Known classes. Must align with clues.
        model       optional str: Name of an sklearn.linear_model.
        **kwargs    will be passed to the chosen model.

    Call inputs:
        clues       DataFrame: Same columns as training 'clues'.
        probs       bool: Return a DataFrame of class probabilties?

    Note: Some models cannot return class probabilities.
    """

    def __init__(self, clues, answers, model="LogisticRegressionCV", **kwargs):
        answers = Categorical(answers)
        clues = DataFrame(clues)
        model = getattr(linear_model, str(model))

        self.cats = answers.categories.tolist()
        self.columns = clues.columns.tolist()
        self.model = model(**kwargs).fit(clues, answers.codes)

    def __call__(self, clues, probs=False):
        cats, model = self.cats, self.model

        clues = DataFrame(clues)
        if probs:
            data = DataFrame(model.predict_proba(clues), columns=cats)
            data.index = clues.index
        else:
            data = Categorical.from_codes(model.predict(clues), categories=cats)
            data = Series(data, index=clues.index, name="class")

        return data

    def __repr__(self):
        clsname = type(self).__name__
        modname = type(self.model).__name__
        keyvals = " ".join(f"\n    {k}={v}" for k, v in self.params.items())

        return f"{clsname}(\n    model={modname}, {keyvals})"

    @property
    def params(self):
        """ dict: Model parameters. """
        return self.model.get_params()

    @property
    def coefs(self):
        """ DataFrame: Model coefficients. """
        return DataFrame(self.model.coef_, index=self.cats, columns=self.columns)


class Cluster:
    """
    Assign each row of a table to exactly one cluster.
    Input numeric observations, then call to return a Series.
    Each row of input matrix is assigned to exactly one cluster.

    Constructor inputs:
        data        DataFrame: Numeric columns with or without index.
        **kwargs    are passed to scipy.cluster.hierarchy.linkage().

    Call inputs:
        n           int: Maximum number of distinct clusters.
        cats        optional Iterable: Category labels for clusters.
        **kwargs    are passed to scipy.cluster.hierarchy.fcluster().

    See scipy.cluster.hierarchy docs for more information.
    """

    def __init__(self, data, **kwargs):
        kwargs.setdefault("method", "average")
        kwargs.setdefault("metric", "cosine")
        data = DataFrame(data)

        links = linkage(data, **kwargs)
        links = DataFrame(links, columns="a b distance count".split())
        for c in links.columns.drop("distance"):
            links[c] = links[c].astype(int)

        self.links = links

    def __call__(self, n, cats=(), **kwargs):
        leaves, links = self.leaves, self.links

        kwargs.setdefault("criterion", "maxclust")
        cluster = fcluster(links, n, **kwargs) - 1
        if len(cats):
            cluster = Categorical.from_codes(cluster, cats)

        return Series(cluster, name="cluster")

    def __len__(self):
        return len(self.links)

    def __repr__(self):
        return f"{type(self).__name__} with {len(self)} links\n{self.links}"

    @property
    def leaves(self):
        """ List[int]: Row numbers for the original input data. """
        return list(range(1 + len(self.links)))


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
