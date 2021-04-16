from .enums import GainEntry, Pets, CovidExposure
from .validators import validate_date_greater
from common.models import CommonData
from geoinfo.models import City, State, Country
from datetime import date
from datetime import time

from django.db.models import CharField, BooleanField, ForeignKey, DO_NOTHING, EmailField, IntegerField, TextField, ManyToManyField, FloatField, DateField, TimeField
from django_enumfield.enum import EnumField


class BasePrice(CommonData):
    description: str = CharField(verbose_name='Description', max_length=100)
    price: int = FloatField(verbose_name='price')
    
    def __str__(self) -> str:
        return f'{self.description}'


class ServiceArea(CommonData):
    description: str = CharField(verbose_name='area', max_length=30)
    price: int = IntegerField(verbose_name='area price')
    minutes: int = IntegerField(verbose_name='estimated service time (in minutes)', default=0)

    def __str__(self) -> str:
        return f'{self.description}'

    class Meta:
        ordering = ['id']


class CleaningType(CommonData):
    description: str = CharField(verbose_name='service type', max_length=30)
    price: int = IntegerField(verbose_name='cleaning price')
    minutes: int = IntegerField(verbose_name='estimated service time (in minutes)', default=0)

    def __str__(self) -> str:
        return f'{self.description}'


class Room(CommonData):
    description: str = CharField(verbose_name='room types', max_length=30)
    price: int = IntegerField(verbose_name='room price')
    minutes: int = IntegerField(verbose_name='estimated service time (in minutes)', default=0)

    def __str__(self) -> str:
        return f'{self.description}'
    
    class Meta:
        ordering = ['id']


class Bathroom(CommonData):
    description: str = CharField(verbose_name='bathroom types', max_length=30)
    price: int = IntegerField(verbose_name='bathroom price')
    minutes: int = IntegerField(verbose_name='estimated service time (in minutes)', default=0)

    def __str__(self) -> str:
        return f'{self.description}'
    
    class Meta:
        ordering = ['id']


class Frequency(CommonData):
    description: str = CharField(verbose_name='frequency', max_length=50)
    discount: int = IntegerField(verbose_name='frequency price')

    def __str__(self) -> str:
        return f'{self.description}'

class ExtraOption(CommonData):
    description: str = CharField(verbose_name='option', max_length=100)
    price: int = IntegerField(verbose_name='option price')
    icon: str = CharField(verbose_name='option icon', max_length=100)
    minutes: int = IntegerField(verbose_name='estimated service time (in minutes)', default=0)
    is_active: bool = BooleanField(verbose_name='active?', default=True)

    def __str__(self) -> str:
        return f'{self.description}'

class Flexibility(CommonData):
    description: str = CharField(verbose_name='description', max_length=30)

    def __str__(self) -> str:
        return f'{self.description}'

class Appointment(CommonData):
    city: City = ForeignKey(City, on_delete=DO_NOTHING)
    state: State = ForeignKey(State, on_delete=DO_NOTHING)
    country: Country = ForeignKey(Country, on_delete=DO_NOTHING)
    firstname: str = CharField(verbose_name='First Name', max_length=100)
    lastname: str = CharField(verbose_name='Last Name', max_length=100)
    phone: str = CharField(verbose_name='Phone Number', max_length=50)
    email: str = EmailField(verbose_name='email')
    address: str = CharField(verbose_name='address', max_length=300)
    suite: str = CharField(verbose_name='app/suite', max_length=50)
    zipcode: str = CharField(verbose_name='zipcode', max_length=50)
    area: ServiceArea = ForeignKey(ServiceArea, on_delete=DO_NOTHING)
    cleaning_type: CleaningType = ForeignKey(CleaningType, on_delete=DO_NOTHING, blank=True, null=True)
    maid_qty: str = CharField(verbose_name='Maid Qty', max_length=20, blank=True, null=True)
    hours_qty: str = CharField(verbose_name="Hours", max_length=5, blank=True, null=True)
    room_type: Room = ForeignKey(Room, on_delete=DO_NOTHING, blank=True, null=True)
    bathroom: Bathroom = ForeignKey(Bathroom, on_delete=DO_NOTHING, blank=True, null=True)
    frequency: Frequency = ForeignKey(Frequency, on_delete=DO_NOTHING)
    extra_opts: ExtraOption = ManyToManyField(ExtraOption, blank=True)
    flexibility: Flexibility = ManyToManyField(Flexibility, blank=True)
    date: date = DateField(verbose_name='date', blank=False, null=False, validators=[validate_date_greater])
    time: time = TimeField(verbose_name='time', blank=False, null=False)
    subtotal: float = FloatField(verbose_name='subtotal')
    tax: float = FloatField(verbose_name='tax')
    total: float = FloatField(verbose_name='total')
    estimated_time: int = IntegerField(verbose_name='Total estimated time')

    entry: GainEntry = EnumField(verbose_name='gain entry', enum=GainEntry)
    pets: Pets = EnumField(verbose_name='pets', enum=Pets)
    covid: CovidExposure = EnumField(verbose_name='covid exposure', enum=CovidExposure)
    comments: str = TextField(verbose_name='Customer Comments', blank=True, null=True)


    def __str__(self) -> str:
        return f'{self.date}-{self.time} / {self.address} / ${self.total} / {self.area}'

    class Meta:
        ordering = ['date']


class DateTimeDisabler(CommonData):
    from_date: date = DateField(verbose_name='From this date', blank=False, null=False)
    to_date: date = DateField(verbose_name='To this date', blank=False, null=False)
    from_time: time = TimeField(verbose_name='From this time', blank=False, null=False)
    to_time: time = TimeField(verbose_name='To this time', blank=False, null=False)
    comment: str = CharField(verbose_name='Comment', max_length=100, default='No comment')

    def __str__(self) -> str:
        return f'{self.comment} <--> From:{self.from_date} {self.from_time} To: {self.to_date} {self.to_time}'
    
    class Meta:
        ordering = ['from_date']
