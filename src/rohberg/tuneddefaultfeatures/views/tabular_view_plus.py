# -*- coding: utf-8 -*-

# from rohberg.tuneddefaultfeatures import _
from plone.app.contenttypes.browser.collection import CollectionView
from plone.app.vocabularies.metadatafields import get_field_label
from plone.dexterity.utils import iterSchemata
from plone.restapi.interfaces import IFieldSerializer
from Products.CMFPlone.utils import safe_callable
from z3c.relationfield.interfaces import IRelationValue
from zope.component import getMultiAdapter
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ITabularViewPlus(Interface):
    """Marker Interface for ITabularViewPlus"""


class TabularViewPlus(CollectionView):
    """Translate column headers. Transform values with field vocabularies"""

    def __init__(self, context, request):
        super(TabularViewPlus, self).__init__(context, request)
        self.message_factory_domain = self.context.message_factory_domain or "plone"

    def tabular_field_label(self, fieldname):
        """Return the internationalized label corresponding
        to the field.
        """
        fieldname_translated = self.context.translate(
            fieldname, domain=self.message_factory_domain, default=fieldname
        )
        if fieldname_translated == fieldname:
            fieldname_translated = get_field_label(fieldname)
        return fieldname_translated

    def serialize(self, fieldname, value, type_object):
        field = None
        for schema in iterSchemata(type_object):
            if fieldname in schema:
                field = schema.get(fieldname)
                break
        # dm = getMultiAdapter((type_object, field), IDataManager)
        # dm.set(value)
        if not field:
            return "Dieses Feld gibts hier nicht."
        serializer = getMultiAdapter(
            (field, type_object, self.request), IFieldSerializer
        )
        return serializer()

    def tabular_fielddata_plus(self, item, fieldname):
        """Serialize field value"""
        value = getattr(item, fieldname, "")
        if safe_callable(value):
            value = value()
        elif fieldname in [
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
        else:
            type_object = item.getObject()
            if IRelationValue.providedBy(value):
                value = value.to_object.title
            elif isinstance(value, list):
                if len(value) == 0:
                    pass
                elif IRelationValue.providedBy(value[0]):
                    new_value = []
                    for el in value:
                        new_value.append(el.to_object.title)
                    value = new_value
                else:
                    new_value = []
                    for el in value:
                        el = self.serialize(fieldname, el, type_object)
                        if isinstance(el, dict):
                            new_value.append(el.get("title"))
                        else:
                            new_value.append(el)
                    value = new_value
                value = ", ".join(value)
            else:
                value = self.serialize(fieldname, value, type_object)
                if isinstance(value, dict):
                    value = value.get("title")
                elif isinstance(value, list):
                    if len(value) == 0:
                        pass
                    elif isinstance(value[0], dict):
                        new_value = []
                        for el in value:
                            new_value.append(el["title"] or el["token"])
                        value = new_value
                    else:
                        new_value = []
                        for el in value:
                            new_value.append(el)
                        value = new_value
                    value = ", ".join(value)
                else:
                    pass

        return {
            "title": self.context.translate(
                fieldname, domain=self.message_factory_domain, default=fieldname
            ),
            "value": value,
        }

    def __call__(self):
        # Implement your own actions:
        return super(TabularViewPlus, self).__call__()
