# Generated by Django 3.0.6 on 2020-05-27 06:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agreement', '0004_agreement_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buyer',
            name='profile',
            field=models.ImageField(default='profile/default.jpg', upload_to='profile'),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='id_number',
            field=models.IntegerField(unique=True),
        ),
    ]
