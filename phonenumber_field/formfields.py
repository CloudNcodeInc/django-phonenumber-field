#-*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _, string_concat
from django.forms.fields import CharField
from django.core.exceptions import ValidationError
from phonenumber_field.validators import validate_international_phonenumber
from phonenumber_field.phonenumber import to_python
from phonenumber_field.widgets import PhoneNumberWidget


class PhoneNumberField(CharField):
    widget = PhoneNumberWidget
    default_error_messages = {
        'invalid': _(u'Enter a valid phone number.'),
    }
    default_validators = [validate_international_phonenumber]

    def to_python(self, value):
        phone_number = to_python(value)
        if phone_number and not phone_number.is_valid():
            msg = string_concat(
                self.error_messages['invalid'],
                u" The provided value, {0}, is invalid.".format(phone_number.raw_input)
            )
            raise ValidationError(msg)
        return phone_number
