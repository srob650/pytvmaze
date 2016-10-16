#!/usr/bin/python
 # -*- coding: utf-8 -*-

import unittest
import datetime
import sys

from pytvmaze.tvmaze import *


class EndpointTests(unittest.TestCase):
    def test_show_search(self):
        show_list = show_search('dexter')
        self.assertIsInstance(show_list, list)
        self.assertIsInstance(show_list[0], Show)

        with self.assertRaises(ShowNotFound):
            show_search('abcdefg')

    def test_show_single_search(self):
        show1 = show_single_search(show='bobs burgers')
        self.assertIsInstance(show1, Show)

        show2 = show_single_search(show='extant', embed='episodes')
        self.assertIsInstance(show2, Show)
        self.assertTrue(show2.episodes)

        show3 = show_single_search(show='archer', embed='cast')
        self.assertIsInstance(show3, Show)
        self.assertTrue(show3.cast)

        with self.assertRaises(ShowNotFound):
            show_single_search('show that doesnt exist')

    def test_lookup_tvrage(self):
        show = lookup_tvrage(24493)
        self.assertIsInstance(show, Show)

        with self.assertRaises(IDNotFound):
            lookup_tvrage(9999999999)

    def test_lookup_tvdb(self):
        show = lookup_tvdb(81189)
        self.assertIsInstance(show, Show)

        with self.assertRaises(IDNotFound):
            lookup_tvdb(9999999999)

    def test_get_schedule(self):
        schedule = get_schedule()
        self.assertIsInstance(schedule, list)
        self.assertIsInstance(schedule[0], Episode)
        self.assertIsInstance(schedule[0].show, Show)

        gb_schedule = get_schedule(country='gb', date='2015-01-01')
        self.assertIsInstance(gb_schedule, list)
        self.assertIsInstance(gb_schedule[0], Episode)
        self.assertEqual(gb_schedule[0].airdate, '2015-01-01')

        with self.assertRaises(ScheduleNotFound):
            get_schedule(country='fakecountry')

    def test_get_full_schedule(self):
        schedule = get_full_schedule()
        self.assertIsInstance(schedule, list)
        self.assertIsInstance(schedule[0], Episode)
        self.assertIsInstance(schedule[0].show, Show)

    def test_show_main_info(self):
        show1 = show_main_info(maze_id=1)
        self.assertIsInstance(show1, Show)

        show2 = show_main_info(maze_id=2, embed='episodes')
        self.assertIsInstance(show2, Show)
        self.assertTrue(show2.episodes)

        with self.assertRaises(IDNotFound):
            show_main_info(9999999999)

    def test_episode_list(self):
        episodes = episode_list(3)
        self.assertIsInstance(episodes, list)
        self.assertIsInstance(episodes[0], Episode)

        specials = episode_list(4, specials=True)
        self.assertIsInstance(specials, list)
        self.assertIsInstance(specials[0], Episode)
        self.assertTrue(specials[0].special, True)

        with self.assertRaises(IDNotFound):
            episode_list(9999999999)

    def test_episode_by_number(self):
        episode = episode_by_number(5, 1, 1)
        self.assertIsInstance(episode, Episode)

        with self.assertRaises(EpisodeNotFound):
            episode_by_number(9999999999, 1, 1)

    def test_episodes_by_date(self):
        episodes1 = episodes_by_date(1, '2013-07-01')
        self.assertIsInstance(episodes1, list)

        with self.assertRaises(NoEpisodesForAirdate):
            episodes_by_date(1, '1999-01-01')

    def test_show_cast(self):
        cast = show_cast(6)
        self.assertIsInstance(cast, Cast)
        self.assertIsInstance(cast.people[0], Person)
        self.assertIsInstance(cast.characters[0], Character)

        with self.assertRaises(CastNotFound):
            show_cast(9999999999)

    def test_show_crew(self):
        crew = get_show_crew(161)
        self.assertIsInstance(crew[0], Crew)
        self.assertIsInstance(crew[0].person, Person)

    def test_show_index(self):
        index = show_index()
        self.assertIsInstance(index, list)
        self.assertIsInstance(index[0], Show)

        with self.assertRaises(ShowIndexError):
            show_index(page=9999999999)

    def test_people_search(self):
        people = people_search('jennifer carpenter')
        self.assertIsInstance(people, list)
        self.assertIsInstance(people[0], Person)

        with self.assertRaises(PersonNotFound):
            people_search('person who does not exist')

    def test_person_main_info(self):
        person1 = person_main_info(100, embed='crewcredits')
        self.assertIsInstance(person1, Person)
        self.assertIsInstance(person1.crewcredits, list)
        self.assertIsInstance(person1.crewcredits[0], CrewCredit)

        person2 = person_main_info(2, embed='castcredits')
        self.assertIsInstance(person2, Person)
        self.assertIsInstance(person2.castcredits, list)
        self.assertIsInstance(person2.castcredits[0], CastCredit)

        with self.assertRaises(PersonNotFound):
            person_main_info(9999999999)

    def test_person_cast_credits(self):
        credits1 = person_cast_credits(6, embed='character')
        self.assertIsInstance(credits1, list)
        self.assertIsInstance(credits1[0], CastCredit)
        self.assertIsInstance(credits1[0].character, Character)
        self.assertIsInstance(credits1[0].links, dict)

        credits2 = person_cast_credits(7, embed='show')
        self.assertIsInstance(credits2, list)
        self.assertIsInstance(credits2[0], CastCredit)
        self.assertIsInstance(credits2[0].show, Show)
        self.assertIsInstance(credits2[0].links, dict)

        with self.assertRaises(CreditsNotFound):
            person_cast_credits(9999999999)

    def test_person_crew_credits(self):
        credits1 = person_crew_credits(100)
        self.assertIsInstance(credits1, list)
        self.assertIsInstance(credits1[0], CrewCredit)
        self.assertIsInstance(credits1[0].links, dict)

        credits2 = person_crew_credits(100, embed='show')
        self.assertIsInstance(credits2, list)
        self.assertIsInstance(credits2[0], CrewCredit)
        self.assertIsInstance(credits2[0].show, Show)
        self.assertIsInstance(credits2[0].links, dict)

        with self.assertRaises(CreditsNotFound):
            person_crew_credits(9999999999)

    def test_show_updates(self):
        updates = show_updates()
        self.assertIsInstance(updates, Updates)
        self.assertIsInstance(updates[1], Update)
        self.assertIsInstance(updates[1].timestamp, datetime)

    def test_show_akas(self):
        akas = show_akas(1)
        self.assertIsInstance(akas, list)
        self.assertIsInstance(akas[0], AKA)

    def test_show_seasons(self):
        seasons = show_seasons(1)
        self.assertIsInstance(seasons, dict)
        self.assertIsInstance(seasons[1], Season)

    def test_season_by_id(self):
        season = season_by_id(1)
        self.assertIsInstance(season, Season)

    def test_episode_by_id(self):
        episode = episode_by_id(1)
        self.assertIsInstance(episode, Episode)


class ObjectTests(unittest.TestCase):
    def test_get_show(self):
        tvm = TVMaze()
        show1 = tvm.get_show(maze_id=163, embed='episodes')
        self.assertIsInstance(show1, Show)
        self.assertTrue(hasattr(show1, 'episodes'))
        with self.assertRaises(SeasonNotFound):
            show1[999]
        with self.assertRaises(EpisodeNotFound):
            show1[1][999]

        show2 = tvm.get_show(tvdb_id=81189, embed='episodes')
        self.assertIsInstance(show2, Show)
        self.assertTrue(hasattr(show2, 'episodes'))

        show3 = tvm.get_show(tvrage_id=24493, embed='episodes')
        self.assertIsInstance(show3, Show)
        self.assertTrue(hasattr(show3, 'episodes'))

        show31 = tvm.get_show(imdb_id='tt3107288', embed='episodes')
        self.assertIsInstance(show31, Show)
        self.assertTrue(hasattr(show31, 'episodes'))

        show4 = tvm.get_show(show_name='person of interest', embed='episodes')
        self.assertIsInstance(show4, Show)
        self.assertTrue(hasattr(show4, 'episodes'))

        show5 = tvm.get_show(show_name='utopia', show_country='au', show_network='abc', embed='episodes')
        self.assertIsInstance(show5, Show)
        self.assertTrue(hasattr(show5, 'episodes'))
        self.assertTrue(show5.network.code == 'AU')
        self.assertTrue(show5.network.name == 'ABC')
        self.assertIsInstance(show5.network, Network)

        show6 = tvm.get_show(show_name='the flash', show_year='1967', embed='episodes')
        self.assertIsInstance(show6, Show)
        self.assertTrue(hasattr(show6, 'episodes'))
        self.assertTrue(show6.premiered == '1967-11-11')

        show7 = tvm.get_show(show_name='drunk history', show_language='english', embed='episodes')
        self.assertIsInstance(show7, Show)
        self.assertTrue(hasattr(show7, 'episodes'))
        self.assertTrue(show7.language == 'English')

        show8 = tvm.get_show(show_name='jessica jones', show_web_channel='netflix', embed='episodes')
        self.assertIsInstance(show8, Show)
        self.assertTrue(hasattr(show8, 'episodes'))
        self.assertTrue(show8.language == 'English')
        self.assertTrue(show8.web_channel.name == 'Netflix')
        self.assertIsInstance(show8.web_channel, WebChannel)

        # Test lookup with bad ID but good name
        show9 = tvm.get_show(maze_id=999999999, tvdb_id=999999999, tvrage_id=999999999, show_name='lost')
        self.assertIsInstance(show9, Show)

        # Test foreign language
        if sys.version_info[0] == 3:
            show10 = tvm.get_show(maze_id=8103, embed='cast')
            self.assertTrue(show10.cast.people[1].name, '黃心娣')

        with self.assertRaises(MissingParameters):
            empty_search = tvm.get_show()

    def test_get_show_list(self):
        shows = get_show_list('utopia')
        self.assertIsInstance(shows, list)
        self.assertIsInstance(shows[0], Show)

        with self.assertRaises(ShowNotFound):
            get_show_list('show that doesnt exist')

    def test_get_people(self):
        people = get_people('jennifer')
        self.assertIsInstance(people, list)
        self.assertIsInstance(people[0], Person)

        with self.assertRaises(PersonNotFound):
            get_people('person that doesnt exist')

    def test_cast_embed(self):
        tvm = TVMaze()
        show = tvm.get_show(maze_id=161, embed='cast')
        self.assertIsInstance(show.cast.people[0], Person)
        self.assertIsInstance(show.cast.characters[0], Character)
        self.assertIsInstance(show.cast.characters[0].person, Person)
        self.assertIsInstance(show.cast.people[0].character, Character)

    def test_unicode_shows(self):
        tvm = TVMaze()
        show1 = tvm.get_show(show_name=u'Unit\xe9 9')
        self.assertTrue(show1.id == 8652)
        self.assertTrue(show1.network.name == u'ICI Radio-Canada T\u00e9l\u00e9')


class ExceptionsTests(unittest.TestCase):
    def test_InvalidEmbedValue_exception(self):
        tvm = TVMaze()
        with self.assertRaises(InvalidEmbedValue):
            result = tvm.get_show(maze_id=13, embed='sdfgsdfgs')

    def test_MissingParameters_exception(self):
        tvm = TVMaze()
        with self.assertRaises(MissingParameters):
            result = tvm.get_show()

    def test_ShowNotFound1_exception(self):
        with self.assertRaises(ShowNotFound):
            result = show_search('sdfgsdfgsdfg4t4w3dfg')

    def test_ShowNotFound2_exception(self):
        with self.assertRaises(ShowNotFound):
            result = show_single_search('sdfgsdfgsdfg4t4w3dfg')

    def test_IDNotFound1_exception(self):
        with self.assertRaises(IDNotFound):
            result = lookup_tvdb(999999999)

    def test_IDNotFound2_exception(self):
        with self.assertRaises(IDNotFound):
            result = lookup_tvrage(999999999)

    def test_IDNotFound3_exception(self):
        with self.assertRaises(IDNotFound):
            result = show_main_info(maze_id=4563456354)

    def test_IDNotFound4_exception(self):
        with self.assertRaises(IDNotFound):
            result = episode_list(maze_id=4563456354)

    def test_ScheduleNotFound1_exception(self):
        with self.assertRaises(ScheduleNotFound):
            result = get_schedule(country='fdsfgf')

    def test_ScheduleNotFound2_exception(self):
        with self.assertRaises(ScheduleNotFound):
            result = get_schedule(date=(datetime(1900, 1, 1)))

    def test_EpisodeNotFound_exception(self):
        with self.assertRaises(EpisodeNotFound):
            result = episode_by_number(maze_id=4563456354, season_number=1, episode_number=2)

    def test_NoEpisodesForAirdate_exception(self):
        with self.assertRaises(NoEpisodesForAirdate):
            result = episodes_by_date(maze_id=4563456354, airdate='2015-01-01')

    def test_IllegalAirDate_exception(self):
        with self.assertRaises(IllegalAirDate):
            result = episodes_by_date(maze_id=4563456354, airdate='dfdfdf')

    def test_CastNotFound_exception(self):
        with self.assertRaises(CastNotFound):
            result = show_cast(maze_id=4563456354)

    def test_PersonNotFound1_exception(self):
        with self.assertRaises(PersonNotFound):
            result = people_search('345345')

    def test_PersonNotFound2_exception(self):
        with self.assertRaises(PersonNotFound):
            result = person_main_info(person_id=5634563456)

    def test_CreditsNotFound1_exception(self):
        with self.assertRaises(CreditsNotFound):
            result = person_cast_credits(person_id=5634563456)

    def test_CreditsNotFound2_exception(self):
        with self.assertRaises(CreditsNotFound):
            result = person_crew_credits(person_id=5634563456)

    def test_AKASNotFound_exception(self):
        with self.assertRaises(AKASNotFound):
            result = show_akas(maze_id=5634563456)
