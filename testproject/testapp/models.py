# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from phonenumber_field import modelfields


class TestModel(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    phone = modelfields.PhoneNumberField()


class TestModelBlankPhone(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    phone = modelfields.PhoneNumberField(blank=True)


class LowerCaseCharFieldTestModel(models.Model):
    value = modelfields.LowerCaseCharField(primary_key=True, max_length=1)
