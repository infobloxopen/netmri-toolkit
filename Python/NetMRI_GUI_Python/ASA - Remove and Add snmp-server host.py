# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     $vendor eq "Cisco" and $model like /ASA/
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

# Create NetMRI context manager. It will close the session after execution

with NetMRIEasy(**defaults) as easy:
    # Everything has to be indented under the context manager if we are sending commands to NetMRI

    # first I want to collect the interface the existing snmp-host is using
    # I only show a specific snmp-host to make it easier to parse the output
    # first I split the string on the spaces, then I take the 6th split
    # this will work for any length of interface name as long as the name doesn't contain spaces 

    parse = easy.send_command('show snmp-server host')
    lines = parse.splitlines()

    # Now let's use the variable 'interface' to run the commands to remove the existing Collectors single line entries
    # and then create the new objects and the new Collectors snmp-host entries.
    # I also show what it looked like before I change it and then after the changes have been applied.

    for line in lines:
        my_output = line.split()
        interface = (my_output[6])
        scr_ip = (my_output[3])
        # we strip the ',' off with rstrip
        ip = scr_ip.rstrip(',')
        easy.send_command('conf t')
        easy.send_command('no snmp-server host {} {}'.format(interface,ip))
    
    easy.send_command('object network Collectors_1')
    easy.send_command('range 10.10.10.84 10.10.10.104')
    easy.send_command('object network Collectors_2')
    easy.send_command('range 10.10.12.66 10.10.12.89')
    easy.send_command('snmp-server host-group {} Collectors_1 community infoblox version 2c' .format(interface))
    easy.send_command('snmp-server host-group {} Collectors_2 community infoblox version 2c' .format(interface))
    easy.send_command('end')
    easy.send_command('wri mem')
    easy.send_command('show snmp-server host')
    easy.send_command('term p 24')