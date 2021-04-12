from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView


from .forms import AppointmentForm
from .models import Appointment, Frequency, ServiceArea, CleaningType, BasePrice, Room, Bathroom, ExtraOption
from .serializers import FrequencySerializer, AreaSerializer, CleaningTypeSerializer, BasePriceSerializer, RoomSerializer, BathroomSerializer, ExtraOptsSerializer
from common.mailman import send_html_mail
from geoinfo.models import Country, State, City


class AppointmentCreate(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'booking.html'
    success_url = reverse_lazy('booking:new_booking')

    def post(self, request, *args, **kwargs):
        appointment_form = AppointmentForm(request.POST)

        if appointment_form.is_valid():
            result = appointment_form.save()
            response = send_html_mail(result)
            print(
                f'mail thread created for  {result.id} with email {result.email} {response}')
            return self.form_valid(appointment_form)
        else:
            print(appointment_form.errors)
            return self.form_invalid(appointment_form.errors)


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


class GetDiscount(RetrieveAPIView):
    lookup_field = 'id'
    queryset = Frequency.objects.all()
    serializer_class = FrequencySerializer


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
