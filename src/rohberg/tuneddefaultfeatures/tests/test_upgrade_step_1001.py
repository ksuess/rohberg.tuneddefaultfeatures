# -*- coding: utf-8 -*-
from plone.app.testing import setRoles, TEST_USER_ID
# from rohberg.tuneddefaultfeatures.testing import ROHBERG_TUNEDDEFAULTFEATURES_FUNCTIONAL_TESTING
from rohberg.tuneddefaultfeatures.testing import (
    ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING,
)

import unittest


class UpgradeStepIntegrationTest(unittest.TestCase):

    layer = ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_upgrade_step(self):
        # dummy, add tests here
        self.assertTrue(True)


# class UpgradeStepFunctionalTest(unittest.TestCase):
#
#     layer = ROHBERG_TUNEDDEFAULTFEATURES_FUNCTIONAL_TESTING
#
#     def setUp(self):
#         self.portal = self.layer['portal']
#         setRoles(self.portal, TEST_USER_ID, ['Manager'])
