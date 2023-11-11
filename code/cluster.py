from pandas import Categorical, DataFrame, Series
from scipy.cluster.hierarchy import fcluster, linkage

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
