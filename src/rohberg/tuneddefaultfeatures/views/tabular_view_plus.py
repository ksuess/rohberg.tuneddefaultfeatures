# -*- coding: utf-8 -*-

# from rohberg.tuneddefaultfeatures import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ITabularViewPlus(Interface):
    """ Marker Interface for ITabularViewPlus"""


class TabularViewPlus(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('tabular_view_plus.pt')

    def __call__(self):
        # Implement your own actions:
        return super(TabularViewPlus, self).__call__()
