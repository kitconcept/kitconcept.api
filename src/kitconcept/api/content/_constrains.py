"""Manage constrains on plone content objects."""
from kitconcept.api._typing import ConstrainInformation
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.api.validation import required_parameters
from plone.dexterity.content import DexterityContent
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from typing import List


MODES = {
    "acquire": -1,  # acquire locallyAllowedTypes from parent (default)
    "disabled": 0,  # use default behavior of PortalFolder which uses the FTI info
    "enabled": 1,  # allow types from locallyAllowedTypes only
}


REVERSE_MODES = {value: key for key, value in MODES.items()}


def _get_behavior(obj: DexterityContent) -> ISelectableConstrainTypes:
    """Get ISelectableConstrainTypes for a given content."""
    try:
        behavior = ISelectableConstrainTypes(obj)
    except TypeError:
        # Object does not have the behavior enabled
        raise InvalidParameterError(f"Object {obj} does not support constrains")
    return behavior


@required_parameters("obj")
def get_constrains(obj: DexterityContent) -> ConstrainInformation:
    """Get constrain information for a content object.

    :param obj: [required] Object that we want to get constrain information from.
    :returns: ConstrainInformation if object supports ISelectableConstrainTypes behavior.
    """
    behavior = _get_behavior(obj)
    allowed_types = behavior.getLocallyAllowedTypes()
    immediately_addable_types = behavior.getImmediatelyAddableTypes()
    info = ConstrainInformation(
        mode=REVERSE_MODES.get(behavior.getConstrainTypesMode()),
        allowed_types=allowed_types or [],
        immediately_addable_types=immediately_addable_types or [],
    )
    return info


@required_parameters("obj", "mode")
def set_constrains(
    obj: DexterityContent,
    mode: str,
    allowed_types: List[str] = None,
    immediately_addable_types: List[str] = None,
) -> ConstrainInformation:
    """Set constrain information for a content object.

    :param obj: [required] Object that we want to set constrain information to.
    :returns: ConstrainInformation if object supports ISelectableConstrainTypes behavior.
    """
    behavior = _get_behavior(obj)
    mode_ = MODES.get(mode)
    if not mode_:
        raise InvalidParameterError(
            f"Value {mode} for parameter mode is not valid.\n"
            f"Allowed values are: {','.join(MODES.keys())}"
        )

    behavior.setConstrainTypesMode(mode_)
    # Enabled
    if mode_ == 1:
        if allowed_types is None:
            raise MissingParameterError(
                "With constrains enabled, you must provide at least allowed_types"
            )
        if immediately_addable_types is None:
            immediately_addable_types = allowed_types
        behavior.setLocallyAllowedTypes(allowed_types)
        behavior.setImmediatelyAddableTypes(immediately_addable_types)
    return get_constrains(obj)
