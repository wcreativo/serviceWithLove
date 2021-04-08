from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import CardService, CardCleaning


@plugin_pool.register_plugin
class CardServicePlugin(CMSPluginBase):
    model = CardService
    cache = False

    def get_render_template(self, context, instance, placeholder):
        return '{}'.format(instance.template)


@plugin_pool.register_plugin
class CardCleaningPlugin(CMSPluginBase):
    model = CardCleaning
    cache = False

    def get_render_template(self, context, instance, placeholder):
        return '{}'.format(instance.template)
