# -*- coding: utf-8 -*-

# from rohberg.tuneddefaultfeatures import _
from plone.app.contenttypes.browser.collection import CollectionView
from Products.CMFPlone.utils import safe_callable
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


_ = MessageFactory("plone")


class ITabularViewPlus(Interface):
    """Marker Interface for ITabularViewPlus"""


class TabularViewPlus(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('tabular_view_plus.pt')

    def tabular_fielddata_plus(self, item, fieldname):
        print("item", item)
        value = getattr(item, fieldname, "")
        if safe_callable(value):
            value = value()
        if fieldname in [
            "CreationDate",
            "ModificationDate",
            "Date",
            "EffectiveDate",
            "ExpirationDate",
            "effective",
            "expires",
            "start",
            "end",
            "created",
            "modified",
            "last_comment_date",
        ]:
            value = self.toLocalizedTime(value, long_format=1)

        return {"title": _(fieldname, default=fieldname), "value": value}

    def __call__(self):
        # Implement your own actions:
        return super(TabularViewPlus, self).__call__()
