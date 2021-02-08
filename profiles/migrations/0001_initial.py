# Generated by Django 3.1.6 on 2021-02-04 15:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_contact_number', models.CharField(blank=True, max_length=60, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: 05999999999', regex='^0([1-6][0-9]{8,10}|7[0-9]{9})$')])),
                ('default_street_address1', models.CharField(blank=True, max_length=80, null=True)),
                ('default_street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('default_town', models.CharField(blank=True, max_length=40, null=True)),
                ('default_postcode', models.CharField(blank=True, max_length=10, null=True)),
                ('default_counrty', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]