import requests
import json


requests.packages.urllib3.disable_warnings()
s = requests.Session()

def netmriLogin( temp, querystring ):
    username = "admin"
    password = "infioblox"
    url = "https://demo-netmri.infoblox.com/api/3.3" + temp
    response = s.request("GET", url, params=querystring, verify=False,
                         auth=(username, password))
    t = response.text
    return(t);


t = netmriLogin(temp="/device_group_members/index", querystring={"GroupID":"20","select":"DeviceID"})
z = json.loads(t)

for entry in z['device_group_members']:
    print(entry['DeviceID'])
    filename = str(entry['DeviceID']) + ".txt"
    device = {"DeviceID": entry['DeviceID']}
    with open(filename, "w") as f:
        p = netmriLogin(temp="/devices/diagnostic", querystring=device)
        i = json.loads(p)
        print(type(i))
        print(i)
        f.write(i['text'])


