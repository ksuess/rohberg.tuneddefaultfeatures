# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.browser.contact_info import ContactForm


class ContactFormCustom(ContactForm):
    """Redirect /contact-info to page suggestions with status 404,

    if flag is set in control panel.
    """

    def __call__(self):
        """Redirect if the flag is set in control panel."""
        exclude_default_contact_form = api.portal.get_registry_record("tdf.exclude_default_contact_form", default=False)
        if exclude_default_contact_form:
            return self.response.redirect(self.context.portal_url() + '/kontakt')
        return super(ContactFormCustom, self).__call__()
