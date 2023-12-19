# kingofsnake

Use your favorite data analysis packages without installing multiple Pythons.

<img
  alt="snakepit"
  src="https://raw.githubusercontent.com/samkennerly/posters/master/kingofsnake.jpeg"
  title="Asps. Very dangerous.">

This [template] is for research projects. For production Python projects, see [pydiner].

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[pydiner]: https://github.com/samkennerly/pydiner/


## abstract

`kingofsnake` is a template for a [reproducible] data analysis lab which:

- runs [Jupyter] notebooks in a [Docker container].
- never conflicts with existing Python(s), [Anaconda], or [virtualenvs].
- includes [pinned versions] of these [pip] packages and their dependencies:

```sh
networkx
notebook
pandas[all]
requests
scikit-learn
scipy
seaborn
```
[reproducible]: https://en.wikipedia.org/wiki/Replication_crisis
[Jupyter]: https://jupyter.org/
[Docker container]: https://docs.docker.com/develop/
[Anaconda]: https://www.anaconda.com/
[virtualenvs]: https://virtualenv.pypa.io/en/latest/
[pinned versions]: https://pip.pypa.io/en/stable/user_guide/#pinned-version-numbers
[pip]: https://pip.pypa.io/en/stable/

See the [books] folder for examples of [data cleaning], supervised [classification], unsupervised [clustering], force-directed [graph drawing], and [principal component analysis].

[books]: books
[data cleaning]: https://en.wikipedia.org/wiki/Data_cleansing
[classification]: https://en.wikipedia.org/wiki/Statistical_classification
[clustering]: https://en.wikipedia.org/wiki/Hierarchical_clustering
[graph drawing]: https://en.wikipedia.org/wiki/Force-directed_graph_drawing
[principal component analysis]: https://en.wikipedia.org/wiki/Principal_component_analysis


## basics

Generate a new repo [from this template].

[from this template]: https://help.github.com/en/articles/creating-a-repository-from-a-template

### bake a python environment

1. Open a [terminal] and `cd` to this folder.
1. Edit the [Dockerfile] to choose a Python version.
1. Edit [requirements.txt] to choose Python packages.
1. Run `./kitchen bake` to build a `kingofsnake:latest` [Docker image].
1. Run `./kitchen freeze` to update `requirements.txt` and rebuild.

[terminal]: https://en.wikipedia.org/wiki/Command-line_interface
[Dockerfile]: Dockerfile
[requirements.txt]: requirements.txt
[Docker image]: https://docs.docker.com/engine/reference/commandline/images/

### serve jupyter noteboks

1. Open a [terminal] and `cd` to this folder.
1. Run `./kitchen serve` to start a [Jupyter server].
1. Open a web browser and enter `localhost:8888` in the address bar.

[terminal]: https://en.wikipedia.org/wiki/Command-line_interface
[Jupyter server]: https://jupyter-server.readthedocs.io/en/latest/index.html

This runs Jupyter in a [container], [publishes] port 8888, and [mounts] some folders from this repo:

- `etc/ipython` is mounted as `/home/kos/.ipython`
- `etc/jupyter` is mounted as `/home/kos/.jupyter`
- `books` is mounted as `/home/kos/books`
- `code` is mounted as `/home/kos/code`
- `data` is mounted as `/home/kos/data`

[container]: https://docs.docker.com/engine/reference/run/
[publishes]: https://docs.docker.com/network/
[mounts]: https://docs.docker.com/storage/bind-mounts/

*Jupyter security:* On the first run, Jupyter might ask you to [copypaste a token] and create a password. It will save the hashed password and any custom settings to `etc/ipython` and `etc/jupyter` in this repo. If those folders do not exist, they will be created automatically. Git [ignores] the contents of both folders.

[copypaste a token]: https://jupyter-server.readthedocs.io/en/stable/operators/security.html
[ignores]: https://git-scm.com/docs/gitignore

### delete everything and start over

1. Open a [terminal] and `cd` to this folder.
1. `./kitchen clean` stops and deletes all `kingofsnake` containers.
1. `./kitchen eightysix` deletes the `kingofsnake:latest` image.

The `clean` command is rarely necessary because `kingofsnake` containers [self-destruct].

[terminal]: https://en.wikipedia.org/wiki/Command-line_interface
[from this template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[self-destruct]: https://docs.docker.com/engine/reference/run/#clean-up---rm


## contents

### books

The `books` folder contains example notebooks:

- [classify] uses [sklearn.linear_model] to train and test a classifier.
- [clean] uses [pandas] to standardize, sort, and filter a dataset.
- [cluster] uses [scipy.cluster.hierarchy] to find clusters in a dataset.
- [components] uses [sklearn.decomposition.PCA] to reduce the dimension of a dataset.
- [graph] uses a custom implementation of [ForceAtlas2] to draw graphs.
- [plot] uses [matplotlib] to visualize data.

[classify]: books/classify.ipynb
[sklearn.linear_model]: https://scikit-learn.org/stable/modules/linear_model.html
[clean]: books/clean.ipynb
[pandas]: https://pandas.pydata.org/
[cluster]: books/cluster.ipynb
[scipy.cluster.hierarchy]: https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html
[components]: books/components.ipynb
[sklearn.decomposition.PCA]: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
[graph]: books/graph.ipynb
[ForceAtlas2]: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0098679
[plot]: books/plot.ipynb
[matplotlib]: https://matplotlib.org/

### code

The `code` folder contains example Python [modules]:

- [classify] for classification
- [cluster] for clustering
- [graph] for graph drawing
- [plot] for data visualization
- [tools] for constants and convenience methods

[modules]: https://docs.python.org/3/tutorial/modules.html
[classify]: code/classify.py
[cluster]: code/cluster.py
[graph]: code/graph.py
[plot]: code/plot.py
[tools]: code/tools.py

### data

This folder is for storing data files. Git [ignores] everything in it except a few examples.

[ignores]: https://git-scm.com/docs/gitignore


## dependencies

`kingofsnake` has one dependency:

1. Docker for [Linux] or [Mac] or [Windows].

Windows users may need to edit the [kitchen] script for [path compatibility].

[Linux]: https://docs.docker.com/install/
[Mac]: https://docs.docker.com/docker-for-mac/install/
[Windows]: https://docs.docker.com/docker-for-windows/
[kitchen]: kitchen
[path compatibility]: https://en.wikipedia.org/wiki/Path_(computing)#MS-DOS/Microsoft_Windows_style


## examples

Show all available kitchen commands.
```sh
./kitchen help
```
Run a container as [root] without Jupyter, folder mounts, or published ports.
```sh
./kitchen runit latest
```
Bake another image called `kingofsnake:karl`, freeze it, and serve Jupyter.
```sh
./kitchen bake karl
./kitchen freeze karl
./kitchen serve karl
```
Delete the `kingofsnake:karl` image and its containers:
```sh
./kitchen eightysix karl
```

[root]: https://en.wikipedia.org/wiki/Superuser


## faq

### How do I install `kingofsnake`?

Don't install anything. Use this repo as a [template].

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template

### How do I make it stop?

Click on the terminal running Jupyter and press *CTRL-C*.

### Can I run Jupyter in the background?

Yes. See the [Docker run reference].

[Docker run reference]: https://docs.docker.com/engine/reference/run/

### Do I need all these notebooks and modules?

No. Delete them if you want to.
