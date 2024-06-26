## Dependencies

printf "\n\nChecking & Installing dependencies\n\n"

#Check python
if [[ $(command -v python3) ]]; then
    echo "Python already installed"
else
    echo "Installing Python"
    sudo apt update
    sudo apt upgrade
    sudo apt-get install python3
    sudo apt install python3-venv
fi

# Check pip
if [[ $(command -v pip3) ]]; then
    echo "Pip already installed"
else
    echo "Installing Pip"
    sudo apt-get install python3-pip
fi

# Check Docker
if [[ $(command -v docker) ]]; then
    echo "Docker already installed"
else
    echo "Installing Docker"
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
        "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update

    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

# Set Up Virtual Environment
if [[ -d "venv" ]]; then
    echo "Virtual Environment already exists"
else
    echo "Setting up Virtual Environment"
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
fi

printf "\n ========== START PYTHON SCRIPT ==========\n\n"

python3 controllarr.py