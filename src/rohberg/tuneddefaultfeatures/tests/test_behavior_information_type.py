# -*- coding: utf-8 -*-
from plone.app.testing import setRoles, TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from rohberg.tuneddefaultfeatures.behaviors.information_type import (
    IInformationTypeMarker,
)
from rohberg.tuneddefaultfeatures.testing import (
    ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING  # noqa,
)
from zope.component import getUtility

import unittest


class InformationTypeIntegrationTest(unittest.TestCase):

    layer = ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_information_type(self):
        behavior = getUtility(IBehavior, 'rohberg.tuneddefaultfeatures.information_type')
        self.assertEqual(
            behavior.marker,
            IInformationTypeMarker,
        )
