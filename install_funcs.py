import subprocess
import os

def get_valid_port(service_name):
    port = input(f"Enter port for {service_name} (default: 3000): ")
    if port == "":
        port = "3000"
    while not port.isdigit() or int(port) < 1 or int(port) > 65535:
        print("Invalid port. Please enter a valid port number.")
        port = input(f"Enter port for {service_name}: ")
    return port

def start_docker_container(GLOBAL_COMPOSE_PATH, service_name):
    #TODO: Change this to grab from github
    print(f"Starting {service_name}...")
    subprocess.run(["cp", f"./compose/{service_name}/docker-compose.yaml", f"{GLOBAL_COMPOSE_PATH}/{service_name}/"])
    cur_dir = os.getcwd()
    os.chdir(f"{GLOBAL_COMPOSE_PATH}/{service_name}")
    subprocess.run(["sudo", "docker", "compose", "up", "-d"])
    os.chdir(cur_dir)
    print(f"{service_name} started.")

def check_service_path(GLOBAL_COMPOSE_PATH, service_name):
    if not os.path.exists(f"{GLOBAL_COMPOSE_PATH}/{service_name}"):
        print("Path does not exist. Creating path...")
        os.makedirs(f"{GLOBAL_COMPOSE_PATH}/{service_name}")
        print(f"Path created: {GLOBAL_COMPOSE_PATH}/{service_name}")

def install_traefik(GLOBAL_COMPOSE_PATH):
    param1 = input("Enter PARAM 1: ")
    print(param1)

def install_dockge(GLOBAL_COMPOSE_PATH):
    service_name = "dockge"
    check_service_path(GLOBAL_COMPOSE_PATH, service_name)
    
    print("Installing Dockge...")
    # Prep ENV File
    env_file = open(GLOBAL_COMPOSE_PATH+"/dockge/.env", "w")
    env_file.write(f"STACKS={GLOBAL_COMPOSE_PATH}")
    env_file.close()

    # Dockge Image
    start_docker_container(GLOBAL_COMPOSE_PATH, service_name)

def install_homepage(GLOBAL_COMPOSE_PATH, PUID, PGID):
    service_name = "homepage"
    check_service_path(GLOBAL_COMPOSE_PATH, service_name)

    print("Installing Homepage...")
    # Prep ENV File
    env_file = open(GLOBAL_COMPOSE_PATH+"/homepage/.env", "w")
    port = get_valid_port("Homepage")
    cfg_path = f"{GLOBAL_COMPOSE_PATH}/homepage/config"
    if not os.path.exists(cfg_path):
        os.makedirs(cfg_path)
    env_file.write(f"PUID={PUID}\nPGID={PGID}\nHOMEPAGE_PORT={port}\nCONFIG_PATH={cfg_path}")
    env_file.close()

    # Homepage Image
    start_docker_container(GLOBAL_COMPOSE_PATH, "homepage")


