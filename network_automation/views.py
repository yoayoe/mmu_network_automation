from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Device, Log
import paramiko
from datetime import datetime
import time
from .forms import FormDevice

def home(request):
    all_device = Device.objects.all()
    cisco_device = Device.objects.filter(vendor="cisco")
    mikrotik_device = Device.objects.filter(vendor="mikrotik")
    last_event = Log.objects.all().order_by('-id')[:10]

    context = {
        'all_device': len(all_device),
        'cisco_device' : len(cisco_device),
        'mikrotik_device' : len(mikrotik_device),
        'last_event' : last_event
    }
    return render(request, 'home.html', context)

def devices(request):
    all_device = Device.objects.all()

    context ={
        "all_device": all_device
    }

    return render(request, 'devices.html', context)

def configure(request):
    if request.method == "POST":
        selected_device_id = request.POST.getlist('device')
        mikrotik_command = request.POST['mikrotik_command'].splitlines()
        cisco_command = request.POST['cisco_command'].splitlines()
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address, username=dev.username, password=dev.password)

                if dev.vendor.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    conn.send ("conf t\n")
                    for cmd in cisco_command:
                        conn.send(cmd +"\n")
                        time.sleep(1)
                else:
                    for cmd in mikrotik_command:
                        ssh_client.exec_command(cmd)
                log = Log(target=dev.ip_address, action="Configure", status="Success", time=datetime.now(), messages= "No Error")
                log.save()
            except Exception as e:
                log = Log(target=dev.ip_address, action="Configure", status="Eror", time=datetime.now(), messages=e)
                log.save()
        return redirect ('home')

    else:
        devices = Device.objects.all()
        context = {
            'devices' : devices,
            'mode' : 'Configure'
        }
        return render(request, 'config.html', context)

def verify_config(request):
    if request.method == "POST":
        resault = []
        selected_device_id = request.POST.getlist('device')
        mikrotik_command = request.POST['mikrotik_command'].splitlines()
        cisco_command = request.POST['cisco_command'].splitlines()
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address, username=dev.username, password=dev.password)

                if dev.vendor.lower() == 'mikrotik':
                    for cmd in mikrotik_command:
                        stdin,stdout,stderr = ssh_client.exec_command(cmd)
                        resault.append("Resault on {}".format(dev.ip_address))
                        resault.append(stdout.read().decode())

                else:
                    conn = ssh_client.invoke_shell()
                    conn.send('terminal length 0\n')
                    for cmd in cisco_command:
                        resault.append("Resault on {}".format(dev.ip_address))
                        conn.send(cmd + "\n")
                        time.sleep(1)
                        output = conn.recv(65535)
                        resault.append(output.decode())
                log = Log(target=dev.ip_address, action="Verify Config", status="Success", time=datetime.now(), messages= "No Error")
                log.save()
            except Exception as e:
                log = Log(target=dev.ip_address, action="Verify Config", status="Eror", time=datetime.now(), messages=e)
                log.save()
        resault = '\n'.join(resault)
        return render(request, 'verify_result.html', {'resault':resault})

    else:
        devices = Device.objects.all()
        context = {
            'devices' : devices,
            'mode' : 'Verify Config'
        }
        return render(request, 'config.html', context)

def log(request):
    logs = Log.objects.all()
    
    context = {
        'logs' :logs
    }
    return render(request, 'log.html', context)

def tambah_device(request):
    if request.POST:
        form = FormDevice(request.POST)
        if form.is_valid():
            form.save()
            form = FormDevice()
            pesan = "Add Success"

            context = {
                'form':form,
                'pesan' : pesan,
            }
            return render(request, 'tambah_device.html', context)


    else:
        form = FormDevice()

        context = {
            'form' : form
        }
    return render(request, 'tambah_device.html', context)