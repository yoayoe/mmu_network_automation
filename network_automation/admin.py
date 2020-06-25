from django.contrib import admin
from network_automation.models import Device, Organisasi

class ListDevice(admin.ModelAdmin):
    list_display = ['hostname','lokasi_unit', 'ip_address', 'vendor']
    search_fields = ['lokasi_unit', 'ip_address', 'hostname', 'vendor']
    list_per_page = 5

admin.site.register(Device, ListDevice)
admin.site.register(Organisasi)
