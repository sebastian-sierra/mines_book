# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mines_book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', to='mines_book.Student'),
        ),
    ]
