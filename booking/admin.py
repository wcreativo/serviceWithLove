from django.contrib import admin
from .models import Appointment, DateTimeDisabler, Charge, ChargeHistory, CleaningType, ExtraOption, ServiceArea, CleaningTypePrice


admin.site.register(Appointment)
admin.site.register(DateTimeDisabler)
admin.site.register(Charge)
admin.site.register(ChargeHistory)
admin.site.register(CleaningType)
admin.site.register(ExtraOption)
admin.site.register(ServiceArea)
admin.site.register(CleaningTypePrice)

