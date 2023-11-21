"""
Data visualization toolbox.
"""
from matplotlib import style as mpstyle
from matplotlib.pyplot import figure
from pandas import DataFrame
from scipy.cluster.hierarchy import dendrogram

AXES = (("frame_on", False),)
FIGURE = (
    ("clear", True),
    ("dpi", 100),
    ("edgecolor", None),
    ("facecolor", None),
    ("figsize", (10, 5)),
    ("frameon", False),
    ("tight_layout", True),
)
LEGEND = (
    ("bbox_to_anchor", (1.05, 1)),
    ("borderaxespad", 0.0),
    ("loc", "upper left"),
)
STYLE = "bmh"


class Plot:
    """
    Visualize pandas.DataFrame or .Series inputs.

    Each Plot() object remembers its own default parameters.
    Most methods are thin wrappers around DataFrame plot methods.
    Call a Plot() to call to DataFrame.plot() with custom arguments.

    Caution: Modifies matplotlib.style when an object is created.
    """

    styles = mpstyle.available

    def __init__(self, style=STYLE, **kwargs):
        mpstyle.use(style)

        params = dict()
        params["axes"] = {k: kwargs.pop(k, v) for k, v in AXES}
        params["figure"] = {k: kwargs.pop(k, v) for k, v in FIGURE}
        params["legend"] = {k: kwargs.pop(k, v) for k, v in LEGEND}
        if kwargs:
            raise KeyError(f"unknown keyword arguments {sorted(kwargs)}")

        self.params = params

    def __call__(self, data, **kwargs):
        axes = self.axes
        params = self.params

        kwargs = {
            "grid": False,
            "legend": False,
        } | kwargs

        data = DataFrame(data)
        axes = kwargs.pop("ax", None) or axes()
        axes = data.plot(ax=axes, **kwargs)
        axes.set_xlabel(kwargs.pop("xlabel", None))
        axes.set_ylabel(kwargs.pop("ylabel", None))
        if kwargs.get("legend"):
            axes.legend(**params["legend"])

        return axes

    def __repr__(self):
        return f"{type(self).__name__}({self.params})"

    def axes(self, **kwargs):
        """AxesSubplot: Create blank axes."""
        return self.figure().add_subplot(**(self.params["axes"] | kwargs))

    def figure(self, **kwargs):
        """Figure: Create a new figure."""
        return figure(**(self.params["figure"] | kwargs))

    # DataFrame input

    def area(self, data, **kwargs):
        """AxesSubplot: Area plot for each column."""
        kwargs = {
            "legend": True,
        } | kwargs

        return self(data, kind="area", **kwargs)

    def bar(self, data, **kwargs):
        """AxesSubplot: Bar plot for each column."""
        kwargs = {
            "legend": True,
            "rot": 90,
            "stacked": True,
            "width": 0.9,
        } | kwargs

        return self(data, kind="bar", **kwargs)

    def barh(self, data, **kwargs):
        """AxesSubplot: Horizontal bar plot for each column."""
        kwargs = {
            "legend": True,
            "stacked": True,
            "width": 0.8,
        } | kwargs

        return self(data.iloc[::-1, :], kind="barh", **kwargs)

    def box(self, data, **kwargs):
        """AxesSubplot: Box plot for each column."""
        kwargs = {
            "grid": True,
            "rot": 90,
        } | kwargs

        return self(data, kind="box", **kwargs)

    def boxh(self, data, **kwargs):
        """AxesSubplot: Horizontal box plot for each column."""
        kwargs = {
            "grid": True,
        } | kwargs

        return self(data.iloc[:, ::-1], kind="box", vert=False, **kwargs)

    def density(self, data, **kwargs):
        """AxesSubplot: Probability density estimate for each column."""
        kwargs = {
            "grid": True,
            "legend": True,
        } | kwargs

        return self(data, kind="density", **kwargs)

    def heat(self, data, **kwargs):
        """AxesSubplot: Heatmap with same rows and columns as input."""
        axes = self.axes

        kwargs = {
            "alpha": 0.707,
            "cmap": "inferno",
            "edgecolor": None,
            "shading": "flat",
        } | kwargs

        kpop = kwargs.pop
        axes = kpop("ax", None) or axes()
        title = kpop("title", None)
        xlabel = kpop("xlabel", None)
        ylabel = kpop("ylabel", None)
        colorbar = kpop("colorbar", False)
        rotation = kpop("rot", 45)

        data = DataFrame(data).iloc[::-1, :]
        cols = data.columns
        rows = data.index
        axes.set_title(title)
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        axes.set_xticks(range(len(cols)))
        axes.set_yticks(range(len(rows)))
        axes.set_xticklabels(cols, ha="left", rotation=rotation)
        axes.set_yticklabels(rows, verticalalignment="bottom")
        axes.tick_params(labeltop=True, labelbottom=False, length=0)
        plot = axes.pcolormesh(data, **kwargs)
        if colorbar:
            axes.figure.colorbar(plot)

        return axes

    def hexbin(self, data, **kwargs):
        """AxesSubplot: Scatterplot with hexagonal bins."""
        kwargs = {
            "cmap": "cubehelix",
            "colorbar": False,
        } | kwargs

        raise NotImplementedError

    def hist(self, data, **kwargs):
        """AxesSubplot: Histogram for each column."""
        kwargs = {
            "bins": 33,
            "grid": True,
            "legend": True,
            "stacked": True,
        } | kwargs

        return self(data, kind="hist", **kwargs)

    def line(self, data, **kwargs):
        """AxesSubplot: Line plot for each column."""
        kwargs = {
            "grid": True,
            "legend": True,
        } | kwargs

        return self(data, kind="line", **kwargs)

    def scatter(self, data, **kwargs):
        """
        AxesSubplot: Scatterplot with first 2 columns as (x,y) pairs.
        If 3rd column exists, then its values are point colors.
        If 4th column exists, then its values are point sizes.
        """
        cols = data.columns
        kwargs = {
            "alpha": 0.707,
            "cmap": "nipy_spectral_r",
            "colorbar": False,
            "grid": True,
            "legend": False,
            "x": cols[0],
            "y": cols[1],
        } | kwargs
        if len(cols) > 2:
            kwargs = {"c": data[cols[2]]} | kwargs
        if len(cols) > 3:
            kwargs = {"s": data[cols[3]]} | kwargs

        return self(data, kind="scatter", **kwargs)

    # Timeseries input

    def quant(self, ts, freq, q=(), **kwargs):
        """
        AxesSubplot: Contour plot of quantiles per period.
        Input must be a Series with a datetime-like index.
        """
        kwargs = {
            "color": list("krygbck"),
            "grid": True,
            "legend": True,
            "stacked": False,
        } | kwargs

        q = list(q) or [0, 0.05, 0.25, 0.50, 0.75, 0.95, 1]
        data = ts.resample(freq).quantile(q).unstack()
        data.columns = [f"{int(100 * x)} percentile" for x in data.columns]

        return self(data, kind="line", **kwargs)
