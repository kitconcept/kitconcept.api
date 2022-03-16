"""Tests for kitconcept.api.content.serialize."""
from kitconcept import api
from kitconcept.api.testing import INTEGRATION_TESTING  # noqa: E501
from plone.api.env import plone_version

import unittest


class TestAPIContentSerialize(unittest.TestCase):
    """TestCase for kitconcept.api.content.serialize."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]
        self.pas = api.portal.get_tool("acl_users")
        self.document = api.content.create(
            **{
                "container": self.portal,
                "type": "Document",
                "id": "a-document",
                "title": "A document",
                "description": "A simple document",
            }
        )

    def test_api_content_serialize_portal(self):
        """Test api.content.serialize with portal as the content."""
        func = api.content.serialize
        data = func(self.portal)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["@type"], "Plone Site")
        self.assertEqual(data["id"], "plone")
        self.assertEqual(data["title"], "Site")

    def test_api_content_serialize_portal_plone_version_diff(self):
        """Test api.content.serialize with portal as the content."""
        func = api.content.serialize
        data = func(self.portal)
        self.assertIsInstance(data, dict)
        if plone_version().startswith("5"):
            self.assertEqual(data["@id"], "http://nohost")
        else:
            self.assertEqual(data["@id"], "http://nohost/plone")

    def test_api_content_serialize_document(self):
        """Test api.content.serialize with a document as the content."""
        func = api.content.serialize
        data = func(self.document)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["@id"], "http://nohost/plone/a-document")
        self.assertEqual(data["title"], "A document")
        self.assertEqual(data["description"], "A simple document")
        self.assertFalse(data["exclude_from_nav"])

    def test_api_content_serialize_summary(self):
        """Test api.content.serialize a content with a summary."""
        func = api.content.serialize
        data = func(self.document, summary=True)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["@id"], "http://nohost/plone/a-document")
        # Attributes not available in a summary serialization
        self.assertNotIn("exclude_from_nav", data)
        self.assertNotIn("subjects", data)
