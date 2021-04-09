from django.contrib import admin
from .models import Appointment, DateTimeDisabler


admin.site.register(Appointment)
admin.site.register(DateTimeDisabler)