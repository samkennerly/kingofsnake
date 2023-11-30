import matplotlib.pyplot
import matplotlib.style

class Plotter:
    """
    Convenience class for plotting pandas DataFrame and Series data.
    Each Plotter object stores parameters for matplotlib plots.

    Call to call DataFrame.plot() with custom arguments.
    This (and most other methods) returns an AxesSubplot.

    Modify .style to change the global matplotlib style setting.
    """

    styles = matplotlib.style.available

    def __init__(self, style="bmh"):
        params = {
            "axes": {
                "frame_on": False,
            },
            "figure": {
                "clear": True,
                "dpi": 100,
                "edgecolor": None,
                "facecolor": None,
                "figsize": (10,5),
                "frameon": False,
                "tight_layout": True,
            },
            "legend": {
                "bbox_to_anchor": (1.05, 1),
                "borderaxespad": 0.0,
                "loc": "upper left",
            },
            "plot": {
                "grid": False,
                "legend": False,
                "xlabel": None,
                "ylabel": None,
            }
        }

        self.params = params
        self.style = style

    def __call__(self, data, **kwargs):
        axes = self.axes
        params = self.params

        kwargs = params["plot"] | kwargs

        ax = data.plot(ax=axes(), **kwargs)
        ax.set_xlabel(kwargs["xlabel"])
        ax.set_ylabel(kwargs["ylabel"])
        if kwargs.get("legend"):
            ax.legend(**params["legend"])

        return ax

    def __repr__(self):
        return f"{type(self).__name__}(style='{self.style}')"

    # Properties

    @property
    def style(self):
        """str: Name of selected matplotlib style."""
        return self._style

    @style.setter
    def style(self, name):
        """None: Modify matplotlib.style."""
        matplotlib.style.use(name)

        self._style = name

    # Blank matplotlib objects

    def axes(self, **kwargs):
        """AxesSubplot: Create blank axes."""
        return self.figure().add_subplot(**(self.params["axes"] | kwargs))

    def figure(self, **kwargs):
        """Figure: Create a new figure."""
        return matplotlib.pyplot.figure(**(self.params["figure"] | kwargs))

    # Plot methods with DataFrame input

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
            "rot": 45,
            "shading": "flat",
            "title": None,
            "xlabel": None,
            "ylabel": None,
        } | kwargs

        data = data.iloc[::-1, :]
        cols = data.columns
        rows = data.index

        ax = axes()
        ax.set_title(kwargs.pop("title"))
        ax.set_xlabel(kwargs.pop("xlabel"))
        ax.set_ylabel(kwargs.pop("ylabel"))
        ax.set_xticks(range(len(cols)))
        ax.set_yticks(range(len(rows)))
        ax.set_xticklabels(cols, ha="left", rotation=kwargs.pop("rot"))
        ax.set_yticklabels(rows, verticalalignment="bottom")
        ax.tick_params(labeltop=True, labelbottom=False, length=0)
        subplot = ax.pcolormesh(data, **kwargs)
        if kwargs.pop("colorbar", False):
            ax.figure.colorbar(subplot)

        return ax

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
            "colorbar": False,
            "grid": True,
            "legend": False,
            "x": cols[0],
            "y": cols[1],
        } | kwargs


        ncols = len(cols)
        if ncols > 2:
            kwargs = {"c": data[cols[2]]} | kwargs
        if ncols > 3:
            kwargs = {"s": data[cols[3]]} | kwargs

        return self(data, kind="scatter", **kwargs)

    # Plot methods with Series input

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
