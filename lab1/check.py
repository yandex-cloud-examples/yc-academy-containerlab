import os
import json
from pprint import pprint

def capture_command_output(command):
    stream = os.popen(command)
    output = stream.read().strip()
    return output

def first_check():
    show_run_router1 = capture_command_output('docker exec clab-frrlab-router1 vtysh -c "show run"')
    if 'ospf' in show_run_router1:
        pass
    else:
        raise Exception ('OSPF не настроен на clab-frrlab-router1')
    
    show_run_router2 = capture_command_output('docker exec clab-frrlab-router2 vtysh -c "show run"')
    if 'ospf' in show_run_router2:
        pass
    else:
        raise Exception ('OSPF не настроен на clab-frrlab-router2')
    
    show_run_router3 = capture_command_output('docker exec clab-frrlab-router3 vtysh -c "show run"')
    if 'ospf' in show_run_router3:
        pass
    else:
        raise Exception ('OSPF не настроен на clab-frrlab-router3')

    return True

def second_check():
    neighbor_ips = []
    neighbors = json.loads(capture_command_output('docker exec clab-frrlab-router1 vtysh -c "show ip ospf neigh json"')).get("neighbors")
    for neighbor, parameters in neighbors.items():
        neighbor_ips.append(neighbor)
    if "10.10.10.2" in neighbor_ips and "10.10.10.3" in neighbor_ips:
        pass
    else:
        raise Exception (f'\nВторая проверка сфейлилась: 10.10.10.2 или 10.10.10.3 отсутствуют в списке OSPF соседей на clab-frrlab-router1\nСписок текущих соседей: \n{neighbor_ips}')
    
    return True

print("Первая проверка на наличие OSPF в конфигурации")
print(first_check())

print("Вторая проверка на наличие OSPF соседств на clab-frrlab-router1:")
print(second_check())
