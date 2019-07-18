###########################################################################
## Export of Script: Sif - Python Create Hostname in NIOS
## Script-Level: 3
## Script-Category: 
## Script-Language: Python
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	Sif - Python Create Hostname in NIOS

# Script-Description:
# 	'https://jsonplaceholder.typicode.com/users'

# END-INTERNAL-SCRIPT-BLOCK

# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# Script-Variables:
#     $gmuser string 'Grid Master Username'
#     $gmpassword password 'Grid Master Password'
#     $gmipaddress string '192.168.1.2'
#
# END-SCRIPT-BLOCK

from infoblox_netmri.easy import NetMRIEasy
import requests, json

requests.packages.urllib3.disable_warnings()
# This values will be provided by NetMRI before execution
defaults = {
    'api_url': api_url,
    'http_username': http_username,
    'http_password': http_password,
    'job_id': job_id,
    'device_id': device_id,
    'batch_id': batch_id
}

# Create NetMRI context manager. It will close session after execution
with NetMRIEasy(**defaults) as easy:
    device = device_devicename
    our_ip = device_deviceipdotted
    data = {
    	"name": "host3.aaa.com",
    	"ipv4addrs": [
    		{
    			"ipv4addr": our_ip
    		}
    	]
    }
    print (data)
    headers = {'Content-type': 'application/json'}
    url = "https://{}/wapi/v2.5/record:host".format(gmipaddress)
    r = requests.request("POST", url, verify=False,  data=json.dumps(data), headers=headers, auth=(gmuser, gmpassword))
    print (r.text)
