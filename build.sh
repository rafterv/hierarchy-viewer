#!/bin/bash

# Dependancies
sudo apt update
sudo apt upgrade -y
sudo apt install graphviz git nginx python3 python3-pip ntp -y
pip install pyyaml ua-parser user-agents pandas flask

#NTP Config
NTP_SERVERS="172.30.1.2"
echo -e "$NTP_SERVERS" | sudo tee /etc/ntp.conf > /dev/null
sudo systemctl restart ntp

# Install Application
cd /var/www
sudo git clone https://github.com/rafterv/hierarchy-viewer.git
mkdir /var/www/hierarchy-viewer/uploads
mkdir /var/www/hierarchy-viewer/downloads
sudo chown hviewer:hviewer uploads
sudo chown hviewer:hviewer downloads
sudo mkdir /usr/share/fonts/truetype/century-gothic
sudo cp /var/www/hierarchy-viewer/data/CenturyGothic\ -\ Century\ Gothic\ -\ Regular.ttf /usr/share/fonts/truetype/century-gothic


# Setup File Cleanup
CRON_JOB_COMMAND="/usr/bin/python3 /var/www/hierarchy-viewer/backend/file_cleanup.py"
echo "0 * * * * $CRON_JOB_COMMAND" | crontab -


# Setup Logging
APP_DIR="/var/www/hierarchy-viewer"
APP_FILE="server.py"
FLASK_LOG_FILE="/var/log/flask.log"
VIEWER_LOG_FILE="/var/log/viewer.log"
METRICS_LOG_FILE="/var/log/metrics.log"
sudo touch "$FLASK_LOG_FILE"
sudo touch "$VIEWER_LOG_FILE"
sudo touch "$METRICS_LOG_FILE"
sudo chown hviewer:hviewer "$FLASK_LOG_FILE"
sudo chown hviewer:hviewer "$VIEWER_LOG_FILE"
sudo chown hviewer:hviewer "$METRICS_LOG_FILE"
sudo chmod 664 "$FLASK_LOG_FILE"
sudo chmod 664 "$VIEWER_LOG_FILE"
sudo chmod 664 "$METRICS_LOG_FILE"

# Create a systemd service unit file for Flask
cat << EOF | sudo tee /etc/systemd/system/flask.service > /dev/null
[Unit]
Description=Flask Application
After=network.target

[Service]
User=hviewer
Group=hviewer
WorkingDirectory=$APP_DIR
Environment="FLASK_APP=$APP_FILE"
ExecStart=/usr/bin/python3 -u $APP_FILE > $FLASK_LOG_FILE 2>&1
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable flask
sudo systemctl start flask

# Setup NGINX Reverse Proxy
cat << 'EOF' | sudo tee /etc/nginx/sites-available/hviewer-proxy > /dev/null
server {
    listen 80;
    server_name hostname.domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/hviewer-proxy /etc/nginx/sites-enabled
sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/default.backup
sudo systemctl reload nginx

#Setup Firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable






