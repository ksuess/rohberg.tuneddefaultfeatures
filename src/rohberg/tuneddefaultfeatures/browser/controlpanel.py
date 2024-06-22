from plone import schema
from plone.app.discussion import _ as _pad
from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope.component import adapter
from zope.interface import Interface


import json


VOCABULARY_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "titles": {
                            "type": "object",
                            "properties": {
                                "lang": {"type": "string"},
                                "title": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
    }
)


# class IVocabularyItem(Interface):
#     vocabularyItemToken = schema.TextLine(title="vocabulary item token", description="Bitte keine Umlaute, Satzzeichen oder Leerzeichen im token bitte.", required=True)
#     vocabularyItemValue = schema.TextLine(title="vocabulary item value", required=False)


class ITDFControlPanel(Interface):

    sitemappathstobeexcluded = schema.List(
        title='Sitemap paths to be excluded (/sitemap.xml.gz)',
        default=[],
        missing_value=[],
        required=False,
        value_type=schema.TextLine(),
    )

    moderator_notification_enabled = schema.Bool(
        title=_pad(
            "label_moderator_notification_enabled",
            default="Enable moderator email notification",
        ),
        description=_pad(
            "help_moderator_notification_enabled",
            default="If selected, the moderator is notified if a comment "
            "needs attention. The moderator email address can "
            "be set below.",
        ),
        required=False,
        default=False,
    )
    stopwords = schema.List(
        title='Stop words which mark email as spam',
        default=[],
        missing_value=[],
        required=False,
        value_type=schema.TextLine(),
    )

    exclude_default_contact_form = schema.Bool(
        title=_pad(
            "label_exclude_default_contact_form",
            default="Disable default contact form /contact-info",
        ),
        required=False,
        default=False,
    )

    informationtype = schema.JSONField(
        title="informationtype",
        required=False,
        schema=VOCABULARY_SCHEMA,
        widget="vocabularyterms",
        default={
            "items": [
                {
                    "token": "manual",
                    "titles": {
                        "en": "Manual",
                        "de": "Anleitung",
                    },
                },
            ]
        },
        missing_value={"items": []},
    )


@adapter(Interface, Interface)
class TDFControlPanel(RegistryConfigletPanel):
    schema = ITDFControlPanel
    schema_prefix = 'tdf'
    configlet_id = 'tdf-controlpanel'
    configlet_category_id = 'Products'
    title = 'TDF Settings'
    group = ''


class TDFControlPanelForm(RegistryEditForm):
    schema = ITDFControlPanel
    schema_prefix = 'tdf'
    label = 'TDF Settings'


TDFControlPanelView = layout.wrap_form(
    TDFControlPanelForm, ControlPanelFormWrapper)
