from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import CardService


@plugin_pool.register_plugin
class CardServicePlugin(CMSPluginBase):
    model = CardService
    cache = False

    def get_render_template(self, context, instance, placeholder):
        return '{}'.format(instance.template)
