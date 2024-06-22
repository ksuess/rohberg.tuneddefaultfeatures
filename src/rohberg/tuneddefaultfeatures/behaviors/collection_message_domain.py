# -*- coding: utf-8 -*-

from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from rohberg.tuneddefaultfeatures import _
from zope.component import adapter
from zope.interface import implementer, Interface, provider


class ICollectionMessageDomainMarker(Interface):
    pass


@provider(IFormFieldProvider)
class ICollectionMessageDomain(model.Schema):
    """ """

    message_factory_domain = schema.TextLine(
        title=_("message_factory_domain"),
        description=_("Type in a message factory domain name"),
        required=False,
        default="plone",
    )


@implementer(ICollectionMessageDomain)
@adapter(ICollectionMessageDomainMarker)
class CollectionMessageDomain(object):
    def __init__(self, context):
        self.context = context

    @property
    def message_factory_domain(self):
        if safe_hasattr(self.context, "message_factory_domain"):
            return self.context.message_factory_domain
        return None

    @message_factory_domain.setter
    def message_factory_domain(self, value):
        self.context.message_factory_domain = value
