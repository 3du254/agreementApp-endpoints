# Generated by Django 3.0.6 on 2020-05-14 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agreement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyer',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='updated_date',
        ),
        migrations.RemoveField(
            model_name='buyer',
            name='updated_user',
        ),
    ]
