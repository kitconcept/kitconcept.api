"""Tests for kitconcept.api.redirection methods."""
from kitconcept import api
from kitconcept.api.testing import INTEGRATION_TESTING  # noqa: E501
from plone.behavior.registration import BehaviorRegistration
from plone.dexterity.fti import DexterityFTI

import unittest


class TestAPIFti(unittest.TestCase):
    """TestCase for kitconcept.api.fti."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]

    def test_api_get_types(self):
        """Test api.fti.get_types."""
        result = api.fti.get_types()
        self.assertIsInstance(result, dict)
        # Document FTI should be present
        self.assertIn("Document", result)
        self.assertIsInstance(result["Document"], DexterityFTI)

    def test_api_get(self):
        """Test api.fti.get."""
        result = api.fti.get(type="Document")
        self.assertIsInstance(result, DexterityFTI)
        self.assertEqual(result.id, "Document")

    def test_api_get_error(self):
        """Test api.fti.get."""
        with self.assertRaises(api.exc.InvalidParameterError) as cm:
            api.fti.get(type="foobar")
        self.assertIn("Type foobar is not available.", str(cm.exception))

    def test_api_behaviors_for_type(self):
        """Test api.fti.behaviors_for_type."""
        result = api.fti.behaviors_for_type(type="Document")
        self.assertIsInstance(result, list)
        self.assertIn("plone.dublincore", result)

    def test_api_behaviors_for_type_error(self):
        """Test api.fti.behaviors_for_type."""
        with self.assertRaises(api.exc.InvalidParameterError) as cm:
            api.fti.behaviors_for_type(type="foobar")
        self.assertIn("Type foobar is not available.", str(cm.exception))

    def test_api_get_behavior_registration(self):
        """Test api.fti.get_behavior_registration."""
        result = api.fti.get_behavior_registration(name="plone.dublincore")
        self.assertIsInstance(result, BehaviorRegistration)
        self.assertEqual(result.title, "Dublin Core metadata")

    def test_api_get_behavior_registration_error(self):
        """Test api.fti.get_behavior_registration."""
        with self.assertRaises(api.exc.InvalidParameterError) as cm:
            api.fti.get_behavior_registration(name="foobar")
        self.assertIn(
            "Behavior registration named foobar is not available.", str(cm.exception)
        )

    def test_api_add_behavior_for_type(self):
        """Test api.fti.add_behavior_for_type."""
        api.fti.add_behavior_for_type("Document", "plone.leadimage")
        doc_behaviors = api.fti.behaviors_for_type(type="Document")
        self.assertIn("plone.leadimage", doc_behaviors)

    def test_api_remove_behavior_for_type(self):
        """Test api.fti.add_behavior_for_type."""
        api.fti.remove_behavior_for_type("Document", "plone.allowdiscussion")
        doc_behaviors = api.fti.behaviors_for_type(type="Document")
        self.assertNotIn("plone.allowdiscussion", doc_behaviors)
