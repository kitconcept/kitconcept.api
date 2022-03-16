"""Facade for plone.api.portal."""
from plone.api.env import adopt_roles
from plone.api.env import adopt_user
from plone.api.env import debug_mode
from plone.api.env import plone_version
from plone.api.env import read_only_mode
from plone.api.env import test_mode
from plone.api.env import zope_version


__all__ = (
    "adopt_roles",
    "adopt_user",
    "debug_mode",
    "plone_version",
    "read_only_mode",
    "test_mode",
    "zope_version",
)
