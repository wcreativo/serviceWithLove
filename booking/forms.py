from django import forms
from .models import Appointment, ExtraOption
from geoinfo.models import City, State, Country


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = [
            'country',
            'state',
            'city',
            'firstname',
            'lastname',
            'phone',
            'email',
            'address',
            'suite',
            'zipcode',
            'date',
            'time',
            'area',
            'cleaning_type',
            'maid_qty',
            'hours_qty',
            'room_type',
            'bathroom',
            'frequency',
            'extra_opts',
            'flexibility',
            'entry',
            'pets',
            'pets',
            'covid',
            'comments',
            'subtotal',
            'discount',
            'tax',
            'total'
        ]

        HOUR_CHOICES = [( (x+1)/2, f'{(x+1)/2} hours' ) for x in range(3, 24)]
        MAID_CHOICES = [(x, f'{x} maids ' if x > 1 else f'{x} maid') for x in range(1, 6)]
        
        widgets = {
           'country': forms.Select(),
           'state': forms.Select(),
           'city': forms.Select(),
           'address': forms.TextInput(attrs={'placeholder': 'address where the service is needed'}),
           'email': forms.EmailInput(attrs={'placeholder': 'contact email'}),
           'suite': forms.TextInput(attrs={'placeholder': 'apt/suite'}),
           'zipcode': forms.TextInput(attrs={'placeholder': 'zipcode'}),
           'area': forms.Select(),
           'cleaning_type': forms.Select(),
           'room_type': forms.Select(),
           'bathroom': forms.Select(),
           'frequency': forms.Select(),
           'extra_opts': forms.CheckboxSelectMultiple(),
           'flexibility': forms.CheckboxSelectMultiple(),
           'entry': forms.Select(),
           'pets': forms.Select(),
           'covid': forms.Select(),
           'comments': forms.Textarea(),
           'maid_qty': forms.Select(choices=MAID_CHOICES, attrs={'style': 'display: none'}),
           'hours_qty': forms.Select(choices=HOUR_CHOICES, attrs={'style': 'display: none'}),
           'firstname': forms.TextInput(attrs={'placeholder': 'First Name'}),
           'lastname': forms.TextInput(attrs={'placeholder': 'Last Name'}),
           'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
           'date': forms.DateInput(format='%d/%m/%Y'),
           'time': forms.TimeInput(format='HH:MM'),
           'subtotal': forms.HiddenInput(),
           'discount': forms.HiddenInput(),
           'tax': forms.HiddenInput(),
           'total': forms.HiddenInput()
        }

        
        labels = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.fields['area'].empty_label = None
        self.fields['cleaning_type'].empty_label = None
        self.fields['room_type'].empty_label = None
        self.fields['bathroom'].empty_label = None
        self.fields['frequency'].empty_label = None
        self.fields['country'].empty_label = None
        self.fields['state'].empty_label = None
        self.fields['city'].empty_label = None
        self.fields['country'].queryset = Country.objects.filter(is_active=True)
        self.fields['extra_opts'].queryset = ExtraOption.objects.filter(is_active=True)
