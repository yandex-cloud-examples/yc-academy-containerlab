import os
import json


IP_TO_NAME = {
    "10.0.0.1": "R1",
    "10.0.0.2": "R2",
    "10.0.0.3": "R3",
    "10.0.0.4": "R4",
    "10.0.0.5": "R5",
}

NEIGHBOR_IPS = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"]


def capture_command_output(command):
    stream = os.popen(command)
    output = stream.read().strip()
    return output


def neighbor_check(route_reflector):
    command = (
        f"docker exec clab-bgp-{route_reflector} vtysh -c 'show bgp neighbor json'"
    )
    neighbors = json.loads(capture_command_output(command))

    for ip in NEIGHBOR_IPS:
        try:
            if ip in neighbors:
                bgp_state = neighbors[ip].get("bgpState")
                nbr_internal_link = neighbors[ip].get("nbrInternalLink")
                is_rr_client = (
                    neighbors[ip]
                    .get("addressFamilyInfo", {})
                    .get("ipv4Unicast", {})
                    .get("routeReflectorClient")
                )

                if bgp_state == "Established" and nbr_internal_link and is_rr_client:
                    print(
                        f"Пиринг между {route_reflector} и {IP_TO_NAME[ip]} настроен согласно схеме"
                    )
                else:
                    raise ValueError(
                        f"Ошибка в конфигурации пиринга между {route_reflector} и {IP_TO_NAME[ip]}"
                    )
            else:
                raise ValueError(
                    f"На {route_reflector} не настроен пиринг с {IP_TO_NAME[ip]}"
                )
        except ValueError as e:
            raise Exception(e)


def check_locPrf(router):
    try:
        command = f"docker exec clab-bgp-{router} vtysh -c 'show bgp ipv4 uni 5.3.93.0/24 json'"
        bgp_routes = json.loads(capture_command_output(command))

        for path in bgp_routes["paths"]:
            locPrf = path.get("locPrf")
            if locPrf > 100:
                print(
                    f"local preference для маршрута {bgp_routes['prefix']} выбран верно"
                )
            else:
                raise ValueError(
                    f"local preference для маршрута {bgp_routes['prefix']} выбран неверно. Фактическое значение ({locPrf})"
                )
    except ValueError as e:
        raise Exception(e)


def check_route_validity(router, prefix):
    try:
        command = (
            f"docker exec clab-bgp-{router} vtysh -c 'show bgp ipv4 uni {prefix} json'"
        )
        bgp_routes = json.loads(capture_command_output(command))

        valid = bgp_routes["paths"][0].get("valid")
        if valid:
            print(f"{router}: Префикс {prefix} получен с корректными атрибутами пути")
        else:
            raise ValueError(
                f"{router}: Префикс {prefix} отправлен с некорректными атрибутами пути. Необходимо перепроверить настройки, перечитать задание"
            )
    except ValueError as e:
        raise Exception(e)


print("\n##### Проверка BGP соседств на RR1 #####")
neighbor_check("RR1")


print("\n##### Проверка BGP соседств на RR2 #####")
neighbor_check("RR2")


print("\n##### Проверка local preference #####")
check_locPrf("R1")


print("\n##### Проверка валидности внешних маршрутов на рефлекторах #####")
check_route_validity("RR1", "5.3.93.0/24")
check_route_validity("RR1", "89.179.16.0/24")
check_route_validity("RR2", "5.3.93.0/24")
check_route_validity("RR2", "89.179.16.0/24")
