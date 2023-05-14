#!/usr/bin/python3

import os
from time import sleep
import threading

def getTasks(file):
    r = os.popen("ps | grep "+file).read().strip().split('\n')
    print ('# of tasks is %s' % (len(r)))
    if (len(r) > 2):
        return False
    else:
        return True

def main_code():
    while True:
        r = getTasks("'python3 /root/medc/meter/main.py'")
        print(r)
        if (r):
            sleep(3)
            os.system("python3 /root/medc/meter/main.py")
            sleep(5) 

def check_code():
    while True:
        r = getTasks("'python3 /root/medc/check.py'")
        print(r)
        if (r):
            sleep(3)
            os.system("python3 /root/medc/check.py")
            sleep(5) 

t = threading.Thread(target=main_code)
#t.daemon = True
t.start()

t2 = threading.Thread(target=check_code)
#t2.daemon = True
t2.start()
