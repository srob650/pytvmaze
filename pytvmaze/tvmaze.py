#!/usr/bin/python
from __future__ import unicode_literals

import re
import unicodedata
import sys
if sys.version_info[0] == 3:
    def unicode(text, encoding):
        return str(text, encoding)

from pytvmaze import endpoints
from pytvmaze.exceptions import *

try:
    # Python 3 and later
    from urllib.request import urlopen
    from urllib.parse import quote as url_quote, unquote as url_unquote
    from urllib.error import URLError
except ImportError:
    # Python 2
    from urllib2 import urlopen
    from urllib import quote as url_quote, unquote as url_unquote
    from urllib2 import URLError
import json
from datetime import datetime


class Show(object):
    def __init__(self, data):
        self.data = data
        self.status = self.data.get('status')
        self.rating = self.data.get('rating')
        self.genres = self.data.get('genres')
        self.weight = self.data.get('weight')
        self.updated = self.data.get('updated')
        self.name = self.data.get('name')
        self.language = self.data.get('language')
        self.schedule = self.data.get('schedule')
        self.url = self.data.get('url')
        self.image = self.data.get('image')
        self.externals = self.data.get('externals')
        self.premiered = self.data.get('premiered')
        self.summary = self.remove_tags(self.data.get('summary'))
        self._links = self.data.get('_links')
        self.webChannel = self.data.get('webChannel')
        self.runtime = self.data.get('runtime')
        self.type = self.data.get('type')
        self.id = self.data.get('id')
        self.maze_id = self.id
        self.network = self.data.get('network')
        self.episodes = list()
        self.seasons = dict()
        self.cast = list()
        self.characters = list()
        self.populate()

    def __repr__(self):
        maze_id = self.maze_id
        name = self.name
        try:
            year = str(self.data.get('premiered')[:-6])
        except:
            year = None
        try:
            network = str(self.network.get('name'))
        except:
            network = None

        return '<Show(maze_id={id},name={name},year={year},network={network})>'.format(
            id=maze_id, name=name, year=year, network=network
        )

    def __str__(self):
        return self.name

    def __iter__(self):
        return iter(self.seasons.values())

    # Python 3 bool evaluation
    def __bool__(self):
        return bool(self.data)

    # Python 2 bool evaluation
    def __nonzero__(self):
        return bool(self.data)

    def __len__(self):
        return len(self.seasons)

    def __getitem__(self, item):
        try:
            return self.seasons[item]
        except KeyError:
            raise SeasonNotFound('Season {0} does not exist for show {1}.'.format(item, self.name))

    def populate(self):
        embedded =  self.data.get('_embedded')
        if embedded:
            if embedded.get('episodes'):
                for episode in embedded.get('episodes'):
                    self.episodes.append(Episode(episode))
                for episode in self.episodes:
                    season_num = int(episode.season_number)
                    if season_num not in self.seasons:
                        self.seasons[season_num] = Season(self, season_num)
                    self.seasons[season_num].episodes[episode.episode_number] = episode
            if embedded.get('cast'):
                for cast_member in embedded.get('cast'):
                    self.cast.append(Person(cast_member['person']))
                    self.characters.append(Character(cast_member['character']))


    def remove_tags(self, text):
        return re.sub(r'<.*?>', '', text)


class Season(object):
    def __init__(self, show, season_number):
        self.show = show
        self.season_number = season_number
        self.episodes = dict()

    def __repr__(self):
        return '<Season(showname={name},season_number={number})>'.format(
            name=self.show.name,
            number=str(self.season_number).zfill(2)
        )

    def __str__(self):
        return self.show.name + ' S' + str(self.season_number).zfill(2)

    def __iter__(self):
        return iter(self.episodes.values())

    def __len__(self):
        return len(self.episodes)

    def __getitem__(self, item):
        try:
            return self.episodes[item]
        except KeyError:
            raise EpisodeNotFound(
                'Episode {0} does not exist for season {1} of show {2}.'.format(item, self.season_number, self.show))


class Episode(object):
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
        return '<Episode(season={season},episode_number={number})>'.format(
            season=str(self.season_number).zfill(2),
            number=str(self.episode_number).zfill(2)
        )

    def __str__(self):
        season = 'S' + str(self.season_number).zfill(2)
        episode = 'E' + str(self.episode_number).zfill(2)
        return season + episode + ' ' + self.title


class Person(object):
    def __init__(self, data):
        if data.get('person'):
            self.data = data['person']
        else:
            self.data = data
        self._links = self.data.get('_links')
        self.id = self.data.get('id')
        self.image = self.data.get('image')
        self.name = self.data.get('name').encode('utf-8')
        self.score = self.data.get('score')
        self.url = self.data.get('url')


    def __repr__(self):
        return u'<Person(name={name},maze_id={id})>'.format(
            name=unicodedata.normalize(
                'NFD', unicode(self.name, 'utf-8')).encode('ascii', 'ignore'),
            id=self.id
        )

    def __str__(self):
        return self.name


class Character(object):
    def __init__(self, data):
        self.data = data
        self.id = self.data.get('id')
        self.url = self.data.get('url')
        self.name = self.data.get('name').encode('utf-8')
        self.image = self.data.get('image')
        self._links = self.data.get('_links')

    def __repr__(self):
        return u'<Character(name={name},maze_id={id})>'.format(
            name=unicodedata.normalize(
                'NFD', unicode(self.name, 'utf-8')).encode('ascii', 'ignore'),
            id=self.id
        )

    def __str__(self):
        return self.name


# Query TV Maze endpoints
def query_endpoint(url):
    try:
        data = urlopen(url).read()
    except URLError as e:
        if e.code == 404 or e.code == 422:
            return None
        else:
            raise ConnectionError(repr(e))

    try:
        results = json.loads(data)
    except:
        results = json.loads(data.decode('utf8'))

    if results:
        return results
    else:
        return None

# Get Show object
def get_show(maze_id=None, tvdb_id=None, tvrage_id=None, show_name=None,
             show_year=None, show_network=None, show_language=None,
             show_country=None, embed=None):
    '''
    Get Show object directly via id or indirectly via name + optional qualifiers

    If only a show_name is given, the show with the highest score using the
    tvmaze algorithm will be returned.
    If you provide extra qualifiers such as network or language they will be
    used for a more specific match, if one exists.
    '''
    if maze_id:
        return Show(show_main_info(maze_id, embed=embed))
    elif tvdb_id:
        return Show(show_main_info(lookup_tvdb(tvdb_id)['id'],
                                   embed=embed))
    elif tvrage_id:
        return Show(show_main_info(lookup_tvrage(tvrage_id)['id'],
                                   embed=embed))
    elif show_name:
        show = get_show_by_search(show_name, show_year, show_network,
                                  show_language, show_country, embed=embed)
        return show
    else:
        raise MissingParameters(
            'Either maze_id, tvdb_id, tvrage_id or show_name are required to get show, none provided,')


# Search with user-defined qualifiers, used by get_show() method
def get_show_by_search(show_name, show_year, show_network, show_language, show_country, embed):
    shows = get_show_list(show_name, embed)
    qualifiers = [
        q.lower() for q in [str(show_year), show_network, show_language, show_country]
        if q
        ]
    if qualifiers:
        for show in shows:
            try:
                premiered = show.premiered[:-6].lower()
            except:
                premiered = ''
            try:
                country = show.network['country']['code'].lower()
            except:
                country = ''
            try:
                network = show.network['name'].lower()
            except:
                network = ''
            try:
                language = show.language.lower()
            except:
                language = ''
            attributes = [premiered, country, network, language]
            show.matched_qualifiers = len(set(qualifiers) & set(attributes))
        # Return show with most matched qualifiers
        return max(shows, key=lambda k: k.matched_qualifiers)
    else:
        # Return show with highest tvmaze search score
        return shows[0]


# Return list of Show objects
def get_show_list(show_name, embed=None):
    '''
    Return list of Show objects from the TVMaze "Show Search" endpoint

    List will be ordered by tvmaze score and should mimic the results you see
    by doing a show search on the website.
    '''
    shows = show_search(show_name)
    return [
        Show(show_main_info(show['show']['id'], embed=embed))
        for show in shows
        ]


# Get list of Person objects
def get_people(name):
    '''
    Return list of Person objects from the TVMaze "People Search" endpoint
    '''
    people = people_search(name)
    if people:
        return [Person(person) for person in people]


# TV Maze Endpoints
def show_search(show):
    show = url_quote(show)
    url = endpoints.show_search.format(show)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise ShowNotFound(str(show) + ' not found')


def show_single_search(show, embed=None):
    show = url_quote(show)
    if embed:
        url = endpoints.show_single_search.format(show) + '&embed=' + embed
    else:
        url = endpoints.show_single_search.format(show)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise ShowNotFound(str(show) + ' not found')


def lookup_tvrage(tvrage_id):
    url = endpoints.lookup_tvrage.format(tvrage_id)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise IDNotFound('TVRage id ' + str(tvrage_id) + ' not found')


def lookup_tvdb(tvdb_id):
    url = endpoints.lookup_tvdb.format(tvdb_id)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise IDNotFound('TVdb id ' + str(tvdb_id) + ' not found')


def get_schedule(country='US', date=str(datetime.today().date())):
    url = endpoints.get_schedule.format(country, date)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise ScheduleNotFound('Schedule for country ' + str(country) + ' not found')


# ALL known future episodes, several MB large, cached for 24 hours
def get_full_schedule():
    url = endpoints.get_full_schedule
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise GeneralError('Something went wrong, www.tvmaze.com may be down')


def show_main_info(maze_id, embed=None):
    if embed:
        url = endpoints.show_main_info.format(maze_id) + '?embed=' + embed
    else:
        url = endpoints.show_main_info.format(maze_id)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise IDNotFound('Maze id ' + str(maze_id) + ' not found')


def episode_list(maze_id, specials=None):
    if specials:
        url = endpoints.episode_list.format(maze_id) + '&specials=1'
    else:
        url = endpoints.episode_list.format(maze_id)
    q = query_endpoint(url)
    if q:
        return [Episode(episode) for episode in q]
    else:
        raise IDNotFound('Maze id ' + str(maze_id) + ' not found')


def episode_by_number(maze_id, season_number, episode_number):
    url = endpoints.episode_by_number.format(maze_id,
                                             season_number,
                                             episode_number)
    q = query_endpoint(url)
    if q:
        return Episode(q)
    else:
        raise EpisodeNotFound(
            'Couldn\'t find season ' + str(season_number) + ' episode ' + str(episode_number) + ' for TVMaze ID ' + str(
                maze_id))


def episodes_by_date(maze_id, airdate):
    try:
        datetime.strptime(airdate, '%Y-%m-%d')
    except ValueError:
        raise IllegalAirDate('Airdate must be string formatted as \"YYYY-MM-DD\"')
    url = endpoints.episodes_by_date.format(maze_id, airdate)
    q = query_endpoint(url)
    if q:
        return [Episode(episode) for episode in q]
    else:
        raise NoEpisodesForAirdate('Couldn\'t find an episode airing ' + str(airdate) + ' for TVMaze ID' + str(maze_id))


def show_cast(maze_id):
    url = endpoints.show_cast.format(maze_id)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise CastNotFound('Couldn\'nt find show cast for TVMaze ID' + str(maze_id))


def show_index(page=1):
    url = endpoints.show_index.format(page)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise ShowIndexError('Error getting show_index, www.tvmaze.com may be down')


def people_search(person):
    person = url_quote(person)
    url = endpoints.people_search.format(person)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise PersonNotFound('Couldn\'t find person: ' + str(person))


def person_main_info(person_id, embed=None):
    if embed:
        url = endpoints.person_main_info.format(person_id) + '?embed=' + embed
    else:
        url = endpoints.person_main_info.format(person_id)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise PersonNotFound('Couldn\'t find person: ' + str(person_id))


def person_cast_credits(person_id, embed=None):
    if embed:
        url = endpoints.person_cast_credits.format(person_id) + '?embed=' + embed
    else:
        url = endpoints.person_cast_credits.format(person_id)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise CreditsNotFound('Couldn\'t find cast credits for person ID: ' + str(person_id))


def person_crew_credits(person_id, embed=None):
    if embed:
        url = endpoints.person_crew_credits.format(person_id) + '?embed=' + embed
    else:
        url = endpoints.person_crew_credits.format(person_id)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise CreditsNotFound('Couldn\'t find crew credits for person ID: ' + str(person_id))


def show_updates():
    url = endpoints.show_updates
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise ShowIndexError('Error getting show_index, www.tvmaze.com may be down')


def show_akas(maze_id):
    url = endpoints.show_akas.format(maze_id)
    q = query_endpoint(url)
    if q:
        return q
    else:
        raise AKASNotFound('Couldn\'t find AKA\'s for TVMaze ID: ' + str(maze_id))
