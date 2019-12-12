from collections import namedtuple
from itertools import chain, starmap
from json import dump, load
from operator import itemgetter
from pathlib import Path
from sys import stderr as STDERR
from time import sleep

from requests import get as getrequest

BASE = 'https://ergast.com/api/f1'
LIMIT = 1000

def alert(*args, file=STDERR):
    """ None: Print error message. """
    print("ERROR ErgastF1", *args, file=file)

class ErgastF1:
    """
    UNDER CONSTRUCTION
    """

    def __init__(self, folder=None, retries=4, timeout=1/2):
        self.folder = Path(folder) if folder else None
        self.retries = int(retries)
        self.timeout = float(timeout)

    def __repr__(self):
        name = type(self).__name__
        params = ", ".join( f"{k}={v}" for k,v in vars(self).items() )

        return f"{name}({params})"

    def __getitem__(self, query):
        return self.read(query) if self.folder else self.pages(query)

    # Generic queries

    def ondisk(self, query):
        """ List[Path]: Paths to saved query replies (if any). """
        return sorted((self.folder / str(query)).glob('*.json'))

    def pages(self, query, limit=LIMIT):
        """ Iterator[Dict]: Raw replies to query. """
        queried = self.queried

        offset, total = 0, 1
        while offset < total:
            page = queried(query, limit=limit, offset=offset)
            total = int(page['MRData']['total'])
            offset += limit
            yield page

    def queried(self, query, limit=LIMIT, offset=0):
        """ dict: JSON response to query. Retries automatically. """
        retries, timeout = self.retries, self.timeout

        url = f"{BASE}/{query}.json?limit={limit}&offset={offset}"
        for trials in reversed(range(retries)):
            try:
                print(f"GET {url}")
                reply = getrequest(url, timeout=timeout)
                reply.raise_for_status()

                return reply.json()

            except Exception as err:
                if trials:
                    alert(err)
                    print(f"Retry in {timeout} seconds ({trials} left)")
                    sleep(timeout)
                    timeout *= 2
                else:
                    raise err

    def read(self, query):
        """ Iterator[dict]: Saved query replies. """
        ondisk, save = self.ondisk, self.save

        paths = ondisk(query) or save(query) or ondisk(query)
        for path in paths:
            with open(path) as file:
                yield load(file)

    def save(self, query, limit=LIMIT, **kwargs):
        """ None: Get query replies and save to JSON files. """
        folder, pages = self.folder, self.pages

        kwargs.setdefault("allow_nan", False)
        kwargs.setdefault("check_circular", False)
        kwargs.setdefault("indent", 2)

        if not folder:
            raise ValueError(f"cache folder is {folder}")

        subdir = folder / query
        if not subdir.exists():
            print("mkdir", subdir)
            subdir.mkdir(parents=True)
        for path in subdir.glob('*.json'):
            print("rm", path)
            path.unlink()

        for i, page in enumerate(pages(query, limit=limit)):
            path = (subdir / str(i)).with_suffix('.json')
            with open(path, "w") as file:
                print("save", path)
                dump(page, file, **kwargs)

    # Unpackers

    @staticmethod
    def tupled(rows, name, *cols):
        """ Iterator[namedtuple]: Rows with selected column names. """
        return starmap(namedtuple(name, cols), map(itemgetter(*cols), rows))

    def unpacked(self, query, *keys):
        """ Iterator: Row dictionaries extracted from query replies. """
        rows = self[query]
        for key in keys:
            rows = map(itemgetter(key), rows)

        return chain.from_iterable(rows)

    # Specific queries

    def circuits(self):
        tupled, unpacked = self.tupled, self.unpacked

        cols = 'circuitId circuitName country lat long locality url'.split()
        rows = unpacked('circuits', 'MRData', 'CircuitTable', 'Circuits')
        rows = ( {**x, **x.pop('Location')} for x in rows )

        return tupled(rows, 'Circuit', *cols)

    def constructors(self):
        tupled, unpacked = self.tupled, self.unpacked

        cols = 'constructorId name nationality url'.split()
        rows = unpacked('constructors', 'MRData', 'ConstructorTable', 'Constructors')

        return tupled(rows, 'Constructor', *cols)

    def drivers(self):
        tupled, unpacked = self.tupled, self.unpacked

        cols = 'driverId dateOfBirth familyName givenName nationality url'.split()
        rows = unpacked('drivers', 'MRData', 'DriverTable', 'Drivers')

        return tupled(rows, 'Driver', *cols)

    def races(self):
        seasons, tupled, unpacked = self.seasons, self.tupled, self.unpacked

        cols = 'circuitId date raceName round season url'.split()
        rows = ( unpacked(x, 'MRData', 'RaceTable', 'Races') for x in seasons() )
        rows = chain.from_iterable(rows)
        rows = ( (x, x.pop('Circuit').pop('circuitId')) for x in rows )
        rows = ( {**x, **{'circuitId': y}} for x, y in rows )

        return tupled(rows, 'Race', *cols)

    def seasons(self):
        unpacked = self.unpacked

        rows = self.unpacked('seasons', 'MRData', 'SeasonTable', 'Seasons')
        rows = map(itemgetter('season'), rows)

        return sorted(rows)






















