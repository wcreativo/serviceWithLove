from common.models import CommonData
from django.db.models import CharField, BooleanField, TextField, IntegerField, ForeignKey, CASCADE

class Country(CommonData):
    model_name = 'Country'
    name: str = CharField(verbose_name='name', max_length=200, null=False, blank=False)
    region: str = CharField(verbose_name='region', max_length=100, null=True)
    alpha2: str = CharField(verbose_name='alpha2', max_length=2, null=False, blank=False)
    alpha3: str = CharField(verbose_name='alpha3', max_length=3, null=False, blank=False)
    numeric: str = CharField(verbose_name='numeric', max_length=4, null=False, blank=False)
    is_active: bool = BooleanField(verbose_name='is active?', default=False)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class State(CommonData):
    model_name = 'State'
    name: str = CharField(verbose_name='name', max_length=200, null=False, blank=False)
    code: str = CharField(verbose_name='code', max_length=2, null=False, blank=False)
    country: str = ForeignKey(Country, on_delete=CASCADE)
    is_active: bool = BooleanField(verbose_name='is active?', default=False)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class City(CommonData):
    model_name = 'City'
    name: str = CharField(verbose_name='name', max_length=200, null=False, blank=False)
    state: str = ForeignKey(State, on_delete=CASCADE)
    is_active: bool = BooleanField(verbose_name='is active?', default=False)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        ordering = ['name']