from json import dump as jsondump
from operator import itemgetter
from pathlib import Path
from time import sleep

from requests import get as getrequest

from utils import DATADIR, alert, read_json, save_json

BASE = 'https://ergast.com/api/f1'
FOLDER = DATADIR / 'ergast.com/api/f1'

class Ergast:
    """
    UNDER CONSTRUCTION
    """

    def __init__(self, folder=FOLDER, limit=5, retry=4, timeout=1):
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
        limit, response = self.limit, self.response

        offset, total = 0, 1
        while offset < total:
            page = response(query, limit=limit, offset=offset)
            total = int(page['MRData']['total'])
            offset += limit
            yield page

    @classmethod
    def queries(cls):
        raise NotImplementedError

    def response(self, query, **kwargs):
        """ dict or None: JSON-decoded response to query. """
        retry, timeout, url = self.retry, self.timeout, self.url

        url = url(query, **kwargs)
        for i in reversed(range(retry)):
            raw = getrequest(url, timeout=timeout)
            status = raw.status_code
            if status != 200:
                alert(f"{status} ({i} retries left) {url}")
                sleep(timeout)
                continue

            return raw.json()

    def save(self, query):
        """ None: Save query response pages as JSON files. """
        folder, pages = self.folder, self.pages

        for i, page in enumerate(pages(query)):
            save_json(page, folder / str(i))

    @classmethod
    def url(cls, query, **kwargs):
        """ str: Target URL for GET requests. """
        params = "&".join( f"{k}={v}" for k,v in kwargs.items() )

        return f"{BASE}/{query}.json?{params}"

    # Specific queries

    def seasons(self):
        page = self.page

        data = page('seasons').pop('MRData').pop('SeasonTable').pop('Seasons')
        data = map(itemgetter('season'), data)

        return tuple(map(int, data))







