sudo apt update
sudo apt upgrade

## Dependencies

printf "\n\nInstalling dependencies\n\n"


#Check python
if [[ $(command -v python3) ]]; then
    echo "Python already installed"
else
    echo "Installing Python"
    sudo apt-get install python3
fi

# Check Docker
if [[ $(command -v docker) ]]; then
    echo "Docker already installed"
else
    echo "Installing Docker"
    sudo apt-get update
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

printf "\n ========== START PYTHON SCRIPT ==========\n\n"

python3 controllarr.py