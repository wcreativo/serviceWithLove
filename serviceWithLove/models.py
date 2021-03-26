from cms.models.pluginmodel import CMSPlugin
from django.db import models


class CardService(CMSPlugin):
    title = models.TextField(max_length=50, default='Service')
    description = models.TextField(max_length=1000, default='Description')
    image = models.ImageField(upload_to='images/')
    logo = models.ImageField(upload_to='logos/')
