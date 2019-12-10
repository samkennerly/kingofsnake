# kingofsnake (UNDER CONSTRUCTION)

Keep your Pythons separated so they don't get entangled.

![poster](kingofsnake.jpeg)

## abstract

`kingofsnake` is a [template] for a [reproducible] research project which:

- runs [Jupyter] in [Docker containers] which [self-destruct].
- never installs software outside of its own [Docker images].
- never uses or modifies other Pythons, [Anaconda], or [virtualenvs].
- updates `requirements.txt` with [pinned versions] of all [pip] installs.

For developing [production] code, see the [pydiner] template.

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[reproducible]: https://en.wikipedia.org/wiki/Replication_crisis
[Jupyter]: https://jupyter.org/
[Docker containers]: https://docs.docker.com/develop/
[self-destruct]: https://docs.docker.com/engine/reference/run/#clean-up---rm
[Docker images]: https://docs.docker.com/engine/docker-overview/
[Anaconda]: https://www.anaconda.com/
[virtualenvs]: https://virtualenv.pypa.io/en/latest/
[pinned versions]: https://pip.pypa.io/en/stable/user_guide/#pinned-version-numbers
[pip]: https://pip.pypa.io/en/stable/
[production]: https://en.wikipedia.org/wiki/Deployment_environment
[pydiner]: https://github.com/samkennerly/pydiner/

## basics

1. Generate a new repo [from this template].
1. Open a [terminal] and `cd` to this folder.
1. Run `./kitchen` to see available commands.

The `kitchen` script defines [shell functions] for Docker commands.

[from this template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[terminal]: https://en.wikipedia.org/wiki/Command-line_interface
[shell functions]: https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html

### bake a Python

1. Edit the `Dockerfile` to choose a Python version.
1. Edit `requirements.txt` to choose Python packages.
1. Run `./kitchen bake` to build the `kingofsnake:latest` image.
1. Run `./kitchen freeze` to update `requirements.txt` with [pinned versions].

The first bake usually takes a few minutes. Subsequent bakes are much faster.

[pinned versions]: https://pip.pypa.io/en/stable/user_guide/#pinned-version-numbers

### serve Jupyter

1. Run `./kitchen serve` to start a [Jupyter server].
1. Open a browser and enter `localhost:8888` in the address bar.

[Jupyter server]: https://jupyter-notebook.readthedocs.io/en/stable/public_server.html
[mount]: https://docs.docker.com/storage/bind-mounts/

## contents

## dependencies

`kingofsnake` does not require Python. It has one dependency:

- Docker for [Linux] or [Mac] or [Windows]

Windows users may need to edit the `kitchen` script for [path compatibility].

[Linux]: https://docs.docker.com/install/
[Mac]: https://docs.docker.com/docker-for-mac/install/
[Windows]: https://docs.docker.com/docker-for-windows/
[path compatibility]: https://en.wikipedia.org/wiki/Path_(computing)#MS-DOS/Microsoft_Windows_style

## examples

## faq

### Make it stop!!!1!

Click on the terminal running Jupyter and press *CTRL-C* twice.

### How do I install `kingofsnake`?

Don't. Use it as a [template] for a new repository.

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template

### Can I run Jupyter in the background?

Yes, but not with the `kitchen` script. See the [Docker run reference].

[Docker run reference]: https://docs.docker.com/engine/reference/run/


