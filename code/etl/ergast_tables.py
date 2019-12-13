"""
ErgastCSV class for reading ergast.com/mrd/db/ database images.
"""
from pathlib import Path
from zipfile import ZipFile

from pandas import read_csv

class ErgastTables:
    """
    UNDER CONSTRUCTION
    """

    def __init__(self, path):
        self.path = Path(path).resolve()

    def __repr__(self):
        name = type(self).__name__
        params = ", ".join( f"{k}={v}" for k,v in vars(self).items() )

        return f"{name}({params})"

    def get(self, name, **kwargs):
        """ DataFrame: Read CSV file inside ZIP file. """
        path = self.path

        kwargs.setdefault('header', None)
        kwargs.setdefault('index_col', 'id')
        kwargs.setdefault('na_values', ['\\N'])
        name = Path(name).with_suffix('.csv').name

        with ZipFile(path) as zed:
            with zed.open(name) as file:
                data = read_csv(file, **kwargs).sort_index(axis=1)

        return data

    @property
    def names(self):
        """ Tuple[str]: Table names. """
        with ZipFile(self.path) as zed:
            return tuple( x.split('.')[0] for x in zed.namelist() )

    # Series

    @property
    def status(self):
        get, kw = self.get, { }

        kw['names'] = 'id status'.split()
        data = get('status.csv', **kw)

        return data.pop('status')

    # DataFrames

    @property
    def circuits(self):
        get, kw = self.get, { }

        kw['names'] = 'id ref circuit location country lat long alt url'.split()
        kw['usecols'] = set(kw['names']) - {'alt', 'url'}
        data = get('circuits.csv', **kw)

        return data

    @property
    def drivers(self):
        get, kw = self.get, { }

        kw['names'] = 'id ref number code first last birthday nation url'.split()
        kw['parse_dates'] = ['birthday']
        kw['usecols'] = set(kw['names']) - {'url'}
        data = get('driver.csv', **kw)
        data['number'] = data['number'].fillna(0).astype(int)

        return data

    @property
    def races(self):
        get, kw = self.get, { }

        kw['names'] = 'id year round circuit_id race date time url'.split()
        kw['parse_dates'] = ['date', 'time']
        kw['usecols'] = set(kw['names']) - {'url', 'year'}
        data = get('races.csv', **kw)
        data['time'] = data['time'].dt.time

        return data

    @property
    def teams(self):
        get, kw = self.get, { }

        kw['names'] = 'id ref team nation url'.split()
        kw['usecols'] = set(kw['names']) - {'url'}
        data = get('constructors.csv', **kw)

        return data

    @property
    def team_results(self):
        get, kw = self.get, { }

        kw['names'] = 'id race_id team_id points status'.split()
        data = get('constructor_results.csv', **kw)
        data['dsq'] = data.pop('status') == 'D'

        return data

    @property
    def team_standings(self):
        get, kw = self.get, { }

        kw['names'] = 'id race_id team_id points rank rank_str wins'.split()
        kw['usecols'] = set(kw['names']) - {'rank_str'}
        data = get('constructor_standings.csv', **kw)

        return data













"""
Copyright © 2019 Sam Kennerly

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""