"""Implement an api to manage fti in Plone."""
from ._fti import behaviors_for_type
from ._fti import get
from ._fti import get_behavior_registration
from ._fti import get_types


__all__ = (
    "behaviors_for_type",
    "get_behavior_registration",
    "get_types",
    "get",
)
