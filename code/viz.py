"""
Data visualization toolbox.
"""
from matplotlib import style as mpstyle
from matplotlib.pyplot import figure
from pandas import DataFrame

AXES = (
    ('frame_on', False),
    ('xlabel', None),
    ('ylabel', None),
)
COLORMAP = 'nipy_spectral_r'
FIGURE = (
    ('clear', True),
    ('dpi', 100),
    ('figsize', (9, 5)),
)
LEGEND = (
    ('bbox_to_anchor', (1.05, 1)),
    ('borderaxespad', 0.0),
    ('loc', 'upper left'),
)
DEFAULT = (
    ('figsize', (10, 5)),
    ('fontsize', None),
    ('grid', True),
    ('legend', True),
    ('logx', False),
    ('logy', False),
    ('rot', 0),
    ('style', None),
    ('title', None),
    ('use_index', True),
    ('xlim', None),
    ('xticks', None),
    ('ylim', None),
    ('yticks', None),
)

class Plot:
    """
    Plotting methods for pandas.DataFrame or .Series inputs.
    Initialize with defaults. Call with keyword arguments to override defaults.
    """
    styles = mpstyle.available

    def __init__(self, style='bmh', **kwargs):
        self.default = {**dict(DEFAULT), **kwargs}
        mpstyle.use(style)

    def __call__(self, data, **kwargs):
        """ AxesSubplot: Fill default values and create figure. """
        kwargs = {**self.default, **kwargs}

        if 'color' in kwargs:
            kwargs.pop('colormap', None)

        data = DataFrame(data)
        fig = figure(**{ k:kwargs.pop(k, v) for k, v in FIGURE })
        ax = fig.add_subplot(**{ k:kwargs.pop(k, v) for k, v in AXES })
        ax = data.plot(ax=ax, **kwargs)
        if kwargs.get('legend'):
            ax.legend(**dict(LEGEND))

        return ax

    def __repr__(self):
        name = type(self).__name__
        params = ", ".join( f"{k}={v}" for k,v in vars(self).items() )

        return f"{name}({params})"

    # DataFrame input

    def area(self, data, **kwargs):
        """ AxesSubplot: Area plot for each column. """
        raise NotImplementedError

    def bar(self, data, **kwargs):
        """ AxesSubplot: Bar plot for each column. """
        kwargs.setdefault('grid', False)
        kwargs.setdefault('rot', 90)
        kwargs.setdefault('stacked', True)
        kwargs.setdefault('width', 0.9)

        return self(data, kind='bar', **kwargs)

    def barh(self, data, **kwargs):
        """ AxesSubplot: Horizontal bar plot for each column. """
        kwargs.setdefault('grid', False)
        kwargs.setdefault('stacked', True)
        kwargs.setdefault('width', 0.8)

        return self(data.iloc[::-1, :], kind='barh', **kwargs)

    def box(self, data, **kwargs):
        """ AxesSubplot: Box plot for each column. """
        kwargs.setdefault('color', None)
        kwargs.setdefault('legend', False)
        kwargs.setdefault('grid', True)
        kwargs.setdefault('rot', 90)

        return self(data, kind='box', **kwargs)

    def boxh(self, data, **kwargs):
        """ AxesSubplot: Horizontal box plot for each column. """
        kwargs.setdefault('vert', False)
        kwargs.setdefault('rot', 0)

        return self.box(data[reversed(data.columns)], **kwargs)

    def density(self, data, **kwargs):
        """ AxesSubplot: Probability density estimate for each column. """
        return self(data, kind='density', **kwargs)

    def heat(self, data, **kwargs):
        """ AxesSubplot: Heatmap with same rows and columns as input. """
        raise NotImplementedError

    def hexbin(self, data, **kwargs):
        """ AxesSubplot: Scatterplot with hexagonal bins. """
        raise NotImplementedError

    def hist(self, data, **kwargs):
        """ AxesSubplot: Histogram for each column. """
        kwargs.setdefault('bins', 33)
        kwargs.setdefault('stacked', True)

        return self(data, kind='hist', **kwargs)

    def line(self, data, **kwargs):
        """ AxesSubplot: Line plot for each column. """
        return self(data, kind='line', **kwargs)

    def scatter(self, data, **kwargs):
        """
        AxesSubplot: Scatterplot with first 2 columns as (x,y) pairs.
        If 3rd column exists, then its values are colors for each point.
        If 4th column exists, then its values are sizes for each point.
        """
        cols = data.columns
        kwargs.setdefault('alpha', .707)
        kwargs.setdefault('colormap', COLORMAP)
        kwargs.setdefault('legend', False)
        kwargs.setdefault('x', cols[0])
        kwargs.setdefault('y', cols[1])
        kwargs.setdefault('c', data[cols[2]] if len(cols) > 2 else 'black')
        kwargs.setdefault('s', data[cols[3]] if len(cols) > 3 else 64)

        return self(data, kind='scatter', **kwargs)

    # Timeseries input

    def quant(self, ts, freq, q=(), **kwargs):
        """ AxesSubplot: Contour plot of quantiles per period. """
        kwargs.setdefault('color', list('krygbck'))
        kwargs.setdefault('stacked', False)

        q = list(q) or [0, 0.05, 0.25, 0.50, 0.75, 0.95, 1]
        data = ts.resample(freq).quantile(q).unstack()
        data.columns = [ f"{int(100 * x)} percentile" for x in data.columns ]

        return self(data, kind='line', **kwargs)
