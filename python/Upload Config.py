###########################################################################
## Export of Script: Sif - Upload Config
## Script-Level: 3
## Script-Category: Uncategorized
## Script-Language: Python
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	Sif - Upload Config

# END-INTERNAL-SCRIPT-BLOCK


# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# Script-Variables:
#     $gmuser string "Grid Master Username"
#     $gmpassword password "Grid Master Password"
#
# END-SCRIPT-BLOCK

import requests
import json, re
# This will not error when you are not verifying Certs for https
#
requests.packages.urllib3.disable_warnings()
#
# gmip is a variable we asked for the Grid Master IP/FQDN
url = "https://192.168.0.201/api/3.3/config_revisions/import_custom_config/"
#

#
# The WPI call that we are going to use
payload = {'DeviceID': '4', 'RunningConfig': 'Testing 123456','SavedConfig': 'Testing 654321'}


r = requests.request("POST",url, auth=(gmuser, gmpassword), data=payload, verify=False)


