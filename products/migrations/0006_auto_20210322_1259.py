# Generated by Django 3.1.6 on 2021-03-22 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210320_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finish',
            name='finish',
            field=models.CharField(max_length=50),
        ),
    ]
