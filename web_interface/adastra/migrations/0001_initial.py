# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-17 17:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='TaskListModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adastra.ProjectModel')),
            ],
        ),
        migrations.CreateModel(
            name='TaskModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('description', models.CharField(blank=True, max_length=10000)),
                ('expiration_date', models.DateTimeField(blank=True)),
                ('status', models.IntegerField(choices=[(0, 'CREATED'), (1, 'IN_WORK'), (2, 'DONE')])),
                ('priority', models.IntegerField(choices=[(0, 'LOW'), (1, 'MIDDLE'), (2, 'HIGH')])),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('task_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adastra.TaskListModel')),
            ],
        ),
        migrations.CreateModel(
            name='UserProjectRelationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adastra.ProjectModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
