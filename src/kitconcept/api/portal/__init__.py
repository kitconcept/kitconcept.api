"""Facade for plone.api.portal."""
from plone.api.portal import get
from plone.api.portal import get_current_language
from plone.api.portal import get_default_language
from plone.api.portal import get_localized_time
from plone.api.portal import get_navigation_root
from plone.api.portal import get_registry_record
from plone.api.portal import get_tool
from plone.api.portal import send_email
from plone.api.portal import set_registry_record
from plone.api.portal import show_message
from plone.api.portal import translate


__all__ = (
    "get",
    "get_current_language",
    "get_default_language",
    "get_localized_time",
    "get_navigation_root",
    "get_registry_record",
    "get_tool",
    "send_email",
    "set_registry_record",
    "show_message",
    "translate",
)
