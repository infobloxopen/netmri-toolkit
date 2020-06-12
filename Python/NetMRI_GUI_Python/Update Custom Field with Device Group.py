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
    # get device
    device = easy.get_device()
    print(device.DeviceID)
    grp_broker = easy.broker('DeviceGroup')
    mem_broker = easy.broker('DeviceGroupMember')
    members = mem_broker.index
    grp = grp_broker.index
    params = {
        'DeviceID': device.DeviceID,
        'select': 'GroupID'
    }
    result = members(**params)
    groups= ""
    for entry in result:
        print(entry.GroupID)
        grp_params = {
            'DeviceGroupID': entry.GroupID,
            'select': 'GroupName'
        }
        grp_r = grp(**grp_params)
        print(grp_r)
        for entry1 in grp_r:
            print(entry1.GroupName)
            r1 = re.findall(r"^[a-z]{3}\d.*", entry1.GroupName, re.IGNORECASE)
            if r1:
                groups += str(entry1.GroupName) + " "

    # Custom field "sif_test2" update
    # all custom fields should start with 'custom_'
    print(groups)
    device_broker = easy.broker('Device')
    field_name = "custom_{}".format('sif_test2')
    params = {
        'DeviceID': device.DeviceID,
        field_name: groups
    }
    result = device_broker.update(**params)
