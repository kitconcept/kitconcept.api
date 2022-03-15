"""Additional methods for plone.api.user."""
from DateTime import DateTime
from plone import api
from plone.api.exc import InvalidParameterError
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters
from Products.CMFPlone.utils import transaction_note
from Products.PlonePAS.tools.memberdata import MemberData
from Products.PluggableAuthService.interfaces import plugins
from random import choice
from typing import Any
from typing import Dict
from typing import Iterable
from typing import NoReturn
from typing import Optional
from uuid import uuid4
from zope.globalrequest import getRequest

import string


def create(
    email: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    roles: Iterable[str] = ("Member",),
    properties: Dict = None,
) -> MemberData:
    """Create a user.

    :param email: [required] Email for the new user.
    :param username: Username for the new user. This is required if email
        is not used as a username.
    :param password: Password for the new user. If it's not set we generate
        a random 8-char alpha-numeric one.
    :param roles: User roles to assign to the new user.
    :param properties: User properties to assign to the new user. The list of
        available properties is available in ``portal_memberdata`` through ZMI.
    :returns: Newly created user
    :raises:
        MissingParameterError
        InvalidParameterError
    :Example: :ref:`user_create_example`
    """
    properties = properties if properties else {}

    # it may happen that someone passes email in the properties dict, catch
    # that and set the email so the code below this works fine
    if not email and properties.get("email"):
        email = properties.get("email")

    use_email_as_username = False
    if not use_email_as_username and not username:
        raise InvalidParameterError(
            "The portal is configured to use username "
            "that is not email so you need to pass a username.",
        )

    user_id = uuid4().hex
    # Generate a random 8-char password
    if not password:
        chars = string.ascii_letters + string.digits
        password = "".join(choice(chars) for _ in range(8))

    properties.update({"username": username, "email": email, "created_at": DateTime()})
    # Create the user using portal_registration
    registration = api.portal.get_tool("portal_registration")
    registration.addMember(  # noQA
        user_id,
        password,
        roles,
        properties=properties,
    )
    # Get current user
    user = api.user.get(userid=user_id)
    # Update login name
    user = change_username(user, username)

    transaction_note(f"User {username} created.")
    return user


@required_parameters("member", "password")
def change_password(member: MemberData, password: str) -> NoReturn:
    """Change user password.

    :param member: User to change the password.
    :param password: New user password.
    """
    pas = api.portal.get_tool("acl_users")
    user = member.getUser()
    if getattr(user, "changePassword", None):
        user.changePassword(password)
    else:
        pas._doChangeUser(member.getUserId(), password, member.getRoles())  # noQA

    transaction_note(f"User {member.getUserName()} changed their password.")


@required_parameters("member", "password")
def update_credentials(
    member: MemberData,
    password: str,
) -> NoReturn:
    """Update User credentials.

    :param member: Member object.
    :param password: New password.
    """
    request = getRequest()
    pas = api.portal.get_tool("acl_users")
    username = member.getUserName()
    # Reset credentials (session and cookie plugins)
    for _, plugin in pas.plugins.listPlugins(plugins.ICredentialsUpdatePlugin):
        plugin.updateCredentials(
            request,
            request.response,
            username,
            password,
        )


def logout() -> NoReturn:
    """Logout the current user."""
    request = getRequest()
    mt = api.portal.get_tool("portal_membership")
    mt.logoutUser(request)


@required_parameters("member", "username")
def change_username(
    member: MemberData,
    username: str,
) -> MemberData:
    """Change username.

    :param member: User to change the password.
    :param username: New username.
    :returns: MemberData.
    """
    current_username = member.getUserName()
    if current_username == username:
        raise ValueError("Username not changed")
    elif api.user.get(username=username):
        raise ValueError(f"Username {username} is taken")
    pas = api.portal.get_tool("acl_users")
    user_id = member.getUserId()
    pas.updateLoginName(user_id, username)
    member = api.user.get(username=username)
    transaction_note(
        f"User {current_username} changed username to {member.getUserName()}.",
    )
    return member


@mutually_exclusive_parameters("userid", "username")
@at_least_one_of("userid", "username")
def request_reset_password(
    username: Optional[str] = None,
    userid: Optional[str] = None,
) -> Dict[str, Any]:
    """Request a password reset.

    :param username: Username.
    :param userid: Userid.
    :returns: Dictionary with request reset password information.
    """
    if not userid:
        user = api.user.get(username=username)
        userid = user.getId()
    tool = api.portal.get_tool("portal_password_reset")
    reset = tool.requestReset(userid)
    return reset
