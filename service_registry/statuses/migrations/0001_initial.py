# Generated by Django 5.0.4 on 2024-04-28 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeProjectStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_installation', models.DateTimeField(auto_now=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=1000)),
                ('color', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='ChangeLayerStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_installation', models.DateTimeField(auto_now=True, unique=True)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='comments.comment')),
            ],
        ),
    ]
