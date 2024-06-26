import socket
from contextlib import closing
import re
import pytz

def check_other_service_ports(all_env: list, port: int) -> bool:
    for env in all_env:
        for key, value in env.items():
            if "PORT" in key and value == port:
                print(f"\nPort {port} is in use by another service: {key}")
                return True
    return False
                

def port_in_use(port: int) -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        if s.connect_ex(('localhost', port)) == 0:
            return False
        else:
            print(f"\nPort {port} is in use.")
            return True

def get_valid_port(service_name: str, default:int, all_env: list) -> int:
    port = input(f"Enter port for {service_name} (default: {default}): ")
    if port == "":
        port = f"{default}"
    while not port.isdigit() or int(port) < 1 or int(port) > 65535 or port_in_use(int(port)) or check_other_service_ports(all_env, int(port)):
        print("\nInvalid port. Please enter a valid port number.")
        port = input(f"Enter port for {service_name}: ")
    return int(port)

def get_valid_interval(service_name: str, default: str) -> str:
    proposed_interval = input(f"Enter scrape interval for {service_name} (default: {default}): ")
    if proposed_interval == "":
        proposed_interval = default
    while not re.match(r"[0-9]+(s|m|h)\Z", proposed_interval):
        print(f"\n{proposed_interval} is an invalid interval. Please enter a valid interval. (e.g. 15s, 1m, 1h)")
        proposed_interval = input(f"Enter scrape interval for {service_name}: ")
    return proposed_interval

def get_valid_timezone(service_name: str, default: str) -> str:
    proposed_tz = input(f"Enter timezone for {service_name} (default: {default}): ")
    if proposed_tz == "":
        proposed_tz = default
    while not proposed_tz in pytz.all_timezones:
        print(f"\n{proposed_tz} is an invalid timezone. Please enter a valid timezone. To see a list of valid timezones, visit https://en.wikipedia.org/wiki/List_of_tz_database_time_zones.")
        proposed_tz = input(f"Enter timezone: ")
    return proposed_tz
