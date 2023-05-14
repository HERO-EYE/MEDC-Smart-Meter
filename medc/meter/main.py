#!/usr/bin/python3

import onionGpio
import os

buzzer = 11
red    = 3
green  = 2

try:
    BUZZER = onionGpio.OnionGpio(buzzer)
    RED    = onionGpio.OnionGpio(red)
    GREEN  = onionGpio.OnionGpio(green)
    status = BUZZER.setOutputDirection(0)
    status = RED.setOutputDirection(0)
    status = GREEN.setOutputDirection(0)
except:
    print("GPIO Exceptio")
    os.system("reboot")

    
medc_path = "/root/medc/"

import sys
import traceback
from gurux_serial import GXSerial
from gurux_dlms.enums import ObjectType
from gurux_dlms.objects.GXDLMSObjectCollection import GXDLMSObjectCollection
from MySettings import MySettings
from GXDLMSReader import GXDLMSReader
from gurux_dlms.GXDLMSClient import GXDLMSClient
from gurux_common.GXCommon import GXCommon
from gurux_dlms.enums.DataType import DataType
import locale
from gurux_dlms.GXDateTime import GXDateTime
from gurux_dlms.internal._GXCommon import _GXCommon
from gurux_dlms import GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError
from data import *
from time import sleep
from datetime import datetime
try:
    import pkg_resources
except Exception:
    print("pkg_resources not found")

main_error = 0
count = 0
reader = None
settings = MySettings()


def record(t):
    text = str(t)
    file = open("../mylog.txt", "w")
    file.write(text)
    file.close()
	
def tone():
    global buzzer
    status  = BUZZER.setValue(1)
    sleep(0.05)
    status  = BUZZER.setValue(0)
    
def readObjects():
    obj = input("Enter logical object with index(separated by : ) : ")
    dat = obj.split(":")
    if(len(dat)==2):
        getDataFromMeter(obj)           
    elif(obj=="0"):
        getDataFromMeter(settings.KWH)
                                                 
def getMeterDateTime():
    dt = DT = None
    DT = getDataFromMeter(settings.DATE_TIME)
    dt = datetime.strptime(str(DT), '%m/%d/%y %H:%M:%S')
    return dt
    
def getDataFromMeter(D):
    global settings, reader
    k = D.split(":")[0]
    v = int(D.split(":")[1])
    val = reader.read(settings.client.objects.findByLN(ObjectType.NONE, k), v)
    if (D!=settings.BILL): value = reader.showValue2(v, val)
    else: value = val
    if (D!=settings.BILL_CAPTURE): print("value : " , value)
    if (value == None):
        print("reconnect")
        reader.initializeConnection()
        print("initilization end.")
        val = reader.read(settings.client.objects.findByLN(ObjectType.NONE, k), v)
        if (D!=settings.BILL): value = reader.showValue2(v, val)
        else: value = val
        if (D!=settings.BILL_CAPTURE): print("value : " , value)
    return value
 
def calculateCost(kwh):
    if(kwh<=3000):
        cost = kwh*0.01
    elif(kwh<=5000):
        cost = kwh*0.015
    elif(kwh<=7000):
        cost = kwh*0.02
    elif(kwh<=10000):
        cost = kwh*0.025
    else:
        cost = kwh*0.03
    return cost
    
def getStartKwhMonthly(meterid):
    cap = getDataFromMeter(settings.BILL_CAPTURE)
    bill = getDataFromMeter(settings.BILL)

    print("all : " , len(bill))
    kwh_dt = []
    i = 0
    for b in bill:
        count = len(b)
        st_kwh = float(b[count-2])/1000.0
        print("kwh = " , st_kwh)
        dt = b[0]
        dt = dt.toFormatString("%x")
        da = datetime.strptime(dt, '%m/%d/%y')
        dat = str(da).replace(" 00:00:00" , "")
        print("date: " , b[0])
        print("datetime : " , dat)
        print("--------------------------------------------------------")   
        exist = False
    
        for d in kwh_dt:
            if (d[0]==dat): exist = True
        if (not(exist)):
        	kwh_dt.append([dat,float(st_kwh)])
        i += 1
    
    for j in range(len(kwh_dt)):
        val = kwh_dt[j]
        DT = val[0]
        k_start = val[1]
        
        if(j<(len(kwh_dt)-1)):
	        k_end = kwh_dt[j+1][1]
	        cost = calculateCost(float(k_end)-float(k_start))
        else:
            k_end = getDataFromMeter(settings.KWH)
            #kwh = getDataFromMeter(settings.KWH)
        
        if ('01' not in DT.split("-")[2]):
        	date_sp = DT.split("-")
        	m = str(int(date_sp[1])+1)
        	y = int(date_sp[0])
        	if (int(m)>12): 
        		m = "1"
        		y = int(date_sp[0])+1
        	if len(m)==1: m = "0" + m
        	DT = str(y) + "-" + str(m) + "-01"
        	
        #data = str(k_start) + ":" + str(k_end) + ":" + str(DT) + ":" + str(cost)
        data = str(int(k_start)) + ":" + str(int(k_end)) + ":" + str(DT)
        r = upload_startmonth_kwh(meterid , data)
        print("r : " , r)
        print("r.text : " , r.text)
        
        if (r!=None):
            if (r.text!='1'):
                return False
        else:
            return False
    
    #kwh = getDataFromMeter(settings.KWH)
    return True

def save_id(meter_id):
	global medc_path
	if (len(meter_id)>10):
		file = open(medc_path + "id.txt","w")
		file.write(meter_id)
		file.close()

def main():
        global settings, reader, main_error

        error = 0
        try:
                ret = settings.Parameters()
                status  = RED.setValue(1)

                reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter, settings.iec)
                settings.media.open()
             
                reader.initializeConnection()
                reader.getAssociationView()
                meter_id = getDataFromMeter(settings.DEVICE_SN)
                save_id(meter_id)
                reader.setMeterID_LDN(meter_id)
                
                if (check_internet()):
                    print("connected")
                else:
                    print("not connected")
                
                once = True
                res = getStartKwhMonthly(meter_id)
                if (res): once = False
                
                readObj = False
                 
                while True:
                    status  = RED.setValue(1)
                    try:
                        if (readObj): readObjects()
                        else:
	                        kwh = getDataFromMeter(settings.KWH)
	                        power = getDataFromMeter(settings.POWER)
	                        voltage = getDataFromMeter(settings.VOLTAGE)
	                        dt = getMeterDateTime()
	                        
	                        print("date : " , dt)
	                        kwh = float(kwh)/1000.0
	                        data = str(int(kwh)) + "@" + str(power) + "@" + str(voltage) + "@" + str(dt).replace(" " , "_")
	                        
	                        if (once):
	                            res = getStartKwhMonthly(meter_id)
	                            if (res): once = False
	                        error = 0
	                        r = upload(meter_id, data)
	                        if (r!=None):
	                            print("response : " , r.text)
	                            if (r.text=='1'):
	                                tone()
	                                sleep(15)
	                        else:
	                            if (check_internet()):
	                                print("connected")
	                                for i in range(3):
	                                	status = GREEN.setValue(1)
	                                	sleep(0.3)
	                                	status = GREEN.setValue(0)
	                                	sleep(0.3)
	                                status = GREEN.setValue(1)
	                            else:
	                                print("not connected")
                                        
                    except KeyboardInterrupt:
                        break
                    except Exception as e:
                        error += 1
                        print(e)
                        print("Exception (1)")
                        record(e)
                        #if (error > 5):
                            #reader.close()
                            #sleep(1)
                            #quit()
                        sleep(3)
                        #settings.media.open()
                        #reader.initializeConnection()
                        main()
                        if (error>2):
                        	try:
                        		reader.close()
                        	except: 
                        		pass
                        	os.system("reboot")
                        
                status  = RED.setValue(0)  
        except (ValueError, GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError) as ex:
            main_error += 1
            print("Exception (2)")
            print(ex)
            record(ex)
            sleep(3)
            if reader:
                try:
                    reader.close()
                except Exception:
                    traceback.print_exc()
            sleep(2)
            print("Running again")
            #os.system("reboot")
            if (main_error>2):
                os.system("reboot")
            else:
                main()
            #sys.exit("Exit")
        except (KeyboardInterrupt, SystemExit, Exception) as ex:
            main_error += 1
            print("Exception (3)")
            print(ex)
            record(ex)
            sleep(3)
            if reader:
                try:
                    reader.close()
                except Exception:
                    traceback.print_exc()
            sleep(2)
            print("Running again")
            if (main_error>2):
                os.system("reboot")
            else:
                main()
            #sys.exit("Exit")
            #os.system("reboot")

        finally:
        	main_error += 1
        	status  = RED.setValue(0)

        	if reader:
        		try:
        			reader.close()
        		except Exception:
        			traceback.print_exc()
        			
        	for i in range(3):
        		status  = RED.setValue(1)  
        		status  = BUZZER.setValue(1)  
        		sleep(0.3)
        		status  = RED.setValue(0)  
        		status  = BUZZER.setValue(0)  
        		sleep(0.3)
        		
        	print("Ended. Press any key to continue.")
        	sleep(3)
        	status  = RED.setValue(1)  
        	print("Running again")
        	os.system("reboot")

if __name__ == '__main__':
    main()
