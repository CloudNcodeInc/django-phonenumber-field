# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core import validators as dj_validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.six import string_types
from django.utils.translation import ugettext_lazy as _

from . import formfields, phonenumber, validators


class LowerCaseCharField(models.CharField):

    def get_prep_value(self, value):
        """Return data in a format that has been prepared for use as a parameter in a query."""
        value = super(LowerCaseCharField, self).get_prep_value(value)
        return value.lower() if value else value

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            value = value.lower()
        setattr(model_instance, self.attname, value)
        return value


class PhoneNumberDescriptor(object):
    """
    The descriptor for the phone number attribute on the model instance.
    Returns a PhoneNumber when accessed so you can do stuff like::

        >>> instance.phone_number.as_international

    Assigns a phone number object on assignment so you can do::

        >>> instance.phone_number = PhoneNumber(...)
    or
        >>> instance.phone_number = '+414204242'
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '{0.field.name}' attribute can only be accessed from {1.__name__} instances.".format(self, owner)
            )
        return getattr(instance, self.field.name)

    def __set__(self, instance, value):
        setattr(instance, self.field.name, instance.to_python(value))


class PhoneNumberField(models.Field):
    attr_class = phonenumber.PhoneNumber
    descriptor_class = PhoneNumberDescriptor
    default_validators = [validators.validate_international_phonenumber]

    description = _('Phone number')

    def __init__(self, *args, **kwargs):
        # 128 for longest phone number + 2 for country id + 1 for comma
        kwargs.setdefault('max_length', 131)
        super(PhoneNumberField, self).__init__(*args, **kwargs)
        self.validators.append(dj_validators.MaxLengthValidator(self.max_length))

    def get_internal_type(self):
        return 'CharField'

    def get_prep_value(self, value):
        """Returns field's value prepared for saving into a database."""
        value = self.to_python(value)  # self.attr_class or None
        if isinstance(value, self.attr_class):
            format_string = getattr(settings, 'PHONENUMBER_DB_FORMAT', 'E164')
            fmt = self.attr_class.format_map[format_string]
            pieces = [value.format_as(fmt)]
            if value.country_id:
                pieces.insert(0, value.country_id)
            value = self.attr_class.country_id_sep.join(pieces)
        else:
            if not self.null:
                value = ''
        return value

    def to_python(self, value):
        if isinstance(value, string_types):
            value = phonenumber.to_python(value)
        if value is None or isinstance(value, self.attr_class):
            return value
        raise ValidationError("'{0}' is an invalid value.".format(value))

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': formfields.PhoneNumberField}
        defaults.update(kwargs)
        return super(PhoneNumberField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([
        (
            [PhoneNumberField],
            [],
            {}
        ),
    ], ['^phonenumber_field\.modelfields\.PhoneNumberField'])
except ImportError:
    pass
