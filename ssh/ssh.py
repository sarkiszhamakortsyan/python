#!/usr/bin/python3

import paramiko

ip='192.168.1.100'
port=22
username='sako'
password='S@k0'

cmd='sh /bin/server-update &'

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,port,username,password)

stdin,stdout,stderr=ssh.exec_command(cmd)
outlines=stdout.readlines()
resp=''.join(outlines)
print(resp)

stdin,stdout,stderr=ssh.exec_command('ls')
outlines=stdout.readlines()
resp=''.join(outlines)
print(resp)
