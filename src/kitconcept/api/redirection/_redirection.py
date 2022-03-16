"""Implement api methods for redirection."""
from kitconcept.api._typing import Redirect
from kitconcept.api.portal import get as get_portal
from plone.api.validation import required_parameters
from plone.app.redirector.interfaces import IRedirectionStorage
from plone.app.redirector.storage import RedirectionStorage
from typing import List
from typing import Optional
from zope.component import getUtility


def _redirection_storage() -> RedirectionStorage:
    """Return the Redirection storage object."""
    return getUtility(IRedirectionStorage)


def _process_redirect_info(old_path: str, redirect_info: dict) -> Optional[Redirect]:
    """Return a Redirect object from redirect information.

    :param old_path: Source path.
    :param redirect_info: Dictionary with redirect information.
    :return: Redirect object.
    """
    portal_path = "/".join(get_portal().getPhysicalPath())
    len_portal_path = len(portal_path)
    if old_path.startswith(portal_path):
        old_path = old_path[len_portal_path:]
    if not isinstance(redirect_info, tuple):
        # Old data: only a single path, no date and manual boolean.
        redirect_info = (redirect_info, None, True)
    new_path = redirect_info[0]
    if new_path is None:
        return None
    created_at = redirect_info[1]
    manual = redirect_info[2]
    if new_path.startswith(portal_path):
        new_path = new_path[len_portal_path:]
    return Redirect(old_path, new_path, created_at, manual)


def get_all() -> List[Redirect]:
    """List all redirects in the site.

    :returns: A list of active redirects in the site.
    """
    results = []
    storage = _redirection_storage()
    paths = storage._paths
    for old_path, redirect_info in paths.items():
        redirect = _process_redirect_info(old_path, redirect_info)
        results.append(redirect)
    return results


@required_parameters("old_path", "new_path")
def create(old_path: str, new_path: str) -> Redirect:
    """Create a manual redirect from a source path to a destination path.

    :param old_path: Source path of the object.
    :param new_path: Destination path of the object.
    :return: Redirect object.
    """
    storage = _redirection_storage()
    storage.add(old_path, new_path, manual=True)
    redirect_info = storage.get_full(old_path)
    return _process_redirect_info(old_path, redirect_info)


@required_parameters("path")
def get(path: str) -> Optional[Redirect]:
    """Return  a manual redirect from a source path.

    :param path: Source path of the object.
    :return: Redirect object.
    """
    storage = _redirection_storage()
    redirect_info = storage.get_full(path)
    return _process_redirect_info(path, redirect_info)


@required_parameters("path")
def delete(path: str):
    """Remove redirect for a path.

    :param path: Source path of the object.
    """
    storage = _redirection_storage()
    storage.remove(path)
