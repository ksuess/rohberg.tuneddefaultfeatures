# -*- coding: utf-8 -*-

from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from rohberg.tuneddefaultfeatures import _
from zope.component import adapter
from zope.interface import implementer, Interface, provider


class IInformationTypeMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IInformationType(model.Schema):
    """
    """

    informationtype = schema.List(
        title=_("informationtype"),
        value_type=schema.Choice(vocabulary="rohberg.tuneddefaultfeatures.informationtype"),
        required=False,
    )


@implementer(IInformationType)
@adapter(IInformationTypeMarker)
class InformationType(object):
    def __init__(self, context):
        self.context = context

    @property
    def informationtype(self):
        if safe_hasattr(self.context, 'informationtype'):
            return self.context.informationtype
        return None

    @informationtype.setter
    def informationtype(self, value):
        self.context.informationtype = value
