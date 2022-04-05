"""Implement api methods for fti."""
from kitconcept.api.exc import InvalidParameterError
from plone.api.validation import required_parameters
from plone.behavior.interfaces import IBehavior
from plone.behavior.registration import BehaviorRegistration
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from typing import Dict
from typing import List
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface.interfaces import ComponentLookupError


def get_types() -> Dict[str, DexterityFTI]:
    """Return all FTIs available on the site.

    :returns: Dictionary will all FTIs registered on the site.
    """
    ftis = [fti for fti in getUtilitiesFor(IDexterityFTI)]
    return dict(ftis)


@required_parameters("type")
def get(type: str) -> DexterityFTI:  # noQA: A002
    """Return FTI for a type.

    :param type: Name of the type.
    :returns: DexterityFTI for type.
    """
    try:
        fti = getUtility(IDexterityFTI, name=type)
    except ComponentLookupError:
        raise InvalidParameterError(f"Type {type} is not available.")
    return fti


@required_parameters("type")
def behaviors_for_type(type: str) -> List[str]:  # noQA: A002
    """Return behavior names for a type.

    :param type: Name of the type.
    :returns: List of behavior names for a type.
    """
    fti = get(type=type)
    return list(fti.behaviors)


@required_parameters("name")
def get_behavior_registration(name: str) -> BehaviorRegistration:
    """Return a behavior registration with given name.

    :param name: Name of the behavior.
    :returns: Behavior Registration.
    """
    try:
        behavior = getUtility(IBehavior, name)
    except ComponentLookupError:
        raise InvalidParameterError(
            f"Behavior registration named {name} is not available."
        )
    return behavior


@required_parameters("portal_type", "behavior")
def add_behavior_for_type(portal_type, behavior):
    """Add the given behavior to the given portal type.

    :param portal_type: Name of the portal type.
    :param behavior: Name of the behavior.
    """
    fti = queryUtility(IDexterityFTI, name=portal_type)
    if fti is not None:
        # This prevents to add the behavior twice
        new = [
            currentbehavior
            for currentbehavior in fti.behaviors
            if currentbehavior != behavior
        ]
        new.append(behavior)
        fti.behaviors = tuple(new)


@required_parameters("portal_type", "behavior")
def remove_behavior_for_type(portal_type, behavior):
    """Remove the given behavior from the given portal type.

    :param portal_type: Name of the portal type.
    :param behavior: Name of the behavior.
    """
    fti = queryUtility(IDexterityFTI, name=portal_type)
    if fti is not None:
        new = [
            currentbehavior
            for currentbehavior in fti.behaviors
            if currentbehavior != behavior
        ]
        fti.behaviors = tuple(new)
