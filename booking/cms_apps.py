from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class django_booking(CMSApp):
    app_name = "booking"
    name = _("BOOKING")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["booking.urls"]


apphook_pool.register(django_booking)  # register the application