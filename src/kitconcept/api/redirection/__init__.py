"""Implement an api to manage redirects in Plone."""
from ._redirection import create
from ._redirection import delete
from ._redirection import get
from ._redirection import get_all
from ._redirection import Redirect


__all__ = (
    "create",
    "delete",
    "get_all",
    "get",
    "Redirect",
)
