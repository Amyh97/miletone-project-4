# Generated by Django 3.1.6 on 2021-03-24 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_orderitem_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='image',
            field=models.ImageField(default='default img', upload_to=''),
            preserve_default=False,
        ),
    ]