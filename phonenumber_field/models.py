# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.core import validators
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from . import modelfields


@python_2_unicode_compatible
class Country(models.Model):
    class Meta:
        verbose_name_plural = 'Countries'

    id = modelfields.UpperCaseCharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{0.name} ({0.id})'.format(self)


@python_2_unicode_compatible
class Code(models.Model):
    class Meta:
        ordering = ('id', )

    id = models.PositiveSmallIntegerField(primary_key=True, validators=[validators.MinValueValidator(1)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{0.id}'.format(self)


class CountryCodeManager(models.Manager):
    def get_by_natural_key(self, country, code):
        return self.get(country=country, code=code)


@python_2_unicode_compatible
class CountryCode(models.Model):
    class Meta:
        unique_together = ('country', 'code')
        ordering = unique_together

    objects = CountryCodeManager()

    country = models.ForeignKey(Country, related_name='country_codes')
    code = models.ForeignKey(Code, related_name='country_codes')
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{0.country}, +{0.code}'.format(self)
