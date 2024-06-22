# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from rohberg.tuneddefaultfeatures.testing import (
    ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING  # noqa: E501,,,,
)

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that rohberg.tuneddefaultfeatures is properly installed."""

    layer = ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if rohberg.tuneddefaultfeatures is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'rohberg.tuneddefaultfeatures'))

    def test_browserlayer(self):
        """Test that IRohbergTuneddefaultfeaturesLayer is registered."""
        from rohberg.tuneddefaultfeatures.interfaces import (
            IRohbergTuneddefaultfeaturesLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IRohbergTuneddefaultfeaturesLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = ROHBERG_TUNEDDEFAULTFEATURES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['rohberg.tuneddefaultfeatures'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if rohberg.tuneddefaultfeatures is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'rohberg.tuneddefaultfeatures'))

    def test_browserlayer_removed(self):
        """Test that IRohbergTuneddefaultfeaturesLayer is removed."""
        from rohberg.tuneddefaultfeatures.interfaces import \
            IRohbergTuneddefaultfeaturesLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IRohbergTuneddefaultfeaturesLayer,
            utils.registered_layers())
