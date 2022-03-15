"""Facade for plone.api.exc."""
from plone.api.exc import CannotGetPortalError
from plone.api.exc import GroupNotFoundError
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.api.exc import PloneApiError
from plone.api.exc import UserNotFoundError


__all__ = (
    "CannotGetPortalError",
    "GroupNotFoundError",
    "InvalidParameterError",
    "MissingParameterError",
    "PloneApiError",
    "UserNotFoundError",
)
