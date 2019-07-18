#Device subinterface data retrieval script. Copyright Ingmar Van Glabbeek ingmar@infoblox.com
#Licensed under Apache-2.0

#This script will pull all devices of a given device group and then list the devices management ip as well as the available management ips.
#By default it saves the output to "deviceinterfacedump.json"
#Tested on NetMRI 7.3.1 and 7.3.2

#Modules required:
import getpass
import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth
from http.client import responses
import time

#You can hardcode credentials here, it's not safe. Don't do it.
#hostname = "netmri.infoblox.com"
#username = "admin"
#password = "infoblox"
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():

    cookie_host = wapi_connect()
    #print(cookie_host)
    devicelist = getdevices(cookie_host)
    filtered_data = devicedata(devicelist)
    #uncomment next line if you want to write to console
    #print(json.dumps(filtered_data,indent=4, sort_keys=True))
    filename = open("deviceinterfacedump.json","w")
    filename.write(json.dumps(filtered_data,indent=4))
    filename.close()

    print("Data retrieved successfully")

def devicedata(devicelist):
    listload = json.loads(devicelist)
    data = []
    for e in listload['rows']:
        if not e["if_addrs"]:
            device = {"DeviceID":e["DeviceID"],"DeviceName":e["DeviceName"],"DeviceType":e["DeviceType"],"DeviceIPDotted":e["DeviceIPDotted"],"Other InterfaceIP":["none"]}
            data.append(device)
        else:
            device = {"DeviceID": e['DeviceID'], "DeviceName": e["DeviceName"], "DeviceType": e["DeviceType"],
                      "DeviceIPDotted": e["DeviceIPDotted"], "Other InterfaceIP":[]}
            for f in e["if_addrs"]:
                i=1
                interface = {"InterfaceIP":f["ifIPDotted"], "Interfacename":f["ifName"]}
                device["Other InterfaceIP"].insert(i,interface)
                data.append(device)
                i=i+1
    dataftw=json.dumps(data)
    returndata=json.loads(dataftw)
    return returndata


def getdevices(cookie_host):
    if not cookie_host:
        print("No connection established.")
        return 0
    #get current time
    ts = time.time()
    hostname=cookie_host[1]
    #limits number of results
    limit = input("Limit to this number of devices: ")
    get_url = "https://" + hostname + "/api/3.3/device_groups/index"
    response = requests.get(get_url, cookies=cookie_host[0], verify=False)
    d=response.text
    dl=json.loads(d)
    print("List of DeviceGroups")
    for e in dl["device_groups"]:
        dglist={"GroupName":e["GroupName"],"GroupID":e["GroupID"]}
        print(dglist)

    devicegroup = input("Based on the output specify the devicegroup ID by its ID: ")

    get_url = "https://" + hostname + "/api/3.3/discovery_statuses/static/current.extjs"
    querystring = {"_dc": ts, "filename": "recent_activity.csv", "filter": "null", "limit": limit,
                   "GroupID": devicegroup}

    response = requests.get(get_url, cookies=cookie_host[0], verify=False, params=querystring)
    t=response.text
    print("We are fetching a list of " + str(limit) +
          " devices for devicegroup " + str(devicegroup) + ".")
    return(t)



def wapi_connect():
    hostname = input("Enter the NetMRI hostname or IP: ")
    username = input("Enter your NetMRI username: ")
    password = getpass.getpass("Enter your Password: ")
    https_val = input("Disable SSL validations?(y/n) ")
    if https_val in ("y", "Y"):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print("SSL validation disabled")
    if https_val in ("n", "N"):
        print("SSL validation enabled")

    login_url = "https://" + hostname + "/api/3.3/device_groups/index"
    print("logging in to " + hostname)
    try:
        login_result = requests.get(
            login_url,
            auth=HTTPBasicAuth(username, password),
            timeout=5,
            verify=False)
    except requests.exceptions.ConnectTimeout as e:
        print("Connection time out after 5 seconds.")
        exit(1)
    except requests.exceptions.ConnectionError as e:
        print("No route to host " + hostname)
        exit(1)

    if has_error(login_result):
        exit(1)
    else:
        print("Login OK")
        return(login_result.cookies,hostname)


def has_error(_result):
    if _result.status_code == 200:
        return 0
    elif _result.status_code == 201:
        return 0

    try:
        err_text = _result.json()['text']
    except KeyError as e:
        err_text = "Response contains no error text"
    except json.decoder.JSONDecodeError as e:
        err_text = "No JSON Response"

    # print out the HTTP response code, description, and error text
    http_code = _result.status_code
    http_desc = responses[http_code]
    print("HTTP Code [%3d] %s. %s" % (http_code, http_desc, err_text))
    return 1


if __name__ == "__main__":
    main()
