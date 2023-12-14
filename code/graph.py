from numpy import fromiter, linspace, tanh
from numpy.random import randn
from pandas import Categorical, DataFrame
from scipy.sparse import coo_matrix, diags
from scipy.sparse.csgraph import laplacian


def radlimited(z, maxrad):
    """numpy array: z with magnitudes smoothly compressed to <= maxrad."""
    rad = abs(z).clip(1e-9, None)

    return z * maxrad * tanh(rad) / rad


def randomz(n):
    """numpy complex128 array: Random points inside unit square."""
    return randn(n).astype("complex128") + 1j * randn(n).astype("complex128")


def repel(points):
    """numpy complex128 array: 1/distance repulsive force on each point."""
    forces = (z - points for z in points)
    forces = (z / (z * z.conj()).real.clip(1e-9, None) for z in forces)
    forces = (z.mean() for z in forces)

    return fromiter(forces, count=len(points), dtype="complex128")


class GraphFrame:
    """
    Draw force-directed graphs with the Gephi ForceAtlas2 energy model.
    Graphs can be directed and/or weighted with integers or floats.
    If no weights are given, then links are weighted by how often they appear.
    Links with weight zero will be dropped.

    Inputs:
        DataFrame with [source, target, weight] as first 3 columns, OR
        DataFrame with [source, target] as first 2 columns, OR
        anything that pandas.DataFrame() can convert to one of the above
    """

    def __init__(self, links):
        links = DataFrame(links)

        cols = list(links.columns)
        links = links.groupby(cols[0:2], observed=True)
        links = links[cols[2]].sum() if (len(cols) > 2) else links.size()
        links.index.names, links.name = "source target".split(), "weight"
        links = links.loc[links.ne(0)].reset_index()

        cats = sorted(set(links["source"].unique()) | set(links["target"].unique()))
        links["source"] = Categorical(links["source"], categories=cats)
        links["target"] = Categorical(links["target"], categories=cats)

        self.links = links

    def __call__(self, nsteps=128):
        """
        DataFrame: Calculate ['x', 'y'] coordinates for each node.
        Nodes are recentered and scaled to fit in the unit circle.
        Initial positions are random in the unit square.
        """
        nodes = self.nodes
        springs = self.springs

        points = randomz(len(nodes))
        for speed in linspace(1, 0.1, nsteps - 1):
            forces = springs.dot(points) + repel(points)
            points += radlimited(forces, speed)

        points -= points.mean()
        points /= abs(points).max()

        return DataFrame({"x": points.real, "y": points.imag}, index=nodes)

    def __iter__(self):
        """Iterable of namedtuples: (source, target, weight) for each link."""
        return self.links.itertuples(index=False, name="Link")

    def __len__(self):
        """int: Number of links in graph."""
        return len(self.links)

    def __repr__(self):
        return f"{type(self).__name__} with {len(self)} links"

    def __str__(self):
        return "\n".join(f"{s} -> {t}: {w}" for s, t, w in self)

    # Constructors

    @classmethod
    def example(cls):
        """GraphFrame: Krackhardt kite with weighted tail links."""
        targets = {
            "a": list("bcdf"),
            "b": list("adeg"),
            "c": list("adf"),
            "d": list("abcefg"),
            "e": list("bdg"),
            "f": list("acdgh"),
            "g": list("bdefh"),
            "h": list("fgi"),
            "i": list("hj"),
            "j": list("ii"),
        }

        return cls.from_targets(targets)

    @classmethod
    def from_sources(cls, sources):
        """GraphFrame: New graph from {node: [iterable of sources]} mapping."""
        return cls.from_targets(sources).flipped

    @classmethod
    def from_targets(cls, targets):
        """GraphFrame: New graph from {node: [iterable of targets]} mapping."""
        return cls((s, t) for s, vals in targets.items() for t in vals)

    # Properties

    @property
    def degin(self):
        """Series: Total weight pointing into each node."""
        return self.links.groupby("target", observed=False)["weight"].sum()

    @property
    def degout(self):
        """Series: Total weight pointing out of each node."""
        return self.links.groupby("source", observed=False)["weight"].sum()

    @property
    def flipped(self):
        """GraphFrame: New graph with all links reversed."""
        return type(self)(self.links[["target", "source", "weight"]])

    @property
    def matrix(self):
        """scipy.sparse.csr: Sparse adjacency matrix."""
        links = self.links

        n = len(links["source"].cat.categories)
        i = links["source"].cat.codes.values
        j = links["target"].cat.codes.values
        k = links["weight"].values

        return coo_matrix((k, (i, j)), shape=(n, n)).tocsr()

    @property
    def nodes(self):
        """list: Sorted union of sources and targets."""
        return self.links["source"].cat.categories.tolist()

    @property
    def springs(self):
        """scipy.sparse.csr: Spring force matrix."""
        matrix = self.matrix

        springs = matrix - diags(matrix.diagonal())  # remove loops
        springs *= matrix.shape[0] / springs.sum()  # normalize spring constants
        springs = -1 * laplacian(springs, use_out_degree=True)

        return springs

    @property
    def weights(self):
        """Series: Weight of each (source, target) pair."""
        return self.links.groupby(["source", "target"], observed=True)["weight"].sum()

    # Exporters

    def pairs(self):
        """Generate 2-tuples: (source, target) pairs without weights."""
        return ((s, t) for s, t, w in self)

    def sources(self):
        """Generate (node, list[nodes]) tuples: Nodes pointing to each node."""
        return self.flipped.targets()

    def targets(self):
        """Generate (node, list[nodes]) tuples: Nodes to which each node points."""
        for k, v in self.links.groupby("source", observed=True)["target"]:
            yield k, sorted(v)

    # Plotting methods

    def plot(self, **kwargs):
        """AxesSubplot: Quick preview of graph layout for interactive use."""
        kwargs = {
            "alpha": 0.707,
            "figsize": (6, 6),
            "x": "x",
            "xlim": (-1, 1),
            "y": "y",
            "ylim": (-1, 1),
        } | kwargs

        return self().plot.scatter(**kwargs)
