"""kitconcept.api package."""
from kitconcept.api import addon
from kitconcept.api import content
from kitconcept.api import env
from kitconcept.api import exc
from kitconcept.api import group
from kitconcept.api import portal
from kitconcept.api import redirection
from kitconcept.api import relation
from kitconcept.api import user
from kitconcept.api import vocabulary

import pkg_resources


__all__ = (
    "addon",
    "content",
    "env",
    "exc",
    "group",
    "portal",
    "redirection",
    "relation",
    "user",
    "vocabulary",
)

__version__ = pkg_resources.get_distribution("kitconcept.api").version
