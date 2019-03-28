# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# Script-Variables:
#     $gmuser string "Grid Master Username"
#     $gmpassword password "Grid Master Password"
#     $gmipaddress string "192.168.1.2"
#
# END-SCRIPT-BLOCK

import requests
import json, re
# This will not error when you are not verifing Certs for https
#
requests.packages.urllib3.disable_warnings()
#
# gmip is a varible we asked for the Grid Master IP/FQDN
gmip = "https://{}/wapi/".format(gmipaddress)
#
# The version of WAPI you are using
wapi = "v2.5"
#
# The WPI call that we are going to use
call = "/network?*NetMRI%3A=Yes&_return_fields%2B=extattrs"
#
# Now we combine all the above to equal "url"
# https://192.168.1.2/wapi/v2.5/network?network=10.10.10.0/24
url = gmip + wapi + call

r = requests.get(url, auth=(gmuser, gmpassword), verify=False)

json_input = r.text

decoded = json.loads(json_input)
#print (decoded['network'])

for j in decoded:
    print (j['network'], j['network_view'],j['_ref'])
    url1 = "{}/api/3.2/discovery_settings/create?range_value=".format(api_url)
    url2 = j['network']
    url3 = "&range_type=CIDR&discovery_status=INCLUDE"
    url4 = url1 + url2 + url3
    #print (url4)
    add_net = requests.get(url4, auth=(gmuser, gmpassword), verify=False)
    print ("Added")
    call2 = j['_ref']
    url_update = gmip + wapi + "/" + call2
    print (url_update)
    payload = "{\n\t\"extattrs\": {\n\t\t\"NetMRI\": {\n\t\t\t\"value\": \"Done\"\n\t\t}\n\t}\n}"
    response = requests.request("PUT", url_update,auth=(gmuser, gmpassword), data=payload, verify=False)
    print(response.text)
