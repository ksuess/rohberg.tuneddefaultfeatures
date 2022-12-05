"""The default comment class and factory.

Changes
- No notification of moderator if stopword found.
"""
from Acquisition import aq_parent
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.discussion import _
from plone.app.discussion.comment import MAIL_NOTIFICATION_MESSAGE_MODERATOR
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from Products.CMFPlone.utils import safe_unicode
from smtplib import SMTPException
from zope.component import getUtility, queryUtility
from zope.i18n import translate
from zope.i18nmessageid import Message

import logging


logger = logging.getLogger("rohberg.tuneddefaultfeatures")


def notify_moderator(obj, event):
    print("*** tuneddefaultfeatures. custom notify_moderator marking emails with stopwords as spam.")
    """Tell the moderator when a comment needs attention.

    This method sends an email to the moderator if comment moderation a new
    comment has been added that needs to be approved.

    The moderator_notification setting has to be enabled in the discussion
    control panel.

    Configure the moderator e-mail address in the discussion control panel.
    If no moderator is configured but moderator notifications are turned on,
    the site admin email (from the mail control panel) will be used.
    """
    # Check if moderator notification is enabled
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IDiscussionSettings, check=False)
    # if not settings.moderator_notification_enabled:
    #     return
    moderator_notification_enabled = api.portal.get_registry_record('tdf.moderator_notification_enabled')
    if not moderator_notification_enabled:
        logger.debug("Moderator notification not enabled.")
        return

    # No notification of moderator if stopword found.
    stopwords = api.portal.get_registry_record('tdf.stopwords')
    for stopword in stopwords:
        print("stopword", stopword)
        if stopword in obj.text:
            try:
                with api.env.adopt_roles(['Reviewer']):
                    api.content.transition(obj=obj, transition='mark_as_spam')
                    print(f"$$$ Comment marked as spam! {stopword}\n {obj.text}")
                    return  # No notification of moderator if stopword found.
            except InvalidParameterError as e:
                print(f"<<< DEBUG {e}. Transition could not be executed.")

    # Get informations that are necessary to send an email
    mail_host = getToolByName(obj, "MailHost")
    registry = getUtility(IRegistry)
    mail_settings = registry.forInterface(IMailSchema, prefix="plone")
    sender = mail_settings.email_from_address

    if settings.moderator_email:
        mto = settings.moderator_email
    else:
        mto = sender

    # Check if a sender address is available
    if not sender:
        return

    conversation = aq_parent(obj)
    content_object = aq_parent(conversation)

    # Compose email
    subject = translate(_("A comment has been posted."), context=obj.REQUEST)
    message = translate(
        Message(
            MAIL_NOTIFICATION_MESSAGE_MODERATOR,
            mapping={
                "title": safe_unicode(content_object.title),
                "link": content_object.absolute_url() + "/view#" + obj.id,
                "text": obj.text,
                "commentator": obj.author_email
                or translate(
                    Message(
                        _(
                            "label_anonymous",
                            default="Anonymous",
                        ),
                    ),
                ),
            },
        ),
        context=obj.REQUEST,
    )

    # Send email
    try:
        mail_host.send(message, mto, sender, subject, charset="utf-8")
    except SMTPException as e:
        logger.error(
            "SMTP exception (%s) while trying to send an "
            + "email notification to the comment moderator "
            + "(from %s to %s, message: %s)",
            e,
            sender,
            mto,
            message,
        )
