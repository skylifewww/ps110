# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-26 18:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200)),
                ('classroom_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 26, 18, 43, 39, 387414, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 26, 18, 43, 39, 385107, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='parent',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 26, 18, 43, 39, 386900, tzinfo=utc)),
        ),
    ]
