#!/usr/bin/python3

import sys, paramiko

hostname = "192.168.1.100"
password = "S@k0"
command = "ls"

username = "sako"
port = 22

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.connect(hostname, port, username, password)
    stdin, stdout, stderr = client.exec_command(command)
#    print stdout.read()

finally:
    client.close()
