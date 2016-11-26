from __future__ import unicode_literals

from .api import Show, Person, Network, WebChannel


class Followed(object):
    def __init__(self, data):
        self._embedded = data.get('_embedded')


class FollowedShow(object):
    def __init__(self, data):
        self.maze_id = data.get('show_id')
        self.show = None
        if data.get('_embedded'):
            self.show = Show(data['_embedded'].get('show'))

    def __repr__(self):
        return '<{cls}(maze_id={id})>'.format(
            cls=self.__class__.__name__,
            id=self.maze_id,
        )


class FollowedPerson(object):
    def __init__(self, data):
        self.person_id = data.get('person_id')
        self.person = None
        if data.get('_embedded'):
            self.person = Person(data['_embedded'].get('person'))

    def __repr__(self):
        return '<{cls}(person_id={id})>'.format(
            cls=self.__class__.__name__,
            id=self.person_id,
        )


class FollowedNetwork(object):
    def __init__(self, data):
        self.network_id = data.get('network_id')
        self.network = None
        if data.get('_embedded'):
            self.network = Network(data['_embedded'].get('network'))

    def __repr__(self):
        return '<{cls}(network_id={id})>'.format(
            cls=self.__class__.__name__,
            id=self.network_id,
        )


class FollowedWebChannel(object):
    def __init__(self, data):
        self.web_channel_id = data.get('webchannel_id')
        self.web_channel = None
        if data.get('_embedded'):
            self.web_channel = WebChannel(data['_embedded'].get('webchannel'))

    def __repr__(self):
        return '<{cls}(web_channel_id={id})>'.format(
            cls=self.__class__.__name__,
            id=self.web_channel_id,
        )
