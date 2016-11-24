# coding=utf-8
from six import text_type


class BaseError(Exception):
    def __init__(self, value):
        self.value = text_type(value)

    def __repr__(self):
        return self.value


class ShowNotFound(BaseError):
    pass


class IDNotFound(BaseError):
    pass


class ScheduleNotFound(BaseError):
    pass


class EpisodeNotFound(BaseError):
    pass


class NoEpisodesForAirdate(BaseError):
    pass


class CastNotFound(BaseError):
    pass


class ShowIndexError(BaseError):
    pass


class PersonNotFound(BaseError):
    pass


class CreditsNotFound(BaseError):
    pass


class UpdateNotFound(BaseError):
    pass


class AKASNotFound(BaseError):
    pass


class SeasonNotFound(BaseError):
    pass


class GeneralError(BaseError):
    pass


class MissingParameters(BaseError):
    pass


class IllegalAirDate(BaseError):
    pass


class ConnectionError(BaseError):
    pass


class BadRequest(BaseError):
    pass


class NoFollowedShows(BaseError):
    pass


class ShowNotFollowed(BaseError):
    pass


class NoFollowedPeople(BaseError):
    pass


class PersonNotFollowed(BaseError):
    pass


class NoMarkedEpisodes(BaseError):
    pass


class EpisodeNotMarked(BaseError):
    pass


class InvalidMarkedEpisodeType(BaseError):
    pass


class InvalidEmbedValue(BaseError):
    pass


class NetworkNotFound(BaseError):
    pass


class NetworkNotFollowed(BaseError):
    pass


class NoFollowedWebChannels(BaseError):
    pass


class NoVotedShows(BaseError):
    pass


class ShowNotVotedFor(BaseError):
    pass


class InvalidVoteValue(BaseError):
    pass


class NoVotedEpisodes(BaseError):
    pass


class EpisodeNotVotedFor(BaseError):
    pass


class CrewNotFound(BaseError):
    pass
