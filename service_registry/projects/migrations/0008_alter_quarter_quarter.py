# Generated by Django 5.0.4 on 2024-05-26 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_quarter_quarter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quarter',
            name='quarter',
            field=models.CharField(choices=[('Q1', 'q1'), ('Q2', 'q2'), ('Q3', 'q3'), ('Q4', 'q4')], max_length=9),
        ),
    ]
