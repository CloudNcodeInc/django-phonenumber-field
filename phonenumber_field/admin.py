# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.encoding import force_text

from . import models


class CountryCodeInline(admin.TabularInline):
    model = models.CountryCode


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active', 'codes')
    inlines = (CountryCodeInline, )
    extra = 0

    def codes(self, country):
        ids = list(country.country_codes.values_list('code__id', flat=True).distinct())
        ids.sort()
        return ', '.join([force_text(i) for i in ids])


@admin.register(models.Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'active', 'countries')
    inlines = (CountryCodeInline, )
    extra = 0

    def countries(self, code):
        names = list(code.country_codes.values_list('country__name', flat=True).distinct())
        names.sort()
        return ', '.join(names)


@admin.register(models.CountryCode)
class CountryCodeAdmin(admin.ModelAdmin):
    list_display = (
        'get_country_id', 'get_country_name', 'get_code_id', 'get_country_active', 'get_code_active', 'active',
        'all_active'
    )

    def get_country_id(self, country_code):
        return country_code.country.id
    get_country_id.short_description = 'Country ID'
    get_country_id.admin_order_field = 'country__id'

    def get_country_name(self, country_code):
        return country_code.country.name
    get_country_name.short_description = 'Country Name'
    get_country_name.admin_order_field = 'country__name'

    def get_country_active(self, country_code):
        if country_code.country.active:
            return '<img src="/static/admin/img/icon-yes.gif" alt="True" />'
        return '<img src="/static/admin/img/icon-no.gif" alt="False" />'
    get_country_active.short_description = 'Country Active'
    get_country_active.admin_order_field = 'country__active'
    get_country_active.allow_tags = True

    def get_code_id(self, country_code):
        return country_code.code.id
    get_code_id.short_description = 'Code ID'
    get_code_id.admin_order_field = 'code__id'

    def get_code_active(self, country_code):
        if country_code.code.active:
            return '<img src="/static/admin/img/icon-yes.gif" alt="True" />'
        return '<img src="/static/admin/img/icon-no.gif" alt="False" />'
    get_code_active.short_description = 'Code Active'
    get_code_active.admin_order_field = 'code__active'
    get_code_active.allow_tags = True

    def all_active(self, country_code):
        if country_code.active and country_code.country.active and country_code.code.active:
            return '<img src="/static/admin/img/icon-yes.gif" alt="True" />'
        return '<img src="/static/admin/img/icon-no.gif" alt="False" />'
    all_active.allow_tags = True
