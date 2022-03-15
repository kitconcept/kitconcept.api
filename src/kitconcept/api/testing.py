"""Testing setup for kitconcept.api."""
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME


class KitconceptApiLayer(PloneSandboxLayer):
    """Test layer for kitconcept.api."""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Prepare Zope instance by loading appropriate ZCMLs."""
        import plone.api
        import plone.app.contenttypes
        import plone.app.dexterity
        import plone.restapi

        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=plone.app.contenttypes)
        self.loadZCML(package=plone.restapi)

    def setUpPloneSite(self, portal):
        """Prepare a Plone instance for testing."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, "Products.CMFPlone:plone")
        self.applyProfile(portal, "plone.app.contenttypes:default")

        # Login as manager
        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)

    def tearDownZope(self, app):
        """Tear down Zope."""


FIXTURE = KitconceptApiLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="KitconceptApiLayer:Integration",
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="KitconceptApiLayer:Functional",
)
