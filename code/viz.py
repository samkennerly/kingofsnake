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
        setkw = kwargs.setdefault
        setkw('cmap', CMAP)
        setkw('figsize', FIGSIZE)
        setkw('title', None)

        self.default = kwargs
        self.legend = dict(LEGEND)

    def __call__(self, data, **kwargs):
        """ AxesSubplot: Fill default values and create figure. """
        default, legend = self.default, self.legend

        kwargs = {**default, **kwargs}
        kwargs.pop('cmap') if 'color' in kwargs else None
        facecolor = kwargs.pop('facecolor', None)
        xlabel = kwargs.pop('xlabel', None)
        ylabel = kwargs.pop('ylabel', None)

        axes = DataFrame(data).plot(**kwargs)
        axes.figure.tight_layout()
        axes.set_facecolor(facecolor) if facecolor else None
        axes.set_xlabel(xlabel) if xlabel else None
        axes.set_ylabel(ylabel) if ylabel else None
        axes.legend(**legend)

        return axes

    def __repr__(self):
        name = type(self).__name__
        params = ", ".join( f"{k}={v}" for k,v in vars(self).items() )

        return f"{name}({params})"

    # DataFrame input

    def area(self, data, **kwargs):
        """ AxesSubplot: Mountain plot for each column. """
        raise NotImplementedError

    def bar(self, data, **kwargs):
        """ AxesSubplot: Bar chart for each column. """
        setkw = kwargs.setdefault
        setkw('grid', False)
        setkw('kind', 'bar')
        setkw('stacked', True)
        setkw('width', 0.9)

        return self(data, **kwargs)

    def heat(self, data, **kwargs):
        """ AxesSubplot: Heatmap with same rows and columns as input. """
        raise NotImplementedError

    def hist(self, data, **kwargs):
        """ AxesSubplot: Histogram for each column. """
        setkw = kwargs.setdefault
        setkw('grid', True)
        setkw('kind', 'hist')
        setkw('stacked', True)
        setkw('bins', 33)

        return self(data, **kwargs)

    def line(self, data, **kwargs):
        """ AxesSubplot: Line plot for each column. """
        raise NotImplementedError

    def scatter(self, data, **kwargs):
        raise NotImplementedError

    # Timeseries input

    def quant(self, ts, freq, q=(), **kwargs):
        """ AxesSubplot: Contour plot of quantiles per period. """
        kwset = kwargs.setdefault
        kwset('color', list('krygbck'))
        kwset('grid', True)
        kwset('stacked', False)
        q = list(q) or [0, 0.05, 0.25, 0.50, 0.75, 0.95, 1]
        data = ts.resample(freq).quantile(q).unstack()
        data.columns = [ f"{int(100 * x)} percentile" for x in data.columns ]

        return self(data, **kwargs)




