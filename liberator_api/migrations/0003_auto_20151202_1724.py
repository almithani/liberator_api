# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liberator_api', '0002_usermeta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=600)),
                ('author', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('cover', models.ImageField(upload_to=b'covers/', blank=True)),
                ('ISBN', models.CharField(max_length=14, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='usermeta',
            name='avatar',
            field=models.ImageField(upload_to=b'user_avatars/', blank=True),
        ),
        migrations.AlterField(
            model_name='usermeta',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='usermeta',
            name='displayName',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='usermeta',
            name='tagline',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
