from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_date_greater(value):
    present = date.today()
    
    if value <= present:
        raise ValidationError(
            _('%(value)s is not greater than today'),
            params={'value': value},
        )