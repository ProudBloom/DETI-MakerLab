from django.urls import re_path

from detimakerlab.wiki.core.plugins import registry
from detimakerlab.wiki.core.plugins.base import BasePlugin
from . import settings, views


class NotifyPlugin(BasePlugin):
    slug = settings.SLUG
    urlpatterns = {
        "root": [
            re_path(
                r"^$",
                views.NotificationSettings.as_view(),
                name="notification_settings",
            ),
        ]
    }

    article_view = views.NotificationSettings().dispatch

    settings_form = "wiki.plugins.notifications.forms.SubscriptionForm"


registry.register(NotifyPlugin)
