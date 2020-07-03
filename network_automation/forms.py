from django.forms import ModelForm
from django import forms
from network_automation.models import Device


class FormDevice(ModelForm):
    class Meta:
        model = Device
        # exclude = ['unit']
        fields = '__all__'

        widgets = {
            'ip_address' : forms.TextInput({'class':'form-control'}),
            'hostname' : forms.TextInput({'class':'form-control'}),
            'username' : forms.TextInput({'class':'form-control'}),
            'password' : forms.TextInput({'class':'form-control'}),
            'ssh_port' : forms.NumberInput({'class':'form-control'}),
            'vendor' : forms.Select({'class':'form-control'}),
            'koordinat' : forms.TextInput({'class':'form-control'}),
            'unit_induk' : forms.Select({'class':'form-control'}),
            'unit_pelaksana' : forms.Select({'class':'form-control'}),
            'unit_layanan' : forms.Select({'class':'form-control'}),
        }