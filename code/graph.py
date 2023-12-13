from numpy import fromiter, linspace, sqrt, tanh
from numpy.random import randn
from pandas import Categorical, DataFrame
from scipy.sparse import coo_matrix, diags, identity
from scipy.sparse.csgraph import laplacian


def radlimited(z, maxr):
    """ndarray: Array with magnitudes smoothly compressed to <= maxr."""
    rad = abs(z).clip(1e-9, None)
    rad = tanh(rad) / rad
    rad *= maxr

    return rad * z


def randomz(n):
    """Numpy complex128 array: Random points inside unit square."""
    points = randn(n).astype("complex128")
    points += 1j * randn(n).astype("complex128")

    return points


def repel(points):
    """Numpy complex128 array: Repulsive force on each point"""
    vectors = (z - points for z in points)
    invsqrd = (z / (z * z.conj()).real.clip(1e-9, None) for z in vectors)
    forces = (z.mean() for z in invsqrd)

    return fromiter(forces, count=len(points), dtype="complex128")


class GraphFrame:
    """
    Store graph data and calculate coordinates for drawing that graph.
    Uses drawing physics based on based on Gephi's ForceAtlas2 energy model.

    Inputs:
        DataFrame with [source, target] as first 2 columns, OR
        DataFrame with [source, target, weight] as first 3 columns, OR
        anything accepted by pandas.DataFrame() constructor

    If no weight is provided, links are weighted by how often they appear.

    Call with a number of timesteps to return two NumPy arrays (x, y).
    Call accepts optional starting coordinates as 'x', 'y' keyword arguments.
    Coordinates are typically, but not always, in the range [-1, 1].
    """

    def __init__(self, links):
        links = DataFrame(links)
        cols = list(links.columns)

        # Sum weights for each (source, target) pair
        links = links.groupby(cols[0:2], observed=True)
        links = links[cols[2]].sum() if (len(cols) > 2) else links.size()
        links.index.names = "source target".split()
        links.name = "weight"

        # Drop zero-weight links and convert to DataFrame
        links = links.loc[links.ne(0)].reset_index()

        # Convert sources and targets to Categorical
        cats = sorted(set(links["source"].unique()) | set(links["target"].unique()))
        links["source"] = Categorical(links["source"], categories=cats)
        links["target"] = Categorical(links["target"], categories=cats)

        self.links = links

    def __call__(self, nsteps=64):
        nodes = self.nodes
        springs = self.springs

        points = randomz(len(nodes))
        for speed in linspace(1, 0.1, nsteps - 1):
            forces = springs.dot(points) + repel(points)
            points += radlimited(forces, speed)

        points -= points.mean()
        points /= abs(points).max()

        data = DataFrame(index=nodes)
        data["x"] = points.real
        data["y"] = points.imag

        return data

    def __len__(self):
        return len(self.links)

    def __repr__(self):
        return f"{type(self).__name__} with {len(self)} links\n{self.links}"

    # Constructors

    @classmethod
    def example(cls):
        """GraphFrame: Krackhardt kite graph. """
        targets = {
            'a': list('bcdf'),
            'b': list('adeg'),
            'c': list('adf'),
            'd': list('abcefg'),
            'e': list('bdg'),
            'f': list('acdgh'),
            'g': list('bdefh'),
            'h': list('fgi'),
            'i': list('h'),
            'j': list('i'),
        }

        return cls.from_targets(targets)

    def flipped(self):
        """GraphFrame: New graph with all links reversed."""
        return type(self)(self.links[["target", "source", "weight"]])

    @classmethod
    def from_sources(cls, sources):
        """GraphFrame: New graph from {node: [iterable of sources]} mapping."""
        return cls.from_targets(sources).flipped()

    @classmethod
    def from_targets(cls, targets):
        """GraphFrame: New graph from {node: [iterable of targets]} mapping."""
        return cls((s, t) for s, vals in targets.items() for t in vals)

    # Properties

    @property
    def matrix(self):
        """scipy.sparse.csr: Sparse adjacency matrix."""
        links, nodes = self.links, self.nodes

        i = links["source"].cat.codes.values
        j = links["target"].cat.codes.values
        k = links["weight"].values
        n = len(nodes)

        return coo_matrix((k, (i, j)), shape=(n, n)).tocsr()

    @property
    def nodes(self):
        """list: Sorted union of sources and targets."""
        return self.links["source"].cat.categories.tolist()

    @property
    def springs(self):
        """scipy.sparse.csr: Spring force matrix."""
        matrix = self.matrix
        nodes = self.nodes

        nrows = len(nodes)
        springs = matrix - diags(matrix.diagonal())  # remove loops
        springs *= nrows / springs.sum()  # normalize spring constants
        springs = laplacian(springs, use_out_degree=True)
        springs *= -1

        return springs

    @property
    def weights(self):
        """Series: Weight of each (source, target) pair."""
        return self.links.groupby(["source", "target"], observed=True)["weight"].sum()

    # Iterators

    def __iter__(self):
        return self.links.itertuples(index=False, name="Link")

    def pairs(self):
        """list of lists: [source, target] pairs without weights."""
        return ((s, t) for s, t, w in self)

    def sources(self):
        """dict of lists: Sources for each target in graph."""
        return self.flipped().targets()

    def targets(self):
        """dict of lists: Targets for each source in graph."""
        for k, v in self.links.groupby("source", observed=True)["target"]:
            yield k, sorted(v)

    # Drawing methods

    def plot(self, t=64, **kwargs):
        """AxesSubplot: Scatterplot of graph node coordinates after t timesteps."""
        kwargs = {
            "color": "k",
            "figsize": (8, 8),
            "x": "x",
            "xlim": (-1, 1),
            "y": "y",
            "ylim": (-1, 1),
        } | kwargs

        return self(t).plot.scatter(**kwargs)
