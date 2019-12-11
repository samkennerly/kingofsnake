"""
Constants and convenience functions.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
CONFIG = REPO / "etc"
DATADIR = REPO / "data"

def alert(*args, file=sys.stderr):
    """ None: Print error message to STDERR. """
    print("ERROR", *args, file=file)

def read_json(path, **kwargs):
    """ dict or list: Data from JSON file. """
    path = pathlib.Path(path).with_suffix('.json')

    print("read", path)
    with open(path) as file:
        return json.load(file, **kwargs)

def save_json(data, path, **kwargs):
    """ None: Save data as JSON file. """
    path = pathlib.Path(path).with_suffix('.json')
    kwargs.setdefault("allow_nan", True)
    kwargs.setdefault("check_circular", False)
    kwargs.setdefault("indent", 2)

    folder = path.parent
    if not folder.exists():
        print("mkdir", folder)
        folder.mkdir(parents=True)

    print("save", path)
    with open(path, "w") as file:
        json.dump(data, file, **kwargs)
