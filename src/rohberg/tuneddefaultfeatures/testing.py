# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import rohberg.tuneddefaultfeatures


class RohbergTuneddefaultfeaturesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=rohberg.tuneddefaultfeatures)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rohberg.tuneddefaultfeatures:default')


ROHBERG_TUNEDDEFAULTFEATURES_FIXTURE = RohbergTuneddefaultfeaturesLayer()


ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ROHBERG_TUNEDDEFAULTFEATURES_FIXTURE,),
    name='RohbergTuneddefaultfeaturesLayer:IntegrationTesting',
)


ROHBERG_TUNEDDEFAULTFEATURES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ROHBERG_TUNEDDEFAULTFEATURES_FIXTURE,),
    name='RohbergTuneddefaultfeaturesLayer:FunctionalTesting',
)


ROHBERG_TUNEDDEFAULTFEATURES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ROHBERG_TUNEDDEFAULTFEATURES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='RohbergTuneddefaultfeaturesLayer:AcceptanceTesting',
)
