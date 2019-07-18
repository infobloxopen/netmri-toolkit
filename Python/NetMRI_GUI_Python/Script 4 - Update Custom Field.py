# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     $vendor eq "Cisco" and $type eq “Firewall”
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
    "batch_id": batch_id
}

# Create NetMRI context manager. It will close session after execution
with NetMRIEasy(**defaults) as easy:
    # Everything has to be indented under the context manager if we are sending commmands to NetMRI
    #
    # This is how you will create a custom field name, we are using "Sif Test2"
    #
    broker = easy.client.get_broker('CustomFields')
    broker.create_field(
        model='Device',
        name='Sif Test2',
        type='string'
    )

    # get device
    device = easy.get_device()
    #
    # The method for retrieving the serial number via the
    # CLI depends on the type of device.
    #
    # This portion of the code will run if the Device is a Router
    # For the gather the serial number we are using RegEx - check out FB/ArtOfRegex
    #
    if device.DeviceType == 'Router':
        inventory = easy.send_command('show inventory')
        serial = re.search('(?<=SN: ).*$', inventory).group()
    #
    # This portion of the code will run if the Device is anything but a Router
    # For the gather the serial number we are using RegEx - check out FB/ArtOfRegex
    #
    else:
        info = easy.send_command('show version | inc System serial')
        serial = re.search('(?<=System serial number: ).*$', info).group()


    # Custom field "sif_test" update
    # all custom fields should start with 'custom_'
    device_broker = easy.client.get_broker('Device')
    field_name = "custom_{}".format('sif_test2')
    params = {
        'DeviceID': device.DeviceID,
        field_name: serial
    }
    result = device_broker.update(**params)
    print(result)
