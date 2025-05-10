import os
import json
from pprint import pprint


def capture_command_output(command):
    stream = os.popen(command)
    output = stream.read().strip()
    return output


def area0_check():
    # Проверка OSPF соседств на R1
    r1_neigbors = json.loads(capture_command_output('docker exec clab-ospf-router1 vtysh -c "show ip ospf neighbor json"'))
    try: 
        if "Full" in r1_neigbors['neighbors']['192.168.10.2'][0]['state']:
            print("R1: Статус соседа 192.168.10.2 Full")
            pass
        else:
            raise ValueError(f'\nR1: Статус соседа 192.168.10.2 NOT Full')
    except:
        raise Exception (f'\nНа R1 не установились соседство с 192.168.10.2')
    try: 
        if "Full" in r1_neigbors['neighbors']['192.168.10.3'][0]['state']:
            print("R1: Статус соседа 192.168.10.3 Full")
            pass
        else:
            raise ValueError(f'\nR1: Статус соседа 192.168.10.3 NOT Full')
    except:
        raise Exception (f'\nНа R1 не установились соседство с 192.168.10.3')

    # Проверка OSPF соседств на R2
    r2_neigbors = json.loads(capture_command_output('docker exec clab-ospf-router2 vtysh -c "show ip ospf neighbor json"'))
    try: 
        if "Full" in r2_neigbors['neighbors']['192.168.10.1'][0]['state']:
            print("R2: Статус соседа 192.168.10.1 Full")
            pass
        else:
            raise ValueError(f'\nR2: Статус соседа 192.168.10.1 NOT Full')
    except:
        raise Exception (f'\nНа R2 не установились соседство с 192.168.10.1')
    try: 
        if "Full" in r2_neigbors['neighbors']['192.168.10.4'][0]['state']:
            print("R2: Статус соседа 192.168.10.4 Full")
            pass
        else:
            raise ValueError(f'\nR2: Статус соседа 192.168.10.4 NOT Full')
    except:
        raise Exception (f'\nНа R2 не установились соседство с 192.168.10.4')
    return True


def area1_check():
    # Проверка OSPF соседств на R5
    r5_neigbors = json.loads(capture_command_output('docker exec clab-ospf-router5 vtysh -c "show ip ospf neighbor json"'))
    try: 
        if "Full" in r5_neigbors['neighbors']['192.168.10.1'][0]['state']:
            print("R5: Статус соседа 192.168.10.1 Full")
            pass
        else:
            raise ValueError(f'\nR5: Статус соседа 192.168.10.1 NOT Full')
    except:
        raise Exception (f'\nНа R5 не установились соседство с 192.168.10.1')
    try: 
        if "Full" in r5_neigbors['neighbors']['192.168.10.2'][0]['state']:
            print("R5: Статус соседа 192.168.10.2 Full")
            pass
        else:
            raise ValueError(f'\nR5: Статус соседа 192.168.10.2 NOT Full')
    except:
        raise Exception (f'\nНа R5 не установились соседство с 192.168.10.2')

    # Проверка настройки NSSA в Area1 на R5 
    r5_area1 = json.loads(capture_command_output('docker exec clab-ospf-router5 vtysh -c "show ip ospf json"'))
    try:
        if r5_area1['areas']['0.0.0.1']['nssa'] == True:
            print("Area1 NSSA")
            pass
        else:
            raise ValueError(f'\nArea1 NOT NSSA')
    except:
        raise Exception (f'\nArea1 не является NSSA')
    try:
        if r5_area1['areas']['0.0.0.1']['authentication'] == "authenticationMessageDigest":
            print("В Area1 настроена аутентификация MessageDigest")
            pass
        else:
            raise ValueError(f'\nВ Area1 НЕ настроена аутентификация MessageDigest"')
    except:
        raise Exception (f'\nВ Area1 не настроена аутентификация')
    try:
        if r5_area1['areas']['0.0.0.1']['nssaNoSummary'] == True:
            print("Area1 NSSA NoSummary")
            pass
        else:
            raise ValueError(f'\nВ Area1 не включена опция NoSummary')
    except:
        raise Exception (f'\nВ Area1 не включена опция NoSummary')

    # Проверка редистрибуции сети 192.168.1.0/24 на R1
    # Баг в FRR, периодически при старте лабы не применяется команде redistribute
    """
    r1_ospf_route = json.loads(capture_command_output('docker exec clab-ospf-router1 vtysh -c "show ip ospf route json"'))
    try:
        if r1_ospf_route['192.168.1.0/24']['routeType'] == "N E2":
            print("На R1 есть внешний маршрут к 192.168.1.0/24")
            pass
        else:
            raise ValueError(f'\nа R1 нет внешнего маршрута к 192.168.1.0/24')
    except:
        raise Exception (f'\nНа R1 нет внешнего маршрута к 192.168.1.0/24')
    return True

    """

def area2_check():
    # Проверка OSPF соседств на R3
    r3_neigbors = json.loads(capture_command_output('docker exec clab-ospf-router3 vtysh -c "show ip ospf neighbor json"'))
    try: 
        if "Full" in r3_neigbors['neighbors']['192.168.10.4'][0]['state']:
            print("R3: Статус соседа 192.168.10.4 Full")
            pass
        else:
            raise ValueError(f'\nR3: Статус соседа 192.168.10.4 NOT Full')
    except:
        raise Exception (f'\nНа R3 не установились соседство с 192.168.10.4')
    try: 
        if "Full" in r3_neigbors['neighbors']['192.168.10.6'][0]['state']:
            print("R3: Статус соседа 192.168.10.6 Full")
            pass
        else:
            raise ValueError(f'\nR3: Статус соседа 192.168.10.6 NOT Full')
    except:
        raise Exception (f'\nНа R3 не установились соседство с 192.168.10.6')

    # Проверка OSPF соседств на R4
    r4_neigbors = json.loads(capture_command_output('docker exec clab-ospf-router4 vtysh -c "show ip ospf neighbor json"'))
    try: 
        if "Full" in r4_neigbors['neighbors']['192.168.10.3'][0]['state']:
            print("R4: Статус соседа 192.168.10.3 Full")
            pass
        else:
            raise ValueError(f'\nR4: Статус соседа 192.168.10.3 NOT Full')
    except:
        raise Exception (f'\nНа R4 не установились соседство с 192.168.10.3')
    try: 
        if "Full" in r4_neigbors['neighbors']['192.168.10.6'][0]['state']:
            print("R4: Статус соседа 192.168.10.6 Full")
            pass
        else:
            raise ValueError(f'\nR4: Статус соседа 192.168.10.6 NOT Full')
    except:
        raise Exception (f'\nНа R4 не установились соседство с 192.168.10.6')
    return True


def rip_route_check():
    # Проверка на R7 в протоколе RIP маршрута из OSPF 
    r7_route = json.loads(capture_command_output('docker exec clab-ospf-router7 vtysh -c "show ip route json"'))
    try:
        if r7_route['192.168.10.5/32'][0]['protocol'] == "rip":
            print("R7: Есть маршрут к 192.168.10.5/32")
            pass
        else:
            raise ValueError(f'\nНа R7 нет RIP маршрута к 192.168.10.5/32')
    except:
        raise Exception (f'\nНа R7 нет RIP маршрута к 192.168.10.5/32')
    return True


def redistribution_route_map_check():
    # Проверяем на R1 наличие специфик маршрута к 192.168.2.0
    r1_route = json.loads(capture_command_output('docker exec clab-ospf-router1 vtysh -c "show ip route 192.168.2.0 json"'))
    try:
        if r1_route['192.168.2.0/24'][0]['protocol'] == "ospf":
            print("R1: Есть маршрут к 192.168.2.0/24")
            pass
        else:
            raise ValueError(f'\nНа R1 нет OSPF маршрута к 192.168.2.0/24')
    except:
        raise Exception (f'\nНа R1 нет OSPF маршрута к 192.168.2.0/24')

    # Проверяем на R1 отсутствие специфик маршрута к 192.168.3.0
    r1_route_1 = json.loads(capture_command_output('docker exec clab-ospf-router1 vtysh -c "show ip route 192.168.3.0 json"'))
    try:
        if r1_route_1['0.0.0.0/0']:
            print("R1: Нет специфик маршрута к 192.168.3.0/24")
            pass
    except:
        raise Exception (f'\nНа R1 есть специфик маршрут к 192.168.2.0/24, редистрибуция протокола RIP в протокол OSPF настроена некорректно')
    return True


def traffic_control_check():
    # Проверяем что в OSPF есть только один лучший маршрут по умолчанию и он идет через eth2
    r5_ospf_route = json.loads(capture_command_output('docker exec clab-ospf-router5 vtysh -c "show ip ospf route json"'))
    try:
        if len(r5_ospf_route['0.0.0.0/0']['nexthops']) == 1 and r5_ospf_route['0.0.0.0/0']['nexthops'][0]['via'] == 'eth2':
            print("R5: Есть только один лучший маршрут по умолчанию и он проходит через eth2")
            pass
        else:
            raise ValueError(f'\nНа R5 маршрут по умолчанию не идет через eth2')
    except:
        raise Exception (f'\nНа R5 маршрут по умолчанию не идет через eth2')
    return True


print("\n##### Проверка OSPF соседства в Area0 #####")
print(area0_check())
print("\n##### Проверка OSPF соседства в Area1 #####")
print(area1_check())
print("\n##### Проверка OSPF соседства в Area2 #####")
print(area2_check())
print("\n##### Проверка маршрутов на R7#####")
print(rip_route_check())
print("\n##### Проверка редистрибуции маршрутов#####")
print(redistribution_route_map_check())
print("\n##### Проверка управления трайиком#####")
print(traffic_control_check())
