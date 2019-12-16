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
        kwset = kwargs.setdefault
        kwset('cmap', CMAP)
        kwset('figsize', FIGSIZE)
        kwset('grid', True)
        kwset('title', None)

        self.default = kwargs
        self.legend = dict(LEGEND)

    def __call__(self, data, **kwargs):
        """ AxesSubplot: Fill default values and create figure. """
        default, legend = self.default, self.legend

        kwargs = {**default, **kwargs}
        kwargs.pop('cmap') if 'color' in kwargs else None
        facecolor = kwargs.pop('facecolor', None)
        legend = kwargs.pop('legend', legend)
        xlabel = kwargs.pop('xlabel', None)
        ylabel = kwargs.pop('ylabel', None)

        axes = DataFrame(data).plot(**kwargs)
        axes.figure.tight_layout()
        if facecolor:
            axes.set_facecolor(facecolor)
        if legend:
            axes.legend(**legend)
        if xlabel:
            axes.set_xlabel(xlabel)
        if ylabel:
            axes.set_ylabel(ylabel)

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
        kwset = kwargs.setdefault
        kwset('grid', False)
        kwset('kind', 'bar')
        kwset('stacked', True)
        kwset('width', 0.9)

        return self(data, **kwargs)

    def barh(self, data, **kwargs):
        """ AxesSubplot: Horizontal bar chart for each column. """
        kwset = kwargs.setdefault
        kwset('kind', 'barh')

        return self.bar(data.iloc[::-1, :], **kwargs)

    def heat(self, data, **kwargs):
        """ AxesSubplot: Heatmap with same rows and columns as input. """
        raise NotImplementedError

    def hist(self, data, **kwargs):
        """ AxesSubplot: Histogram for each column. """
        kwset = kwargs.setdefault
        kwset('kind', 'hist')
        kwset('stacked', True)
        kwset('bins', 33)

        return self(data, **kwargs)

    def line(self, data, **kwargs):
        """ AxesSubplot: Line plot for each column. """
        kwset = kwargs.setdefault
        kwset('kind', 'line')
        kwset('stacked', False)

        return self(data, **kwargs)

    def scatter(self, data, **kwargs):
        """
        AxesSubplot: Scatterplot with first 2 columns as (x,y) pairs.
        If 3rd column exists, then its values are colors for each point.
        If 4th column exists, then its values are sizes for each point.
        """
        cols = data.columns
        kwset = kwargs.setdefault
        kwset('alpha', .5)
        kwset('cmap', None)
        kwset('kind', 'scatter')
        kwset('legend', False)
        kwset('x', cols[0])
        kwset('y', cols[1])
        kwset('c', data[cols[2]] if len(cols) > 2 else 'black')
        kwset('s', data[cols[3]] if len(cols) > 3 else 64)

        return self(data, **kwargs)

    # Timeseries input

    def quant(self, ts, freq, q=(), **kwargs):
        """ AxesSubplot: Contour plot of quantiles per period. """
        kwset = kwargs.setdefault
        kwset('color', list('krygbck'))
        kwset('stacked', False)

        q = list(q) or [0, 0.05, 0.25, 0.50, 0.75, 0.95, 1]
        data = ts.resample(freq).quantile(q).unstack()
        data.columns = [ f"{int(100 * x)} percentile" for x in data.columns ]

        return self(data, **kwargs)




