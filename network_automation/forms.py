from django.forms import ModelForm
from network_automation.models import Device


class FormDevice(ModelForm):
    class Meta:
        model = Device
        exclude = ['unit']
        # fields = '__all__'