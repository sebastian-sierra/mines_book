# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mines_book', '0005_auto_20151107_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='option',
            field=models.CharField(max_length=6, choices=[(b'GSI', b'GSI'), (b'OMTI', b'OMTI'), (b'GIPAD', b'GIPAD'), (b'QSF', b'QSF'), (b'GOPL', b'GOPL'), (b'AII', b'AII'), (b'NSTE', b'NSTE'), (b'STAR', b'STAR'), (b'GSE', b'GSE'), (b'GE', b'GE')]),
        ),
    ]
