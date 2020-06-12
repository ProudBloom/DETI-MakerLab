from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EditSectionConfig(AppConfig):
    name = "detimakerlab.wiki.plugins.editsection"
    verbose_name = _("Wiki edit section")
    label = "wiki_editsection"
