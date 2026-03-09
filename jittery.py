# ============================
# Jittery v1 - Full Anti-Cheat Scanner
# ============================

Clear-Host
Write-Host ""
Write-Host "====================================="
Write-Host "           J I T T E R Y"
Write-Host "        Anti-Cheat Scanner"
Write-Host "====================================="
Write-Host ""

# Temp Python file
$pyTemp = "$env:TEMP\jittery.py"

# Full Python scanner
$pyCode = @"
import os, json, psutil, sqlite3, socket, subprocess, platform, re
from datetime import datetime

# ====== Banner ======
print('\\n=====================================')
print('           J I T T E R Y')
print('        Anti-Cheat Scanner')
print('=====================================\\n')

# ====== Boot time ======
boot = datetime.fromtimestamp(psutil.boot_time())
print('INSTANCE TIMES')
print('--------------------')
print('Boot:', boot)

# ====== Java runtime ======
java_times = []
for proc in psutil.process_iter(['name','create_time']):
    if proc.info['name'] and 'javaw.exe' in proc.info['name'].lower():
        start = datetime.fromtimestamp(proc.info['create_time'])
        java_times.append(start)
if java_times:
    java_start = min(java_times)
    delta = datetime.now() - java_start
    print('Javaw:', java_start, f'(For {delta})')
else:
    print('Javaw: Not running')

# ====== Prefetch scan ======
prefetch_path = r'C:\Windows\Prefetch'
print('\\nPREFETCH')
print('--------------------')
if os.path.exists(prefetch_path):
    prefetch_files = [f for f in os.listdir(prefetch_path) if f.endswith('.pf')]
    for f in sorted(prefetch_files):
        print(f)
else:
    print('Prefetch not found')

# ====== VPN Detection ======
vpn_keywords = ['nord','proton','expressvpn','surfshark','mullvad','openvpn','zerotier','hamachi']
print('\\nVPN CHECK')
print('--------------------')
vpn_found = []
for proc in psutil.process_iter(['name']):
    name = proc.info['name']
    if name:
        for vpn in vpn_keywords:
            if vpn in name.lower():
                vpn_found.append(name)
print('\\n'.join(set(vpn_found)) if vpn_found else 'No VPN detected')

# ====== Hotspot / ICS detection ======
print('\\nNETWORK CHECK')
print('--------------------')
hotspot = False
try:
    net = subprocess.check_output('netsh wlan show hostednetwork', shell=True, text=True)
    if 'Status' in net and 'Started' in net:
        hotspot = True
        print('Possible hosted network detected')
    else:
        print('No hotspot detected')
except:
    print('Could not detect hotspot')

# ====== Minecraft Accounts ======
print('\\nMINECRAFT ACCOUNTS')
print('--------------------')
accounts_path = os.path.expandvars(r'%APPDATA%\.minecraft\launcher_accounts.json')
if os.path.exists(accounts_path):
    with open(accounts_path) as f:
        data = json.load(f)
        for acc in data.get('accounts', {}):
            print(acc)
else:
    print('No Minecraft accounts found')

# ====== Minecraft Mods / Cheat Clients ======
check_mods = input('Check Minecraft Mods? (Y/N): ').strip().lower()
if check_mods == 'y':
    mods_path = input('Enter path to mods folder: ').strip()
    cheat_mods = ['meteor','wurst','impact','aristois','liquidbounce','future','rise','vape']
    found = []
    if os.path.exists(mods_path):
        for f in os.listdir(mods_path):
            for cheat in cheat_mods:
                if cheat in f.lower():
                    found.append(f)
    print('MOD CHECK')
    print('--------------------')
    if found:
        for m in found:
            print(m)
    else:
        print('No suspicious mods found')

# ====== Browser History ======
print('\\nBROWSER HISTORY')
print('--------------------')
chrome_hist = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\History')
cheat_sites = ['vape.gg','drip.gg','intent.store','novoline']
if os.path.exists(chrome_hist):
    try:
        conn = sqlite3.connect(chrome_hist)
        cursor = conn.cursor()
        cursor.execute('SELECT url FROM urls')
        for row in cursor.fetchall():
            for site in cheat_sites:
                if site in row[0]:
                    print(row[0])
        conn.close()
    except:
        print('Could not read Chrome history (maybe Chrome is open)')
else:
    print('Chrome history not found')

# ====== Drives ======
print('\\nDRIVES')
print('--------------------')
for part in psutil.disk_partitions():
    print(part.device, part.fstype, part.opts)

# ====== USB Devices ======
print('\\nUSB DEVICES')
print('--------------------')
try:
    import winreg
    usb_path = r'SYSTEM\CurrentControlSet\Enum\USBSTOR'
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, usb_path)
    for i in range(winreg.QueryInfoKey(key)[0]):
        devices = winreg.EnumKey(key, i)
        print(devices)
except:
    print('Could not access USB registry info (run as admin)')

# ====== $UsnJrnl check (basic) ======
print('\\nUSN JOURNAL CHECK')
print('--------------------')
if os.path.exists(r'C:\$Extend\$UsnJrnl'):
    print('USN Journal exists')
else:
    print('No USN Journal detected (NTFS?)')
"@

# Write Python code to temp file
Set-Content -Path $pyTemp -Value $pyCode -Encoding UTF8

# Run Python
python $pyTemp

# Optional: cleanup
# Remove-Item $pyTemp
