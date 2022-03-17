"""Tests for kitconcept.api.redirection methods."""
from kitconcept import api
from kitconcept.api.testing import INTEGRATION_TESTING  # noqa: E501
from plone.api.exc import InvalidParameterError
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import unittest


class TestAPIVocabularyy(unittest.TestCase):
    """TestCase for kitconcept.api.vocabulary."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]

    def test_api_get_vocabularies_names(self):
        """Test api.vocabulary.get_vocabularies_names."""
        result = api.vocabulary.get_vocabularies_names()
        self.assertIsInstance(result, list)
        self.assertIn("plone.app.vocabularies.Month", result)

    def test_api_get(self):
        """Test api.vocabulary.get."""
        result = api.vocabulary.get("plone.app.vocabularies.Month")
        self.assertIsInstance(result, SimpleVocabulary)
        term = result.getTerm(0)
        self.assertIsInstance(term, SimpleTerm)
        self.assertEqual(term.title, "month_jan")

    def test_api_get_fail(self):
        """Test api.vocabulary.get with non existing vocabulary."""
        name = "not a vocabulary name"
        with self.assertRaises(InvalidParameterError) as cm:
            api.vocabulary.get(name)
        self.assertIn(f"No vocabulary with name '{name}' available", str(cm.exception))
