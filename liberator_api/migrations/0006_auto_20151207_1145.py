# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('liberator_api', '0005_shelfitem_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shelfitem',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='shelf',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
