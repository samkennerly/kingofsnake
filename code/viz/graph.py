from pandas import Categorical, DataFrame
from scipy.sparse import coo_matrix

LINKS = (
    ('dave', 'dave'),
    ('dave', 'eve'),
    ('alice', 'bob'),
    ('bob', 'carol'),
    ('carol', 'alice'),
)

def weighted(links):
    """ DataFrame: [source, target, weight] for each link. """
    links = DataFrame(links)
    cols = list(links.columns)
    links = links.groupby(cols[0:2], observed=True)
    links = links[cols[2]].sum() if (len(cols) > 2) else links.size().rename("_")

    nodes = links.index.unique(level=0) | links.index.unique(level=1)
    links = links.loc[links.ne(0)].astype(float).reset_index()
    links.columns = 'source target weight'.split()
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

    def __init__(self, links):
        self.frame = links.frame if isinstance(links, type(self)) else weighted(links)

    def __len__(self):
        return len(self.frame)

    def __repr__(self):
        return f"{type(self).__name__} with {len(self)} links\n{self.frame}"

    @property
    def links(self):
        """ Iterator[namedtuple]: (source, target, weight) for each link. """
        return self.frame.itertuples(index=False, name='Link')

    @property
    def matrix(self):
        """ scipy.sparse.coo: Links as a sparse matrix. """
        frame, nodes = self.frame, self.nodes

        i = frame['source'].cat.codes.values
        j = frame['target'].cat.codes.values
        k = frame['weight'].values
        n = len(nodes)

        return coo_matrix((k, (i, j)), shape=(n, n))

    @property
    def nodes(self):
        """ Index: Sorted union of sources and targets. """
        return self.frame['source'].cat.categories
















