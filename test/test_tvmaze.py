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

    def test_lookup_tvrage(self):
        show = lookup_tvrage(24493)
        self.assertIsInstance(show, dict)
        with self.assertRaises(IDNotFound):
            show = lookup_tvrage(9999999999)

    def test_lookup_tvdb(self):
        show = lookup_tvdb(81189)
        self.assertIsInstance(show, dict)
        with self.assertRaises(IDNotFound):
            show = lookup_tvdb(9999999999)

    def test_get_schedule(self):
        schedule = get_schedule()
        self.assertIsInstance(schedule, list)
        self.assertIsInstance(schedule[0], dict)

        gb_schedule = get_schedule(country='gb', date='2015-01-01')
        self.assertIsInstance(gb_schedule, list)
        self.assertIsInstance(gb_schedule[0], dict)
        self.assertEqual(gb_schedule[0]['airdate'], '2015-01-01')

        with self.assertRaises(ScheduleNotFound):
            bad_schedule = get_schedule(country='fakecountry')

    # def test_get_full_schedule(self):
    #     schedule = get_full_schedule()
    #     self.assertIsInstance(schedule, list)

    def test_show_main_info(self):
        show1 = show_main_info(1)
        self.assertIsInstance(show1, dict)

        show2 = show_main_info(2, embed='episodes')
        self.assertIsInstance(show2, dict)
        self.assertIn('episodes', show2['_embedded'].keys())

        with self.assertRaises(IDNotFound):
            show3 = show_main_info(9999999999)

    def test_episode_list(self):
        episodes = episode_list(3)
        self.assertIsInstance(episodes, list)
        self.assertIsInstance(episodes[0], dict)

        specials = episode_list(4, specials=True)
        self.assertIsInstance(specials, list)
        self.assertIsInstance(specials[0], dict)

        with self.assertRaises(IDNotFound):
            bad_episodes = episode_list(9999999999)

    def test_episode_by_number(self):
        episode = episode_by_number(5,1,1)
        self.assertIsInstance(episode, dict)

        with self.assertRaises(EpisodeNotFound):
            bad_episode = episode_by_number(9999999999,1,1)
