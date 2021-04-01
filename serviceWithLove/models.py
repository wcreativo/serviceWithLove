from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Add additional choices through the ``settings.py``.
def get_templates():
    choices = [
        ('cleaning/card_img_left.html', _('Cleaning Image Left')),
        ('cleaning/card_img_right.html', _('Cleaning Image Right')),
        ('organizing/card_img_left.html', _('Organizing Image Left')),
        ('organizing/card_img_right.html', _('Organizing Image Right')),
        ('decorating/card_img_right.html', _('Decorating Image Right')),
    ]
    choices += getattr(
        settings,
        'DJANGOCMS_PICTURE_TEMPLATES',
        [],
    )
    return choices


class CardService(CMSPlugin):
    title = models.TextField(max_length=50, default='Service')
    description = models.TextField(max_length=1000, default='Description')
    image = models.ImageField(upload_to='images/')
    logo = models.ImageField(upload_to='logos/')
    template = models.CharField(
        verbose_name=_('Template'),
        choices=get_templates(),
        default=get_templates()[0][0],
        max_length=255,
    )
