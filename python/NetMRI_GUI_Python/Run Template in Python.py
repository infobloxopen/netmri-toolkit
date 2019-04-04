# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# Script-Variables:
#     $command word "show version"
# END-SCRIPT-BLOCK

import requests, json, re
from infoblox_netmri.easy import NetMRIEasy
import time

# This values will be provided by NetMRI before execution
defaults = {
    "api_url": api_url,
    "http_username": http_username,
    "http_password": http_password,
    "job_id": job_id,
    "device_id": device_id,
    "batch_id": batch_id
}

myeasy = NetMRIEasy(**defaults)
broker = myeasy.broker('ConfigTemplate')
sif = {
   "id" : '35',
   "device_ids" : device_id,
   "$sif" : 'siftest',
   "$templatemode" : 'bulk'
}
broker.run (**sif)

broker_script = myeasy.broker('Script')

save_new = {
    "name" : "sif_adhoc",
    "device_ids" : device_id,
    "job_name" : "Save New Config"

}
time.sleep(20)

broker_script.run (**save_new)