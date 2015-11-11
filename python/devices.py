#!/usr/bin/python

import os

import infoblox_netmri

url = os.environ['NETMRI_API_URL']
user = os.environ['NETMRI_USER']
password = os.environ['NETMRI_PASSWORD']
sslverify = os.environ.get('NETMRI_SSLVERIFY')

if sslverify is not None and sslverify.lower() == "false":
    sslverify = False
else:
    sslverify = True


c = infoblox_netmri.InfobloxNetMRI({
    'url': url,
    'username': user,
    'password': password,
    'sslverify': sslverify
})

devices = c.api_request('devices/index', {'limit': 10})

FORMAT='%30s %16s %10s'
print FORMAT % ('Device Name', 'IP Address', 'Vendor')
for d in devices['devices']:
    print FORMAT % (d['DeviceName'], d['DeviceIPDotted'], d['DeviceVendor'])
