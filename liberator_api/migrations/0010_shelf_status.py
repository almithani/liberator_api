# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liberator_api', '0009_book_amazon_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelf',
            name='status',
            field=models.IntegerField(default=1, choices=[(0, b'PRIVATE'), (1, b'PUBLIC'), (2, b'FRONTPAGE')]),
        ),
    ]
