from detimakerlab.wiki.core.plugins import registry
from detimakerlab.wiki.core.plugins.base import BasePlugin


class Plugin(BasePlugin):
    markdown_extensions = [
        "wiki.plugins.redlinks.mdx.redlinks",
    ]


registry.register(Plugin)
