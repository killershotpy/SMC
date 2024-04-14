#!/bin/bash

cd ..
git clone https://github.com/killershotpy/SMC.git

cat <<EOF > /etc/systemd/system/SMC.service
[Unit]
Description=SMC socket server
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/SMC
ExecStart=/usr/bin/python3.9 /SMC/server_multiprocessing.py
StandardOutput=append:/var/log/SMC.log
StandardError=append:/var/log/SMC.log

[Install]
WantedBy=multi-user.target
EOF

systemctl enable SMC
systemctl daemon-reload
systemctl restart SMC