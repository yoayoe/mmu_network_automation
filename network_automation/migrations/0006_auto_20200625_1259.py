# Generated by Django 3.0.7 on 2020-06-25 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network_automation', '0005_auto_20200625_1258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='Keterangan',
            new_name='unit',
        ),
    ]