"""Tests for kitconcept.api.redirection methods."""
from kitconcept import api
from kitconcept.api._typing import AddonInformation
from kitconcept.api.testing import INTEGRATION_TESTING  # noqa: E501

import unittest


class TestAPIAddonGetAddons(unittest.TestCase):
    """TestCase for kitconcept.api.addon.get_addons."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]
        # Install plone.restapi
        api.addon.install("plone.restapi")

    def test_api_get_addons(self):
        """Test api.addon.get_addons without any filter."""
        result = api.addon.get_addons()
        self.assertIsInstance(result, list)
        addon_ids = [addon.id for addon in result]
        self.assertIn("plone.restapi", addon_ids)

    def test_api_get_addons_limit_broken(self):
        """Test api.addon.get_addons filtering for broken addons."""
        result = api.addon.get_addons(limit="broken")
        self.assertEqual(len(result), 0)

    def test_api_get_addons_limit_non_installable(self):
        """Test api.addon.get_addons filtering for non_installable addons."""
        result = api.addon.get_addons(limit="non_installable")
        self.assertNotEqual(len(result), 0)
        addon_ids = [addon.id for addon in result]
        self.assertIn("plone.app.dexterity", addon_ids)

    def test_api_get_addons_limit_installed(self):
        """Test api.addon.get_addons filtering for installed addons."""
        result = api.addon.get_addons(limit="installed")
        self.assertEqual(len(result), 1)
        addon_ids = [addon.id for addon in result]
        self.assertIn("plone.restapi", addon_ids)

    def test_api_get_addons_limit_upgradable(self):
        """Test api.addon.get_addons filtering for addons with upgradable."""
        result = api.addon.get_addons(limit="upgradable")
        self.assertEqual(len(result), 0)

    def test_api_get_addons_limit_invalid(self):
        """Test api.addon.get_addons filtering with an invalid parameter."""
        with self.assertRaises(api.exc.InvalidParameterError) as cm:
            api.addon.get_addons(limit="foobar")
        self.assertIn(
            "Value foobar for parameter mode is not valid.", str(cm.exception)
        )

    def test_api_get_addons_ids(self):
        """Test api.addon.get_addons_ids."""
        result = api.addon.get_addons_ids(limit="installed")
        self.assertEqual(len(result), 1)
        self.assertIn("plone.restapi", result)


class TestAPIAddon(unittest.TestCase):
    """TestCase for kitconcept.api.addon."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Set up TestCase."""
        self.portal = self.layer["portal"]

    def test_api_install(self):
        """Test api.addon.install."""
        result = api.addon.install("plone.restapi")
        self.assertTrue(result)

    def test_api_uninstall_unavailable(self):
        """Test api.addon.install unavailable addon."""
        result = api.addon.install("Foobar")
        self.assertFalse(result)

    def test_api_uninstall(self):
        """Test api.addon.uninstall."""
        # First install the addon
        api.addon.install("plone.restapi")
        result = api.addon.uninstall("plone.restapi")
        self.assertTrue(result)

    def test_api_uninstall_unavailable(self):
        """Test api.addon.uninstall unavailable addon."""
        result = api.addon.uninstall("Foobar")
        self.assertFalse(result)

    def test_api_get(self):
        """Test api.addon.get."""
        result = api.addon.get("plone.restapi")
        self.assertIsInstance(result, AddonInformation)
        self.assertEqual(result.id, "plone.restapi")
        self.assertTrue(result.valid)
        self.assertEqual(result.description, "RESTful hypermedia API for Plone.")
        self.assertEqual(result.profile_type, "default")
        self.assertIsInstance(result.version, str)
        self.assertIsInstance(result.install_profile, dict)
        self.assertIsInstance(result.uninstall_profile, dict)
        self.assertIsInstance(result.upgrade_info, dict)
