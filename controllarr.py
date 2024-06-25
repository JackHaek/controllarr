import os
import install_funcs as controllarr

TESTING = True

PUID = os.getuid()
PGID = os.getgid()

if not TESTING:
    GLOBAL_COMPOSE_PATH = input("Enter complete path to compose file locations: ")
else:
    GLOBAL_COMPOSE_PATH = "/workspaces/ubuntu/tc"

if GLOBAL_COMPOSE_PATH == "":
    print("No path entered. Using /opt/stacks as default.")
    GLOBAL_COMPOSE_PATH = "/opt/stacks"
print("Using path: " + GLOBAL_COMPOSE_PATH)
if not os.path.exists(GLOBAL_COMPOSE_PATH):
    print("Path does not exist. Creating path...")
    os.makedirs(GLOBAL_COMPOSE_PATH)
    print("Path created.")


# ========== BEGIN CONTROLLARR ========== #

to_install_traefik = False
to_install_dockge = True
to_install_homepage = True

print("\n========== Welcome to Controllarr! ==========\n")

if to_install_traefik:
    print("\n========== Begin Traefik Config ==========\n")
    controllarr.install_traefik(GLOBAL_COMPOSE_PATH)

if to_install_dockge:
    print("\n========== Begin Dockge Config ==========\n")
    controllarr.install_dockge(GLOBAL_COMPOSE_PATH)

if to_install_homepage:
    print("\n==========Begin Homepage Config ==========\n")
    controllarr.install_homepage(GLOBAL_COMPOSE_PATH, PUID, PGID)
