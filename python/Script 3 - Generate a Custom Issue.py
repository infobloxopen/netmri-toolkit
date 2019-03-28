# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# Script-Variables:
#     $command word "show version"
# END-SCRIPT-BLOCK

import requests, json, re
from infoblox_netmri.easy import NetMRIEasy

# This values will be provided by NetMRI before execution
defaults = {
    "api_url": api_url,
    "http_username": http_username,
    "http_password": http_password,
    "job_id": job_id,
    "device_id": device_id,
    "batch_id": batch_id
}

# Create NetMRI context manager. It will close session after execution
with NetMRIEasy(**defaults) as easy:
    vtpstatus = easy.send_command('show vtp status')
    regexp = re.compile(r"VTP Operating Mode\s*: (.*)")
    if regexp.search(vtpstatus):
        #print ('matched')
        status = re.search('(?<=VTP Operating Mode\s.)(.*)', vtpstatus, re.MULTILINE).group()
        if re.search(r'Server', status):
            issue_id = easy.generate_issue("info", "siftest",**{
                 "Host":device_devicename,
                 "IPAddress":device_deviceipdotted,
                 "noclue1":'test1',
                 "noclue2":'test2',
                 "device_id": device_id,
                 "batch_id": batch_id
            })
        else:
            print ('no match')
