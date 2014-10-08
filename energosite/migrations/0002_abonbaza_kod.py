# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('energosite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='abonbaza',
            name='kod',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True),
            preserve_default=True,
        ),
    ]
