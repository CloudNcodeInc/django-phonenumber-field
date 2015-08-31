# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], serialize=False, primary_key=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', phonenumber_field.modelfields.LowerCaseCharField(serialize=False, primary_key=True, max_length=2)),
                ('name', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='CountryCode',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('code', models.ForeignKey(related_name='country_codes', to='phonenumber_field.Code')),
                ('country', models.ForeignKey(related_name='country_codes', to='phonenumber_field.Country')),
            ],
            options={
                'ordering': ('country', 'code'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='countrycode',
            unique_together=set([('country', 'code')]),
        ),
    ]
