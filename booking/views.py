from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

from .forms import AppointmentForm
from .models import Appointment, Frequency, ServiceArea, CleaningType, BasePrice, Room, Bathroom, ExtraOption
from .serializers import AreaSerializer, CleaningTypeSerializer, BasePriceSerializer, RoomSerializer, BathroomSerializer, ExtraOptsSerializer
from common.mailman import send_html_mail
from geoinfo.models import Country, State, City
from stripe_api import customer
from stripe_api.models import StripeCustomer

class AppointmentCreate(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'booking.html'

    def post(self, request, *args, **kwargs):
        appointment_form = AppointmentForm(request.POST)

        if appointment_form.is_valid():
            if request.POST.get('stripeToken'):
                new_customer = customer.create_customer(request.POST.get('email'))
                new_stripe_customer = StripeCustomer(
                    email=request.POST.get('email'), 
                    token=request.POST.get('stripeToken'),
                    str_customer_id=new_customer.id
                    )
                new_stripe_customer.save()
                
            # result = appointment_form.save()
            # response = send_html_mail(result)

            # print(
            #     f'mail thread created for  {result.id} with email {result.email} {response}')

            # response_data ={
            #     'serviceid': result.id,
            #     'serviceemail': result.email,
            #     'servicefirstname': result.firstname,
            #     'servicelastname': result.lastname,
            #     'servicetotal': result.total,
            # }

            response_data = { 'result': 'todo ok'}

            return JsonResponse(response_data, status=201)
        else:
            errors = appointment_form.errors.get_json_data()
            return JsonResponse(errors, status=500)
            

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
