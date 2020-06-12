from django.urls import re_path
from django.utils.translation import gettext as _

from detimakerlab.wiki.core.plugins import registry
from detimakerlab.wiki.core.plugins.base import BasePlugin
from detimakerlab.wiki.plugins.article_dependencies import forms, views


class ArticleDependenciesPlugin(BasePlugin):
    slug = "dependencies"
    urlpatterns = {
        "article": [
            re_path(
                r"^test/$",
                views.DependenciesView.as_view(),
                name="dependencies_view",
            ),
        ]
    }

    sidebar = {
        "headline": _("Equipment"),
        "icon_class": "fa-tools",
        "template": "wiki/plugins/article_dependencies/dependencies_form.html",
        "form_class": forms.CreateDependencieForm,
        "get_form_kwargs": (lambda a: {}),
    }

    markdown_extensions = []


registry.register(ArticleDependenciesPlugin)
