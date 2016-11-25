#!/usr/bin/python
# coding=utf-8
from __future__ import unicode_literals

import re
from datetime import datetime
from six import text_type

import requests
import requests.compat
from requests.packages.urllib3 import util
from requests.adapters import HTTPAdapter

from pytvmaze import (
    endpoints,
    exceptions,
)


def _url_quote(show):
    return requests.compat.quote(show.encode('UTF-8'))


def _remove_tags(text):
    if not text:
        return None
    return re.sub(r'<.*?>', '', text)


# Requests >= 2.12.2 required for Retry
def make_retry_adapter(**kwargs):
    adapter = None
    try:
        adapter = HTTPAdapter(
            max_retries=util.retry.Retry(**kwargs),
        )
    except AttributeError:
        pass
    return adapter

retry_adapter = make_retry_adapter(
    total=5,
    backoff_factor=0.1,
    status_forcelist=0.1,
)


class TVMazeStandard(object):
    """This is the main class of the module enabling interaction with both free and Premium
    TVMaze features.

    Attributes:
        username (str): Username for http://www.tvmaze.com
        api_key (str): TVMaze api key.  Find your key at http://www.tvmaze.com/dashboard

    """

    session = None
    username = None
    api_key = None

    @classmethod
    def make_session(cls, session=None, **kwargs):
        # attach a session
        cls.session = session or requests.Session()

        # mount a retry adapter if available
        # TODO: change this so it does not overwrite
        # already mounted adapters
        if retry_adapter:
            cls.session.mount('http://', retry_adapter)

        cls.session.headers.update({
            'User-Agent': kwargs.pop('user_agent', 'pytvmaze'),
        })
        return cls.session

    @classmethod
    def request(cls, *args, **kwargs):
        kwargs.setdefault('method', 'GET')
        if not cls.session:
            cls.session = cls.make_session()
        try:
            response = cls.session.request(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            raise exceptions.ConnectionError(repr(e))

        if response.status_code in [404, 422]:
            return None

        if response.status_code == 400:
            raise exceptions.BadRequest('Bad Request for url: {request.url}'.format(request=response.request))
        return response

    # Query TVMaze free endpoints
    @classmethod
    def _endpoint_standard_get(cls, url, *args, **kwargs):
        response = cls.request(url=url, *args, **kwargs)
        return response.json() if response else None

    # Get Show object
    def get_show(self, maze_id=None, tvdb_id=None, tvrage_id=None, imdb_id=None, show_name=None,
                 show_year=None, show_network=None, show_language=None, show_country=None,
                 show_web_channel=None, embed=None):
        """
        Get Show object directly via id or indirectly via name + optional qualifiers

        If only a show_name is given, the show with the highest score using the
        tvmaze algorithm will be returned.
        If you provide extra qualifiers such as network or language they will be
        used for a more specific match, if one exists.
        Args:
            maze_id: Show maze_id
            tvdb_id: Show tvdb_id
            tvrage_id: Show tvrage_id
            imdb_id: Show imdb_id
            show_name: Show name to be searched
            show_year: Show premiere year
            show_network: Show TV Network (like ABC, NBC, etc.)
            show_web_channel: Show Web Channel (like Netflix, Amazon, etc.)
            show_language: Show language
            show_country: Show country
            embed: embed parameter to include additional data. Currently 'episodes' and 'cast' are supported
        """
        errors = []
        if not (maze_id or tvdb_id or tvrage_id or imdb_id or show_name):
            raise exceptions.MissingParameters(
                    'Either maze_id, tvdb_id, tvrage_id, imdb_id or show_name are required to get show, none provided,')
        if maze_id:
            try:
                return self.show_main_info(maze_id, embed=embed)
            except exceptions.IDNotFound as e:
                errors.append(e.value)
        if tvdb_id:
            try:
                return self.show_main_info(self.lookup_tvdb(tvdb_id).id, embed=embed)
            except exceptions.IDNotFound as e:
                errors.append(e.value)
        if tvrage_id:
            try:
                return self.show_main_info(self.lookup_tvrage(tvrage_id).id, embed=embed)
            except exceptions.IDNotFound as e:
                errors.append(e.value)
        if imdb_id:
            try:
                return self.show_main_info(self.lookup_imdb(imdb_id).id, embed=embed)
            except exceptions.IDNotFound as e:
                errors.append(e.value)
        if show_name:
            try:
                show = self._get_show_by_search(show_name, show_year, show_network, show_language,
                                                show_country, show_web_channel, embed=embed)
                return show
            except exceptions.ShowNotFound as e:
                errors.append(e.value)
        raise exceptions.ShowNotFound(' ,'.join(errors))

    @classmethod
    def _get_show_with_qualifiers(cls, show_name, qualifiers):
        shows = cls.get_show_list(show_name)
        best_match = -1  # Initialize match value score
        show_match = None

        for show in shows:
            if show.premiered:
                premiered = show.premiered[:-6].lower()
            else:
                premiered = None
            if show.network and show.network.name:
                network = show.network.name.lower()
            else:
                network = None
            if show.web_channel and show.web_channel.name:
                web_channel = show.web_channel.name.lower()
            else:
                web_channel = None
            if show.network and show.network.code:
                country = show.network.code.lower()
            else:
                if show.web_channel and show.web_channel.code:
                    country = show.web_channel.code.lower()
                else:
                    country = None
            if show.language:
                language = show.language.lower()
            else:
                language = None

            attributes = [premiered, country, network, language, web_channel]
            show_score = len(set(qualifiers) & set(attributes))
            if show_score > best_match:
                best_match = show_score
                show_match = show
        return show_match

    # Search with user-defined qualifiers, used by get_show() method
    def _get_show_by_search(self, show_name, show_year, show_network, show_language, show_country,
                            show_web_channel, embed):
        if show_year:
            show_year = str(show_year)
        qualifiers = list(filter(None, [show_year, show_network, show_language, show_country, show_web_channel]))
        if qualifiers:
            qualifiers = [q.lower() for q in qualifiers if q]
            show = self._get_show_with_qualifiers(show_name, qualifiers)
        else:
            return self.show_single_search(show=show_name, embed=embed)
        if embed:
            return self.show_main_info(maze_id=show.id, embed=embed)
        else:
            return show

    @classmethod
    def episode_by_id(cls, episode_id):
        url = endpoints.episode_by_id.format(episode_id)
        q = cls._endpoint_standard_get(url)
        if q:
            return Episode(q)
        else:
            raise exceptions.EpisodeNotFound(
                'Couldn\'t find Episode with ID {0}'.format(episode_id))

    @classmethod
    def episode_by_number(cls, maze_id, season_number, episode_number):
        url = endpoints.episode_by_number.format(maze_id)
        q = cls._endpoint_standard_get(url, params={
            'season': season_number,
            'number': episode_number,
        })
        if q:
            return Episode(q)
        else:
            raise exceptions.EpisodeNotFound(
                'Couldn\'t find season {0} episode {1} for TVMaze ID {2}'.format(
                    season_number, episode_number, maze_id))

    @classmethod
    def episode_list(cls, maze_id, specials=None):
        url = endpoints.episode_list.format(maze_id)
        q = cls._endpoint_standard_get(url, params={
            'specials': 1 if specials else None})
        if type(q) == list:
            return [Episode(episode) for episode in q]
        else:
            raise exceptions.IDNotFound(
                'Maze id {0} not found'.format(maze_id))

    @classmethod
    def episodes_by_date(cls, maze_id, airdate):
        try:
            datetime.strptime(airdate, '%Y-%m-%d')
        except ValueError:
            raise exceptions.IllegalAirDate(
                'Airdate must be string formatted as \"YYYY-MM-DD\"')
        url = endpoints.episodes_by_date.format(maze_id)
        q = cls._endpoint_standard_get(url, params={'date': airdate})
        if q:
            return [Episode(episode) for episode in q]
        else:
            raise exceptions.NoEpisodesForAirdate(
                'Couldn\'t find an episode airing {0} for TVMaze ID {1}'.format(
                    airdate, maze_id))

    # ALL known future episodes, several MB large, cached for 24 hours
    @classmethod
    def get_full_schedule(cls, ):
        url = endpoints.get_full_schedule
        q = cls._endpoint_standard_get(url)
        if q:
            return [Episode(episode) for episode in q]
        else:
            raise exceptions.GeneralError(
                'Something went wrong, www.tvmaze.com may be down')

    # Get list of Person objects
    @classmethod
    def get_people(cls, name):
        """
        Return list of Person objects from the TVMaze "People Search" endpoint
        :param name: Name of person
        :return: List of Person(s)
        """
        people = cls.people_search(name)
        if people:
            return people

    @classmethod
    def get_schedule(cls, country=None, date=None):
        url = endpoints.get_schedule
        q = cls._endpoint_standard_get(url, params={
            'country': country,
            'date': date,
        })
        if q:
            return [Episode(episode) for episode in q]
        else:
            raise exceptions.ScheduleNotFound(
                'Schedule for country {0} at date {1} not found'.format(
                    country, date))

    @classmethod
    def get_show_crew(cls, maze_id):
        url = endpoints.show_crew.format(maze_id)
        q = cls._endpoint_standard_get(url)
        if q:
            return [Crew(crew) for crew in q]
        else:
            raise exceptions.CrewNotFound(
                'Couldn\'t find crew for TVMaze ID {}'.format(maze_id))

    # Return list of Show objects
    @classmethod
    def get_show_list(cls, show_name):
        """
        Return list of Show objects from the TVMaze "Show Search" endpoint

        List will be ordered by tvmaze score and should mimic the results you see
        by doing a show search on the website.
        :param show_name: Name of show
        :return: List of Show(s)
        """
        shows = cls.show_search(show_name)
        return shows

    @classmethod
    def lookup_imdb(cls, imdb_id):
        url = endpoints.lookup
        q = cls._endpoint_standard_get(url, params={'imdb': imdb_id})
        if q:
            return Show(q)
        else:
            raise exceptions.IDNotFound(
                'IMDB ID {0} not found'.format(imdb_id))

    @classmethod
    def lookup_tvdb(cls, tvdb_id):
        url = endpoints.lookup
        q = cls._endpoint_standard_get(url, params={'thetvdb': tvdb_id})
        if q:
            return Show(q)
        else:
            raise exceptions.IDNotFound(
                'TVDB ID {0} not found'.format(tvdb_id))

    @classmethod
    def lookup_tvrage(cls, tvrage_id):
        url = endpoints.lookup
        q = cls._endpoint_standard_get(url, params={'tvrage': tvrage_id})
        if q:
            return Show(q)
        else:
            raise exceptions.IDNotFound(
                'TVRage ID {0} not found'.format(tvrage_id))

    @classmethod
    def person_cast_credits(cls, person_id, embed=None):
        if embed not in [None, 'show', 'character']:
            raise exceptions.InvalidEmbedValue(
                'Value for embed must be "show", "character" or None')
        if embed:
            url = endpoints.person_cast_credits.format(
                person_id) + '?embed=' + embed
        else:
            url = endpoints.person_cast_credits.format(person_id)
        q = cls._endpoint_standard_get(url)
        if q:
            return [CastCredit(credit) for credit in q]
        else:
            raise exceptions.CreditsNotFound(
                'Couldn\'t find cast credits for person ID {0}'.format(
                    person_id))

    @classmethod
    def person_crew_credits(cls, person_id, embed=None):
        if embed not in [None, 'show']:
            raise exceptions.InvalidEmbedValue(
                'Value for embed must be "show" or None')
        if embed:
            url = endpoints.person_crew_credits.format(
                person_id) + '?embed=' + embed
        else:
            url = endpoints.person_crew_credits.format(person_id)
        q = cls._endpoint_standard_get(url)
        if q:
            return [CrewCredit(credit) for credit in q]
        else:
            raise exceptions.CreditsNotFound(
                'Couldn\'t find crew credits for person ID {0}'.format(
                    person_id))

    @classmethod
    def person_main_info(cls, person_id, embed=None):
        if embed not in [None, 'castcredits', 'crewcredits']:
            raise exceptions.InvalidEmbedValue(
                'Value for embed must be "castcredits" or None')
        if embed:
            url = endpoints.person_main_info.format(
                person_id) + '?embed=' + embed
        else:
            url = endpoints.person_main_info.format(person_id)
        q = cls._endpoint_standard_get(url)
        if q:
            return Person(q)
        else:
            raise exceptions.PersonNotFound(
                'Couldn\'t find person {0}'.format(person_id))

    @classmethod
    def people_search(cls, person):
        url = endpoints.people_search
        q = cls._endpoint_standard_get(url, params={'q': person})
        if q:
            return [Person(person) for person in q]
        else:
            raise exceptions.PersonNotFound(
                'Couldn\'t find person {0}'.format(person))

    @classmethod
    def season_by_id(cls, season_id):
        url = endpoints.season_by_id.format(season_id)
        q = cls._endpoint_standard_get(url)
        if q:
            return Season(q)
        else:
            raise exceptions.SeasonNotFound(
                'Couldn\'t find Season with ID {0}'.format(season_id))

    @classmethod
    def show_akas(cls, maze_id):
        url = endpoints.show_akas.format(maze_id)
        q = cls._endpoint_standard_get(url)
        if q:
            return [AKA(aka) for aka in q]
        else:
            raise exceptions.AKASNotFound(
                'Couldn\'t find AKA\'s for TVMaze ID {0}'.format(maze_id))

    @classmethod
    def show_cast(cls, maze_id):
        url = endpoints.show_cast.format(maze_id)
        q = cls._endpoint_standard_get(url)
        if q:
            return Cast(q)
        else:
            raise exceptions.CastNotFound(
                'Couldn\'nt find show cast for TVMaze ID {0}'.format(maze_id))

    @classmethod
    def show_index(cls, page=0):
        url = endpoints.show_index
        q = cls._endpoint_standard_get(url, params={'page': page})
        if q:
            return [Show(show) for show in q]
        else:
            raise exceptions.ShowIndexError(
                'Error getting show index, www.tvmaze.com may be down')

    @classmethod
    def show_main_info(cls, maze_id, embed=None):
        embed_options = [None, 'episodes', 'cast', 'previousepisode',
                         'nextepisode']
        if embed not in embed_options:
            raise exceptions.InvalidEmbedValue(
                'Value for embed must be one of the following: {0!r}'.format(
                    embed_options))
        url = endpoints.show_main_info.format(maze_id)
        q = cls._endpoint_standard_get(url, params={'embed': embed})
        if q:
            return Show(q)
        else:
            raise exceptions.IDNotFound(
                'Maze id {0} not found'.format(maze_id))

    @classmethod
    def show_search(cls, show):
        url = endpoints.show_search
        q = cls._endpoint_standard_get(url, params={'q': show})
        if q:
            shows = []
            for result in q:
                show = Show(result['show'])
                show.score = result['score']
                shows.append(show)
            return shows
        else:
            raise exceptions.ShowNotFound('Show {0} not found'.format(show))

    @classmethod
    def show_seasons(cls, maze_id):
        url = endpoints.show_seasons.format(maze_id)
        q = cls._endpoint_standard_get(url)
        if q:
            season_dict = dict()
            for season in q:
                season_dict[season['number']] = Season(season)
            return season_dict
        else:
            raise exceptions.SeasonNotFound(
                'Couldn\'t find Season\'s for TVMaze ID {0}'.format(maze_id))

    @classmethod
    def show_single_search(cls, show, embed=None):
        embed_options = [None, 'episodes', 'cast', 'previousepisode',
                         'nextepisode']
        if embed not in embed_options:
            raise exceptions.InvalidEmbedValue(
                'Value for embed must be one of the following: {0!r}'.format(
                    embed_options))
        url = endpoints.show_single_search
        q = cls._endpoint_standard_get(url, params={
            'q': show,
            'embed': embed,
        })
        if q:
            return Show(q)
        else:
            raise exceptions.ShowNotFound(
                'show name "{0}" not found'.format(show))

    @classmethod
    def show_updates(cls, ):
        url = endpoints.show_updates
        q = cls._endpoint_standard_get(url)
        if q:
            return Updates(q)
        else:
            raise exceptions.ShowIndexError(
                'Error getting show updates, www.tvmaze.com may be down')


class AKA(object):
    def __init__(self, data):
        self.name = data.get('name')
        self.country = data.get('country')

    def __repr__(self):
        return '<AKA(name={name},country={country})>'.format(name=self.name, country=self.country)


class Cast(object):
    def __init__(self, data):
        self.people = []
        self.characters = []
        self.populate(data)

    def populate(self, data):
        for cast_member in data:
            self.people.append(Person(cast_member['person']))
            self.characters.append(Character(cast_member['character']))
            self.people[-1].character = self.characters[-1]  # add reference to character
            self.characters[-1].person = self.people[-1]  # add reference to cast member


class CastCredit(object):
    def __init__(self, data):
        self.links = data.get('_links')
        self.character = None
        self.show = None
        self.populate(data)

    def populate(self, data):
        if data.get('_embedded'):
            if data['_embedded'].get('character'):
                self.character = Character(data['_embedded']['character'])
            elif data['_embedded'].get('show'):
                self.show = Show(data['_embedded']['show'])


class Character(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.url = data.get('url')
        self.name = data.get('name')
        self.image = data.get('image')
        self.links = data.get('_links')
        self.person = None

    def __repr__(self):
        return text_type('<Character(name={name},maze_id={id})>'.format(
                name=self.name,
                id=self.id
        ))

    def __str__(self):
        return text_type(self.name)

    def __unicode__(self):
        return self.name


class Crew(object):
    def __init__(self, data):
        self.person = Person(data.get('person'))
        self.type = data.get('type')

    def __repr__(self):
        return text_type('<Crew(name={name},maze_id={id},type={type})>'.format(
                name=self.person.name,
                id=self.person.id,
                type=self.type
        ))


class CrewCredit(object):
    def __init__(self, data):
        self.links = data.get('_links')
        self.type = data.get('type')
        self.show = None
        self.populate(data)

    def populate(self, data):
        if data.get('_embedded'):
            if data['_embedded'].get('show'):
                self.show = Show(data['_embedded']['show'])


class Episode(object):
    def __init__(self, data):
        self.title = data.get('name')
        self.airdate = data.get('airdate')
        self.url = data.get('url')
        self.season_number = data.get('season')
        self.episode_number = data.get('number')
        self.image = data.get('image')
        self.airstamp = data.get('airstamp')
        self.airtime = data.get('airtime')
        self.runtime = data.get('runtime')
        self.summary = _remove_tags(data.get('summary'))
        self.maze_id = data.get('id')
        self.special = self.is_special()
        # Reference to show for when using get_schedule()
        if data.get('show'):
            self.show = Show(data.get('show'))
        # Reference to show for when using get_full_schedule()
        if data.get('_embedded'):
            if data['_embedded'].get('show'):
                self.show = Show(data['_embedded']['show'])

    def __repr__(self):
        if self.special:
            epnum = 'Special'
        else:
            epnum = self.episode_number
        return '<Episode(season={season},episode_number={number})>'.format(
                season=str(self.season_number).zfill(2),
                number=str(epnum).zfill(2)
        )

    def __str__(self):
        season = 'S' + str(self.season_number).zfill(2)
        if self.special:
            episode = ' Special'
        else:
            episode = 'E' + str(self.episode_number).zfill(2)
        return text_type(season + episode + ' ' + self.title)

    def is_special(self):
        if self.episode_number:
            return False
        return True


class Network(object):
    def __init__(self, data):
        self.name = data.get('name')
        self.maze_id = data.get('id')
        if data.get('country'):
            self.country = data['country'].get('name')
            self.timezone = data['country'].get('timezone')
            self.code = data['country'].get('code')

    def __repr__(self):
        return '<Network(name={name},country={country})>'.format(name=self.name, country=self.country)


class Person(object):
    def __init__(self, data):
        if data.get('person'):
            data = data['person']
        self.links = data.get('_links')
        self.id = data.get('id')
        self.image = data.get('image')
        self.name = data.get('name')
        self.score = data.get('score')
        self.url = data.get('url')
        self.character = None
        self.castcredits = None
        self.crewcredits = None
        self.populate(data)

    def populate(self, data):
        if data.get('_embedded'):
            if data['_embedded'].get('castcredits'):
                self.castcredits = [CastCredit(credit)
                                    for credit in data['_embedded']['castcredits']]
            elif data['_embedded'].get('crewcredits'):
                self.crewcredits = [CrewCredit(credit)
                                    for credit in data['_embedded']['crewcredits']]

    def __repr__(self):
        return text_type('<Person(name={name},maze_id={id})>'.format(
                name=self.name,
                id=self.id
        ))

    def __str__(self):
        return text_type(self.name)


class Season(object):
    def __init__(self, data):
        self.show = None
        self.episodes = dict()
        self.id = data.get('id')
        self.url = data.get('url')
        self.season_number = data.get('number')
        self.name = data.get('name')
        self.episode_order = data.get('episodeOrder')
        self.premier_date = data.get('premierDate')
        self.end_date = data.get('endDate')
        if data.get('network'):
            self.network = Network(data.get('network'))
        else:
            self.network = None
        if data.get('webChannel'):
            self.web_channel = WebChannel(data.get('webChannel'))
        else:
            self.web_channel = None
        self.image = data.get('image')
        self.summary = data.get('summary')
        self.links = data.get('_links')

    def __repr__(self):
        return text_type('<Season(id={id},season_number={number})>'.format(
                id=self.id,
                number=str(self.season_number).zfill(2)
        ))

    def __iter__(self):
        return iter(self.episodes.values())

    def __len__(self):
        return len(self.episodes)

    def __getitem__(self, item):
        try:
            return self.episodes[item]
        except KeyError:
            raise exceptions.EpisodeNotFound(
                    'Episode {0} does not exist for season {1} of show {2}.'.format(item, self.season_number,
                                                                                    self.show))

    # Python 3 bool evaluation
    def __bool__(self):
        return bool(self.id)

    # Python 2 bool evaluation
    def __nonzero__(self):
        return bool(self.id)


class Show(object):
    def __init__(self, data, api=None):
        self.api = api or TVMazeStandard
        self.status = data.get('status')
        self.rating = data.get('rating')
        self.genres = data.get('genres')
        self.weight = data.get('weight')
        self.updated = data.get('updated')
        self.name = data.get('name')
        self.language = data.get('language')
        self.schedule = data.get('schedule')
        self.url = data.get('url')
        self.image = data.get('image')
        self.externals = data.get('externals')
        self.premiered = data.get('premiered')
        self.summary = _remove_tags(data.get('summary'))
        self.links = data.get('_links')
        if data.get('webChannel'):
            self.web_channel = WebChannel(data.get('webChannel'))
        else:
            self.web_channel = None
        self.runtime = data.get('runtime')
        self.type = data.get('type')
        self.id = data.get('id')
        self.maze_id = self.id
        if data.get('network'):
            self.network = Network(data.get('network'))
        else:
            self.network = None
        self.__episodes = list()
        self.seasons = dict()
        self.cast = None
        self.__nextepisode = None
        self.__previousepisode = None
        self.populate(data)

    def __repr__(self):
        if self.premiered:
            year = str(self.premiered[:4])
        else:
            year = None
        if self.web_channel:
            platform = ',show_web_channel='
            network = self.web_channel.name
        elif self.network:
            platform = ',network='
            network = self.network.name
        else:
            platform = ''
            network = ''

        return text_type('<Show(maze_id={id},name={name},year={year}{platform}{network})>'.format(
                id=self.maze_id,
                name=self.name,
                year=year,
                platform=platform,
                network=network)
        )

    def __str__(self):
        return text_type(self.name)

    def __unicode__(self):
        return self.name

    def __iter__(self):
        return iter(self.seasons.values())

    # Python 3 bool evaluation
    def __bool__(self):
        return bool(self.id)

    # Python 2 bool evaluation
    def __nonzero__(self):
        return bool(self.id)

    def __len__(self):
        return len(self.seasons)

    def __getitem__(self, item):
        try:
            return self.seasons[item]
        except KeyError:
            raise exceptions.SeasonNotFound('Season {0} does not exist for show {1}.'.format(item, self.name))

    @property
    def next_episode(self):
        if self.__nextepisode is None and 'nextepisode' in self.links and 'href' in self.links['nextepisode']:
            episode_id = self.links['nextepisode']['href'].rsplit('/', 1)[1]
            if episode_id.isdigit():
                self.__nextepisode = self.api.episode_by_id(episode_id)
        return self.__nextepisode

    @property
    def previous_episode(self):
        if self.__previousepisode is None and 'previousepisode' in self.links and 'href' in self.links['previousepisode']:
            episode_id = self.links['previousepisode']['href'].rsplit('/', 1)[1]
            if episode_id.isdigit():
                self.__previousepisode = self.api.episode_by_id(episode_id)
        return self.__previousepisode

    @property
    def episodes(self):
        if not self.__episodes:
            self.__episodes = self.api.episode_list(self.maze_id, specials=True)
        return self.__episodes

    def populate(self, data):
        embedded = data.get('_embedded')
        if embedded:
            if embedded.get('episodes'):
                seasons = self.api.show_seasons(self.maze_id)
                for episode in embedded.get('episodes'):
                    self.__episodes.append(Episode(episode))
                for episode in self.__episodes:
                    season_num = int(episode.season_number)
                    if season_num not in self.seasons:
                        self.seasons[season_num] = seasons[season_num]
                        self.seasons[season_num].show = self
                    self.seasons[season_num].episodes[episode.episode_number] = episode
            if embedded.get('cast'):
                self.cast = Cast(embedded.get('cast'))


class Update(object):
    def __init__(self, maze_id, time):
        self.maze_id = int(maze_id)
        self.seconds_since_epoch = time
        self.timestamp = datetime.fromtimestamp(time)

    def __repr__(self):
        return '<Update(maze_id={maze_id},time={time})>'.format(
                maze_id=self.maze_id,
                time=self.seconds_since_epoch
        )


class Updates(object):
    def __init__(self, data):
        self.updates = dict()
        self.populate(data)

    def populate(self, data):
        for maze_id, time in data.items():
            self.updates[int(maze_id)] = Update(maze_id, time)

    def __getitem__(self, item):
        try:
            return self.updates[item]
        except KeyError:
            raise exceptions.UpdateNotFound('No update found for Maze id {}.'.format(item))

    def __iter__(self):
        return iter(self.updates.values())


class WebChannel(object):
    def __init__(self, data):
        self.name = data.get('name')
        self.maze_id = data.get('id')
        if data.get('country'):
            self.country = data['country'].get('name')
            self.timezone = data['country'].get('timezone')
            self.code = data['country'].get('code')

    def __repr__(self):
        return '<WebChannel(name={name},country={country})>'.format(name=self.name, country=self.country)
