"""Implement an api to manage addons in Plone."""
from ._installer import get
from ._installer import get_addons
from ._installer import get_addons_ids
from ._installer import install
from ._installer import uninstall


__all__ = (
    "get_addons",
    "get_addons_ids",
    "get",
    "install",
    "uninstall",
)
