"""API to handle addon management."""
from functools import lru_cache
from kitconcept.api._typing import AddonInformation
from kitconcept.api._typing import NonInstallableAddons
from kitconcept.api.exc import InvalidParameterError
from kitconcept.api.logger import logger
from plone import api
from plone.api.validation import required_parameters
from Products.CMFPlone.controlpanel.browser.quickinstaller import InstallerView
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.utils import get_installer
from Products.GenericSetup import EXTENSION
from typing import List
from typing import Tuple
from zope.component import getAllUtilitiesRegisteredFor
from zope.globalrequest import getRequest

import pkg_resources


def _get_installer() -> InstallerView:
    """Return the InstallerView."""
    portal = api.portal.get()
    return get_installer(portal, getRequest())


@lru_cache(maxsize=1)
def _get_non_installable_addons() -> NonInstallableAddons:
    """Return information about non installable addons.

    We cache this on first use, as those utilities are registered
    during the application startup

    :returns: NonInstallableAddons instance.
    """
    ignore_profiles = []
    ignore_products = []
    utils = getAllUtilitiesRegisteredFor(INonInstallable)
    for util in utils:
        ni_profiles = getattr(util, "getNonInstallableProfiles", None)
        if ni_profiles is not None:
            ignore_profiles.extend(ni_profiles())
        ni_products = getattr(util, "getNonInstallableProducts", None)
        if ni_products is not None:
            ignore_products.extend(ni_products())
    return NonInstallableAddons(
        profiles=ignore_profiles,
        products=ignore_products,
    )


@lru_cache(maxsize=1)
def _cached_addons() -> Tuple[Tuple[str, AddonInformation]]:
    """Return information about addons in this installation.

    :returns: Tuple of tuples with addon id and AddonInformation.
    """
    installer = _get_installer()
    setup_tool = installer.ps
    addons = {}
    non_installable = _get_non_installable_addons()
    # Known profiles:
    profiles = setup_tool.listProfileInfo()
    # Profiles that have upgrade steps (which may or may not have been
    # applied already).
    # profiles_with_upgrades = self.ps.listProfilesWithUpgrades()
    for profile in profiles:
        if profile["type"] != EXTENSION:
            continue

        pid = profile["id"]
        if pid in non_installable.profiles:
            continue
        pid_parts = pid.split(":")
        if len(pid_parts) != 2:
            logger.error(f"Profile with id '{pid}' is invalid.")
        # Which package (product) is this from?
        product_id = profile["product"]
        flags = []
        is_broken = not installer.is_product_installable(product_id, allow_hidden=True)
        is_non_installable = product_id in non_installable.products
        valid = not (is_broken or is_non_installable)
        if is_broken:
            flags.append("broken")
        if is_non_installable:
            flags.append("non_installable")
        profile_type = pid_parts[-1]
        if product_id not in addons:
            # get some basic information on the product
            product = {
                "id": product_id,
                "version": get_version(product_id),
                "title": product_id,
                "description": "",
                "upgrade_profiles": {},
                "other_profiles": [],
                "install_profile": {},
                "uninstall_profile": {},
                "upgrade_info": {},
                "profile_type": profile_type,
                "valid": valid,
                "flags": flags,
            }
            install_profile = installer.get_install_profile(product_id)
            if install_profile is not None:
                product["title"] = install_profile["title"]
                product["description"] = install_profile["description"]
                product["install_profile"] = install_profile
                product["profile_type"] = "default"
            uninstall_profile = installer.get_uninstall_profile(product_id)
            if uninstall_profile is not None:
                product["uninstall_profile"] = uninstall_profile
                # Do not override profile_type.
                if not product["profile_type"]:
                    product["profile_type"] = "uninstall"
        if "version" in profile:
            product["upgrade_profiles"][profile["version"]] = profile
        else:
            product["other_profiles"].append(profile)
        addons[product_id] = AddonInformation(**product)
    return tuple(addons.items())


def _update_addon_info(
    installer: InstallerView, addon: AddonInformation
) -> AddonInformation:
    """Update information about an addon."""
    addon_id = addon.id
    if addon.valid:
        flags = []
        # Update only what could be changed
        is_installed = installer.is_product_installed(addon_id)
        if is_installed:
            addon.upgrade_info = installer.upgrade_info(addon_id) or {}
            if addon.upgrade_info.get("available"):
                flags.append("upgradable")
            else:
                flags.append("installed")
        else:
            flags.append("available")
        addon.flags = flags
    return addon


def _get_addons() -> List[AddonInformation]:
    """Return an updated list of addon information.

    :returns: List of AddonInformation.
    """
    installer = _get_installer()
    addons = dict(_cached_addons())
    result = []
    for addon in addons.values():
        result.append(_update_addon_info(installer, addon))
    return result


def get_addons(limit: str = "") -> List[AddonInformation]:
    """List addons in this Plone site.

    :param limit: Limit list of addons.
        'installed': only products that are installed and not hidden
        'upgradable': only products with upgrades
        'available': products that are not installed but could be
        'non_installable': Non installable products
        'broken': uninstallable products with broken dependencies
    :returns: List of AddonInformation.
    """
    addons = _get_addons()
    if limit in ("non_installable", "broken"):
        return [addon for addon in addons if limit in addon.flags]

    addons = [addon for addon in addons if addon.valid]
    if limit in ("installed", "upgradable", "available"):
        addons = [addon for addon in addons if limit in addon.flags]
    elif limit != "":
        raise InvalidParameterError(f"Value {limit} for parameter mode is not valid.")
    return addons


def get_addons_ids(limit: str = "") -> List[str]:
    """List addons ids in this Plone site.

    :param limit: Limit list of addons.
        'installed': only products that are installed and not hidden
        'upgradable': only products with upgrades
        'available': products that are not installed but could be
        'non_installable': Non installable products
        'broken': uninstallable products with broken dependencies
    :returns: List of addon ids.
    """
    addons = get_addons(limit=limit)
    return [addon.id for addon in addons]


@required_parameters("addon")
def get_version(addon: str) -> str:
    """Return the version of the product (package)."""
    try:
        dist = pkg_resources.get_distribution(addon)
        return dist.version
    except pkg_resources.DistributionNotFound:
        if "." in addon:
            return ""
    return get_version(f"Products.{addon}")


@required_parameters("addon")
def get(addon: str) -> AddonInformation:
    """Information about an Addon.

    :param addon: ID of the addon to be retrieved.
    :returns: Addon information.
    """
    addons = dict(_cached_addons())
    if addon not in addons:
        raise InvalidParameterError(f"No addon {addon} found.")
    return _update_addon_info(_get_installer(), addons.get(addon))


@required_parameters("addon")
def install(addon: str) -> bool:
    """Install an addon.

    :param addon: ID of the addon to be installed.
    :returns: Status of the installation.
    """
    installer = _get_installer()
    return installer.install_product(addon)


@required_parameters("addon")
def uninstall(addon: str) -> bool:
    """Uninstall an addon.

    :param addon: ID of the addon to be uninstalled.
    :returns: Status of the uninstallation.
    """
    installer = _get_installer()
    return installer.uninstall_product(addon)
