# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# Script-Variables:
#     $new_password string "Enter Password"
#
# END-SCRIPT-BLOCK

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

command = "username bob secret 0 {}".format(new_password)
#print (command)
# Create NetMRI context manager. It will close session after execution
with NetMRIEasy(**defaults) as easy:
    easy.send_command('config t')
    easy.send_command(command)
    easy.send_command('end')
    easy.send_command('wr mem')
