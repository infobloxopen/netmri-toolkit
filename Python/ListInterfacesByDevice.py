#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import infoblox_netmri
import requests
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import getpass

disable_warnings(category=InsecureRequestWarning)

r = requests.Session()

# NetMRI base URL
NetMRIBaseUrl = "https://netmri.nwie.net/api/3.3/"

netmri_password = getpass.getpass("Enter the Password: ")

# Set our counters and incrementers
page_inc = 50
startpoint = 0

querystring = {
        'op_DeviceName': "rlike",
        'val_c_DeviceName': ".*",      # <- add you're regex here
        'methods': "interfaces",
        'select': "DeviceID,DeviceName,DeviceIPDotted",
        'start': startpoint,
        'limit': page_inc,
        }

# Find all network devices, include interfaces and interface addresses
response = r.get(
    NetMRIBaseUrl+'devices/find', params=querystring,
    verify=False,
    auth=('admin', netmri_password))
devices = json.loads(response.text)

while devices["total"]:

    # Loop thru all the devices
    for d in devices['devices']:
    
        # Loop thru all the interfaces for the device
        for i in range(len(d['interfaces'])):
            
            # Print out the interfaces
            print(d['DeviceName'], d['interfaces'][i]['ifName'], d['interfaces'][i]['ifDescr'])
        
    # Get the next page
    startpoint = startpoint + page_inc
    querystring.update({'start': startpoint})

    # Find all network devices, include interfaces and interface addresses
    response = r.get(
        NetMRIBaseUrl+'devices/find', params=querystring,
        verify=False,
        auth=('admin', netmri_password))
    devices = json.loads(response.text)
