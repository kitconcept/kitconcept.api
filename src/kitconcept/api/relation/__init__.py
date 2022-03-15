"""Facade for plone.api.relatiom."""
from plone.api.relation import create
from plone.api.relation import delete
from plone.api.relation import get


__all__ = (
    "get",
    "create",
    "delete",
)
