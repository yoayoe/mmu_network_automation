from django.db import models
from datetime import datetime

class UnitInduk(models.Model):
    LIST_UNIT_INDUK = (
        ('UIW MMU', 'UIW Maluku dan Maluku Utara'),
        ('UIP MALUKU', 'UIP Maluku'),
    )
    unit_induk = models.CharField(max_length=255,choices=LIST_UNIT_INDUK)
    keterangan = models.CharField(max_length=255)
    def __str__(self):
        return "{}".format(self.unit_induk)

class UnitPelaksana(models.Model):
    unit_induk = models.ForeignKey(UnitInduk, null=True, on_delete=models.CASCADE)
    unit_pelaksana = models.CharField(null=True,max_length=255)
    keterangan = models.CharField(max_length=255)
    def __str__(self):
        return "{}".format(self.unit_pelaksana)

class UnitLayanan(models.Model):
    unit_induk = models.ForeignKey(UnitInduk, null=True, on_delete=models.CASCADE)
    unit_pelaksana = models.ForeignKey(UnitPelaksana, null=True, on_delete=models.CASCADE)
    unit_layanan = models.CharField(null=True, max_length=255)
    keterangan = models.CharField(max_length=255)
    def __str__(self):
        return "{}".format(self.unit_layanan)
    
class Device(models.Model):
    ip_address = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField (max_length=255)
    ssh_port = models.IntegerField(default=22)

    VENDOR_CHOICES = (
        ('mikrotik', 'Mikrotik'),
        ('cisco', 'Cisco'),
    )
    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES)
    koordinat = models.CharField(null=True, max_length=255)
    unit_induk = models.ForeignKey(UnitInduk, null=True, on_delete=models.CASCADE)
    unit_pelaksana = models.ForeignKey(UnitPelaksana, null=True, on_delete=models.CASCADE)
    unit_layanan = models.ForeignKey(UnitLayanan, null=True, on_delete=models.CASCADE)
    

    def __str__(self):
        return "{}. {}. {}".format(self.ip_address, self.hostname, self.unit_layanan)

class Log(models.Model):
    target = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)
    messages = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.target, self.action, self.status)