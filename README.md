# kingofsnake

Analyze data without installing multiple Pythons.

<img
  alt="snakepit"
  src="https://raw.githubusercontent.com/samkennerly/posters/master/kingofsnake.jpeg"
  title="Asps. Very dangerous.">

Includes examples of [classification], [clustering], [graph layout], and [plotting].

[classification]: books/classify.ipynb
[clustering]: books/cluster.ipynb
[graph layout]: books/graph.ipynb
[plotting]: books/plot.ipynb

## abstract

`kingofsnake` is a [template] for a [reproducible] research project which:

- runs [Jupyter] in a [container].
- installs nothing outside of its [Docker images].
- never conflicts with system Python(s), [Anaconda], or [virtualenvs].
- updates `requirements.txt` with [pinned versions] of all [pip] installs.

This template is for [research]. For production code, see [pydiner].

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[reproducible]: https://en.wikipedia.org/wiki/Replication_crisis
[Jupyter]: https://jupyter.org/
[container]: https://docs.docker.com/develop/
[Docker images]: https://docs.docker.com/engine/docker-overview/
[Anaconda]: https://www.anaconda.com/
[virtualenvs]: https://virtualenv.pypa.io/en/latest/
[pinned versions]: https://pip.pypa.io/en/stable/user_guide/#pinned-version-numbers
[pip]: https://pip.pypa.io/en/stable/
[modules]: https://docs.python.org/3/tutorial/modules.html
[research]: https://knowyourmeme.com/photos/234739-i-have-no-idea-what-im-doing
[pydiner]: https://github.com/samkennerly/pydiner/

## basics

Generate a new repo [from this template].

### bake an image

1. Open a [terminal] and `cd` to this folder.
1. Edit the `Dockerfile` to choose a Python version.
1. Edit `requirements.txt` to choose Python packages.
1. Run `./kitchen bake` to build a `kingofsnake:latest` image.
1. Run `./kitchen freeze` to update `requirements.txt` and rebuild.

Baking a new image takes a few minutes. Rebuilding is much faster.

### serve jupyter

1. Open a [terminal] and `cd` to this folder.
1. Run `./kitchen serve` to start a [Jupyter server].
1. Open a web browser and enter `localhost:8888` in the address bar.

The `serve` command [mounts] some folders.
These folders will be created if they do not exist:

- `~/.ipython` as `/home/kos/.ipython`
- `~/.jupyter` as `/home/kos/.jupyter`
- current folder as `/context`

Jupyter might ask you to [copypaste a token] and/or [create a password].
It saves the password to:
```sh
~/.jupyter/jupyter_notebook_config.json
```

The `serve` command [publishes] port 8888. Other ports are restricted by a [firewall].

### delete everything

1. Open a [terminal] and `cd` to this folder.
1. `./kitchen clean` stops and deletes all `kingofsnake` containers.
1. `./kitchen eightysix` deletes the `kingofsnake:latest` image.

Cleaning is usually not necessary because `kingofsnake` containers [self-destruct].

[from this template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[terminal]: https://en.wikipedia.org/wiki/Command-line_interface
[Jupyter server]: https://jupyter-notebook.readthedocs.io/en/stable/public_server.html
[mounts]: https://docs.docker.com/storage/bind-mounts/
[copypaste a token]: https://jupyter-notebook.readthedocs.io/en/stable/security.html#
[create a password]: https://jupyter-notebook.readthedocs.io/en/stable/public_server.html
[publishes]: https://docs.docker.com/engine/reference/commandline/run/#publish-or-expose-port--p---expose
[firewall]: https://docs.docker.com/v17.12/config/containers/container-networking/
[self-destruct]: https://docs.docker.com/engine/reference/run/#clean-up---rm

## contents

### books

- [classify.ipynb](books/classify.ipynb) supervised classification
- [cluster.ipynb](books/cluster.ipynb) unsupervised clustering
- [graph.ipynb](books/graph.ipynb) graph data and layout
- [iris.ipynb](books/iris.ipynb) data normalization
- [plot.ipynb](books/plot.ipynb) data visualization

### code

- [graph.py](code/graph.py) graph data and layout
- [learn.py](code/learn.py) machine learning
- [plot.py](code/plot.py) data visualization
- [tools.py](code/tools.py) constants and functions

### data

This folder is [gitignored] except for an example dataset from [data.ny.gov].

[gitignored]: https://git-scm.com/docs/gitignore
[data.ny.gov]: https://data.ny.gov/Energy-Environment/Electric-Generation-By-Fuel-Type-GWh-Beginning-196/h4gs-8qnu

## dependencies

1. Docker for [Linux] or [Mac] or [Windows].

Python is not required. Windows users may need to edit `kitchen` for [path compatibility].

[Linux]: https://docs.docker.com/install/
[Mac]: https://docs.docker.com/docker-for-mac/install/
[Windows]: https://docs.docker.com/docker-for-windows/
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

Delete all traces of `kingofsnake:karl`.
```sh
./kitchen eightysix karl
```

Load `kitchen` into the shell to avoid typing `./kitchen` repeatedly.
```sh
source kitchen
```

[root]: https://en.wikipedia.org/wiki/Superuser

## faq

### How do I make it stop?

Click on the terminal running Jupyter and press *CTRL-C*.

### How do I install `kingofsnake`?

Don't. Use it as a [template] for a new repository.

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template

### Can I run Jupyter in the background?

Yes, but not with the `kitchen` script. See the [Docker run reference].

[Docker run reference]: https://docs.docker.com/engine/reference/run/

### Do I need all these notebooks and modules?

No. Delete them if you want to. The `kitchen` script does not require them.
