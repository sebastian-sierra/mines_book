# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mines_book', '0006_auto_20151112_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='prom',
            field=models.CharField(max_length=4),
        ),
    ]
