#!/usr/bin/python

from __future__ import print_function
from pytvmaze import endpoints, fuzzymatch

try:
    # Python 3 and later
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import urlopen
import json
from datetime import datetime

class Show():
    def __init__(self, data):
        self.data = data
        self.__dict__.update(data)
        self.maze_id = self.data.get('id')
        self.episodes = list()
        self.seasons = dict()
        self.populate()

    def __repr__(self):
        return self.name

    def __iter__(self):
        return iter(self.seasons.values())

    def __len__(self):
        return len(self.seasons)

    def __getitem__(self, item):
        return self.seasons[item]

    def populate(self):
        for episode in self.data.get('_embedded').get('episodes'):
            self.episodes.append(Episode(episode))
        for episode in self.episodes:
            season_num = int(episode.season_number)
            if season_num not in self.seasons:
                self.seasons[season_num] = Season(self, season_num)
            self.seasons[season_num].episodes[episode.episode_number] = episode

class Season():
    def __init__(self, show, season_number):
        self.show = show
        self.season_number = season_number
        self.episodes = dict()

    def __repr__(self):
        return self.show.name + ' S' + str(self.season_number).zfill(2)

    def __iter__(self):
        return iter(self.episodes.values())

    def __len__(self):
        return len(self.episodes)

    def __getitem__(self, item):
        return self.episodes[item]

class Episode():
    def __init__(self, data):
        self.data = data
        self.title = self.data.get('name')
        self.airdate = self.data.get('airdate')
        self.url = self.data.get('url')
        self.season_number = self.data.get('season')
        self.episode_number = self.data.get('number')
        self.image = self.data.get('image')
        self.airstamp = self.data.get('airstamp')
        self.runtime = self.data.get('runtime')
        self.maze_id = self.data.get('id')

    def __repr__(self):
        season = 'S' + str(self.season_number).zfill(2)
        episode = 'E' + str(self.episode_number).zfill(2)
        return season + episode + ' ' + self.title

# Query TV Maze endpoints
def query(url):
    url = url.replace(' ', '+')

    try:
        data = urlopen(url).read()
    except:
        return None

    try:
        results = json.loads(data)
    except:
        results = json.loads(data.decode('utf8'))

    if results:
        return results
    else:
        return None

# Create Show object
def get_show(show):
    search_text = fuzzymatch.parse_user_text(show)
    results = show_search(search_text['showname'])
    s = fuzzymatch.fuzzy_search(search_text, results)
    if s:
        return Show(show_main_info(s, embed='episodes'))

# Return list of Show objects from the TVMaze "Show Search" endpoint
def get_show_list(name):
    shows = show_search(name)
    if shows:
        return [
            Show(show_main_info(show['show']['id'], embed='episodes'))
            for show in shows
        ]

# TV Maze Endpoints
def show_search(show):
    url = endpoints.show_search.format(show)
    q = query(url)
    return q if q else print(show, 'not found')

def show_single_search(show, embed=False):
    if embed:
        url = endpoints.show_single_search.format(show) + '&embed=' + embed
    else:
        url = endpoints.show_single_search.format(show)
    q = query(url)
    return q if q else print(show, 'not found')

def lookup_tvrage(tvrage_id):
    url = endpoints.lookup_tvrage.format(tvrage_id)
    q = query(url)
    return q if q else print('TVRage id', tvrage_id, 'not found')

def lookup_tvdb(tvdb_id):
    url = endpoints.lookup_tvdb.format(tvdb_id)
    q = query(url)
    return q if q else print('TVDB id', tvdb_id, 'not found')

def get_schedule(country='US', date=str(datetime.today().date())):
    url = endpoints.get_schedule.format(country, date)
    q = query(url)
    return q if q else print('Schedule for country', country, 'not found')

# ALL known future episodes, several MB large, cached for 24 hours
def get_full_schedule():
    url = endpoints.get_full_schedule
    q = query(url)
    return q if q else print('Something went wrong,',
                             'www.tvmaze.com may be down')

def show_main_info(maze_id, embed=False):
    if embed:
        url = endpoints.show_main_info.format(maze_id) + '?embed=' + embed
    else:
        url = endpoints.show_main_info.format(maze_id)
    q = query(url)
    return q if q else print('TVMaze ID', maze_id, 'not found')

def episode_list(maze_id, specials=False):
    if specials:
        url = endpoints.episode_list.format(maze_id) + '&specials=1'
    else:
        url = endpoints.episode_list.format(maze_id)
    q = query(url)
    return q if q else print('TVMaze ID', maze_id, 'not found')

def episode_by_number(maze_id, season_number, episode_number):
    url = endpoints.episode_by_number.format(maze_id,
                                             season_number,
                                             episode_number)
    q = query(url)
    return q if q else print('Couldn\'t find season', season_number,
                             'episode', episode_number, 'for TVMaze ID',
                             maze_id)

def episodes_by_date(maze_id, airdate):
    url = endpoints.episodes_by_date.format(maze_id, airdate)
    q = query(url)
    return q if q else print('Couldn\'t find an episode airing', airdate,
                             'for TVMaze ID', maze_id)

def show_cast(maze_id):
    url = endpoints.show_cast.format(maze_id)
    q = query(url)
    return q if q else print('Couldn\'nt find show cast for TVMaze ID',
                             maze_id)

def show_index(page=1):
    url = endpoints.show_index.format(page)
    q = query(url)
    return q if q else print('Error getting show_index,',
                             'www.tvmaze.com may be down')

def people_search(person):
    url = endpoints.people_search.format(person)
    q = query(url)
    return q if q else print('Couldn\'t find person:', person)

def person_main_info(person_id, embed=False):
    if embed:
        url = endpoints.person_main_info.format(person_id) + '?embed=' + embed
    else:
        url = endpoints.person_main_info.format(person_id)
    q = query(url)
    return q if q else print('Couldn\'t find person ID:', person_id)

def person_cast_credits(person_id, embed=False):
    if embed:
        url = endpoints.person_cast_credits.format(person_id) + '?embed=' + embed
    else:
        url = endpoints.person_cast_credits.format(person_id)
    q = query(url)
    return q if q else print('Couldn\'t find cast credits for person ID:',
                             person_id)

def person_crew_credits(person_id, embed=False):
    if embed:
        url = endpoints.person_crew_credits.format(person_id) + '?embed=' + embed
    else:
        url = endpoints.person_crew_credits.format(person_id)
    q = query(url)
    return q if q else print('Couldn\'t find crew credits for person ID:',
                             person_id)

def show_updates():
    url = endpoints.show_updates
    q = query(url)
    return q if q else print('Error getting show_index,',
                             'www.tvmaze.com may be down')

def show_akas(maze_id):
    url = endpoints.show_akas.format(maze_id)
    q = query(url)
    return q if q else print('Couldn\'t find AKA\'s for TVMaze ID:', maze_id)
