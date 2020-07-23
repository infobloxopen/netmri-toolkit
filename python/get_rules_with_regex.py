import requests
gm_user = "admin"
gm_pwd = "infoblox"

# This is the "find" API call for Policy Rules 
url = "https://netmri/api/3.4/policy_rules/find"

# rlike allows us use regex with the "val_c_name"
# this will return all the rules that start with Sif_
payload = "{\n    \"op_name\":\"rlike\",\n    \"val_c_name\":\"Sif_\"\n}"
headers = {
  'Content-Type': 'application/json',
 }
response = requests.request("GET", url, headers=headers, data = payload,  verify=False, auth=(gm_user, gm_pwd))
print(response.text.encode('utf8'))