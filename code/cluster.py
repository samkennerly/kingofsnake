from matplotlib.pyplot import figure
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
        **kwargs    are passed to scipy.cluster.hierarchy.fcluster()

    See scipy.cluster.hierarchy docs for more information.
    """

    def __init__(self, data, **kwargs):
        kwargs = {
            "method": "weighted",
            "metric": "cosine",
            "optimal_ordering": False,
        } | kwargs

        data = data.select_dtypes("number")
        links = DataFrame(linkage(data, **kwargs))
        links.columns = "left right distance count".split()
        for c in links.columns.drop("distance"):
            links[c] = links[c].astype(int)

        self.features = data.columns.copy()
        self.leaves = data.index.copy()
        self.links = links

    def __call__(self, n, **kwargs):
        leaves = self.leaves
        links = self.links

        kwargs = {"criterion": "maxclust"} | kwargs

        cluster = fcluster(links, n, **kwargs) - 1
        cluster = Series(cluster, index=leaves, name="cluster")

        return cluster

    def __len__(self):
        return len(self.leaves)

    def __repr__(self):
        return f"{type(self).__name__} with {len(self)} leaves"

    def plot(self, n=0, figsize=(9, 3), **kwargs):
        """
        matplotlib Axes: Plot a tree of hierarchical clusters.

        Inputs
            n           int: number of clusters to show
            figsize     (int, int): size of matplotlib figure to create

            **kwargs    are passed to scipy.cluster.hierarchy.dendrogram
        """
        leaves = self.leaves
        links = self.links

        n = int(n) or len(leaves)
        kwargs = {
            "color_threshold": 0.5,
            "count_sort": False,
            "labels": leaves,
            "no_labels": False,
            "orientation": "top",
            "show_contracted": True,
            "truncate_mode": "lastp",
        } | kwargs

        axes = figure(figsize=figsize).add_subplot()
        axes.set_xlabel(f"cluster")
        axes.set_ylabel("distance")

        dendrogram(links, n, ax=axes, **kwargs)

        return axes
