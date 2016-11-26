from __future__ import unicode_literals
from .api import Show


class VotedShow(object):
    def __init__(self, data):
        self.maze_id = data.get('show_id')
        self.voted_at = data.get('voted_at')
        self.vote = data.get('vote')
        if data.get('_embedded'):
            self.show = Show(data['_embedded'].get('show'))

    def __repr__(self):
        return '<{cls}(maze_id={id},voted_at={voted_at},vote={vote})>'.format(
            cls=self.__class__.__name__,
            id=self.maze_id,
            voted_at=self.voted_at,
            vote=self.vote,
        )


class VotedEpisode(object):
    def __init__(self, data):
        self.episode_id = data.get('episode_id')
        self.voted_at = data.get('voted_at')
        self.vote = data.get('vote')

    def __repr__(self):
        return '<{cls}(episode_id={id},voted_at={voted_at},vote={vote})>'.format(
            cls=self.__class__.__name__,
            id=self.episode_id,
            voted_at=self.voted_at,
            vote=self.vote,
        )
