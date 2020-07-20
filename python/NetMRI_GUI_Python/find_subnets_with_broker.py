# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# END-SCRIPT-BLOCK

from infoblox_netmri.easy import NetMRIEasy
import re

# This values will be provided by NetMRI before execution
defaults = {
    "api_url": api_url,
    "http_username": http_username,
    "http_password": http_password,
    "job_id": job_id,
    "device_id": device_id,
    "batch_id": batch_id,
    "script_login" : "false"
}

# Create NetMRI context manager. It will close session after execution
with NetMRIEasy(**defaults) as easy:
    subnet_broker = easy.client.get_broker('Subnet')
    all_subnets = subnet_broker.index
    print(all_subnets)
    params = {
        'select': 'SubnetCIDR'
    }
    results = all_subnets(**params)
    for entry in results:
        print(entry.SubnetCIDR)
