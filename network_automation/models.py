from django.db import models
from datetime import datetime

class Organisasi(models.Model):
    LIST_UNIT_INDUK = (
        ('uiw mmu', 'UIW Maluku dan Maluku Utara'),
        ('uip maluku', 'UIP Maluku'),
    )
    unit_induk = models.CharField(max_length=255,choices=LIST_UNIT_INDUK)
    LIST_UNIT_PELAKSANA = (
        ('UIW Maluku dan Maluku Utara', 'UIW Maluku dan Maluku Utara'),
        ('UIP Maluku', 'UIP Maluku'),
        ('UP3 Ambon', 'UP3 Ambon'),
        ('UP3 Masohi', 'UP3 Masohi'),
        ('UP3 Tual', 'UP3 Tual'),
        ('UP3 Saumlaki', 'UP3 Saumlaki'),
        ('UP3 Ternate', 'UP3 Ternate'),
        ('UP3 Sofifi', 'UP3 Sofifi'),
        ('UP3 Tobelo', 'UP3 Tobelo'),
        ('UPK Maluku', 'UPK Maluku'),
        ('UPP Maluku', 'UPP Maluku'),
        ('UPP Maluku Utara', 'UPP Maluku Utara'),
    )
    unit_pelaksana = models.CharField(null=True,max_length=255,choices=LIST_UNIT_PELAKSANA)
    unit_layanan = models.CharField(null=True, max_length=255)

    def __str__(self):
        return "{}".format(self.unit_layanan)
    
class Device(models.Model):
    ip_address = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    ssh_port = models.IntegerField(default=22)

    VENDOR_CHOICES = (
        ('mikrotik', 'Mikrotik'),
        ('cisco', 'Cisco'),
    )
    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES)
    koordinat = models.CharField(null=True, max_length=255)
    lokasi_unit = models.ForeignKey(Organisasi, null=True, on_delete=models.CASCADE)
    unit = models.CharField(null=True, max_length=255)

    def __str__(self):
        return "{}. {}. {}".format(self.ip_address, self.hostname, self.unit)

class Log(models.Model):
    target = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)
    messages = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.target, self.action, self.status)