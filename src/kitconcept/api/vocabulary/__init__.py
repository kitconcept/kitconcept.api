"""Implement an api to access vocabularies."""
from ._vocabulary import get
from ._vocabulary import get_vocabularies_names


__all__ = (
    "get_vocabularies_names",
    "get",
)
