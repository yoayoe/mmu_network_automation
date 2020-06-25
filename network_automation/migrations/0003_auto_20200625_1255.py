# Generated by Django 3.0.7 on 2020-06-25 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network_automation', '0002_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisasi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_induk', models.CharField(choices=[('uiw mmu', 'UIW Maluku dan Maluku Utara'), ('uip maluku', 'UIP Maluku')], max_length=255)),
                ('unit_pelaksana', models.CharField(choices=[('UIW Maluku dan Maluku Utara', 'UIW Maluku dan Maluku Utara'), ('UIP Maluku', 'UIP Maluku'), ('UP3 Ambon', 'UP3 Ambon'), ('UP3 Masohi', 'UP3 Masohi'), ('UP3 Tual', 'UP3 Tual'), ('UP3 Saumlaki', 'UP3 Saumlaki'), ('UP3 Ternate', 'UP3 Ternate'), ('UP3 Sofifi', 'UP3 Sofifi'), ('UP3 Tobelo', 'UP3 Tobelo'), ('UPK Maluku', 'UPK Maluku'), ('UPP Maluku', 'UPP Maluku'), ('UPP Maluku Utara', 'UPP Maluku Utara')], max_length=255, null=True)),
                ('unit_layanan', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='koordinat',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='lokasi_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='network_automation.Organisasi'),
        ),
    ]