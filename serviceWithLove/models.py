from cms.models.pluginmodel import CMSPlugin
from django.db import models


class CardService(CMSPlugin):
    title = models.CharField(max_length=50, default='Service')
    description = models.CharField(max_length=1000, default='Description')
