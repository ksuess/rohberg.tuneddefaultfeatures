# -*- coding: utf8 -*-
from plone.app.querystring.interfaces import IParsedQueryIndexModifier
from zope.interface import implementer


@implementer(IParsedQueryIndexModifier)
class Subject(object):

    """
    The Subject field in Plone currently uses a utf-8 encoded string.
    When a catalog query tries to compare a unicode string from the
    parsedquery with existing utf-8 encoded string indexes unindexing
    will fail with a UnicodeDecodeError. To prevent this from happening
    we always encode the Subject query.

    XXX: As soon as Plone uses unicode for all indexes, this code can
    be removed.
    """

    def __call__(self, value):
        return ('Subject', value)
