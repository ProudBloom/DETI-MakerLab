from django.apps import AppConfig
from django.core.checks import register
from django.utils.translation import gettext_lazy as _

from detimakerlab.wiki.core.plugins.loader import load_wiki_plugins
from . import checks


# from wiki.core.plugins.loader import load_wiki_plugins


class WikiConfig(AppConfig):
    # default_site = "wiki.sites.WikiSite"
    default_site = "detimakerlab.wiki.sites.WikiSite"
    name = "detimakerlab.wiki"
    verbose_name = _("Wiki")

    def ready(self):
        register(
            checks.check_for_required_installed_apps,
            checks.Tags.required_installed_apps,
        )
        register(
            checks.check_for_obsolete_installed_apps,
            checks.Tags.obsolete_installed_apps,
        )
        register(checks.check_for_context_processors, checks.Tags.context_processors)
        register(
            checks.check_for_fields_in_custom_user_model,
            checks.Tags.fields_in_custom_user_model,
        )
        load_wiki_plugins()
