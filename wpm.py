import sys
import subprocess
import pexpect

if len(sys.argv) != 3:
    print("Использование: python script.py <логин> <пароль>")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

wifi_device = subprocess.check_output(["networksetup", "-listallhardwareports", "|", "grep", "-A", "1", "Wi-Fi", "|", "awk", "'/Device/ { print $2 }'"]).decode('utf-8').strip()
preferred_networks = subprocess.check_output(["networksetup", "-listpreferredwirelessnetworks", wifi_device]).decode('utf-8').strip()

for network_name in preferred_networks.split('\n'):
    command = f'security find-generic-password -D "AirPort network password" -a "{network_name}" -w'
    
    try:
        child = pexpect.spawn(command)

        index = child.expect(['Enter password:', pexpect.EOF, pexpect.TIMEOUT], timeout=5)

        if index == 0:
            child.sendline(password)

        result = child.read().decode('utf-8').strip()
        
        print(f"Output for network {network_name}: {result}")

    except pexpect.ExceptionPexpect as e:
        print(f"Error for network {network_name}: {str(e)}")

print("Wi-Fi Device:", wifi_device)
print("Preferred Wireless Networks:", preferred_networks)
