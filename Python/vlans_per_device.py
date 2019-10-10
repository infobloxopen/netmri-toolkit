from infoblox_netmri.client import InfobloxNetMRI
import getpass

def print_info(object):
    print(type(object))
    print(dir(object))

netmri_password = getpass.getpass("Enter the Password: ")

defaults = {
    "host": "netmri.yourdomain",
    "username": "a_username",
    "password": netmri_password,
}

client = InfobloxNetMRI(
    defaults.get("host"),
    defaults.get("username"),
    defaults.get("password"),
)

'''
Below broker is to get device ID from the "Device" broker
'''
dev_broker = client.get_broker("Device")
devices = dev_broker.index() # Indexes all NetMRI devices, but you could limit based on DeviceID or DeviceGroupID 
devname = "your-device-name" # You could always make this some other input, or just index the DeviceID if you know it.

'''
Below iterates through devices from the device broker indexing.  Then, pull out the "DeviceID"
value from the device that matches "devname" and put that DeviceID in the "VlanMember" broker
index method.
'''
for device in devices:
    if devname in str(device.DeviceName):
        print(device.DeviceName)
        dev_id = str(device.DeviceID)
        vlan_mem_broker = client.get_broker("VlanMember") # Broker for interface VLANs
        vlan_mem_find = vlan_mem_broker.index(DeviceID=dev_id) # Index based on DeviceID
        for val in vlan_mem_find: # Iterate through VlanMembers for specific DeviceID
            vlan_find = vlan_mem_broker.vlan(id=val.VlanMemberID) # Take VlanMemberID and query "vlan" to get VlanIndex
            print(vlan_find.VlanIndex, val.VlanName) # Print VLAN number (aka VlanIndex) and VLAN Name
