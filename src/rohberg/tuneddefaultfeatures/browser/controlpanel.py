from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.autoform import directives
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from plone import schema
from zope.component import adapter
from zope.interface import Interface


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
