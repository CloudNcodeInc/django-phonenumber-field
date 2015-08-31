# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _

from . import phonenumber, validators, widgets


class PhoneNumberField(CharField):
    widget = widgets.PhoneNumberWidget
    default_error_messages = {
        'invalid': _('Enter a valid phone number.')
    }
    default_validators = [validators.validate_international_phonenumber]

    def to_python(self, value):
        phone_number = phonenumber.to_python(value)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages['invalid'])
        return phone_number
