# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class CaseInsensitiveCharField(models.CharField):

    def db_type(self, connection):
        return 'varchar({0.max_length}) collate nocase'.format(self)
