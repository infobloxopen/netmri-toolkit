###########################################################################
## Export of Script: PS Add Device
## Script-Level: 3
## Script-Category: 
## Script-Language: Perl
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	PS Add Device

# END-INTERNAL-SCRIPT-BLOCK


# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
#
# END-SCRIPT-BLOCK
 
use strict;
use warnings;

use NetMRI_Easy;
use Data::Dumper;
# Connect to the NetMRI
my $easy = new NetMRI_Easy;

# find the devices that match the pattern
my $devices = $easy->broker->DiscoverySetting->create({
  range_value    => '10.10.10.1',
  range_type     => 'STATIC',
  discovery_status => 'INCLUDE',
virtual_network_id => '2'
});
print $devices->{id};

sleep(30);
my $disco = $easy->broker->DiscoveryStatuses;
$disco->update_snmp({
DeviceID => $devices->{id},
SNMPVersion => '2',
SNMPRead => "sifread",
virtual_network_id => '2' });

$easy->broker->device->discover({
        ip_address      => $devices->{id},
	virtual_network_id => '2' 
});