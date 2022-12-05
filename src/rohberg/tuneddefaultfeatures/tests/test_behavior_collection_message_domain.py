# -*- coding: utf-8 -*-
from plone.app.testing import setRoles, TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from rohberg.tuneddefaultfeatures.behaviors.collection_message_domain import (
    ICollectionMessageDomainMarker,
)
from rohberg.tuneddefaultfeatures.testing import (
    ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING  # noqa,
)
from zope.component import getUtility

import unittest


class CollectionMessageDomainIntegrationTest(unittest.TestCase):

    layer = ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_collection_message_domain(self):
        behavior = getUtility(IBehavior, 'rohberg.tuneddefaultfeatures.collection_message_domain')
        self.assertEqual(
            behavior.marker,
            ICollectionMessageDomainMarker,
        )
