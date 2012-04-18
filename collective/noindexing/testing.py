from Products.CMFCore.utils import getToolByName
from plone.testing import z2
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
#from plone.app.testing import applyProfile
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


NOINDEXING_FIXTURE = NoIndexingLayer()
NOINDEXING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NOINDEXING_FIXTURE,), name="NoIndexing:Integration")

# A few helper functions.


def make_test_doc(portal, transition=None):
    new_id = portal.invokeFactory('Document', 'doc')
    doc = portal[new_id]
    if transition is not None:
        wf_tool = getToolByName(portal, 'portal_workflow')
        wf_tool.doActionFor(doc, transition)
    doc.reindexObject()  # Might have already happened, but let's be sure.
    return doc


def apply_patches(portal):
    view = getMultiAdapter((portal, portal.REQUEST),
                            name='collective-noindexing-apply')
    view()


def unapply_patches(portal):
    view = getMultiAdapter((portal, portal.REQUEST),
                            name='collective-noindexing-unapply')
    view()
