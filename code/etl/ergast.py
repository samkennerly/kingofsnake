from json import dump as jsondump
from operator import itemgetter
from pathlib import Path
from time import sleep

from requests import get as getrequest

class Ergast:

    BASE = 'https://ergast.com/api/f1'

    def __init__(self, folder='data/ergast.com/api/f1', limit=10, retry=4, timeout=1):
        self.folder = Path(folder)
        self.limit = int(limit)
        self.retry = int(retry)
        self.timeout = int(timeout)

    def __repr__(self):
        name = type(self).__name__
        params = ", ".join( f"{k}={v}" for k,v in vars(self).items() )

        return f"{name}({params})"

    # Generic queries

    def pages(self, query):
        """ Iterator[Dict]: Raw pages returned by query. """
        limit, raw = self.limit, self.raw

        offset, total = 0, 1
        while offset < total:
            page = raw(query, limit=limit, offset=offset)
            total = int(page['MRData']['total'])
            offset += limit
            yield page

    @classmethod
    def queries(cls):
        raise NotImplementedError

    def raw(self, query, **kwargs):
        """ dict or None: JSON-decoded response to query. """
        retry, timeout, url = self.retry, self.timeout, self.url

        url = url(query, **kwargs)
        for i in reversed(range(retry)):
            raw = getrequest(url, timeout=timeout)
            status = raw.status_code
            if status != 200:
                print(f"{status} ({i} retries left) {url}")
                sleep(timeout)
                continue

            return raw.json()

    def save(self, query):
        """ None: Save query response pages as JSON files. """
        folder, pages = self.folder, self.pages

        folder = folder / str(query)
        if not folder.exists():
            print("mkdir", folder)
            folder.mkdir(parents=True)

        for i, page in enumerate(pages(*args)):
            path = (folder / str(i)).with_suffix('.json')
            with open(path, "w") as file:
                print("save", path)
                jsondump(page, file)

    @classmethod
    def url(cls, query, **kwargs):
        """ str: Target URL for GET requests. """
        BASE = cls.BASE
        params = "&".join( f"{k}={v}" for k,v in kwargs.items() )

        return f"{cls.BASE}/{query}.json?{params}"

    # Specific queries

    def seasons(self):
        page = self.page

        data = page('seasons').pop('MRData').pop('SeasonTable').pop('Seasons')
        data = map(itemgetter('season'), data)

        return tuple(map(int, data))







