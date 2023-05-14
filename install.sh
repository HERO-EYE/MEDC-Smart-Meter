#!/bin/sh

opkg update
opkg install python3 
opkg install python3-pip
pip3 install pyserial
pip3 install gurux-common
#pip3 install gurux-serial
pip3 install gurux-dlms
pip3 install requests

wget http://89.147.133.137/medc/update/medc.tar
tar -xvf medc.tar

rm medc.tar

cd medc
mv rc.local /etc/rc.local
cp meter/onionGpio.py /usr/lib/python3.6/site-packages/
#python3 /root/medc/check.py &
python3 /root/medc/process.py

#reboot