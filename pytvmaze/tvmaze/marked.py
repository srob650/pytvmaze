from __future__ import unicode_literals


class MarkedEpisode(object):
    def __init__(self, data):
        self.episode_id = data.get('episode_id')
        self.marked_at = data.get('marked_at')
        type_ = data.get('type')
        types = {0: 'watched', 1: 'acquired', 2: 'skipped'}
        self.type = types[type_]

    def __repr__(self):
        return '<{cls}(episode_id={id},marked_at={marked_at},type={type})>'.format(
            cls=self.__class__.__name__,
            id=self.episode_id,
            marked_at=self.marked_at,
            type=self.type,
        )
