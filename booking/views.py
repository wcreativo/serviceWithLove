import json
import os

from datetime import date

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView

from . import stripe
from .forms import AppointmentForm
from .models import Appointment, Frequency, ServiceArea, CleaningType, BasePrice, Room, Bathroom, ExtraOption, ChargeHistory, Charge, DateTimeDisabler
from .serializers import AreaSerializer, CleaningTypeSerializer, BasePriceSerializer, RoomSerializer, BathroomSerializer, ExtraOptsSerializer, DateTimeDisablerSerializer
from common.mailman import send_html_mail
from geoinfo.models import Country, State, City
from stripe_api import customer, charge

class AppointmentCreate(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'booking.html'
    

    def post(self, request, *args, **kwargs):
        appointment_form = AppointmentForm(request.POST)

        if appointment_form.is_valid():
            if request.POST.get('stripeToken'):
                new_charge = charge.create_charge(request)

                if 'err' in new_charge:
                    response = {
                        'card_info': [
                            {
                                'message': new_charge['message'],
                                'code': new_charge['code']
                            }
                        ]
                    }
                    return JsonResponse(response, status=new_charge['status'])

                if new_charge['captured'] != True:
                    response = {
                        'card_info': [
                            {
                                'message': 'charge info could not be captured',
                                'code': ''
                            }
                        ]
                    }
                    return JsonResponse(response, status=400)
                    
                    
                order_result = appointment_form.save()
                charge_registry = Charge(stripe_id=new_charge['id'], order=order_result, last_status=new_charge['status'])
                charge_registry.save()
                charge_history = ChargeHistory(stripe_id=charge_registry, stripe_status=new_charge['status'] )
                charge_history.save()

                charge.update_charge(order_result, new_charge['id'])

                response = send_html_mail(order_result)

                print(
                    f'mail thread created for  {order_result.id} with email {order_result.email} {response}')

                response_data ={
                    'serviceid': order_result.id,
                    'serviceemail': order_result.email,
                    'servicefirstname': order_result.firstname,
                    'servicelastname': order_result.lastname,
                    'servicetotal': order_result.total,
                }
                return JsonResponse(response_data, status=201)
                
            else:
                response = {
                        'stripeToken': [
                            {
                                'message': 'stripeToken is not valid',
                                'code': ''
                            }
                        ]
                    }
                return JsonResponse(response, status=400)
        else:
            errors = appointment_form.errors.get_json_data()
            return JsonResponse(errors, status=400)
            

class ListStates(ListView):
    model = State
    template_name = 'booking/state_dropdown.html'

    def get_queryset(self):
        filter = self.request.GET.get('country')
        states = State.objects.filter(country=filter, is_active=True)
        return states

    def get_context_data(self, **kwargs):
        context = super(ListStates, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('country')
        return context


class ListCities(ListView):
    model = City
    template_name = 'booking/city_dropdown.html'

    def get_queryset(self):
        filter = self.request.GET.get('state')
        cities = City.objects.filter(state=filter, is_active=True)
        return cities

    def get_context_data(self, **kwargs):
        context = super(ListCities, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('state')
        return context


class GetAreaPrice(RetrieveAPIView):
    lookup_field = 'id'
    queryset = ServiceArea.objects.all()
    serializer_class = AreaSerializer


class GetCleaningTypePrice(RetrieveAPIView):
    lookup_field = 'id'
    queryset = CleaningType.objects.all()
    serializer_class = CleaningTypeSerializer


class GetBasePrice(RetrieveAPIView):
    lookup_field = 'id'
    queryset = BasePrice.objects.all()
    serializer_class = BasePriceSerializer


class GetRoomPrice(RetrieveAPIView):
    lookup_field = 'id'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetBathroomPrice(RetrieveAPIView):
    lookup_field = 'id'
    queryset = Bathroom.objects.all()
    serializer_class = BathroomSerializer


class GetExtraOptPrice(APIView):

    serializer_class = ExtraOptsSerializer

    def post(self, request, format=None, *args, **kwargs):
        extraopts_list = request.data
        result = ExtraOption.objects.filter(id__in=extraopts_list)
        if request.method == 'POST':
            response = self.serializer_class(result, many=True)
            return JsonResponse(response.data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebHook(APIView):
        
    def post(self, request, format=None, *args, **kwargs):
        stripe_secret_signature = os.environ.get('STRIPE_SECRET_SIGNATURE')
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        body = json.loads(request.body)
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, stripe_secret_signature
            )
        except ValueError as e:
            # invalid payload
            print(f'### err {e}')
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(f'### err {e}')
            return HttpResponse(status=400)

        if event.type == 'charge.refund.updated':
            try:
                charge = Charge.objects.get(stripe_id=body['data']['object']['charge'])
            except Charge.DoesNotExist:
                charge = None
                print(f"[ERROR] in webhook stripe order # {body['data']['object']['charge']} not found")
                return JsonResponse({}, status=404)

            charge_history = ChargeHistory(stripe_id=charge, stripe_status='refund')
            charge_history.save()
            charge.last_status='refund'
            charge.save()
        else:
            print(f'Unhandled event type in webhook {event.type}')

        return JsonResponse({}, status=200)


class ListBlockedTime(ListAPIView):
    today = date.today()
    queryset = DateTimeDisabler.objects.filter(from_date__gt=today)
    serializer_class = DateTimeDisablerSerializer


class ListExtraOptions(ListView):
    model = ExtraOption
    template_name = 'snippets/extra_options.html'

    def get_queryset(self):
        options = ExtraOption.objects.filter(is_active=True)
        print(options)
        return options

    def get_context_data(self, **kwargs):
        context = super(ListExtraOptions, self).get_context_data(**kwargs)
        return context
