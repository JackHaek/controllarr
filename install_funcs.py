import subprocess
import os
import fileinput

def write_cfg_vars(cfg_file_path: str, CFG: dict) -> None:
    with fileinput.FileInput(cfg_file_path, inplace=True, backup='.bak') as file:
        for line in file:
            made_change = False
            for var_name, value in CFG.items():
                if f"${{{var_name}}}" in line:
                    print(line.replace(f"${{{var_name}}}", value), end='')
                    made_change = True
            if not made_change:
                print(line, end='')

def write_env_vars(env_file_path: str, env_vars: dict) -> None:
    env_file = open(env_file_path, "w")
    num_env = len(env_vars)
    for idx, (var_name, value) in enumerate(env_vars.items()):
        if idx + 1 < num_env:
            env_file.write(f"{var_name}={value}\n")
        else:
            env_file.write(f"{var_name}={value}")
    env_file.close()

def start_docker_stack(GLOBAL_COMPOSE_PATH: str, service_name: str) -> None:
    #TODO: Change this to grab from github
    try:
        print(f"Starting {service_name}...")

        #Check if docker-compose.yaml exists in the service folder
        if os.path.isfile(f"{GLOBAL_COMPOSE_PATH}/{service_name}/docker-compose.yaml"):
            response = subprocess.run(["rm", f"{GLOBAL_COMPOSE_PATH}/{service_name}/docker-compose.yaml"])
            if response.returncode != 0:
                print(f"Error removing docker-compose.yaml for {service_name}.")
                return
            
        #Copy docker-compose.yaml from application folder to service folder
        response = subprocess.run(["cp", f"./compose/{service_name}/docker-compose.yaml", f"{GLOBAL_COMPOSE_PATH}/{service_name}/"])
        if response.returncode != 0:
            print(f"Error copying docker-compose.yaml for {service_name}.")
            return
        
        #Change directory to service folder and start docker container
        cur_dir = os.getcwd()
        os.chdir(f"{GLOBAL_COMPOSE_PATH}/{service_name}")
        response = subprocess.run(["sudo", "docker", "compose", "up", "-d"])
        if response.returncode != 0:
            print(f"Error starting {service_name}.")
            #Change back to original directory
            os.chdir(cur_dir)
            return
        
        #Change back to original directory
        os.chdir(cur_dir)
        print(f"{service_name} started.")
    except Exception as e:
        print(f"Error starting {service_name}: {e}")

def check_service_path(GLOBAL_COMPOSE_PATH: str, service_name: str) -> None:
    if not os.path.exists(f"{GLOBAL_COMPOSE_PATH}/{service_name}"):
        print("Path does not exist. Creating path...")
        os.makedirs(f"{GLOBAL_COMPOSE_PATH}/{service_name}")
        print(f"Path created: {GLOBAL_COMPOSE_PATH}/{service_name}")

# ==================== INSTALLER FUNCTIONS ==================== #

def install_traefik(GLOBAL_COMPOSE_PATH: str, ENV: dict) -> None:
    param1 = input("Enter PARAM 1: ")
    print(param1)

def install_dockge(GLOBAL_COMPOSE_PATH: str, ENV: dict) -> None:
    service_name = "dockge"
    check_service_path(GLOBAL_COMPOSE_PATH, service_name)
    
    print("Installing Dockge...")
    # Prep ENV File
    env_file_path = f"{GLOBAL_COMPOSE_PATH}/{service_name}/.env"
    write_env_vars(env_file_path, ENV)

    # Start Dockge Image
    start_docker_stack(GLOBAL_COMPOSE_PATH, service_name)

def install_homepage(GLOBAL_COMPOSE_PATH: str, ENV: dict) -> None:
    service_name = "homepage"
    check_service_path(GLOBAL_COMPOSE_PATH, service_name)

    print("Installing Homepage...")
    cfg_path = f"{GLOBAL_COMPOSE_PATH}/{service_name}/config"
    if not os.path.exists(cfg_path):
        os.makedirs(cfg_path)
    
    # Add CFG Path to ENV
    ENV["HOMEPAGE_CONFIG_PATH"] = cfg_path

    # Prep ENV File
    env_file_path = f"{GLOBAL_COMPOSE_PATH}/{service_name}/.env"
    write_env_vars(env_file_path, ENV)

    # Start Homepage Image
    start_docker_stack(GLOBAL_COMPOSE_PATH, service_name)


def install_prometheus(GLOBAL_COMPOSE_PATH: str, ENV: dict, CFG:dict) -> None:
    service_name = "prometheus-grafana"
    check_service_path(GLOBAL_COMPOSE_PATH, service_name)

    print("Installing Prometheus...")
    # Check config folder
    cfg_path = f"{GLOBAL_COMPOSE_PATH}/{service_name}/config"
    if not os.path.exists(cfg_path):
        os.makedirs(cfg_path)
    
    # Add CFG Path to ENV
    ENV["PROMETHEUS_CONFIG"] = cfg_path

    # Write CFG File
    subprocess.run(["cp", "./compose/prometheus-grafana/config/prometheus.yaml", f"{cfg_path}/prometheus.yaml"])
    write_cfg_vars(f"{cfg_path}/prometheus.yaml", CFG)

    # Prep ENV File
    env_file_path = f"{GLOBAL_COMPOSE_PATH}/{service_name}/.env"
    write_env_vars(env_file_path, ENV)

    # Start Prometheus-Grafana Stack
    start_docker_stack(GLOBAL_COMPOSE_PATH, service_name)

def install_overseerr(GLOBAL_COMPOSE_PATH: str, ENV: dict) -> None:
    pass
    service_name = "overseerr"
    #check_service_path(GLOBAL_COMPOSE_PATH, service_name)

    #print("Installing Overseerr...")
    # Prep ENV File
    #env_file_path = f"{GLOBAL_COMPOSE_PATH}/{service_name}/.env"
    #write_env_vars(env_file_path, ENV)

    # Start Overseerr Image
    #start_docker_stack(GLOBAL_COMPOSE_PATH, service_name)