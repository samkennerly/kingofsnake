"""
Data visualization tools.
UNDER CONSTRUCTION
"""
from pandas import DataFrame

CMAP = 'nipy_spectral_r'
FIGSIZE = (12, 6)
LEGEND = (('bbox_to_anchor', (1, 1)), ('loc', 'upper left'))

class Plot:
    """
    UNDER CONSTRUCTION
    DataFrame inputs
    """

    def __init__(self, **kwargs):
        kwargs.setdefault('cmap', CMAP)
        kwargs.setdefault('figsize', FIGSIZE)
        kwargs.setdefault('title', None)

        self.default = kwargs
        self.legend = dict(LEGEND)

    def __call__(self, data, **kwargs):
        """ AxesSubplot: Fill default values and create figure. """
        default, legend = self.default, self.legend

        kwargs = {**default, **kwargs}
        xlabel = kwargs.pop('xlabel', None)
        ylabel = kwargs.pop('ylabel', None)
        kwargs.pop('cmap') if 'color' in kwargs else None

        axes = DataFrame(data).plot(**kwargs)
        axes.legend(**legend)
        axes.set_xlabel(xlabel) if xlabel else None
        axes.set_ylabel(ylabel) if ylabel else None
        axes.figure.tight_layout()

        return axes

    def __repr__(self):
        name = type(self).__name__
        params = ", ".join( f"{k}={v}" for k,v in vars(self).items() )

        return f"{name}({params})"

    def area(self, data, **kwargs):
        """ AxesSubplot: Mountain plot for each column. """
        raise NotImplementedError

    def bar(self, data, **kwargs):
        """ AxesSubplot: Bar plot for each column. """
        kwargs.setdefault('kind', 'bar')
        kwargs.setdefault('grid', False)
        kwargs.setdefault('stacked', True)
        kwargs.setdefault('width', 0.9)

        return self(data, **kwargs)

    def heat(self, data, **kwargs):
        """ AxesSubplot: Heatmap with same rows and columns as input. """
        raise NotImplementedError

    def hist(self, data, **kwargs):
        """ AxesSubplot: Histogram for each column. """
        raise NotImplementedError

    def line(self, data, **kwargs):
        """ AxesSubplot: Line plot for each column. """
        raise NotImplementedError

    def quant(self, data, q=(), **kwargs):
        """ AxesSubplot: Quantiles for each column. """
        q = list(q) or [0, 0.05, 0.25, 0.50, 0.75, 0.95, 1]
        data = data.quantile(q=q)
        data.columns = data.columns.astype(str)

        axes = data.plot.line(**kwargs)

    def scatter(self, data, **kwargs):
        raise NotImplementedError
