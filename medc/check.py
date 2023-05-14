#!/usr/bin/python3

import requests 
from time import sleep
from os import path
import os
import subprocess, signal

#SERVER = "http://dev-estrlab.000webhostapp.com"
SERVER = "http://89.147.133.137"
medc_path = "/root/medc/"
download_path = "/root/download/"
if (not path.exists(download_path)): os.system("mkdir " + download_path)

_file_ = "medc.tar"

#meterid = "031900101595"
meterid = ""
 
def check_update(meterid):
    global SERVER
    URL = SERVER + "/medc/update.php"
    PARAMS = {'meterid':meterid}
    try:
    	r = requests.get(url = URL, params = PARAMS)
    	if (r!=None):
    		return r.text
    	else:
    		return None
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return None

def download():
	# wget http://89.147.133.137/medc/update/medc.tar
	global SERVER
	#os.system("cd /root/medc/download/")
	cmd = "cd " + download_path + " && wget " + SERVER + "/medc/update/" + _file_
	os.system(cmd)
	sleep(3)
    
	
def done_update(meterid):
    global SERVER
    URL = SERVER + "/medc/done_update.php"
    PARAMS = {'meterid':meterid}
    try:
    	r = requests.get(url = URL, params = PARAMS)
    	if (r!=None):
    		return r.text
    	else:
    		return None
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return None
        
def check_internet():
    url = "http://www.kite.com"
    timeout = 2
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return False

def kill_process():
	p = subprocess.Popen(['ps'], stdout=subprocess.PIPE)
	out, err = p.communicate()
	process = 'python3 ' + medc_path + 'meter/main.py'
	for line in out.splitlines():
		line = line.decode()
		if process in line:
			print(line)
			pid = int(line.split(None, 1)[0])
			print(pid)
			os.kill(pid, signal.SIGKILL)
					
while(not path.exists( medc_path + "id.txt")): pass

file__ = open(medc_path + "id.txt" , "r")
meterid = file__.readline()
file__.close()

while True:     
	t = check_update(meterid)
	print(t)
	if (t=="1"):
		print("new update")
		sleep(2)
		# downlod update
		download()
		
		# check if it is downloaded successfully
		exist = path.exists( download_path + _file_)
		print(exist)
		
		if (exist):
			# move the newer code
			os.system("cd " + download_path + " && tar -xvf " + _file_)
			
			# check exctraction
			exist1 = path.exists( download_path + _file_.replace(".tar",""))
			print(exist1)
		
			if(exist1):
				# stop and remove the older code
				os.system("rm -r /root/medc")
				#os.system("mv " + medc_path + _file_.replace(".tar","") + " " + medc_path + _file_.replace(".tar","") + "2")
				#os.system("mv " + download_path + _file_.replace(".tar","") + " " + medc_path + _file_.replace(".tar","") )
				os.system("cp -r " + download_path + _file_.replace(".tar","") + " /root/" )
				
				# remove
				os.system("rm -r " + download_path + "*" )
				os.system("rm " + download_path +  "*" )

				# check that it is updated
				done_update(meterid)
				
				# stop
				kill_process()
				sleep(1)
				
				print("reboot")
				os.system("reboot")
				sleep(2)
				#exit()
		else:
			print("failed")
			sleep(5)
		
