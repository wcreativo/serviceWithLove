from django import forms
from .models import Appointment, ExtraOption
from geoinfo.models import City, State, Country

input_styles = 'rounded-lg border-transparent flex-1 appearance-none border border-gray-300 w-full py-2 px-4 bg-white' \
               ' text-gray-700 placeholder-gray-400 shadow-sm text-base focus:outline-none focus:ring-2' \
               ' focus:ring-purple-600 focus:border-transparent my-2'

select_styles = 'block w-52 text-gray-700 py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm' \
                'focus:outline-none focus:ring-primary-500 focus:border-primary-500 my-2'

textarea_styles = 'flex-1 appearance-none border border-gray-300 w-full py-2 px-4 bg-white text-gray-700' \
                  'placeholder-gray-400 rounded-lg text-base focus:outline-none focus:ring-2 ' \
                  'focus:ring-purple-600 focus:border-transparent'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment

        fields = [
            'firstname',
            'lastname',
            'email',
            'phone',
            'address',
            'suite',
            'country',
            'state',
            'city',
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

        HOUR_CHOICES = [((x + 1) / 2, f'{(x + 1) / 2} hours') for x in range(3, 24)]
        MAID_CHOICES = [(x, f'{x} maids ' if x > 1 else f'{x} maid') for x in range(1, 6)]

        widgets = {
            'country': forms.Select(attrs={'class': select_styles}),
            'state': forms.Select(attrs={'class': select_styles}),
            'city': forms.Select(attrs={'class': select_styles}),
            'address': forms.TextInput(
                attrs={'placeholder': 'Address where the service is needed', 'class': input_styles}),
            'email': forms.EmailInput(attrs={'placeholder': 'Contact Email',
                                             'class': input_styles}),
            'suite': forms.TextInput(attrs={'placeholder': 'Apt/Suite', 'class': input_styles}),
            'zipcode': forms.TextInput(attrs={'placeholder': 'zipcode', 'class': input_styles}),
            'area': forms.Select(attrs={'class': select_styles}),
            'cleaning_type': forms.Select(attrs={'class': select_styles}),
            'room_type': forms.Select(attrs={'class': select_styles}),
            'bathroom': forms.Select(attrs={'class': select_styles}),
            'frequency': forms.Select(attrs={'class': select_styles}),
            'extra_opts': forms.CheckboxSelectMultiple(),
            'flexibility': forms.CheckboxSelectMultiple(),
            'entry': forms.Select(attrs={'class': select_styles}),
            'pets': forms.Select(attrs={'class': select_styles}),
            'covid': forms.Select(attrs={'class': select_styles}),
            'comments': forms.Textarea(attrs={'class': textarea_styles}),
            'maid_qty': forms.Select(choices=MAID_CHOICES, attrs={'style': 'display: none', 'class': select_styles}),
            'hours_qty': forms.Select(choices=HOUR_CHOICES, attrs={'style': 'display: none', 'class': select_styles}),
            'firstname': forms.TextInput(attrs={'placeholder': 'First Name',
                                                'class': input_styles}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name',
                                               'class': input_styles}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number',
                                            'class': input_styles}),
            'date': forms.DateInput(format='%d/%m/%Y',
                                    attrs={'placeholder': 'Click to Choose a Date',
                                           'class': input_styles}),
            'time': forms.TimeInput(format='HH:MM', attrs={'placeholder': '--:--',
                                                           'class': input_styles}),
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
