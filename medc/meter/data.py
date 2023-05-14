import requests 

#SERVER = "http://dev-estrlab.000webhostapp.com"
SERVER = "http://89.147.133.137"

def upload(meterid , data):
    global SERVER
    URL = SERVER + "/medc/data.php"
    print("url data = " , data)
    PARAMS = {'meterid':meterid , 'data':data}
    try:
        r = requests.get(url = URL, params = PARAMS)
        return r
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return None

def upload_startmonth_kwh(meterid , data):
    global SERVER  
    URL = SERVER + "/medc/sendStartKwhMonthly.php"
    print("kwh url data = " , data)
    PARAMS = {'meterid':meterid , 'data':data}
    try:
        r = requests.get(url = URL, params = PARAMS)
        return r
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
        return None
    

def check_update():
    global SERVER
    URL = SERVER + "/medc/data.php"
    print("url data = " , data)
    PARAMS = {'meterid':meterid , 'data':data}
    try:
        r = requests.get(url = URL, params = PARAMS)
        return r
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
