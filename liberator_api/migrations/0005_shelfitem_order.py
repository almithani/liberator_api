# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liberator_api', '0004_auto_20151202_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelfitem',
            name='order',
            field=models.IntegerField(default=1, blank=True),
        ),
    ]
