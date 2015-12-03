# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liberator_api', '0003_auto_20151202_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('creator', models.ForeignKey(to='liberator_api.UserMeta')),
            ],
        ),
        migrations.CreateModel(
            name='ShelfItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quote', models.CharField(max_length=140, blank=True)),
                ('item', models.ForeignKey(to='liberator_api.Book')),
                ('shelf', models.ForeignKey(to='liberator_api.Shelf')),
            ],
        ),
        migrations.AddField(
            model_name='shelf',
            name='items',
            field=models.ManyToManyField(to='liberator_api.Book', through='liberator_api.ShelfItem'),
        ),
    ]
