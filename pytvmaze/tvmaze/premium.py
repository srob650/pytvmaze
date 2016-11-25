# coding=utf-8
from pytvmaze.tvmaze.api import (
    TVMazeStandard,
    Network,
    Person,
    Show,
    WebChannel,
)
from pytvmaze import exceptions, endpoints


class TVMazePremium(TVMazeStandard):
    def __init__(self, username=None, api_key=None):
        self.username = username or self.username
        self.api_key = api_key or self.api_key

    @classmethod
    def authorized_request(cls, *args, **kwargs):
        # make sure we have a session
        if not cls.session:
            cls.session = cls.make_session()
        if not cls.session.auth:
            # add authentication to the session if it exists
            if cls.username and cls.api_key:
                cls.session.auth = cls.username, cls.api_key
            else:
                raise exceptions.NotAuthorized
        return cls.request(*args, **kwargs)

    # Query TVMaze Premium endpoints
    @classmethod
    def _endpoint_premium_get(cls, url, *args, **kwargs):
        response = cls.authorized_request(url=url, *args, **kwargs)
        return response.json() if response else None

    @classmethod
    def _endpoint_premium_delete(cls, url, *args, **kwargs):
        kwargs.setdefault('method', 'DELETE')
        response = cls.authorized_request(url=url, *args, **kwargs)
        return response.json() if response else None

    @classmethod
    def _endpoint_premium_put(cls, url, payload=None, *args, **kwargs):
        kwargs.setdefault('method', 'PUT')
        kwargs.setdefault('data', payload)
        response = cls.authorized_request(url=url, *args, **kwargs)
        return response.json() if response else None

    # TVMaze Premium Endpoints
    # NOT DONE OR TESTED

    # Follow / Unfollow items
    def follow_network(self, network_id):
        url = endpoints.followed_networks.format('/' + str(network_id))
        q = self._endpoint_premium_put(url)
        if not q:
            raise exceptions.NetworkNotFound('Network with ID {} does not exist'.format(network_id))

    def follow_person(self, person_id):
        url = endpoints.followed_people.format('/' + str(person_id))
        q = self._endpoint_premium_put(url)
        if not q:
            raise exceptions.PersonNotFound('Person with ID {} does not exist'.format(person_id))

    def follow_show(self, maze_id):
        url = endpoints.followed_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_put(url)
        if not q:
            raise exceptions.ShowNotFound('Show with ID {} does not exist'.format(maze_id))

    def follow_web_channel(self, webchannel_id):
        url = endpoints.followed_web_channels.format('/' + str(webchannel_id))
        q = self._endpoint_premium_put(url)
        if not q:
            raise exceptions.WebChannelNotFound('Web Channel with ID {} does not exist'.format(webchannel_id))

    def get_followed_people(self, embed=None):
        if embed not in [None, 'person']:
            raise exceptions.InvalidEmbedValue('Value for embed must be "person" or None')
        url = endpoints.followed_people.format('/')
        if embed == 'person':
            url = endpoints.followed_people.format('?embed=person')
        q = self._endpoint_premium_get(url)
        if q:
            return [FollowedPerson(person) for person in q]
        else:
            raise exceptions.NoFollowedPeople('You have not followed any people yet')

    def get_followed_person(self, person_id):
        url = endpoints.followed_people.format('/' + str(person_id))
        q = self._endpoint_premium_get(url)
        if q:
            return FollowedPerson(q)
        else:
            raise exceptions.PersonNotFound('Person with ID {} is not followed'.format(person_id))

    def get_followed_network(self, network_id):
        url = endpoints.followed_networks.format('/' + str(network_id))
        q = self._endpoint_premium_get(url)
        if q:
            return FollowedNetwork(q)
        else:
            raise exceptions.NetworkNotFound('Network with ID {} is not followed'.format(network_id))

    def get_followed_networks(self, embed=None):
        if embed not in [None, 'network']:
            raise exceptions.InvalidEmbedValue('Value for embed must be "network" or None')
        url = endpoints.followed_networks.format('/')
        if embed == 'network':
            url = endpoints.followed_networks.format('?embed=network')
        q = self._endpoint_premium_get(url)
        if q:
            return [FollowedNetwork(network) for network in q]
        else:
            raise exceptions.NoFollowedNetworks('You have not followed any networks yet')

    def get_followed_show(self, maze_id):
        url = endpoints.followed_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_get(url)
        if q:
            return FollowedShow(q)
        else:
            raise exceptions.ShowNotFollowed('Show with ID {} is not followed'.format(maze_id))

    def get_followed_shows(self, embed=None):
        if embed not in [None, 'show']:
            raise exceptions.InvalidEmbedValue('Value for embed must be "show" or None')
        url = endpoints.followed_shows.format('/')
        if embed == 'show':
            url = endpoints.followed_shows.format('?embed=show')
        q = self._endpoint_premium_get(url)
        if q:
            return [FollowedShow(show) for show in q]
        else:
            raise exceptions.NoFollowedShows('You have not followed any shows yet')

    def get_followed_web_channel(self, webchannel_id):
        url = endpoints.followed_web_channels.format('/' + str(webchannel_id))
        q = self._endpoint_premium_get(url)
        if q:
            return FollowedWebChannel(q)
        else:
            raise exceptions.NetworkNotFound('Web Channel with ID {} is not followed'.format(webchannel_id))

    def get_followed_web_channels(self, embed=None):
        if embed not in [None, 'webchannel']:
            raise exceptions.InvalidEmbedValue('Value for embed must be "webchannel" or None')
        url = endpoints.followed_web_channels.format('/')
        if embed == 'webchannel':
            url = endpoints.followed_web_channels.format('?embed=webchannel')
        q = self._endpoint_premium_get(url)
        if q:
            return [FollowedWebChannel(webchannel) for webchannel in q]
        else:
            raise exceptions.NoFollowedWebChannels('You have not followed any Web Channels yet')

    def unfollow_network(self, network_id):
        url = endpoints.followed_networks.format('/' + str(network_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise exceptions.NetworkNotFollowed('Network with ID {} was not followed'.format(network_id))

    def unfollow_person(self, person_id):
        url = endpoints.followed_people.format('/' + str(person_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise exceptions.PersonNotFollowed('Person with ID {} was not followed'.format(person_id))

    def unfollow_show(self, maze_id):
        url = endpoints.followed_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise exceptions.ShowNotFollowed('Show with ID {} was not followed'.format(maze_id))

    def unfollow_web_channel(self, webchannel_id):
        url = endpoints.followed_web_channels.format('/' + str(webchannel_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise exceptions.WebChannelNotFollowed('Web Channel with ID {} was not followed'.format(webchannel_id))

    # Mark / Unmark items
    def get_marked_episode(self, episode_id):
        path = '/{}'.format(episode_id)
        url = endpoints.marked_episodes.format(path)
        q = self._endpoint_premium_get(url)
        if q:
            return MarkedEpisode(q)
        else:
            raise exceptions.EpisodeNotMarked('Episode with ID {} is not marked'.format(episode_id))

    def get_marked_episodes(self, maze_id=None):
        if not maze_id:
            url = endpoints.marked_episodes.format('/')
        else:
            show_id = '?show_id={}'.format(maze_id)
            url = endpoints.marked_episodes.format(show_id)
        q = self._endpoint_premium_get(url)
        if q:
            return [MarkedEpisode(episode) for episode in q]
        else:
            raise exceptions.NoMarkedEpisodes('You have not marked any episodes yet')

    def mark_episode(self, episode_id, mark_type):
        types = {'watched': 0, 'acquired': 1, 'skipped': 2}
        try:
            status = types[mark_type]
        except IndexError:
            raise exceptions.InvalidMarkedEpisodeType('Episode must be marked as "watched", "acquired", or "skipped"')
        payload = {'type': str(status)}
        path = '/{}'.format(episode_id)
        url = endpoints.marked_episodes.format(path)
        q = self._endpoint_premium_put(url, payload=payload)
        if not q:
            raise exceptions.EpisodeNotFound('Episode with ID {} does not exist'.format(episode_id))

    def unmark_episode(self, episode_id):
        path = '/{}'.format(episode_id)
        url = endpoints.marked_episodes.format(path)
        q = self._endpoint_premium_delete(url)
        if not q:
            raise exceptions.EpisodeNotMarked('Episode with ID {} was not marked'.format(episode_id))

    # Vote / Unvote items
    def remove_episode_vote(self, episode_id):
        path = '/{}'.format(episode_id)
        url = endpoints.voted_episodes.format(path)
        q = self._endpoint_premium_delete(url)
        if not q:
            raise exceptions.EpisodeNotVotedFor('Episode with ID {} was not voted for'.format(episode_id))

    def remove_show_vote(self, maze_id):
        url = endpoints.voted_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_delete(url)
        if not q:
            raise exceptions.ShowNotVotedFor('Show with ID {} was not voted for'.format(maze_id))

    def get_voted_episode(self, episode_id):
        path = '/{}'.format(episode_id)
        url = endpoints.voted_episodes.format(path)
        q = self._endpoint_premium_get(url)
        if q:
            return VotedEpisode(q)
        else:
            raise exceptions.EpisodeNotVotedFor('Episode with ID {} not voted for'.format(episode_id))

    def get_voted_episodes(self):
        url = endpoints.voted_episodes.format('/')
        q = self._endpoint_premium_get(url)
        if q:
            return [VotedEpisode(episode) for episode in q]
        else:
            raise exceptions.NoVotedEpisodes('You have not voted for any episodes yet')

    def get_voted_show(self, maze_id):
        url = endpoints.voted_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_get(url)
        if q:
            return VotedShow(q)
        else:
            raise exceptions.ShowNotVotedFor('Show with ID {} not voted for'.format(maze_id))

    def get_voted_shows(self, embed=None):
        if embed not in [None, 'show']:
            raise exceptions.InvalidEmbedValue('Value for embed must be "show" or None')
        url = endpoints.voted_shows.format('/')
        if embed == 'show':
            url = endpoints.voted_shows.format('?embed=show')
        q = self._endpoint_premium_get(url)
        if q:
            return [VotedShow(show) for show in q]
        else:
            raise exceptions.NoVotedShows('You have not voted for any shows yet')

    def vote_episode(self, episode_id, vote):
        if not 1 <= vote <= 10:
            raise exceptions.InvalidVoteValue('Vote must be an integer between 1 and 10')
        payload = {'vote': int(vote)}
        path = '/{}'.format(episode_id)
        url = endpoints.voted_episodes.format(path)
        q = self._endpoint_premium_put(url, payload=payload)
        if not q:
            raise exceptions.EpisodeNotFound('Episode with ID {} does not exist'.format(episode_id))

    def vote_show(self, maze_id, vote):
        if not 1 <= vote <= 10:
            raise exceptions.InvalidVoteValue('Vote must be an integer between 1 and 10')
        payload = {'vote': int(vote)}
        url = endpoints.voted_shows.format('/' + str(maze_id))
        q = self._endpoint_premium_put(url, payload=payload)
        if not q:
            raise exceptions.ShowNotFound('Show with ID {} does not exist'.format(maze_id))
