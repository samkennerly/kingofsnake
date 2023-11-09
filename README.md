# kingofsnake

Analyze data without installing multiple Pythons.

<img
  alt="snakepit"
  src="https://raw.githubusercontent.com/samkennerly/posters/master/kingofsnake.jpeg"
  title="Asps. Very dangerous.">

This template is for research. For production Python projects, see [pydiner].

[pydiner]: https://github.com/samkennerly/pydiner/

## abstract

`kingofsnake` is a [template] for a [reproducible] Python project which:

- runs [Jupyter] notebooks in a [Docker container].
- installs no Python versions or packages on your computer.
- never conflicts with system Python(s), [Anaconda], or [virtualenvs].
- updates `requirements.txt` with [pinned versions] of all [pip] installs.

By default, it includes these packages (and their dependencies):
```sh
networkx
notebook
pandas[all]
requests
scikit-learn
scipy
seaborn
```
and some example notebooks for [classification], [clustering], [graph layout], and [plotting].

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[reproducible]: https://en.wikipedia.org/wiki/Replication_crisis
[Jupyter]: https://jupyter.org/
[Docker container]: https://docs.docker.com/develop/
[Anaconda]: https://www.anaconda.com/
[virtualenvs]: https://virtualenv.pypa.io/en/latest/
[pinned versions]: https://pip.pypa.io/en/stable/user_guide/#pinned-version-numbers
[pip]: https://pip.pypa.io/en/stable/
[classification]: books/classify.ipynb
[clustering]: books/cluster.ipynb
[graph layout]: books/graph.ipynb
[plotting]: books/plot.ipynb

## basics

Generate a new repo [from this template].

### bake a python environment

1. Open a [terminal] and `cd` to this folder.
1. Edit the `Dockerfile` to choose a Python version.
1. Edit `requirements.txt` to choose Python packages.
1. Run `./kitchen bake` to build a `kingofsnake:latest` [image].
1. Run `./kitchen freeze` to update `requirements.txt` and rebuild.

### serve jupyter noteboks

1. Open a [terminal] and `cd` to this folder.
1. Run `./kitchen serve` to start a [Jupyter server].
1. Open a web browser and enter `localhost:8888` in the address bar.

This runs Jupyter in a [container], [publishes] port 8888, and [mounts] some folders from this repo:

- `etc/ipython` is mounted as `/home/kos/.ipython`
- `etc/jupyter` is mounted as `/home/kos/.jupyter`
- [books](books) is mounted as `/home/kos/books`
- [code](code) is mounted as `/home/kos/code`
- [data](data) is mounted as `/home/kos/data`

On the first run, Jupyter might ask you to [copypaste a token] and create a password. It will save the hashed password and any custom settings to `etc/ipython` and `etc/jupyter` in this repo. If those folders do not exist, they will be created automatically. Git [ignores] the contents of both folders.

### delete everything and start over

1. Open a [terminal] and `cd` to this folder.
1. `./kitchen clean` stops and deletes all `kingofsnake` containers.
1. `./kitchen eightysix` deletes the `kingofsnake:latest` image.

The `clean` is usually unnecessary because `kingofsnake` containers [self-destruct].

[from this template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[image]: https://docs.docker.com/engine/reference/commandline/images/
[terminal]: https://en.wikipedia.org/wiki/Command-line_interface
[Jupyter server]: https://jupyter-server.readthedocs.io/en/latest/index.html
[container]: https://docs.docker.com/engine/reference/run/
[publishes]: https://docs.docker.com/network/
[mounts]: https://docs.docker.com/storage/bind-mounts/
[copypaste a token]: https://jupyter-server.readthedocs.io/en/stable/operators/security.html
[ignores]: https://git-scm.com/docs/gitignore
[from this template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[self-destruct]: https://docs.docker.com/engine/reference/run/#clean-up---rm

## contents

### books

The [books] folder contains example notebooks:

- [classify.ipynb] supervised classification
- [cluster.ipynb] unsupervised clustering
- [graph.ipynb] graph data and layout
- [iris.ipynb] data normalization
- [plot.ipynb] data visualization

### code

The [code] folder contains importable Python [modules]:

- [graph.py] graph data and layout
- [learn.py] machine learning
- [plot.py] data visualization
- [tools.py] constants and functions

### data

This folder is for storing data files. Git [ignores] it except for one example dataset from [data.ny.gov].

[books]: books
[classify.ipynb]: books/classify.ipynb
[cluster.ipynb]: books/cluster.ipynb
[graph.ipynb]: books/graph.ipynb
[iris.ipynb]: books/iris.ipynb
[plot.ipynb]: books/plot.ipynb
[code]: code
[graph.py]: code/graph.py
[learn.py]: code/learn.py
[plot.py]: code/plot.py
[tools.py]: code/tools.py
[ignores]: https://git-scm.com/docs/gitignore
[data.ny.gov]: https://data.ny.gov/Energy-Environment/Electric-Generation-By-Fuel-Type-GWh-Beginning-196/h4gs-8qnu

## dependencies

`kingofsnake` has exactly one dependency:

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

Don't. Use it as a [template] for a new repository.

### How do I make it stop?

Click on the terminal running Jupyter and press *CTRL-C*.

### Can I run Jupyter in the background?

Yes, but not with the [kitchen] script. See the [Docker run reference].

### Do I need all these notebooks and modules?

No. Delete them if you want to. Jupyter does not need them.

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[kitchen]: kitchen
[Docker run reference]: https://docs.docker.com/engine/reference/run/
