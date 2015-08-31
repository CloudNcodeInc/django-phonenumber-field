"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils.encoding import force_text

from phonenumber_field.phonenumber import PhoneNumber, to_python
from testapp import models


class PhonenumberFieldAppTest(TestCase):

    def test_to_python_country_id_parse(self):
        value = PhoneNumber.country_id_sep.join(['CH', '+41524242424'])
        self.assertEqual(to_python(value).country_id, 'CH')
        self.assertIsNone(to_python('+41524242424').country_id)

    def test_save_field_to_database(self):
        instance = models.TestModel()
        instance.phone = '+41 52 424 2424'
        instance.full_clean()
        instance.save()
        instance = models.TestModel.objects.get(pk=instance.pk)
        self.assertIsInstance(instance.phone, PhoneNumber)
        self.assertEqual(force_text(instance.phone), '+41524242424')
        self.assertIsNone(instance.phone.country_id)
        instance.phone = PhoneNumber.country_id_sep.join(['CH', force_text(instance.phone)])
        instance.save()
        instance = models.TestModel.objects.get(pk=instance.pk)
        self.assertEqual(instance.phone.country_id, 'CH')

    def test_save_blank_phone_to_database(self):
        instance = models.TestModelBlankPhone()
        instance.save()
        instance = models.TestModelBlankPhone.objects.get(pk=instance.pk)
        self.assertIsNone(instance.phone)


class LowerCaseCharFieldTestModelTestCase(TestCase):

    def test_integrity_error(self):
        models.LowerCaseCharFieldTestModel.objects.create(value='a')
        self.assertEqual(models.LowerCaseCharFieldTestModel.objects.count(), 1)
        with self.assertRaises(IntegrityError):
            models.LowerCaseCharFieldTestModel.objects.create(value='A')

    def test_max_length(self):
        instance = models.LowerCaseCharFieldTestModel(value='bb')
        with self.assertRaises(ValidationError):
            instance.full_clean()

    def test_max_length_db(self):
        models.LowerCaseCharFieldTestModel.objects.create(value='bb')
        self.assertNotEqual(models.LowerCaseCharFieldTestModel.objects.all()[0].value.lower(), 'bb')

    def test_max_length_db_truncates(self):
        models.LowerCaseCharFieldTestModel.objects.create(value='bb')
        self.assertEqual(models.LowerCaseCharFieldTestModel.objects.all()[0].value.lower(), 'b')

    def test_create_and_lookup_convert_case(self):
        models.LowerCaseCharFieldTestModel.objects.create(value='a')
        self.assertEqual(models.LowerCaseCharFieldTestModel.objects.count(), 1)
        A = models.LowerCaseCharFieldTestModel.objects.get(value='A')
        self.assertEqual(A.value, 'a')

    def test_create_convert_case_and_lookup(self):
        a = models.LowerCaseCharFieldTestModel.objects.create(value='A')
        self.assertEqual(a.value, 'a')
        self.assertEqual(models.LowerCaseCharFieldTestModel.objects.count(), 1)
        A = models.LowerCaseCharFieldTestModel.objects.get(value='a')
        self.assertEqual(A.value, 'a')
