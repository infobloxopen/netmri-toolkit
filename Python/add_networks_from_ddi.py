import requests
import json

requests.packages.urllib3.disable_warnings()

gm_user = "admin"
gm_pwd = "infoblox"
url = "https://192.168.0.200/wapi/v2.7/"
s = requests.Session()
s.auth = (gm_user, gm_pwd)
mri_url = "192.168.0.201"
mri_user = "admin"
mri_pwd = "netmripassword"

def get_networks_to_add():
    # We are going to search an EA called NetMRI and look for any value of ADD
    querystring = {"_return_fields+": "extattrs", "*NetMRI:": "Add"}
    # We are using the API Network method
    url2 = url + "network"
    response = s.get(url2,  params=querystring, verify=False)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def add_network_mri(net_new):
    url3 = "https://" + mri_url + "/api/3.3/discovery_settings/create"
    payload = "{\n\t\"range_value\" : \"" + net_new + \
        "\",\n\t\"range_type\" : \"CIDR\",\n\t\"discovery_status\" : \"INCLUDE\"\n}"
    headers = {'Content-Type': "application/json"}
    response = requests.post(url3,  data=payload, verify=False,
                     auth=(mri_user, mri_pwd), headers=headers)
    if response.status_code == 201:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def update_network_ea(ea):
    url1 = url + ea
    payload = "{\"extattrs\": { \"NetMRI\": { \"value\": \"Done\"}} }"
    headers = {'Content-Type': "application/json"}
    response = s.put( url1,  data=payload, verify=False, auth=(gm_user, gm_pwd), headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


account_info = get_networks_to_add()
#print(account_info)
if account_info is not None:
    print("Found the following network(s) will be added to NetMRI: ")
    for k in account_info:
        new_net_mri = k['network']
        add_netmri = add_network_mri(new_net_mri)
        if add_netmri is not None:
            print("[+] Added network " + new_net_mri + " for discovery")
            ea = k['_ref'] 
            done = update_network_ea(ea)
            if done is not None:
                print("[+] Updated EA for " + k['network'])
            else:
                print('[-] EA Update Request Failed' )
        else:
                print('[-] Update to NetMRI Failed' + k['network'])


else:
    print('[-] Request Failed')

