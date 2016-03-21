#!/usr/bin/python

import os

import infoblox_netmri

host = os.environ['NETMRI_HOST']
user = os.environ['NETMRI_USER']
password = os.environ['NETMRI_PASSWORD']
use_ssl = os.environ['NETMRI_USE_SSL']
api_version = os.environ['NETMRI_API_VERSION']
ssl_verify = os.environ.get('NETMRI_SSL_VERIFY')

c = infoblox_netmri.InfobloxNetMRI(
    host=host,
    username=user,
    password=password,
    api_version=api_version,
    use_ssl=use_ssl,
    ssl_verify=ssl_verify
)

devices = c.api_request('devices/index', {'limit': 10})

print devices.keys()

FORMAT='%30s %16s %10s'
print FORMAT % ('Device Name', 'IP Address', 'Vendor')
for d in devices['devices']:
    print FORMAT % (d['DeviceName'], d['DeviceIPDotted'], d['DeviceVendor'])
