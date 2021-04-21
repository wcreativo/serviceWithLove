from django.contrib import admin
from .models import Appointment, DateTimeDisabler, Charge, ChargeHistory


admin.site.register(Appointment)
admin.site.register(DateTimeDisabler)
admin.site.register(Charge)
admin.site.register(ChargeHistory)