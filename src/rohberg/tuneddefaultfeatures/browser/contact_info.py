# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone import PloneMessageFactory as _pmf
from Products.CMFPlone.browser.contact_info import ContactForm
from zope.i18n import translate
from zope.globalrequest import getRequest


class ContactFormCustom(ContactForm):
    """Redirect /contact-info to page suggestions with status 404,

    if flag is set in control panel.
    """

    def __call__(self):
        """Redirect if the flag is set in control panel."""
        exclude_default_contact_form = api.portal.get_registry_record("tdf.exclude_default_contact_form", default=False)
        if exclude_default_contact_form:
            # https://6.docs.plone.org/i18n-l10n/translating-text-strings.html#manually-translated-message-ids
            # Translate some text
            msgid = _pmf("Contact")  # my_text is zope.

            # Use inherited translate() function to get the final text string
            translated = translate(msgid, context=getRequest())
            translated_lowercase = translated.lower()

            return self.request.response.redirect(self.context.portal_url() + '/' + translated_lowercase)
        return super(ContactFormCustom, self).__call__()
