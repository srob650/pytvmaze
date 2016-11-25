#!/usr/bin/python
# coding=utf-8

# TVMaze Free endpoints

from requests.compat import urljoin

base_url = 'http://api.tvmaze.com'

episode_by_id = urljoin(base_url, '/episodes/{0}')
lookup = urljoin(base_url, '/lookup/shows')
person_main_info = urljoin(base_url, '/people/{0}')
person_cast_credits = urljoin(base_url, '/people/{0}/castcredits')
person_crew_credits = urljoin(base_url, '/people/{0}/crewcredits')
get_schedule = urljoin(base_url, '/schedule')
get_full_schedule = urljoin(base_url, '/schedule/full')
show_search = urljoin(base_url, '/search/shows')
people_search = urljoin(base_url, '/search/people')
season_by_id = urljoin(base_url, '/seasons/{0}')
show_single_search = urljoin(base_url, '/singlesearch/shows')
show_index = urljoin(base_url, '/shows')
show_main_info = urljoin(base_url, '/shows/{0}')
show_akas = urljoin(base_url, '/shows/{0}/akas')
show_cast = urljoin(base_url, '/shows/{0}/cast')
show_crew = urljoin(base_url, '/shows/{0}/crew')
episode_by_number = urljoin(base_url, '/shows/{0}/episodebynumber')
episode_list = urljoin(base_url, '/shows/{0}/episodes')
episodes_by_date = urljoin(base_url, '/shows/{0}/episodesbydate')
show_seasons = urljoin(base_url, '/shows/{0}/seasons')
show_updates = urljoin(base_url, '/updates/shows')

# TVMaze Premium endpoints
marked_episodes = urljoin(base_url, '/v1/user/episodes{0}')
followed_networks = urljoin(base_url, '/v1/user/follows/networks{0}')
followed_people = urljoin(base_url, '/v1/user/follows/people{0}')
followed_shows = urljoin(base_url, '/v1/user/follows/shows{0}')
followed_web_channels = urljoin(base_url, '/v1/user/follows/webchannels{0}')
voted_shows = urljoin(base_url, '/v1/user/votes/shows{0}')
voted_episodes = urljoin(base_url, '/v1/user/votes/episodes{0}')
