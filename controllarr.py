import os
import install_funcs as controllarr
import validity_checker as vc

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
    "STACKS": GLOBAL_COMPOSE_PATH,
    "DOCKGE_PORT": 5001
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

    confirmed = False

    while not confirmed:
        # Configure Dockge ENV
        DOCKGE_ENV["DOCKGE_PORT"] = vc.get_valid_port("Dockge", DOCKGE_ENV["DOCKGE_PORT"], ALL_ENV)
        print(f"Using port {DOCKGE_ENV['DOCKGE_PORT']} for Dockge.")

        print("\nDockge Config:\n")
        for key, value in DOCKGE_ENV.items():
            print(f"{key}={value}")

        while True:
            accepted = input("\nAre these settings correct? (y/n): ")
            if accepted.lower() == "y":
                confirmed = True
                break
            elif accepted.lower() == "n":
                print("\nReconfiguring Dockge...\n")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    controllarr.install_dockge(GLOBAL_COMPOSE_PATH, DOCKGE_ENV)
    ALL_ENV.append(DOCKGE_ENV)

if to_install_homepage:
    print("\n==========Begin Homepage Config ==========\n")

    confirmed = False

    while not confirmed:
        # Configure Homepage ENV
        HOMEPAGE_ENV["HOMEPAGE_PORT"] = vc.get_valid_port("Homepage", HOMEPAGE_ENV["HOMEPAGE_PORT"], ALL_ENV)
        print(f"Using port {HOMEPAGE_ENV['HOMEPAGE_PORT']} for Homepage.")

        print("\nHomepage Config:\n")
        for key, value in HOMEPAGE_ENV.items():
            print(f"{key}={value}")

        while True:
            accepted = input("\nAre these settings correct? (y/n): ")
            if accepted.lower() == "y":
                confirmed = True
                break
            elif accepted.lower() == "n":
                print("\nReconfiguring Homepage...\n")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    # Install Homepage
    print("") # Spacing
    controllarr.install_homepage(GLOBAL_COMPOSE_PATH, HOMEPAGE_ENV)
    ALL_ENV.append(HOMEPAGE_ENV)

if to_install_prometheus:
    print("\n========== Begin Prometheus Config ==========\n")

    confirmed = False
    
    while not confirmed:
        # Configure Prometheus-Grafana ENV
        PROMETHEUS_GRAFANA_ENV["PROMETHEUS_PORT"] = vc.get_valid_port("Prometheus", PROMETHEUS_GRAFANA_ENV["PROMETHEUS_PORT"], ALL_ENV)
        print(f"Using port {PROMETHEUS_GRAFANA_ENV['PROMETHEUS_PORT']} for Prometheus.")

        PROMETHEUS_GRAFANA_ENV["GRAFANA_PORT"] = vc.get_valid_port("Grafana", PROMETHEUS_GRAFANA_ENV["GRAFANA_PORT"], ALL_ENV)
        print(f"Using port {PROMETHEUS_GRAFANA_ENV['GRAFANA_PORT']} for Grafana.")


        # Configure Prometheus-Grafana CFG
        PROMETHEUS_GRAFANA_CFG["GLOBAL_SCRAPE_INTERVAL"] = vc.get_valid_interval("Prometheus - GLOBAL", PROMETHEUS_GRAFANA_CFG["GLOBAL_SCRAPE_INTERVAL"])
        print(f"Global Scrape Interval set to: {PROMETHEUS_GRAFANA_CFG['GLOBAL_SCRAPE_INTERVAL']}")

        PROMETHEUS_GRAFANA_CFG["PROMETHEUS_SCRAPE_INTERVAL"] = vc.get_valid_interval("Prometheus", PROMETHEUS_GRAFANA_CFG["PROMETHEUS_SCRAPE_INTERVAL"])
        print(f"Prometheus Scrape Interval set to: {PROMETHEUS_GRAFANA_CFG['PROMETHEUS_SCRAPE_INTERVAL']}")


        print("\nPrometheus-Grafana Config:\n")
        for key, value in PROMETHEUS_GRAFANA_ENV.items():
            print(f"{key}={value}")
        for key, value in PROMETHEUS_GRAFANA_CFG.items():
            print(f"{key}={value}")

        while True:
            accepted = input("\nAre these settings correct? (y/n): ")
            if accepted.lower() == "y":
                confirmed = True
                break
            elif accepted.lower() == "n":
                print("\nReconfiguring Prometheus-Grafana...\n")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    

    # Install Prometheus-Grafana
    print("") # Spacing
    controllarr.install_prometheus(GLOBAL_COMPOSE_PATH, PROMETHEUS_GRAFANA_ENV, PROMETHEUS_GRAFANA_CFG)
    ALL_ENV.append(PROMETHEUS_GRAFANA_ENV)