import json
import os

def check_vlan_configuration(data):
    expected_values = {
        "ovsp1": [10, 20],
        "ovsp2": [10, 20],
        "ovsp3": [10, 20],
        "ovsp4": [10, 20],
        "ovsp5": [10, 20],
        "ovsp6": [10, 20],
        "ovsp7": [10, 20],
        "ovsp8": [10, 20],
        "ovsp9": 10,
        "ovsp10": 20,
        "ovsp11": 10,
        "ovsp12": 20
    }

    def find_value_in_item(item, value):
        if isinstance(item, list) or isinstance(item, tuple):
            for sub_item in item:
                if find_value_in_item(sub_item, value):
                    return True
        return value == item

    for command, expected_value in expected_values.items():
        port_data = data.get(f"sudo ovs-vsctl --format=json list port {command}", {})
        port_name = command.split()[-1]
        try:
            if 'data' in port_data and isinstance(port_data['data'], list):
                for item in port_data['data']:
                    if isinstance(expected_value, list):
                        if all(find_value_in_item(item, v) for v in expected_value):
                            print(f"Конфигурация порта {port_name} верная")
                            break
                    else:
                        if find_value_in_item(item, expected_value):
                            print(f"Конфигурация порта {port_name} верная")
                            break
                else:
                    raise Exception(f"Порт {port_name} не настроен согласно схеме")
        except Exception as e:
            raise Exception(f"Ошибка при проверке конфигурации: {e}")

def check_stp_priority(data):
    expected_stp_priority = {
        "ovs-bridge1": 4096,
        "ovs-bridge2": 8192
    }

    for bridge_name, expected_priority in expected_stp_priority.items():
        bridge_data = data.get(f"sudo ovs-vsctl --format=json list bridge {bridge_name}", {})

        if 'data' in bridge_data and isinstance(bridge_data['data'], list):
            found_priority = False
            for item in bridge_data['data']:
                for entry in item:
                    if isinstance(entry, list) and entry[0] == "map":
                        for map_entry in entry[1]:
                            try:
                                if map_entry[0] == "rstp-priority":
                                    actual_priority = int(map_entry[1])
                                    if actual_priority == expected_priority:
                                        print(f"STP-приоритет для {bridge_name} верный: {actual_priority}")
                                    else:
                                        raise Exception(f"STP-приоритет у {bridge_name} неверный: {actual_priority} (ожидалось {expected_priority})")
                            except Exception as e:
                                raise Exception(f"Ошибка при проверке STP-приоритета. {e}")

                            found_priority = True
                            break
                if found_priority:
                    break


def main(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    check_vlan_configuration(data)
    check_stp_priority(data)


if __name__ == "__main__":
    input_file = "command_results.json"
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Файл '{input_file}' не найден. Задание не было выполненно корректно")
    
    main(input_file)
