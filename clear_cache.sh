#!/bin/bash

cat <<EOF > /etc/systemd/system/SMC.service
[Unit]
Description=My Shell Script

[Service]
ExecStart=bash "/clear_cache.sh"
Restart=always

[Install]
WantedBy=multi-user.target
EOF

cat <<'EOF' > /clear_cache.sh
#!/bin/bash

while true; do
  sync; echo 1 > /proc/sys/vm/drop_caches;
  sync; echo 2 > /proc/sys/vm/drop_caches;
  sync; echo 3 > /proc/sys/vm/drop_caches;

  sleep 10;
done
EOF

chmod +x /clear_cache.sh
systemctl daemon-reload
systemctl enable clear_cache.service
systemctl start clear_cache.service
