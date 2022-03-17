"""Implement an api to access vocabularies."""
from plone import api
from plone.api.validation import required_parameters
from plone.dexterity.content import DexterityContent
from typing import List
from typing import Optional
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized


@required_parameters("name")
def get(name: str, context: Optional[DexterityContent] = None) -> IVocabularyTokenized:
    """Return a vocabulary object with given name.

    :param name: Name of the vocabulary.
    :param context: Context to be applied to the vocabulary. Default: portal root
    :return: A vocabulary that implements the IVocabularyTokenized interface.
    """
    if not context:
        context = api.portal.get()
    vocab = getUtility(IVocabularyFactory, name)
    return vocab(context)


def get_vocabularies() -> List[str]:
    """Return a list of vocabularies names.

    :return: A list of vocabularies names.
    """
    all_vocabs = getUtilitiesFor(IVocabularyFactory)
    return [v[0] for v in all_vocabs]
