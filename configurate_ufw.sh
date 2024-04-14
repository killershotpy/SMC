#!/bin/bash

cat <<EOF > /etc/ufw/applications.d/smc-server
[SMC]
title=SMC Service
description=Service machine communication socket server
ports=any
EOF

ufw enable
ufw reload

rule_number=$(ufw status numbered | grep 'SMC (v6)' | cut -d ']' -f 1 | tr -d '[')

if [[ -n "$rule_number" ]]; then
    echo "Delete $rule_number IPv6"
    ufw --force delete "$rule_number"
else
    echo "Not found IPv6 rule for SMC"
fi