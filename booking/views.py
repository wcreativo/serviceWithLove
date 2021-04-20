from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

from .forms import AppointmentForm
from .models import Appointment, Frequency, ServiceArea, CleaningType, BasePrice, Room, Bathroom, ExtraOption, ChargeHistory
from .serializers import AreaSerializer, CleaningTypeSerializer, BasePriceSerializer, RoomSerializer, BathroomSerializer, ExtraOptsSerializer
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
                        'card': [
                            {
                                'message': new_charge['message'],
                                'code': new_charge['code']
                            }
                        ]
                    }
                    return JsonResponse(response, status=new_charge['status'])

                if new_charge['captured'] != True:
                    response = {
                        'card': [
                            {
                                'message': 'charge info could not be captured',
                                'code': ''
                            }
                        ]
                    }
                    return JsonResponse(response, status=400)
                    
                    
                order_result = appointment_form.save()
                charge_history = ChargeHistory(order=order_result, stripe_id=new_charge['id'], stripe_status=new_charge['status'] )
                charge_history.save()
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
