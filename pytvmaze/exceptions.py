# coding=utf-8
from six import text_type
import requests.exceptions


class BaseError(Exception):
    def __init__(self, value):
        self.value = text_type(value)

    def __repr__(self):
        return self.value


class GeneralError(BaseError):
    pass


# Request Exceptions
class ConnectionError(BaseError, ):
    pass


class NoEpisodesForAirdate(BaseError):
    pass


class ShowIndexError(BaseError):
    pass


class MissingParameters(BaseError):
    pass


class IllegalAirDate(BaseError):
    pass


class BadRequest(BaseError):
    pass


class NoFollowedShows(BaseError):
    pass


class NoFollowedPeople(BaseError):
    pass


class NoMarkedEpisodes(BaseError):
    pass


class EpisodeNotMarked(BaseError):
    pass


class InvalidMarkedEpisodeType(BaseError):
    pass


class InvalidEmbedValue(BaseError):
    pass


class NoFollowedNetworks(BaseError):
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


class NotAuthorized(BaseError):
    """User authentication missing or invalid."""


# Not Found Exceptions

class NotFoundError(BaseError):
    pass


class ShowNotFound(NotFoundError):
    pass


class IDNotFound(NotFoundError):
    pass


class ScheduleNotFound(NotFoundError):
    pass


class EpisodeNotFound(NotFoundError):
    pass


class CastNotFound(NotFoundError):
    pass


class PersonNotFound(NotFoundError):
    pass


class CreditsNotFound(NotFoundError):
    pass


class UpdateNotFound(NotFoundError):
    pass


class AKASNotFound(NotFoundError):
    pass


class SeasonNotFound(NotFoundError):
    pass


class NetworkNotFound(NotFoundError):
    pass


class WebChannelNotFound(NotFoundError):
    pass


class CrewNotFound(NotFoundError):
    pass


# Not Followed Exceptions

class NotFollowedError(BaseError):
    pass


class ShowNotFollowed(NotFollowedError):
    pass


class PersonNotFollowed(NotFollowedError):
    pass


class NetworkNotFollowed(NotFollowedError):
    pass


class WebChannelNotFollowed(NotFollowedError):
    pass
