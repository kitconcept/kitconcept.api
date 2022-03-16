"""kitconcept.api typing information."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional


__all__ = (
    "ConstrainInformation",
    "Redirect",
    "NonInstallableAddons",
    "AddonInformation",
)


@dataclass
class ConstrainInformation:
    """Constrain information for an object."""

    mode: str
    allowed_types: List[str]
    immediately_addable_types: List[str]


@dataclass
class Redirect:
    """A redirect managed by Plone."""

    old_path: str
    new_path: str
    created_at: Optional[datetime] = None
    manual: bool = False


@dataclass
class NonInstallableAddons:
    """Set of addons not available for installation."""

    profiles: List[str]
    products: List[str]


@dataclass
class AddonInformation:
    """Addon information."""

    id: str  # noQA
    version: str
    title: str
    description: str
    upgrade_profiles: Dict
    other_profiles: List[Dict]
    install_profile: Dict
    uninstall_profile: Dict
    profile_type: str
    upgrade_info: Dict
    valid: bool
    flags: List[str]

    def __repr__(self) -> str:
        """Return a string representation of this object."""
        return f"<AddonInformation id='{self.id}' flags='{self.flags}'>"
