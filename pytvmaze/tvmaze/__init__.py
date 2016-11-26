# coding=utf-8
from .api import (
    TVMazeStandard,
    AKA,
    Cast,
    CastCredit,
    Character,
    Crew,
    CrewCredit,
    Episode,
    Network,
    Person,
    Season,
    Show,
    Update,
    Updates,
    WebChannel,
)
from .premium import (
    TVMazePremium,
    FollowedNetwork,
    FollowedPerson,
    FollowedShow,
    FollowedWebChannel,
    MarkedEpisode,
    VotedEpisode,
    VotedShow,
)

TVMaze = TVMazePremium


def episode_by_id(episode_id):
    return TVMaze.episode_by_id(episode_id)


def episode_by_number(maze_id, season_number, episode_number):
    return TVMaze.episode_by_number(maze_id, season_number, episode_number)


def episode_list(maze_id, specials=None):
    return TVMaze.episode_list(maze_id, specials)


def episodes_by_date(maze_id, airdate):
    return TVMaze.episodes_by_date(maze_id, airdate)


# ALL known future episodes, several MB large, cached for 24 hours
def get_full_schedule():
    return TVMaze.get_full_schedule()


# Get list of Person objects
def get_people(name):
    return TVMaze.get_people(name)


def get_schedule(country=None, date=None):
    return TVMaze.get_schedule(country, date)


def get_show_crew(maze_id):
    return TVMaze.get_show_crew(maze_id)


# Return list of Show objects
def get_show_list(show_name):
    return TVMaze.get_show_list(show_name)


def lookup_imdb(imdb_id):
    return TVMaze.lookup_imdb(imdb_id)


def lookup_tvdb(tvdb_id):
    return TVMaze.lookup_tvdb(tvdb_id)


def lookup_tvrage(tvrage_id):
    return TVMaze.lookup_tvrage(tvrage_id)


def person_cast_credits(person_id, embed=None):
    return TVMaze.person_cast_credits(person_id, embed)


def person_crew_credits(person_id, embed=None):
    return TVMaze.person_crew_credits(person_id, embed)


def person_main_info(person_id, embed=None):
    return TVMaze.person_main_info(person_id, embed)


def people_search(person):
    return TVMaze.people_search(person)


def season_by_id(season_id):
    return TVMaze.season_by_id(season_id)


def show_akas(maze_id):
    return TVMaze.show_akas(maze_id)


def show_cast(maze_id):
    return TVMaze.show_cast(maze_id)


def show_index(page=0):
    return TVMaze.show_index(page)


def show_main_info(maze_id, embed=None):
    return TVMaze.show_main_info(maze_id, embed)


def show_search(show):
    return TVMaze.show_search(show)


def show_seasons(maze_id):
    return TVMaze.show_seasons(maze_id)


def show_single_search(show, embed=None):
    return TVMaze.show_single_search(show, embed)


def show_updates():
    return TVMaze.show_updates()
