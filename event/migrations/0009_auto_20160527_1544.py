# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-27 15:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_auto_20160527_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 27, 15, 44, 18, 705283, tzinfo=utc)),
        ),
    ]
