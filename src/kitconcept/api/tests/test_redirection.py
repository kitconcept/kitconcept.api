"""Tests for kitconcept.api.redirection methods."""
from kitconcept import api
from kitconcept.api._typing import Redirect
from kitconcept.api.testing import INTEGRATION_TESTING  # noqa: E501

import unittest


class TestAPIRedirection(unittest.TestCase):
    """TestCase for kitconcept.api.redirection."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]

    def _make_one(self):
        """Add one redirect."""
        old_path = "/old_path"
        new_path = "/new_path"
        payload = {"old_path": old_path, "new_path": new_path}
        api.redirection.create(**payload)

    def test_api_get_redirects(self):
        """Test api.redirection.get_all."""
        self._make_one()
        func = api.redirection.get_all
        redirects = func()
        self.assertIsInstance(redirects, list)
        self.assertEqual(len(redirects), 1)
        self.assertIsInstance(redirects[0], Redirect)

    def test_api_redirect_for_path(self):
        """Test api.redirection.get."""
        self._make_one()
        func = api.redirection.get
        redirect = func("/old_path")
        self.assertIsInstance(redirect, Redirect)
        self.assertEqual(redirect.new_path, "/new_path")

    def test_api_redirect_for_path_non_existing(self):
        """Test api.redirection.get when no redirection was created."""
        self._make_one()
        func = api.redirection.get
        redirect = func("/anything")
        self.assertIsNone(redirect)

    def test_api_add_redirect(self):
        """Test api.redirection.create."""
        func = api.redirection.create
        old_path = "/categories/politics"
        new_path = "/categories/regional"
        payload = {"old_path": old_path, "new_path": new_path}
        redirect = func(**payload)
        self.assertIsInstance(redirect, Redirect)
        self.assertEqual(redirect.old_path, old_path)
        self.assertEqual(redirect.new_path, new_path)
        self.assertTrue(redirect.manual)

    def test_api_add_redirect_existing_path(self):
        """Test api.redirection.create with existing path."""
        self._make_one()
        func = api.redirection.create
        old_path = "/old_path"
        new_path = "/categories/regional"
        payload = {"old_path": old_path, "new_path": new_path}
        redirect = func(**payload)
        self.assertEqual(redirect.new_path, new_path)

    def test_api_remove_redirect(self):
        """Test api.redirection.delete."""
        self._make_one()
        func = api.redirection.delete
        old_path = "/old_path"
        # Remove redirect
        func(old_path)
        self.assertIsNone(api.redirection.get(old_path))
