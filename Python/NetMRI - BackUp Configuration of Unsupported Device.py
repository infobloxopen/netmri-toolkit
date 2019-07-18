# Adding Install directions can be found here:
# https://community.infoblox.com/t5/Community-Blog/NetMRI-Customized-Configuration-Collection/ba-p/15639
#
# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# Script-Variables:
#     $cliuser string
#     $clipwd password
#
# END-SCRIPT-BLOCK

from infoblox_netmri.easy import NetMRIEasy
import paramiko
import time
import requests
#
# This will not error when you are not verifing Certs for https
#
requests.packages.urllib3.disable_warnings()
#
# "netmri_ipaddress" is a wellknown variable of your NetMRI
# I broke up the API version and the API call
#
api_v = "/api/3.3"
api_command = "/config_revisions/import_custom_config"
url = "https://"+ netmri_ipaddress + api_v + api_command


def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''
    remote_conn.send("terminal length 0\n")
    time.sleep(1)
    # Clear the buffer on the screen
    output = remote_conn.recv(1000)
    return output

if __name__ == '__main__':
    # We will prompt you for the username and password
    # "ip" will equal the well known variable "ipaddress"
    ip = ipaddress
    username = cliuser
    password = clipwd

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
         paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print ("SSH connection established to %s" % ip)

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print ("Interactive SSH session established")

    # Strip the initial router prompt
    output = remote_conn.recv(1000)

    # See what we have
    print (output)

    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send("show ip int brief\n")

    # Wait for the command to complete
    time.sleep(2)
    
    output = remote_conn.recv(5000)
    print (output)
    #
    # Below I statically define the "DeviceID" which is "2" in this example this is my "Home Router" :)
    # We are going to add the following to 'RunningConfig': 'Testing 123456','SavedConfig': 'Testing 654321'
    #
    payload = {'DeviceID': device_id, 'RunningConfig': output,'SavedConfig': 'Testing 654321'}

    #
    # We are going to use the "Username" and "Password" you logined it with for the API call
    # http_username and http_password
    #
    r = requests.get(url, auth=(http_username, http_password), data=payload, verify=False)
