# pydiner

Keep your [development environments] clean.

![The Dirty Fork](pydiner.jpeg)

[development environments]: https://en.wikipedia.org/wiki/Sandbox_(software_development)

## abstract

`pydiner` is a [template] for a generic Python project which:

- runs code in [Docker containers] which [self-destruct].
- never reads or modifies files outside of its repository.
- never installs software outside of its own [Docker images].
- never uses or modifies other Pythons, [Anaconda], or [virtualenvs].
- updates `requirements.txt` with [pinned versions] of all [pip] installs.

These rules are intended to avoid [dependency hell].

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[Docker containers]: https://docs.docker.com/develop/
[self-destruct]: https://docs.docker.com/engine/reference/run/#clean-up---rm
[Docker images]: https://docs.docker.com/engine/docker-overview/
[Anaconda]: https://www.anaconda.com/
[virtualenvs]: https://virtualenv.pypa.io/en/latest/
[pinned versions]: https://pip.pypa.io/en/stable/user_guide/#pinned-version-numbers
[pip]: https://pip.pypa.io/en/stable/
[dependency hell]: https://en.wikipedia.org/wiki/Dependency_hell

## basics

To start a new project:

1. Generate a new repo [from this template].
1. Delete any files and folders you don't want.
1. Edit the `Dockerfile` to choose a Python version.
1. Edit `requirements.txt` to choose Python packages.
1. Open a [terminal], `cd` to this folder, and run this command:
```sh
./kitchen
```
This will show the `kitchen` help message.

[from this template]: https://help.github.com/en/articles/creating-a-repository-from-a-template
[terminal]: https://en.wikipedia.org/wiki/Command-line_interface

### mise en python

The `kitchen` script defines [shell functions] for Docker commands.
```sh
# Bake a Docker image named pydiner:monty
./kitchen bake monty

# Freeze requirements.txt and rebuild pydiner:monty
./kitchen freeze monty

# Serve Python in a pydiner:monty container with $PWD mounted as /context
./kitchen serve monty python

# Run tests in a pydiner:monty container without mounting any folders
./kitchen runit monty python -m test

# Show which files were baked into the image
./kitchen runit monty tree

# Delete the image, its containers, and any leftovers
./kitchen eightysix monty
```
Typing `./kitchen` before each command is optional if the `kitchen` is [sourced].

[shell functions]: https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html
[sourced]: https://en.wikipedia.org/wiki/Source_(command)

### baking images

Baking creates or updates an image with copies of files from the [build context].

- Inside a container, the <q>baked-in</q> copies will appear in the `/context` folder.
- Every new `pydiner` container gets its own independent `/context` folder.
- Edit `.dockerignore` to declare file patterns which should never be copied.
- Edit `Dockerfile` to choose which non-ignored files are copied into images.

Modifying baked-in files does **not** affect the original files.

[build context]: https://docs.docker.com/engine/reference/commandline/build/

### freezing packages

Freezing an image runs `pip freeze` and saves the output to `requirements.txt`.

- [Pinned] versions are necessary to produce [reproducible builds].
- When an image is baked for the first time, `pip` installs packages.
- Baking an image again might not install exactly the same package versions.
- Running `freeze` enables `pip` to install the same package versions every time.

Freezing **overwrites** anything that was in `requirements.txt`.

[Pinned]: https://pip.pypa.io/en/stable/user_guide/#pinned-version-numbers
[reproducible builds]: https://en.wikipedia.org/wiki/Reproducible_builds

### serving with fresh files

Serving an image runs a new container with the current folder [mounted] as `/context`.

- Images are immutable. Rebuilding is the only way to update baked-in files.
- For development work, rebuilding after every code edit can be impractical.
- Mounting a folder gives a container read and write access to the files inside.
- Any files baked into `/context` will be obscured by the <q>fresh</q> mounted files.

Mounts are **not** copies. If a mounted file dies in a container, it dies in the real world.

[mounted]: https://docs.docker.com/storage/bind-mounts/

## contents

`pydiner` includes short examples of common project ingredients:

- [bin/](bin) contains executable scripts.
- [etc/](etc) contains configuration files.
- [src/](src) contains an importable [package].
- [test/](test) is an [executable package] which runs tests.
- [var/](var) contains files output by the script(s).

The [folder structure] is loosely based on a C++ template from [hiltmon.com].

[package]: https://docs.python.org/3/tutorial/modules.html#packages
[executable package]: https://docs.python.org/3/library/__main__.html
[folder structure]: https://en.wikipedia.org/wiki/Directory_structure
[hiltmon.com]: https://hiltmon.com/blog/2013/07/03/a-simple-c-plus-plus-project-structure/

## dependencies

`pydiner` does not require Python. It has one dependency:

- Docker for [Linux] or [Mac] or [Windows]

Windows users may need to edit the `kitchen` script for [path compatibility].

[Linux]: https://docs.docker.com/install/
[Mac]: https://docs.docker.com/docker-for-mac/install/
[Windows]: https://docs.docker.com/docker-for-windows/
[path compatibility]: https://en.wikipedia.org/wiki/Path_(computing)#MS-DOS/Microsoft_Windows_style

## examples

Remember to `cd` to this folder before running any `kitchen` commmands.

Bake a `pydiner:latest` image, freeze it, and serve `bash`.
```sh
./kitchen bake && ./kitchen freeze && ./kitchen serve
Sending build context to Docker daemon  237.6kB
Step 1/10 : FROM python:3.7.5
 ---> fbf9f709ca9f
Step 2/10 : LABEL description="Python development sandbox"
 ---> Using cache
 ---> 4fec2ba14a9c
Step 3/10 : LABEL maintainer="samkennerly@gmail.com"
 ---> Using cache
 ---> c65a9651b61f

...

Successfully tagged pydiner:latest
Total reclaimed space: 0B
root@pydiner:/context#
```

From the inside, a container looks like a real Linux machine.
```sh
root@pydiner:/context# which python
/usr/local/bin/python
root@pydiner:/context# grep PRETTY_NAME /etc/os-release
PRETTY_NAME="Debian GNU/Linux 10 (buster)"
```

Run Python and `import pydiner` without hacking [sys.path].
```sh
root@pydiner:/context# python
Python 3.7.5 (default, Nov 23 2019, 05:59:34)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pydiner
>>> pydiner.echo("Hello, World!")
2019-12-03 21:35:05 Hello, World!
>>> exit()
```

Scripts in `/context/bin` are on the system [PATH].
```sh
root@pydiner:/context# scrambled eggs
2019-12-03 21:36:55 Write derangements of 'eggs' to STDOUT
2019-12-03 21:36:55 10 expected
gesg
gseg
gesg
gseg
2019-12-03 21:36:55 4 found
2019-12-03 21:36:55 0:00:00.000116 time elapsed
```

Save the output of a script and exit the container.
```sh
root@pydiner:/context# scrambled -o var/dirtyfork.txt dirtyfork
2019-12-03 21:42:07 Write derangements of 'dirtyfork' to /context/var/dirtyfork.txt
2019-12-03 21:42:07 145152 expected
2019-12-03 21:42:07 101976 found
2019-12-03 21:42:07 0:00:00.632822 time elapsed
root@pydiner:/context# exit
```

The file `var/dirtyfork.txt` should still exist outside the container.

[sys.path]: https://docs.python.org/3/library/sys.html#sys.path
[PATH]: https://en.wikipedia.org/wiki/PATH_(variable)


## faq

### Let me out!!!1!

Hit *CTRL-D* to exit a container.

### How do I install `pydiner`?

Don't. Use it as a [template] for a new repository.

[template]: https://help.github.com/en/articles/creating-a-repository-from-a-template

### Do I have to run containers as root?

Not if you create a `USER`. See the [Dockerfile reference] for details.

[Dockerfile reference]: https://docs.docker.com/engine/reference/builder/

### Can I run containers in the background?

Yes, but not with the `kitchen` script. See the [Docker run reference].

[Docker run reference]: https://docs.docker.com/engine/reference/run/

### What testing framework does `pydiner` use?

None, but it has been tested with [pytest] to ensure compatibility.

[pytest]: https://docs.pytest.org/en/latest/

### What logging framework does `pydiner` use?

[None]. `achtung()` prints to `STDERR`. `echo()` prints to `STDOUT`.

[None]: https://12factor.net/logs

### What exception handler does `pydiner` use?

None. Programs [stop immediately] when something goes wrong.

[stop immediately]: https://global.toyota/en/company/vision-and-philosophy/production-system/

### What are some other Python project templates?

- [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [PyPA tutorial](https://packaging.python.org/tutorials/packaging-projects/)
- [PyPA sample project](https://github.com/pypa/sampleproject)
- [python-boilerplate.com](https://www.python-boilerplate.com)
