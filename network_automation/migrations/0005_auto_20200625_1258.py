# Generated by Django 3.0.7 on 2020-06-25 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network_automation', '0004_device_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='unit',
            new_name='Keterangan',
        ),
    ]