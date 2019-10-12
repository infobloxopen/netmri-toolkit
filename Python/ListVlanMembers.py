import requests, json
from getpass import getpass
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import pprint

disable_warnings(category=InsecureRequestWarning)

# Username and password
user = "admin"
password = getpass("Enter your Infoblox password: ")

# Setup pretty print
pp = pprint.PrettyPrinter(indent=4)

# Create session for requests
session = requests.Session()

base_url = "https://netmri/api/3.3/"

index_uri = "vlan_members/index"

# DeviceID is hard coded. Uses the method of vlan
index_querystring = {"DeviceID": "102", 'methods':"vlan"}
index_response = session.get(base_url + index_uri , params=index_querystring, verify=False, auth=(user, password))
vlan_members = json.loads(index_response.text)

# To visualize what is returned
pp.pprint(vlan_members)

# List out vlan index for each vlan member
for members in vlan_members['vlan_members']:
    print(members['vlan']['VlanIndex'])
