"""Tests for kitconcept.api.user methods."""
from kitconcept import api
from kitconcept.api.testing import INTEGRATION_TESTING  # noqa: E501

import unittest


class TestAPIUser(unittest.TestCase):
    """TestCase for kitconcept.api.user."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]
        self.pas = api.portal.get_tool("acl_users")
        self.user_payload = {
            "username": "will",
            "email": "will@web.de",
            "password": "123456789ABC",
            "properties": {"location": "Berlin"},
        }

    def _make_one(self):
        """Return a user."""
        return api.user.create(**self.user_payload)

    def _check_password(self, username: str, password: str) -> bool:
        """Check password for a user."""
        return True if self.pas.authenticate(username, password, None) else False

    def test_api_user_create(self):
        """Test api.user.create."""
        func = api.user.create
        payload = self.user_payload
        props = payload["properties"]
        user = func(**payload)
        self.assertEqual(user.getUserName(), payload["username"])
        self.assertEqual(user.getProperty("email"), payload["email"])
        self.assertEqual(user.getProperty("location"), props["location"])
        self.assertNotEqual(user.getId(), user.getUserName())

    def test_api_change_password(self):
        """Test api.user.change_password."""
        func = api.user.change_password
        user = self._make_one()
        username = user.getUserName()
        old_password = self.user_payload["password"]
        self.assertTrue(self._check_password(username, old_password))
        new_password = "a really long new password 123"
        func(user, new_password)
        self.assertFalse(self._check_password(username, old_password))
        self.assertTrue(self._check_password(username, new_password))

    def test_api_change_username_success(self):
        """Test api.user.change_username."""
        func = api.user.change_username
        user = self._make_one()
        current_username = user.getUserName()
        new_username = "will_123"
        user = func(user, new_username)
        self.assertNotEqual(user.getUserName, current_username)
        self.assertNotEqual(user.getUserName, new_username)

    def test_api_change_username_taken_existing(self):
        """Test api.user.change_username with an existing username."""
        func = api.user.change_username
        user = self._make_one()
        # Username is already created
        new_username = "admin"
        with self.assertRaises(ValueError) as cm:
            func(user, new_username)
        self.assertIn(f"Username {new_username} is taken", str(cm.exception))

    def test_api_change_username_same(self):
        """Test api.user.change_username passing the same username."""
        func = api.user.change_username
        user = self._make_one()
        with self.assertRaises(ValueError) as cm:
            func(user, user.getUserName())
        self.assertIn("Username not changed", str(cm.exception))
