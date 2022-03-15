"""Tests for kitconcept.api.content._constrains methods."""
from kitconcept import api
from kitconcept.api.testing import INTEGRATION_TESTING  # noqa: E501
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError

import unittest


class TestAPIContentConstrains(unittest.TestCase):
    """TestCase for kitconcept.api.content._constrains."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]
        self.pas = api.portal.get_tool("acl_users")
        self.folder = api.content.create(
            **{
                "container": self.portal,
                "type": "Folder",
                "id": "folder",
                "title": "A folder",
                "description": "A folder to manage constrains",
            }
        )
        self.link = api.content.create(
            **{
                "container": self.portal,
                "type": "Link",
                "id": "a-link",
                "title": "A Link",
                "description": "A Link object",
                "remote_url": "https://plone.org/",
            }
        )

    def test_api_content_get_constrains(self):
        """Test api.content.get_constrains."""
        info = api.content.get_constrains(self.folder)
        self.assertEqual(info.mode, "disabled")
        self.assertIn("Document", info.allowed_types)
        self.assertIn("Document", info.immediately_addable_types)

    def test_api_content_set_constrains(self):
        """Test api.content.set_constrains."""
        info = api.content.set_constrains(
            self.folder,
            mode="enabled",
            allowed_types=["Folder", "Image"],
            immediately_addable_types=[
                "Image",
            ],
        )
        self.assertEqual(info.mode, "enabled")
        self.assertEqual(info.allowed_types, ["Folder", "Image"])
        self.assertEqual(
            info.immediately_addable_types,
            [
                "Image",
            ],
        )

    def test_api_content_set_constrains_with_wrong_mode(self):
        """Test api.content.set_constrains passing a wrong mode."""
        with self.assertRaises(InvalidParameterError) as cm:
            api.content.set_constrains(
                self.folder,
                mode="foobar",
                allowed_types=[],
                immediately_addable_types=[],
            )
        self.assertIn(
            "Value foobar for parameter mode is not valid.", str(cm.exception)
        )

    def test_api_content_set_constrains_without_allowed_types(self):
        """Test api.content.set_constrains without allowed_types."""
        with self.assertRaises(MissingParameterError) as cm:
            api.content.set_constrains(
                self.folder,
                mode="enabled",
                immediately_addable_types=[],
            )
        self.assertIn(
            "With constrains enabled, you must provide at least allowed_types",
            str(cm.exception),
        )

    def test_api_content_set_constrains_assume_immediately_addable_types(self):
        """Test api.content.set_constrains without immediately_addable_types."""
        info = api.content.set_constrains(
            self.folder,
            mode="enabled",
            allowed_types=["Image"],
        )
        self.assertEqual(info.mode, "enabled")
        self.assertEqual(info.immediately_addable_types, info.allowed_types)

    def test_api_content_get_constrains_object_not_supporting_constrains(self):
        """Test api.content.get_constrains with object not supporting constrains."""
        with self.assertRaises(InvalidParameterError) as cm:
            api.content.get_constrains(self.link)
        self.assertIn(
            "Object <Link at a-link> does not support constrains",
            str(cm.exception),
        )
