# =====================================
# JITTERY Anti-Cheat Scanner v1
# =====================================

import os
import json
import sqlite3
import socket
import subprocess
import platform
from datetime import datetime

# =========================
# Dependency check
# =========================
try:
    import psutil
except ImportError:
    print("\n=====================================")
    print("Jittery Dependency Required")
    print("=====================================")
    print("The module 'psutil' is required to run this scanner.\n")
    print("Please install it using:\n")
    print("python -m pip install psutil\n")

    input("Press ENTER after installing psutil to continue...")

    try:
        import psutil
    except ImportError:
        print("\npsutil still not found. Exiting scanner.")
        input("Press ENTER to exit.")
        exit()

# =========================
# Banner
# =========================
print("\n=====================================")
print("           J I T T E R Y")
print("        Anti-Cheat Scanner")
print("=====================================\n")

# =========================
# Instance Times
# =========================
boot = datetime.fromtimestamp(psutil.boot_time())

print("INSTANCE TIMES")
print("--------------------")
print("Boot:", boot)

java_times = []
for proc in psutil.process_iter(['name', 'create_time']):
    if proc.info['name'] and "javaw.exe" in proc.info['name'].lower():
        java_times.append(datetime.fromtimestamp(proc.info['create_time']))

if java_times:
    start = min(java_times)
    runtime = datetime.now() - start
    print("Javaw:", start, f"(For {runtime})")
else:
    print("Javaw: Not running")

# =========================
# Prefetch Scan
# =========================
print("\nPREFETCH")
print("--------------------")

prefetch_path = r"C:\Windows\Prefetch"

if os.path.exists(prefetch_path):

    pf_files = [f for f in os.listdir(prefetch_path) if f.endswith(".pf")]

    for pf in sorted(pf_files):
        print(pf)

else:
    print("Prefetch folder not found")

# =========================
# VPN Detection
# =========================
print("\nVPN CHECK")
print("--------------------")

vpn_keywords = [
    "nord","proton","expressvpn","surfshark",
    "mullvad","openvpn","zerotier","hamachi"
]

found = []

for proc in psutil.process_iter(['name']):

    name = proc.info['name']

    if name:

        for vpn in vpn_keywords:

            if vpn in name.lower():
                found.append(name)

if found:
    for v in set(found):
        print(v)
else:
    print("No VPN detected")

# =========================
# Hotspot / Hosted Network
# =========================
print("\nNETWORK CHECK")
print("--------------------")

try:

    result = subprocess.check_output(
        "netsh wlan show hostednetwork",
        shell=True,
        text=True
    )

    if "Started" in result:
        print("Possible hotspot detected")

    else:
        print("No hotspot detected")

except:
    print("Could not check hotspot status")

# =========================
# Minecraft Accounts
# =========================
print("\nMINECRAFT ACCOUNTS")
print("--------------------")

accounts_path = os.path.expandvars(
    r"%APPDATA%\.minecraft\launcher_accounts.json"
)

if os.path.exists(accounts_path):

    try:

        with open(accounts_path) as f:

            data = json.load(f)

            for acc in data.get("accounts", {}):
                print(acc)

    except:
        print("Could not parse launcher_accounts.json")

else:
    print("No Minecraft accounts found")

# =========================
# Minecraft Mods Scan
# =========================
check_mods = input("\nCheck Minecraft Mods? (Y/N): ").lower()

if check_mods == "y":

    mods_path = input("Enter mods folder path: ")

    cheat_mods = [
        "meteor","wurst","impact","aristois",
        "liquidbounce","future","rise","vape"
    ]

    found_mods = []

    if os.path.exists(mods_path):

        for file in os.listdir(mods_path):

            for cheat in cheat_mods:

                if cheat in file.lower():
                    found_mods.append(file)

        print("\nMOD CHECK")
        print("--------------------")

        if found_mods:

            for m in found_mods:
                print(m)

        else:
            print("No suspicious mods found")

    else:
        print("Mods path not found")

# =========================
# Browser History Scan
# =========================
print("\nBROWSER HISTORY")
print("--------------------")

chrome_hist = os.path.expandvars(
    r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History"
)

cheat_sites = [
    "vape.gg",
    "drip.gg",
    "intent.store",
    "novoline"
]

if os.path.exists(chrome_hist):

    try:

        conn = sqlite3.connect(chrome_hist)
        cursor = conn.cursor()

        cursor.execute("SELECT url FROM urls")

        for row in cursor.fetchall():

            for site in cheat_sites:

                if site in row[0]:
                    print(row[0])

        conn.close()

    except:
        print("Could not read Chrome history")

else:
    print("Chrome history not found")

# =========================
# Drives
# =========================
print("\nDRIVES")
print("--------------------")

for part in psutil.disk_partitions():
    print(part.device, part.fstype)

# =========================
# USB Devices
# =========================
print("\nUSB DEVICES")
print("--------------------")

try:

    import winreg

    usb_path = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"

    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, usb_path)

    for i in range(winreg.QueryInfoKey(key)[0]):

        device = winreg.EnumKey(key, i)
        print(device)

except:
    print("Could not access USB registry")

# =========================
# USN Journal Check
# =========================
print("\nUSN JOURNAL CHECK")
print("--------------------")

if os.path.exists(r"C:\$Extend\$UsnJrnl"):
    print("USN Journal exists")
else:
    print("USN Journal not found")

print("\nScan complete.")
input("\nPress ENTER to exit.")
