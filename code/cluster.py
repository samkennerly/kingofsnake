from pandas import Categorical, DataFrame, Index, Series
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage

class Hierarchy:
    """
    SciPy hierarchical clustering with pandas inputs and outputs.
    Construct with a DataFrame. Non-numeric columns are ignored.
    Call to return a Series assigning each row to a cluster.

    Constructor inputs:
        data        DataFrame: observations to use for training
        **kwargs    are passed to scipy.cluster.hierarchy.linkage()

    Call inputs:
        n           int: maximum number of distinct clusters
        cats        optional Iterable: category labels for clusters
        **kwargs    are passed to scipy.cluster.hierarchy.fcluster()

    See scipy.cluster.hierarchy docs for more information.
    """

    def __init__(self, data, **kwargs):
        kwargs = {
            "method": "average",
            "metric": "cosine",
            "optimal_ordering": False,
            } | kwargs

        feats = data.select_dtypes("number")
        links = DataFrame(linkage(feats, **kwargs))
        links.columns = "left right distance count".split()
        for c in links.columns.drop("distance"):
            links[c] = links[c].astype(int)

        self.features = feats.columns.tolist()
        self.links = links
        self.params = kwargs

    def __call__(self, n, cats=(), **kwargs):
        leaves = self.leaves
        links = self.links
        kwargs = {
            "criterion": "maxclust",
            "depth": 2,
        } | kwargs

        cluster = fcluster(links, n, **kwargs) - 1
        cluster = Series(cluster, index=leaves, name="cluster")

        return cluster

    def __len__(self):
        return len(self.links)

    def __repr__(self):
        return f"{type(self).__name__} with {len(self)} links"

    @property
    def leaves(self):
        """ Index: Row numbers for the original input data. """
        return Index(range(1 + len(self.links)))

    def plot(self, **kwargs):
        raise NotImplementedError
