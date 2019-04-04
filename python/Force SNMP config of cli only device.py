# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# Script-Variables:
#     $cliuser string
#     $clipwd password
#     $deviceIP string
#
# END-SCRIPT-BLOCK

#The goal of this script is to force the configuration of SNMP. This resolves the issue of network devices with cli
# access which do not have SNMP configured and are therefore not discovered.

#This script requires paramiko to be installed in the sandbox, more info can be found on
#https://community.infoblox.com/t5/Community-Blog/NetMRI-Customized-Configuration-Collection/ba-p/15639

import paramiko
import time
import requests

#
# Following line to disable errors on self signed https certs. If you have a valid https cert you can comment it out.
#
requests.packages.urllib3.disable_warnings()

def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''
    remote_conn.send("terminal length 0\n")
    time.sleep(1)
    # Clear the buffer on the screen
    output = remote_conn.recv(1000)
    return output

if __name__ == '__main__':
    # Prompt you for username and password
    # you cannot run this against a device as many of these devices will not show up
    ip = deviceIP
    username = cliuser
    password = clipwd

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts.
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

    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send("configure terminal\n")
    remote_conn.send("snmp-server community public RO\n")
    remote_conn.send("exit\n")
    remote_conn.send("write memory\n")
    # Wait for the command to complete
    time.sleep(4)

    print ("snmp config applied")

