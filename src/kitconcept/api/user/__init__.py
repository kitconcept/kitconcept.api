"""Facade for plone.api.user."""
from ._user import change_password
from ._user import change_username
from ._user import create
from ._user import logout
from ._user import request_reset_password
from ._user import update_credentials
from plone.api.user import delete
from plone.api.user import get
from plone.api.user import get_current
from plone.api.user import get_permissions
from plone.api.user import get_roles
from plone.api.user import get_users
from plone.api.user import grant_roles
from plone.api.user import has_permission
from plone.api.user import is_anonymous
from plone.api.user import revoke_roles


__all__ = (
    "change_password",
    "change_username",
    "create",
    "delete",
    "get",
    "get_current",
    "get_permissions",
    "get_roles",
    "get_users",
    "grant_roles",
    "has_permission",
    "is_anonymous",
    "logout",
    "request_reset_password",
    "revoke_roles",
    "update_credentials",
)
