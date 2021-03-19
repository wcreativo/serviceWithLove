from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext_lazy as _
from .models import CardService


@plugin_pool.register_plugin
class CardServicePlugin(CMSPluginBase):
    model = CardService
    render_template = "card_service.html"
    cache = False
