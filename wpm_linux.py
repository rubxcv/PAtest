import sys
import subprocess
import pexpect

if len(sys.argv) != 3:
    print("Использование: python script.py <логин> <пароль>")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

try:
    # Получаем список сохраненных Wi-Fi сетей
    saved_networks = subprocess.check_output(["nmcli", "-t", "-f", "name", "connection", "show"]).decode('utf-8').strip().split('\n')

    for network_name in saved_networks:
        print(f"Working on network: {network_name}")

        # Пример получения пароля (нужны права root и соответствующая настройка nmcli)
        try:
            wifi_password = subprocess.check_output(["sudo", "nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", network_name]).decode('utf-8').strip()
            print(f"Password for {network_name}: {wifi_password}")
        except subprocess.CalledProcessError as e:
            print(f"Could not retrieve password for {network_name}: {str(e)}")

except subprocess.CalledProcessError as e:
    print(f"Error: {str(e)}")

print("Preferred Wireless Networks:", saved_networks)
