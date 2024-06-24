import subprocess
import os

def install_traefik():
    param1 = input("Enter PARAM 1: ")
    print(param1)

def install_dockge():
    compose_loc = input("Enter complete path to compose file locations: ")
    if compose_loc == "":
        print("No path entered. Using /opt/stacks as default.")
        compose_loc = "/opt/stacks"
    print("Using path: " + compose_loc)
    if not os.path.exists(compose_loc+"/dockge"):
        print("Path does not exist. Creating path...")
        os.makedirs(compose_loc+"/dockge")
        print("Path created.")
    
    print("Installing Dockge...")
    # Prep ENV File
    env_file = open(compose_loc+"/dockge/.env", "w")
    env_file.write("STACKS="+compose_loc)
    env_file.close()

    #TODO: Change this to grab from github
    # Dockge Image
    subprocess.run(["cp", "./compose/dockge/docker-compose.yaml", compose_loc+"/dockge/"])
    cur_dir = os.getcwd()
    os.chdir(f"{compose_loc}/dockge")
    subprocess.run(["sudo", "docker", "compose", "up", "-d"])
    os.chdir(cur_dir)
   





# ========== BEGIN CONTROLLARR ==========

print("\n========== Welcome to Controllarr! ==========")
print("Installing Traefik...\n")
install_dockge()
