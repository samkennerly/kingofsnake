from collections import namedtuple
from itertools import chain
from json import dump, load
from operator import itemgetter
from pathlib import Path
from sys import stderr as STDERR
from time import sleep

from requests import get as getrequest

BASE = 'https://ergast.com/api/f1'
LIMIT = 1000
RETRIES = 4
TIMEOUT = 1

class ErgastF1:
    """
    UNDER CONSTRUCTION
    """

    def __init__(self, folder=None, retries=RETRIES, timeout=TIMEOUT):
        self.folder = Path(folder) if folder else None
        self.retries = int(retries)
        self.timeout = float(timeout)

    def __repr__(self):
        name = type(self).__name__
        params = ", ".join( f"{k}={v}" for k,v in vars(self).items() )

        return f"{name}({params})"

    @classmethod
    def alert(cls, *args, file=STDERR):
        """ None: Print error message. """
        print("ERROR", cls.__name__, *args, file=file)

    def get(self, *args):
        """ Iterator[Dict]: Replies to query. Uses cache if folder is set. """
        return self.read(*args) if self.folder else self.pages(*args)

    # Row generators

    def circuits(self):
        """ Iterator[namedtuple]: Tacks from all years. """
        get, tupled, unpacked = self.get, self.tupled, self.unpacked

        keys = 'MRData CircuitTable Circuits'.split()
        cols = 'circuitId circuitName country lat long locality url'.split()
        rows = unpacked(get('circuits'), *keys)
        rows = ( {**x, **x.pop('Location')} for x in rows )

        return tupled(rows, 'Circuit', *cols)

    def constructors(self):
        """ Iterator[namedtuple]: Teams from all years. """
        get, tupled, unpacked = self.get, self.tupled, self.unpacked

        keys = 'MRData ConstructorTable Constructors'.split()
        cols = 'constructorId name nationality url'.split()
        rows = unpacked(get('constructors'), *keys)

        return tupled(rows, 'Constructor', *cols)

    def drivers(self):
        """ Iterator[namedtuple]: Drivers from all years. """
        get, tupled, unpacked = self.get, self.tupled, self.unpacked

        keys = 'MRData DriverTable Drivers'.split()
        cols = 'driverId code dateOfBirth familyName givenName nationality'.split()
        cols += 'permanentNumber url'.split()
        rows = unpacked(get('drivers'), *keys)

        return tupled(rows, 'Driver', *cols)

    def races(self, year='current'):
        """ Iterator[namedtuple]: Races from selected year. """
        get, tupled, unpacked = self.get, self.tupled, self.unpacked

        keys = 'MRData RaceTable Races'.split()
        cols = 'circuitId date raceName round season time url'.split()
        rows = unpacked(get(year), *keys)
        rows = ( (x, x.pop('Circuit').pop('circuitId')) for x in rows )
        rows = ( {**x, **{'circuitId': y}} for x, y in rows )

        return tupled(rows, 'Race', *cols)

    # Helpers

    def pages(self, *args, limit=LIMIT):
        """ Iterator[Dict]: Paged replies to query. """
        queried = self.queried

        offset, total = 0, 1
        while offset < total:
            page = queried(*args, limit=limit, offset=offset)
            total = int(page['MRData']['total'])
            offset += limit
            yield page

    def queried(self, *args, **kwargs):
        """ dict: JSON reply to query. Retries automatically. """
        alert, retries, timeout = self.alert, self.retries, self.timeout

        params = "&".join( f"{k}={v}" for k, v in kwargs.items() )
        query = "/".join(map(str, args))
        url = f"{BASE}/{query}.json?{params}"

        for trials in reversed(range(retries)):
            try:
                print(f"GET {url}")
                reply = getrequest(url, timeout=timeout)
                reply.raise_for_status()
                reply = reply.json()
            except Exception as err:
                if trials:
                    alert(f"Try again in {timeout} seconds. {err}")
                    sleep(timeout)
                    timeout *= 2
                else:
                    alert(f"Gave up after {retries} retries.")
                    raise err

            return reply

    def read(self, *args):
        """ Iterator[dict]: Saved replies. Gets missing replies automatically. """
        folder, save = self.folder, self.save

        subdir = folder.joinpath(*args)
        if not any(subdir.glob('*.json')):
            save(*args)

        for path in sorted(subdir.glob('*.json')):
            with open(path) as file:
                yield load(file)

    def save(self, *args, limit=LIMIT, **kwargs):
        """ None: Get query replies and save to JSON files. """
        folder, pages = self.folder, self.pages

        kwargs.setdefault("allow_nan", False)
        kwargs.setdefault("check_circular", False)
        kwargs.setdefault("indent", 2)
        if not folder:
            raise ValueError(f"cache folder is {folder}")

        subdir = folder.joinpath(*map(str, args))
        if not subdir.exists():
            print("mkdir", subdir)
            subdir.mkdir(parents=True)
        for path in subdir.glob('*.json'):
            print("rm", path)
            path.unlink()

        for i, page in enumerate(pages(*args, limit=limit)):
            path = (subdir / str(i)).with_suffix('.json')
            with open(path, "w") as file:
                print("save", path)
                dump(page, file, **kwargs)

    @staticmethod
    def tupled(rows, name, *cols):
        """ Iterator[namedtuple]: Rows with selected column names. """
        Row = namedtuple(name, cols, defaults=[ None for _ in cols ])

        return ( Row(**x) for x in rows )

    @staticmethod
    def unpacked(rows, *keys):
        """ Iterator[dict]: Row dicts extracted from query replies. """
        for key in keys:
            rows = map(itemgetter(key), rows)

        return chain.from_iterable(rows)

    def years(self):
        """ Iterator[int]: Years for which queries are available. """
        get, unpacked = self.get, self.unpacked

        keys = 'MRData SeasonTable Seasons'.split()
        vals = unpacked(get('seasons'), *keys)
        vals = map(itemgetter('season'), vals)

        return map(int, vals)
