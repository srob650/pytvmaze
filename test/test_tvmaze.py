#!/usr/bin/python

import unittest
from pytvmaze.tvmaze import *
from pytvmaze.exceptions import *

class EndpointTests(unittest.TestCase):

    def test_show_search(self):
        show_list = show_search('dexter')
        self.assertIsInstance(show_list, list)
        self.assertIsInstance(show_list[0], dict)

        with self.assertRaises(ShowNotFound):
            show_search('abcdefg')

    def test_show_single_search(self):
        show1 = show_single_search('bobs burgers')
        self.assertIsInstance(show1, dict)

        show2 = show_single_search('extant', embed='episodes')
        self.assertIsInstance(show2, dict)
        self.assertIn('episodes', show2['_embedded'].keys())

        show3 = show_single_search('archer', embed='cast')
        self.assertIsInstance(show3, dict)
        self.assertIn('cast', show3['_embedded'].keys())

        with self.assertRaises(ShowNotFound):
            show_single_search('show that doesnt exist')

    def test_lookup_tvrage(self):
        show = lookup_tvrage(24493)
        self.assertIsInstance(show, dict)

        with self.assertRaises(IDNotFound):
            lookup_tvrage(9999999999)

    def test_lookup_tvdb(self):
        show = lookup_tvdb(81189)
        self.assertIsInstance(show, dict)

        with self.assertRaises(IDNotFound):
            lookup_tvdb(9999999999)

    def test_get_schedule(self):
        schedule = get_schedule()
        self.assertIsInstance(schedule, list)
        self.assertIsInstance(schedule[0], dict)

        gb_schedule = get_schedule(country='gb', date='2015-01-01')
        self.assertIsInstance(gb_schedule, list)
        self.assertIsInstance(gb_schedule[0], dict)
        self.assertEqual(gb_schedule[0]['airdate'], '2015-01-01')

        with self.assertRaises(ScheduleNotFound):
            get_schedule(country='fakecountry')

    def test_get_full_schedule(self):
        schedule = get_full_schedule()
        self.assertIsInstance(schedule, list)

    def test_show_main_info(self):
        show1 = show_main_info(1)
        self.assertIsInstance(show1, dict)

        show2 = show_main_info(2, embed='episodes')
        self.assertIsInstance(show2, dict)
        self.assertIn('episodes', show2['_embedded'].keys())

        with self.assertRaises(IDNotFound):
            show_main_info(9999999999)

    def test_episode_list(self):
        episodes = episode_list(3)
        self.assertIsInstance(episodes, list)
        self.assertIsInstance(episodes[0], Episode)

        specials = episode_list(4, specials=True)
        self.assertIsInstance(specials, list)
        self.assertIsInstance(specials[0], Episode)

        with self.assertRaises(IDNotFound):
            episode_list(9999999999)

    def test_episode_by_number(self):
        episode = episode_by_number(5,1,1)
        self.assertIsInstance(episode, Episode)

        with self.assertRaises(EpisodeNotFound):
            episode_by_number(9999999999,1,1)

    def test_episodes_by_date(self):
        episodes1 = episodes_by_date(1, '2013-07-01')
        self.assertIsInstance(episodes1, list)

        with self.assertRaises(NoEpisodesForAirdate):
            episodes_by_date(1, '1999-01-01')

    def test_show_cast(self):
        cast = show_cast(6)
        self.assertIsInstance(cast, list)
        self.assertIsInstance(cast[0], dict)

        with self.assertRaises(CastNotFound):
            show_cast(9999999999)

    def test_show_index(self):
        index = show_index()
        self.assertIsInstance(index, list)
        self.assertIsInstance(index[0], dict)

        with self.assertRaises(ShowIndexError):
            show_index(page=9999999999)

    def test_people_search(self):
        people = people_search('jennifer carpenter')
        self.assertIsInstance(people, list)
        self.assertIsInstance(people[0], dict)

        with self.assertRaises(PersonNotFound):
            people_search('person who does not exist')

    def test_person_main_info(self):
        person1 = person_main_info(1)
        self.assertIsInstance(person1, dict)

        person2 = person_main_info(2, embed='castcredits')
        self.assertIsInstance(person2, dict)
        self.assertIn('castcredits', person2['_embedded'].keys())

        with self.assertRaises(PersonNotFound):
            person_main_info(9999999999)

    def test_person_cast_credits(self):
        credits1 = person_cast_credits(6)
        self.assertIsInstance(credits1, list)

        credits2 = person_cast_credits(7, embed='show')
        self.assertIsInstance(credits2, list)
        self.assertIn('show', credits2[0]['_embedded'])

        with self.assertRaises(CreditsNotFound):
            person_cast_credits(9999999999)

    def test_person_crew_credits(self):
        credits1 = person_crew_credits(100)
        self.assertIsInstance(credits1, list)

        credits2 = person_crew_credits(100, embed='show')
        self.assertIsInstance(credits2, list)
        self.assertIn('show', credits2[0]['_embedded'])

        with self.assertRaises(CreditsNotFound):
            person_crew_credits(9999999999)

    def test_show_updates(self):
        updates = show_updates()
        self.assertIsInstance(updates, dict)

    def test_show_akas(self):
        akas = show_akas(1)
        self.assertIsInstance(akas, list)
        self.assertIsInstance(akas[0], dict)


class ObjectTests(unittest.TestCase):

    def test_get_show(self):
        show1 = get_show(maze_id=163, embed='episodes')
        self.assertIsInstance(show1, Show)
        self.assertTrue(hasattr(show1, 'episodes'))
        with self.assertRaises(SeasonNotFound):
            show1[999]
        with self.assertRaises(EpisodeNotFound):
            show1[1][999]

        show2 = get_show(tvdb_id=81189, embed='episodes')
        self.assertIsInstance(show2, Show)
        self.assertTrue(hasattr(show2, 'episodes'))

        show3 = get_show(tvrage_id=24493, embed='episodes')
        self.assertIsInstance(show3, Show)
        self.assertTrue(hasattr(show3, 'episodes'))

        show4 = get_show(show_name='person of interest', embed='episodes')
        self.assertIsInstance(show4, Show)
        self.assertTrue(hasattr(show4, 'episodes'))

        show5 = get_show(show_name='utopia', show_country='au', show_network='abc', embed='episodes')
        self.assertIsInstance(show5, Show)
        self.assertTrue(hasattr(show5, 'episodes'))
        self.assertTrue(show5.network['country']['code'] == 'AU')
        self.assertTrue(show5.network['name'] == 'ABC')

        show6 = get_show(show_name='the flash', show_year='1967', embed='episodes')
        self.assertIsInstance(show6, Show)
        self.assertTrue(hasattr(show6, 'episodes'))
        self.assertTrue(show6.premiered == '1967-11-11')

        show7 = get_show(show_name='drunk history', show_language='english', embed='episodes')
        self.assertIsInstance(show7, Show)
        self.assertTrue(hasattr(show7, 'episodes'))
        self.assertTrue(show7.language == 'English')

        show8 = get_show(show_name='jessica jones', show_web_channel='netflix', embed='episodes')
        self.assertIsInstance(show8, Show)
        self.assertTrue(hasattr(show8, 'episodes'))
        self.assertTrue(show8.language == 'English')
        self.assertTrue(show8.webChannel['name'] == 'Netflix')

        with self.assertRaises(MissingParameters):
            empty_search = get_show()


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
        show = get_show(maze_id=161, embed='cast')
        self.assertIsInstance(show.cast[0], Person)
        self.assertIsInstance(show.characters[0], Character)
