"""Serialize objects into a JSON-friendly structure."""
from plone.api.exc import PloneApiError
from plone.api.validation import required_parameters
from plone.dexterity.content import DexterityContent
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest


@required_parameters("obj")
def serialize(obj: DexterityContent, summary: bool = False) -> dict:
    """Serialize the object.

    :param obj: [required] Object that we want to serialize.
    :param summary: Serialize just the summary.
    :returns: Dictionary with serialized object.
    """
    interface = ISerializeToJsonSummary if summary else ISerializeToJson
    serializer = queryMultiAdapter((obj, getRequest()), interface)
    if not serializer:
        raise PloneApiError("Cannot serialize object")
    return serializer()
