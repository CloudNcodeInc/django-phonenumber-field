# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from phonenumber_field.fields.models.caseinsensitivecharfield import CaseInsensitiveCharField
from phonenumber_field.modelfields import PhoneNumberField


class TestModel(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    phone = PhoneNumberField()


class TestModelBlankPhone(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    phone = PhoneNumberField(blank=True)


class CICharFieldTestModel(models.Model):
    value = CaseInsensitiveCharField(primary_key=True, max_length=1)
