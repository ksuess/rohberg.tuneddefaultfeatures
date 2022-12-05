# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from rohberg.tuneddefaultfeatures.testing import (
    ROHBERG_TUNEDDEFAULTFEATURES_FUNCTIONAL_TESTING,
    ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING,
)
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_tabular_view_plus_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='tabular_view_plus'
        )
        self.assertTrue(view.__name__ == 'tabular_view_plus')
        # self.assertTrue(
        #     'Sample View' in view(),
        #     'Sample View is not found in tabular_view_plus'
        # )

    def test_tabular_view_plus_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='tabular_view_plus'
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = ROHBERG_TUNEDDEFAULTFEATURES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
