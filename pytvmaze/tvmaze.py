#!/usr/bin/python

from __future__ import print_function
import endpoints
import fuzzymatch
from __init__ import LOG_LEVEL
import logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

try:
    # Python 3 and later
    from urllib.request import urlopen
    logger.debug('Python 3 -- using urllib.request')
except ImportError:
    # Python 2
    from urllib2 import urlopen
    logger.debug('Python 2 -- using urllib2')
import json
from datetime import datetime

class Show():
    def __init__(self, data):
        self.data = data
        self.__dict__.update(data)
        self.maze_id = self.data.get('id')
        self.episodes = self.get_episode_list()

    def get_episode_list(self):
        eps = []
        episodes = self.data.get('_embedded').get('episodes')
        for episode in episodes:
            eps.append(Episode(episode))
        return eps

    def get_episode(self, season_number, episode_number):
        for episode in self.episodes:
            if (episode.season_number == season_number and
                episode.episode_number == episode_number):
                return episode

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

# Query TV Maze endpoints
def query(url):
    url = url.replace(' ', '+')

    try:
        data = urlopen(url).read()
    except:
        logger.debug('No data from url: {0}'.format(url))
        return None

    try:
        results = json.loads(data)
    except:
        results = json.loads(data.decode('utf8'))

    if results:
        return results
    else:
        logger.debug('No results from url: {0}'.format(url))
        return None

# Create Show object
def get_show(show):
    search_text = fuzzymatch.parse_user_text(show)
    results = show_search(search_text['showname'])
    s = fuzzymatch.fuzzy_search(search_text, results)
    if s:
        return Show(show_main_info(s, embed='episodes'))

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
