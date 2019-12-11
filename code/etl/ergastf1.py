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

    # Generic queries

    def get(self, query, limit=LIMIT, offset=0):
        """ dict: JSON response to query. Retries automatically. """
        retries, timeout = self.retries, self.timeout

        url = f"{BASE}/{query}.json?limit={limit}&offset={offset}"
        for itry in reversed(range(retries)):
            try:
                print(f"GET {url}")
                reply = getrequest(url, timeout=timeout)
                reply.raise_for_status()

                return reply.json()

            except Exception as err:
                if itry:
                    alert(err)
                    print(f"Retry in {timeout} seconds ({itry} left)")
                    sleep(timeout)
                    timeout *= 2
                else:
                    raise err

    def pages(self, query, limit=LIMIT):
        """ Iterator[Dict]: Raw pages returned by query. """
        get = self.get

        offset, total = 0, 1
        while offset < total:
            page = get(query, limit=limit, offset=offset)
            total = int(page['MRData']['total'])
            offset += limit
            yield page

    @classmethod
    def queries(cls):
        raise NotImplementedError

    def read(self, query):
        raise NotImplementedError

    def save(self, query, limit=LIMIT, **kwargs):
        """
        None: Save query response pages as JSON files in a folder.
        Assign paths automatically. Delete existing JSON files in folder.
        """
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

    # Specific queries

    def seasons(self):

        data = page('seasons').pop('MRData').pop('SeasonTable').pop('Seasons')
        data = map(itemgetter('season'), data)

        return tuple(map(int, data))







