"""
Example test fixtures: constants, cleanup methods, etc.
"""
from pathlib import Path
from shutil import rmtree

REPO = Path(__file__).resolve().parent.parent
TMPDIR = REPO / "tmp"


def all_tests(testmodule):
    """ Iterator[Tuple[str, Callable]]: Methods to call in testmodule. """
    for name, obj in vars(testmodule).items():
        if name.startswith("test_") and callable(obj):
            yield name, obj


def bigprint(**kwargs):
    """ None: Fancy print function for key:value pairs. """
    for k, v in kwargs.items():
        print(f"{k}: {repr(v)}")


def cleartmp(meth):
    """ function: Decorator to create and destroy TMPDIR. """

    def wrapped(*args, **kwargs):
        if TMPDIR.exists():
            rmtree(TMPDIR)

        TMPDIR.mkdir()
        output = meth(*args, **kwargs)
        rmtree(TMPDIR)

        return output

    return wrapped


def do(meth):
    """ None or Exception: There is no try. """
    try:
        meth()
    except Exception as err:
        return err


def errors(module):
    """ dict: {name:Exception or None} for tests in module. """
    modname = module.__name__
    errors = ((k, do(v)) for k, v in all_tests(module))
    errors = ((k, v) for k, v in errors if v is not None)

    return {f"{modname}.{name}": err for name, err in errors}
