# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import phonenumbers
from django.db import models
from django.test import TestCase
try:
    from django.test import override_settings
except ImportError:
    # Django <1.7
    from django.test.utils import override_settings
from phonenumber_field import modelfields, phonenumber


###############
# Test Models #
###############

class MandatoryPhoneNumber(models.Model):

    phone_number = modelfields.PhoneNumberField()


class OptionalPhoneNumber(models.Model):

    phone_number = modelfields.PhoneNumberField(blank=True, default='')


##############
# Test Cases #
##############


class PhoneNumberFieldTestCase(TestCase):

    test_number_1 = '+414204242'
    equal_number_strings = ['+44 113 8921113', '+441138921113']
    local_numbers = [
        ('GB', '01606 751 78'),
        ('DE', '0176/96842671')
    ]
    storage_numbers = {
        'E164': ['+44 113 8921113', '+441138921113'],
        'RFC3966': ['+44 113 8921113', 'tel:+44-113-892-1113'],
        'INTERNATIONAL': ['+44 113 8921113', '+44 113 892 1113']
    }
    invalid_numbers = ['+44 113 892111']

    def test_valid_numbers_are_valid(self):
        numbers = [phonenumber.PhoneNumber.from_string(s) for s in self.equal_number_strings]
        self.assertTrue(all(n.is_valid() for n in numbers))
        numbers = [phonenumber.PhoneNumber.from_string(s, region=r) for r, s in self.local_numbers]
        self.assertTrue(all(n.is_valid() for n in numbers))

    def test_invalid_numbers_are_invalid(self):
        numbers = [phonenumber.PhoneNumber.from_string(s) for s in self.invalid_numbers]
        self.assertTrue(all(not n.is_valid() for n in numbers))

    def test_objects_with_same_number_are_equal(self):
        numbers = [MandatoryPhoneNumber.objects.create(phone_number=s).phone_number for s in self.equal_number_strings]
        self.assertTrue(
            all(phonenumbers.is_number_match(n, numbers[0]) == phonenumbers.MatchType.EXACT_MATCH for n in numbers)
        )

    def test_field_returns_correct_type(self):
        model = OptionalPhoneNumber()
        self.assertIsNone(model.phone_number)
        model.phone_number = '+49 176 96842671'
        self.assertIsInstance(model.phone_number, phonenumber.PhoneNumber)

    def test_can_assign_string_phone_number(self):
        opt_phone = OptionalPhoneNumber()
        opt_phone.phone_number = self.test_number_1
        self.assertIsInstance(opt_phone.phone_number, phonenumber.PhoneNumber)
        self.assertEqual(opt_phone.phone_number.as_e164, self.test_number_1)

    def test_does_not_fail_on_invalid_values(self):
        # testcase for
        # https://github.com/stefanfoulis/django-phonenumber-field/issues/11
        phone = phonenumber.to_python(42)
        self.assertIsNone(phone)

    def test_storage_formats(self):
        """Perform aggregate tests for all db storage formats."""
        for phone_format in phonenumber.PhoneNumber.format_map:
            with override_settings(PHONENUMBER_DB_FORMAT=phone_format):
                self.test_objects_with_same_number_are_equal()
                self.test_field_returns_correct_type()
                self.test_can_assign_string_phone_number()

    def test_prep_value(self):
        """
        Tests correct db storage value against different setting of PHONENUMBER_DB_FORMAT.
        Required output format is set as string constant to guarantee consistent database storage values.
        """
        number = modelfields.PhoneNumberField()
        for phone_format in ('E164', 'RFC3966', 'INTERNATIONAL'):
            with override_settings(PHONENUMBER_DB_FORMAT=phone_format):
                self.assertEqual(
                    number.get_prep_value(phonenumber.to_python(self.storage_numbers[phone_format][0])),
                    self.storage_numbers[phone_format][1], msg=phone_format
                )
