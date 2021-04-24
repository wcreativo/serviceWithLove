from django.urls import path

from .views import AppointmentCreate, ListStates, ListCities, GetAreaPrice, GetCleaningTypePrice, GetBasePrice, GetRoomPrice, GetBathroomPrice, GetExtraOptPrice, StripeWebHook, ListBlockedTime, ListExtraOptions

app_name = 'appointments'

urlpatterns = [    
    path('', AppointmentCreate.as_view(), name='new_booking'),
    path('ajax/load-states/', ListStates.as_view(), name='ajax_load_states'),
    path('ajax/load-cities/', ListCities.as_view(), name='ajax_load_cities'),
    path('ajax/load-options/', ListExtraOptions.as_view(), name='ajax_load_options'),
    path('ajax/get-area-price/<int:id>/', GetAreaPrice.as_view(), name='ajax_get_area_price'),
    path('ajax/get-cleaningtype-price/', GetCleaningTypePrice.as_view(), name='ajax_get_cleaningtype_price'),
    path('ajax/get-base-price/<int:id>/', GetBasePrice.as_view(), name='ajax_get_base_price'),
    path('ajax/get-room-price/<int:id>/', GetRoomPrice.as_view(), name='ajax_get_room_price'),
    path('ajax/get-bathroom-price/<int:id>/', GetBathroomPrice.as_view(), name='ajax_get_bathroom_price'),
    path('ajax/get-extraopts-price/', GetExtraOptPrice.as_view(), name='ajax_get_extraops_price'),
    path('ajax/get-blocked-times/', ListBlockedTime.as_view(), name='ajax_get_blocked_time'),
    path('stripe_webhook/', StripeWebHook.as_view(), name='refund_webhook')
]
