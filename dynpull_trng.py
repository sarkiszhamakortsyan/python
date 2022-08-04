#!/usr/bin/python

import os, sys
import pycurl, urllib, StringIO
import json
import fcntl, socket, struct
import binascii, hashlib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd = sock.fileno()
SIOCGIFADDR = 0x8915

def get_ip(iface = 'eth0'):
	ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)
	try:
		res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
	except:
		return None
	ip = struct.unpack('16sH2x4s8x', res)[2]
	return socket.inet_ntoa(ip)


# should we guard: inbound client-initiated, otherwise passthrough?

# get credentials capable of updating user accounts
integration_dir = '/opt/Axway/SecureTransport/autosys-integration'
configfile = integration_dir+'/as2st2.cfg'

# extract credentials from config file
f = open(configfile,'r')
arecovered = binascii.unhexlify(f.read(128))
precovered = binascii.unhexlify(f.read(128))
f.close()

dig = hashlib.sha512()
dig.update('saltpepper')
adigarray = bytearray(dig.digest())
dig = hashlib.sha512()
dig.update('sodiumchloride')
pdigarray = bytearray(dig.digest())

unzipped = b"".join([chr(ord(a)^b) for (a,b) in zip(arecovered,adigarray)])
authuser = unzipped.rstrip()
unzipped = b"".join([chr(ord(a)^b) for (a,b) in zip(precovered,pdigarray)])
authpass = unzipped.rstrip()

print "Dynamic Pull: "

#print sys.argv

if len(sys.argv) < 3:
	print "Bad argument count."
	sys.exit(-1)

#print len(sys.argv)
#print sys.argv[1]

#if sys.argv[1] != "client_upload":
#	print "File not uploaded by client. Order file detection skipped. Exiting normally."
#	sys.exit(0)

#originalfiles = sys.argv[2]
# trim off enclosing "["/"]" brackets, which are always present
#if len(originalfiles) > 1:
#	originalfiles = originalfiles[1:-1]

# now we have a path... so how to recognize order files when the subscription folder is not directly stated?

#print sys.argv[2]
#print len(sys.argv[2])
#print originalfiles
#print len(originalfiles)

accounthome = os.environ.get('ST_ACCOUNT_HOME')
hostname = get_ip('eth0')
# OZ LAB is not configured like DEV/UAT/PROD
if hostname == None:
	hostname = get_ip('eth2')
#loginname = os.environ.get('STSESSION_DXAGENT_LOGINNAME')
# issue... above is not set for server-initiated pull!

# optional flow variable
overridefolder = os.environ.get('Flow_userVars.downloadFolder')

# mandatory flow variable
triggerthis = os.environ.get('Flow_userVars.dynamicSubscription')
# add complaint to carp if None
if triggerthis == None:
	print "Flow_userVars.dynamicSubscription not defined."
	sys.exit(-1)
# be tolerant and ensure prefix is "/"
if triggerthis != None and triggerthis[0] != '/':
	triggerthis = "/"+triggerthis
# it was either that or error out with descriptive message
#print "subscription to trigger="+triggerthis

# security concept: confirm subscription to be triggered is in account
#	then confirm that BU of account is same as BU invoking
#	prevents abuse via account name override
accountname = sys.argv[1]
invokingbu = os.environ.get('ST_ACCOUNT_BU')

# first directory in target dir is subscription folder
targetdir = sys.argv[2]
targetfile = sys.argv[3]

# composite location of target file
orderfile = accounthome+targetdir+"/"+targetfile

print orderfile

# default to "OrderFiles/*"
#ordermatch = "OrderFiles/*"
#if os.environ.get('Flow_userVars.orderfile') == None:
#	print "orderfile (pattern for matching) undefined in subscription. Defaulting to 'OrderFiles/*'."
#else:
#	ordermatch = os.environ.get('Flow_userVars.orderfile')

# if order file filter not implemented; all client-initiated push will trigger
print "processing orderfile="+orderfile


print "account="+accountname

credentials = authuser+":"+authpass

resturl = 'https://'+hostname+":444/api/v1.4/"

# - get loginname of declared account
#url = resturl+"accounts/"+accountname+"/users"
#params = {
#	'accountName': accountname
#}
#fullurl = url+'?'+urllib.urlencode(params)
#buffer = StringIO.StringIO()
#c = pycurl.Curl()
#c.setopt(c.URL, fullurl)
#c.setopt(c.WRITEFUNCTION, buffer.write)
#c.setopt(c.SSL_VERIFYPEER, False)
#c.setopt(c.USERPWD, credentials)
#c.perform()
#c.close()
#body = buffer.getvalue()
#buffer.close()
#users = json.loads(body)
#username = users["users"][0]["name"]

# - compare with account BU from environment
#if loginname != username:
#	print "account name and login name do not match:"
#	sys.exit(-1)

# get subscription folder
# get subscription ID for later transfer site query
url = resturl+"subscriptions"
params = {
	'account': accountname,
	'folder': triggerthis
}
fullurl = url+'?'+urllib.urlencode(params)
buffer = StringIO.StringIO()
c = pycurl.Curl()
c.setopt(c.URL, fullurl)
c.setopt(c.WRITEFUNCTION, buffer.write)
c.setopt(c.SSL_VERIFYPEER, False)
c.setopt(c.USERPWD, credentials)
c.perform()
c.close()
body = buffer.getvalue()
buffer.close()
subs = json.loads(body)
# add check for mismatch?
# JSON contains Unicode; convert to ASCII
subid = subs["subscriptions"][0]["id"].encode("ascii")
folder = subs["subscriptions"][0]["folder"].encode("ascii")

print "dynamicSubscription="+folder

# get transfer site to pull from
url = resturl+'subscriptions/'+subid+'/transferConfigurations'
fullurl = url
buffer = StringIO.StringIO()
c = pycurl.Curl()
c.setopt(c.URL, fullurl)
c.setopt(c.WRITEFUNCTION, buffer.write)
c.setopt(c.SSL_VERIFYPEER, False)
c.setopt(c.USERPWD, credentials)
c.perform()
c.close()
body = buffer.getvalue()
buffer.close()
transferConfigurations = json.loads(body)
# JSON contains Unicode; convert to ASCII
if "site" in transferConfigurations["transferConfigurations"][0]:
	site = transferConfigurations["transferConfigurations"][0]["site"].encode("ascii")
	#print "site="+site
else:
	print "Subscription \""+triggerthis+"\" is missing transfer site to pull from."
	sys.exit(-1)

lines = 0
orders = open(orderfile,"r")
line = orders.readline().rstrip("\r\n")

# undocumented REST API call
url = resturl+'transfers/pull'

while line:
#	print line
	# break line into directory and file
	if line == '':
		continue
	if line[0] != '/':
		line = '/'+line
	components = line.rpartition('/')
	specialfolder = components[0]
	# be tolerant and add prefix
	if specialfolder == '' or triggerthis[0] != '/':
		specialfolder = '/'+specialfolder
	# process subscription override
	if overridefolder != None:
		specialfolder = overridefolder
	specialpattern = components[2]

	fullurl = url

	params = {
		'accountName': accountname,
		'destinationDirectory': folder,
		'site': site,
		'SPECIALFOLDER': "\""+specialfolder+"\"",
		'SPECIALPATTERN': "\""+specialpattern+"\""
	}
	postfields = json.dumps(params)

	lines = lines + 1
	print "line="+str(lines)
	print "pulling="+specialpattern
	print "from="+specialfolder
        print fullurl
        print params

	buffer = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, fullurl)
	c.setopt(pycurl.HTTPHEADER, ['Accept:application/json',"Content-Type:application/json"])
	c.setopt(c.POSTFIELDS, postfields)
	c.setopt(c.WRITEFUNCTION, buffer.write)
	c.setopt(c.SSL_VERIFYPEER, False)
	c.setopt(c.USERPWD, credentials)
	c.perform()
	status = c.getinfo(c.HTTP_CODE)
	c.close()

	body = buffer.getvalue()
	buffer.close()
	subs = json.loads(body)
	print "status="+str(status)

	# read next line
	line = orders.readline().rstrip("\r\n")
orders.close()

print "Lines processed: "
print lines

#print os.environ

# normal exit
sys.exit(0)
