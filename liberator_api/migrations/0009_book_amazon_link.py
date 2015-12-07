# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liberator_api', '0008_auto_20151207_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='amazon_link',
            field=models.CharField(max_length=2083, blank=True),
        ),
    ]
