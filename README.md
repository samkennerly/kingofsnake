# kingofsnake

Did you install too many Pythons?

![poster](kingofsnake.jpeg)

## abstract

`kingofsnake` is a [template] for a [reproducible] research project which:

- runs [Jupyter] in [Docker containers].
- installs nothing outside of its [Docker images].
- never conflicts with system Python(s), [Anaconda], or [virtualenvs].
- updates `requirements.txt` with [pinned versions] of all [pip] installs.

This template is intended for [exploratory] data analysis.
For [production] code, see the [pydiner] template.

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[reproducible]: https://en.wikipedia.org/wiki/Replication_crisis
[exploratory]: https://knowyourmeme.com/photos/234739-i-have-no-idea-what-im-doing
[Jupyter]: https://jupyter.org/
[Docker containers]: https://docs.docker.com/develop/
[Docker images]: https://docs.docker.com/engine/docker-overview/
[Anaconda]: https://www.anaconda.com/
[virtualenvs]: https://virtualenv.pypa.io/en/latest/
[pinned versions]: https://pip.pypa.io/en/stable/user_guide/#pinned-version-numbers
[pip]: https://pip.pypa.io/en/stable/
[production]: https://en.wikipedia.org/wiki/Deployment_environment
[pydiner]: https://github.com/samkennerly/pydiner/

## basics

Do not install `kingofsnake`. Instead:

1. Generate a repo [from this template].
1. Open a [terminal] and `cd` to this folder.
1. Run `./kitchen` to see available commands.

The `kitchen` script defines [shell functions] for common Docker commands.

[from this template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[terminal]: https://en.wikipedia.org/wiki/Command-line_interface
[shell functions]: https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html

### bake an image

1. Edit the `Dockerfile` to choose a Python version.
1. Replace `requirements.txt` with your project's requirements.
1. Run `./kitchen bake` to build a `kingofsnake:latest` image.
1. Run `./kitchen freeze` to update `requirements.txt` and rebuild.

Building a new image takes a few minutes.
Rebuilding is much faster unless requirements have changed.

### serve Jupyter

1. Run `./kitchen serve` to start a [Jupyter server].
1. Open a browser and enter `localhost:8888` in the address bar.
1. To stop Jupyter, click on the terminal running it and press *CTRL-C*.

The `serve` command [mounts] some folders so Jupyter can access them:

- `~/.ipython` as `/home/kos/.ipython`
- `~/.jupyter` as `/home/kos/.jupyter`
- current folder as `/context`

The `~/.ipython` and `~/.jupyter` folders will be created if they do not exist.

[Jupyter server]: https://jupyter-notebook.readthedocs.io/en/stable/public_server.html
[mounts]: https://docs.docker.com/storage/bind-mounts/

### secure Jupyter

Jupyter may ask you to [copypaste a token] and [create a password].
It saves the password to:
```sh
~/.jupyter/jupyter_notebook_config.json
```
If this file contains a password, then Jupyter will ask for it when you run `serve`.

The `serve` command [publishes] port 8888.
Jupyter and anything else inside the container can access this port.
Inside containers, other ports are protected by a [firewall].

[copypaste a token]: https://jupyter-notebook.readthedocs.io/en/stable/security.html#
[create a password]: https://jupyter-notebook.readthedocs.io/en/stable/public_server.html
[publishes]: https://docs.docker.com/engine/reference/commandline/run/#publish-or-expose-port--p---expose
[firewall]: https://docs.docker.com/v17.12/config/containers/container-networking/

### run as root

The `serve` command runs as user `kos`. To run commands as [root]:

1. Run `./kitchen runit` to enter an interactive container.
1. Press *CTRL-D* to exit the container.

The `runit` command does not mount folders, publish ports, or start Jupyter.

[root]: https://en.wikipedia.org/wiki/Superuser

### delete everything

When in doubt, [nuke it from orbit] and start over.

1. Run `./kitchen clean` to stop and delete all `kingofsnake` containers.
1. Run `./kitchen eightysix` to delete the `kingofsnake` image.

Cleaning is often unnecessary because `kingofsnake` containers [self-destruct].

[nuke it from orbit]: https://www.imdb.com/title/tt0090605/characters/nm0000244
[self-destruct]: https://docs.docker.com/engine/reference/run/#clean-up---rm

## contents

### books

Example Jupyter notebooks.

### code

Example [packages] for [APIs], [ETL], and visualization.

### data

This folder is [gitignored] except for an example dataset from [Ergast].

[packages]: https://docs.python.org/3/tutorial/modules.html#packages
[APIs]: https://en.wikipedia.org/wiki/Application_programming_interface
[ETL]: https://en.wikipedia.org/wiki/Extract,_transform,_load
[gitignored]: https://git-scm.com/docs/gitignore
[Ergast]: http://ergast.com/mrd/db/

## dependencies

1. Docker for [Linux] or [Mac] or [Windows].

Python is not required.
Windows users may need to edit the `kitchen` for [path compatibility].

[Linux]: https://docs.docker.com/install/
[Mac]: https://docs.docker.com/docker-for-mac/install/
[Windows]: https://docs.docker.com/docker-for-windows/
[path compatibility]: https://en.wikipedia.org/wiki/Path_(computing)#MS-DOS/Microsoft_Windows_style


## examples

Run Python as root inside a container.
```sh
./kitchen runit latest python
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

## faq

### I'm stuck in a container!

Click on the terminal running Jupyter and press *CTRL-C*.

### How do I install `kingofsnake`?

Don't. Use it as a [template] for a new repository.

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template

### Can I run Jupyter in the background?

Yes, but not with the `kitchen` script. See the [Docker run reference].

[Docker run reference]: https://docs.docker.com/engine/reference/run/
