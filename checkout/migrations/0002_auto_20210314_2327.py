# Generated by Django 3.1.6 on 2021-03-14 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='lineitem_total',
            new_name='orderitem_total',
        ),
    ]
