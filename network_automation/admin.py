from django.contrib import admin
from network_automation.models import Device, UnitInduk, UnitPelaksana, UnitLayanan

class ListDevice(admin.ModelAdmin):
    list_display = ['hostname', 'ip_address', 'vendor']
    search_fields = ['ip_address', 'hostname', 'vendor']
    list_per_page = 5

admin.site.register(UnitInduk)
admin.site.register(UnitPelaksana)
admin.site.register(UnitLayanan)
admin.site.register(Device, ListDevice)


