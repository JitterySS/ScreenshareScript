# jittery.py
import os, json, psutil, sqlite3
from datetime import datetime
import platform

# 1️⃣ Banner
print("\n=====================================")
print("           J I T T E R Y")
print("        Anti-Cheat Scanner")
print("=====================================\n")

# 2️⃣ Boot time
boot = datetime.fromtimestamp(psutil.boot_time())
print("INSTANCE TIMES")
print("--------------------")
print("Boot:", boot, "\n")

# 3️⃣ Prefetch scan
prefetch_path = r"C:\Windows\Prefetch"
print("PREFETCH")
print("--------------------")
if os.path.exists(prefetch_path):
    prefetch_files = [f.split("-")[0] for f in os.listdir(prefetch_path) if f.endswith(".pf")]
    for exe in sorted(set(prefetch_files)):
        print(exe)
else:
    print("Prefetch not found")

# 4️⃣ VPN check
vpn_keywords = ["nord","proton","expressvpn","surfshark","mullvad","openvpn","zerotier","hamachi"]
print("\nVPN CHECK")
print("--------------------")
found_vpn = []
for proc in psutil.process_iter(['name']):
    name = proc.info['name']
    if name:
        for vpn in vpn_keywords:
            if vpn in name.lower():
                found_vpn.append(name)
print("\n".join(set(found_vpn)) if found_vpn else "No VPN detected")

# 5️⃣ Drives
print("\nDRIVES")
print("--------------------")
for part in psutil.disk_partitions():
    print(part.device, part.fstype, part.opts)

# 6️⃣ USB devices
print("\nUSB DEVICES")
print("--------------------")
try:
    import winreg
    usb_path = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, usb_path)
    for i in range(0, winreg.QueryInfoKey(key)[0]):
        devices = winreg.EnumKey(key, i)
        print(devices)
except:
    print("Could not access USB registry info (run as admin)")

# 7️⃣ Minecraft accounts
print("\nMINECRAFT ACCOUNTS")
print("--------------------")
accounts_path = os.path.expandvars(r"%APPDATA%\.minecraft\launcher_accounts.json")
if os.path.exists(accounts_path):
    with open(accounts_path) as f:
        data = json.load(f)
        for acc in data.get("accounts", {}):
            print(acc)
else:
    print("No Minecraft accounts found")

# 8️⃣ Browser history (Chrome)
print("\nBROWSER HISTORY")
print("--------------------")
chrome_hist = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History")
cheat_sites = ["vape.gg","drip.gg","intent.store","novoline"]
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
        print("Could not read Chrome history (maybe Chrome is open)")
else:
    print("Chrome history not found")
