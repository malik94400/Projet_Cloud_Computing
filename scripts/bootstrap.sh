#!/bin/bash
set -e

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y python3 python3-pip python3-venv git

cd /home/azureuser

if [ ! -d "/home/azureuser/Projet_Cloud_Computing" ]; then
  sudo -u azureuser git clone https://github.com/malik94400/Projet_Cloud_Computing.git
else
  cd /home/azureuser/Projet_Cloud_Computing
  sudo -u azureuser git pull
fi

cd /home/azureuser/Projet_Cloud_Computing/backend

sudo -u azureuser python3 -m venv venv
sudo -u azureuser /home/azureuser/Projet_Cloud_Computing/backend/venv/bin/pip install --upgrade pip
sudo -u azureuser /home/azureuser/Projet_Cloud_Computing/backend/venv/bin/pip install -r requirements.txt

cat > /home/azureuser/Projet_Cloud_Computing/backend/.env <<EOF
AZURE_STORAGE_ACCOUNT=${azure_storage_account}
AZURE_STORAGE_KEY=${azure_storage_key}
AZURE_CONTAINER_NAME=${azure_container_name}
EOF

chown azureuser:azureuser /home/azureuser/Projet_Cloud_Computing/backend/.env

cat > /etc/systemd/system/flaskapp.service <<EOF
[Unit]
Description=Flask Backend App
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/Projet_Cloud_Computing/backend
Environment="PATH=/home/azureuser/Projet_Cloud_Computing/backend/venv/bin"
ExecStart=/home/azureuser/Projet_Cloud_Computing/backend/venv/bin/python3 /home/azureuser/Projet_Cloud_Computing/backend/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable flaskapp
systemctl restart flaskapp
