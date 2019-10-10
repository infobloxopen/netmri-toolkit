from infoblox_netmri.client import InfobloxNetMRI
import getpass

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
devices = dev_broker.index()
devname = "your-device-name"

'''
Below iterates through devies from the device broker indexing.  Then, pull out the "DeviceID"
value from the device that matches "devname" and put that DeviceID in the "Interface" broker
find method.
'''
for device in devices:
    if devname in str(device.DeviceName):
        dev_id = str(device.DeviceID)
        int_broker = client.get_broker('Interface')
        int_data = int_broker.find(op_DeviceID="=",
                                 val_c_DeviceID=dev_id) # All interfaces for this device ID
        vlan_broker = client.get_broker("IfVlan") # Broker for interface VLANs
        for int_value in int_data: # Iterate through all of the interface on the device
            if int_value.vlan: # If there are VLANs associated to the interface.
                vlan_data = vlan_broker.find(op_InterfaceID="=",
                                            val_c_InterfaceID=int_value.InterfaceID) # each of the interface ID's
                for i in vlan_data: # Iterate through each of the Interface ID's VLAN values
                    vlanid_data = vlan_broker.vlan(id=i.IfVlanID) # Insert the IfVlanID into the operator
                    print(int_value.ifName, vlanid_data.VlanIndex) # Print out the interface number with VLAN
