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

# ========== DEFINE WHAT TO INSTALL ========== #

to_install_traefik = False
to_install_dockge = False
to_install_homepage = False
to_install_prometheus = True

# ========== ENVIRONMENT VARIABLES FOR CONTAINERS ========== #
# ===================== DO NOT CHANGE ====================== #
# ================ CONTAINS DEFAULT VALUES ================= #

ALL_ENV = []

TRAEFIK_ENV = {

}

DOCKGE_ENV = {
    "STACKS": GLOBAL_COMPOSE_PATH
}

HOMEPAGE_ENV = {
    "PUID": PUID,
    "PGID": PGID,
    "HOMEPAGE_PORT": 3000
}

PROMETHEUS_GRAFANA_ENV = {
    "PROMETHEUS_PORT": 9090,
    "GRAFANA_PORT": 3000,
}

PROMETHEUS_GRAFANA_CFG = {
    "GLOBAL_SCRAPE_INTERVAL": "15s",
    "PROMETHEUS_SCRAPE_INTERVAL": "5s"
}


# =================== END DO NOT CHANGE ==================== #

print("\n========== Welcome to Controllarr! ==========\n")

if to_install_traefik:
    print("\n========== Begin Traefik Config ==========\n")
    controllarr.install_traefik(GLOBAL_COMPOSE_PATH, TRAEFIK_ENV)
    ALL_ENV.append(TRAEFIK_ENV)

if to_install_dockge:
    print("\n========== Begin Dockge Config ==========\n")
    controllarr.install_dockge(GLOBAL_COMPOSE_PATH, DOCKGE_ENV)
    ALL_ENV.append(DOCKGE_ENV)

if to_install_homepage:
    print("\n==========Begin Homepage Config ==========\n")
    controllarr.install_homepage(GLOBAL_COMPOSE_PATH, HOMEPAGE_ENV)
    ALL_ENV.append(HOMEPAGE_ENV)

if to_install_prometheus:
    print("\n========== Begin Prometheus Config ==========\n")
    controllarr.install_prometheus(GLOBAL_COMPOSE_PATH, PROMETHEUS_GRAFANA_ENV, PROMETHEUS_GRAFANA_CFG)
    ALL_ENV.append(PROMETHEUS_GRAFANA_ENV)