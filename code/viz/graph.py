from numpy import fromiter, linspace, tanh
from numpy.random import randn
from pandas import Categorical, DataFrame
from scipy.sparse import coo_matrix, diags, identity
from scipy.sparse.csgraph import laplacian

def limited(z, maxr):
    """ ndarray: Array with magnitudes smoothly compressed to <= 1. """
    rad = abs(z).clip(1e-9, None)
    rad = tanh(rad) / rad
    rad *= maxr

    return rad * z

def weighted(links):
    """ DataFrame: [source, target, weight] for each link. """
    links = DataFrame(links)
    cols = list(links.columns)

    links = links.groupby(cols[0:2], observed=True)
    links = links[cols[2]].sum() if (len(cols) > 2) else links.size().rename("_")
    links = links.loc[links.ne(0)].astype(float).reset_index()
    links.columns = 'source target weight'.split()

    nodes = sorted(set(links['source'].unique()) | set(links['target'].unique()))
    for col in 'source target'.split():
        links[col] = Categorical(links[col], categories=nodes)

    return links

class Graph:
    """
    Directed, weighted graph based on pandas.DataFrame.

    Accepts any valid DataFrame() input with 2 or 3 columns.
    Sums weights if they exist; else counts duplicated links.
    Source and target are categorials with the same categories.
    """

    def __init__(self, graph):
        self.links = graph.links if isinstance(graph, type(self)) else weighted(graph)

    def __call__(self, steps=100):
        matrix, nodes = self.matrix, self.nodes

        n = len(nodes)
        dtype = 'complex128'
        points = 0.5 * (randn(n) + 1j * randn(n)).astype(dtype)

        yield points.real.copy(), points.imag.copy()

        matrix -= diags(matrix.diagonal())
        matrix *= -n / matrix.sum()
        matrix = laplacian(matrix, use_out_degree=True)
        matrix -= identity(n, dtype=matrix.dtype, format=matrix.format)

        for speed in linspace(1, 0.1, steps-1):
            forces = ( z - points for z in points )
            forces = ( z / (z * z.conj()).real.clip(1e-3, None) for z in forces )
            forces = fromiter(( z.mean() for z in forces ), count=n, dtype=dtype)
            forces += matrix.dot(points)
            points += limited(forces, speed)

            yield points.real.copy(), points.imag.copy()

    def __iter__(self):
        return self.links.itertuples(index=False, name='Link')

    def __len__(self):
        return len(self.links)

    def __repr__(self):
        return f"{type(self).__name__} with {len(self)} links\n{self.links}"

    def frame(self, n):
        nodes = self.nodes
        for x,y in self(n): pass

        return DataFrame({'x': x, 'y': y}, index=nodes)

    @property
    def matrix(self):
        """ scipy.sparse.coo: Links as a sparse matrix. """
        links, nodes = self.links, self.nodes

        i = links['source'].cat.codes.values
        j = links['target'].cat.codes.values
        k = links['weight'].values
        n = len(nodes)

        return coo_matrix((k, (i, j)), shape=(n, n)).tocsr()

    @property
    def nodes(self):
        """ Index: Sorted union of sources and targets. """
        return self.links['source'].cat.categories
















