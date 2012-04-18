from Products.CMFCore.utils import getToolByName
from plone.testing import z2
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
from zope.component import getMultiAdapter


class NoIndexingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Install product
        z2.installProduct(app, 'collective.noindexing')
        # Load ZCML
        import collective.noindexing
        xmlconfig.file('configure.zcml', collective.noindexing,
                      context=configurationContext)

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.noindexing')


class NoIndexingAppliedLayer(NoIndexingLayer):

    def testSetUp(self):
        from collective.noindexing import patches
        patches.apply()

    def testTearDown(self):
        from collective.noindexing import patches
        patches.unapply()


NOINDEXING_FIXTURE = NoIndexingLayer()
NOINDEXING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NOINDEXING_FIXTURE,), name="NoIndexing:Integration")

NOINDEXING_APPLIED_FIXTURE = NoIndexingAppliedLayer()
NOINDEXING_APPLIED_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NOINDEXING_APPLIED_FIXTURE,), name="NoIndexingApplied:Integration")

# A few helper functions.


def make_test_doc(portal, transition=None):
    new_id = portal.generateUniqueId('Document')
    portal.invokeFactory('Document', new_id)
    doc = portal[new_id]
    if transition is not None:
        wf_tool = getToolByName(portal, 'portal_workflow')
        wf_tool.doActionFor(doc, transition)
    doc.reindexObject()  # Might have already happened, but let's be sure.
    return doc


def apply_patches(portal):
    """Apply patches.

    We could just do this:

    from collective.noindexing import patches
    patches.apply()

    But it is good to use the browser view here.
    """
    view = getMultiAdapter((portal, portal.REQUEST),
                            name='collective-noindexing-apply')
    view()


def unapply_patches(portal):
    view = getMultiAdapter((portal, portal.REQUEST),
                            name='collective-noindexing-unapply')
    view()
