# Generated by Django 3.1.6 on 2021-02-08 17:49

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210208_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='default_counrty',
            field=django_countries.fields.CountryField(default='GB', max_length=2),
        ),
    ]
