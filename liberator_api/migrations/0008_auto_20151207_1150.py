# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liberator_api', '0007_auto_20151207_1149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shelf',
            options={'ordering': ['-date_added']},
        ),
    ]
