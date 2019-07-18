###########################################################################
## Export of Script: Sif - Python GetList
## Script-Level: 3
## Script-Category: 
## Script-Language: Python
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	Sif - Python GetList

# END-INTERNAL-SCRIPT-BLOCK

# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
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

# Create NetMRI context manager. It will close session after execution
with NetMRIEasy(**defaults) as easy:
    # Everything has to be indented under the context manager if we are sending commmands to NetMRI
    #
    # This is how you get a list named "sif_test" and look up column "name" that contains "device_devicename" and get what's in the "location" column
    #
    mylocation = easy.get_list_value("sif_test", "name", device_devicename,"location", "null");
    # print (mylocation)
    easy.send_command('config t')
    easy.send_command("snmp-server location {}".format(mylocation))
    easy.send_command('end')
    easy.send_command('wr mem')

