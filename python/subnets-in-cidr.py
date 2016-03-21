#!/usr/bin/python


import argparse
import netaddr
import os

import infoblox_netmri

parser = argparse.ArgumentParser()
parser.add_argument("cidr")
args = parser.parse_args()

print("Searching for subnets in %s." % args.cidr)

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

net = netaddr.IPNetwork(args.cidr)
range = "%s,%s" % (long(net.network), long(net.broadcast))

subnets = c.api_request('subnets/find',
                        {'op_SubnetIPNumeric': 'between',
                         'val_c_SubnetIPNumeric': range,
                         'include': 'vlan'})

print("Found %d subnets in %s." % (subnets['total'], args.cidr))
if subnets['total'] > subnets['current']:
    print("Showing first %d subnets found." % subnets['current'])

vlan_map = {}
for v in subnets['vlan']:
    vlan_map[v['VlanID']] = (v['VlanIndex'], v['VlanName'])

FORMAT='%20s %8s %20s'
print FORMAT % ('Subnet', 'VLAN ID', 'VLAN Name')
for s in subnets['subnets']:
    vlan = vlan_map.get(s['VlanID']) or ('n/a', 'Unknown')
    print FORMAT % (s['SubnetCIDR'], vlan[0], vlan[1])
