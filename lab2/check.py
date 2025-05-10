import os
import json
from pprint import pprint

def capture_command_output(command):
    stream = os.popen(command)
    output = stream.read().strip()
    return output

def first_check():
    show_ip_route = json.loads(capture_command_output('docker exec clab-static-routing-router-core vtysh -c "show ip route json"'))
    try: 
        if show_ip_route['192.168.0.0/24'][0]['nexthops'][0]['ip'] != '172.16.1.2': raise ValueError("Nexthop для 192.168.0.0/24 не верный")
        print("Nexthop для 192.168.0.0/24 = 172.16.1.2")
        pass
    except:
        raise Exception (f'\nНе смог найти nexthop для маршрута 10.0.0.0/8 на маршрутизаторе clab-static-routing-router-core')
    try: 
        if show_ip_route['10.0.0.0/8'][0]['nexthops'][0]['ip'] != '172.16.2.2': raise ValueError("Nexthop для 10.0.0.0/8 не верный")
        print("Nexthop для 10.0.0.0/8 = 172.16.2.2")
        pass
    except:
        raise Exception (f'\nНе смог найти nexthop для маршрута 10.0.0.0/8 на маршрутизаторе clab-static-routing-router-core')
    try: 
        if show_ip_route['10.0.3.0/24'][0]['nexthops'][0]['ip'] != '172.16.3.2': raise ValueError("Nexthop для 10.0.3.0/24 не верный")
        print(f"Nexthop для 10.0.3.0/24 = 172.16.3.2")
        pass
    except:
        raise Exception (f'\nНе смог найти nexthop для маршрута 10.0.3.0/24 на маршрутизаторе clab-static-routing-router-core')
    return True

def second_check():
    PC2 = '10.0.2.2'
    PC3 = '10.0.3.2'
    PC4 = '10.0.4.2'

    try:
        ping_pc2 = os.system(f'docker exec clab-static-routing-PC1 /bin/sh -c "ping -c 4 {PC2} > /dev/null 2>&1"') == 0
        if not ping_pc2: raise ValueError(f"PC2 с адресом {PC2} не пингуется")
        print("PC2 пингуется")
    except:
        raise Exception (f'PC2 с адресом {PC2} не пингуется')

    try:
        ping_pc3 = os.system(f'docker exec clab-static-routing-PC1 /bin/sh -c "ping -c 4 {PC3} > /dev/null 2>&1"') == 0
        if not ping_pc3: raise ValueError(f"PC3 с адресом {PC3} не пингуется")
        print("PC3 пингуется")
    except:
        raise Exception (f'PC3 с адресом {PC3} не пингуется')

    try:
        traceroute_to_pc4 = capture_command_output(f'docker exec clab-static-routing-PC1 /bin/sh -c "traceroute -m 4 {PC4}"').split('\n')
        if traceroute_to_pc4[-1].split()[1] != traceroute_to_pc4[-3].split()[1]: raise ValueError("Кольцо не воспроизводится")
        print('Кольцо воспроизвелось')
        print(traceroute_to_pc4)
    except:
        raise Exception (f'При попытке выполнить трассировку до РС4 произошла ошибка')
    
    return True


print("\nПервая проверка на наличие статических маршруов на clab-static-routing-router-core")
print(first_check())

print("\nВторая проверка чекает доступность и трассировку")
print(second_check())
