###########################################################################
## Export of Script: PS Get all OPEN ports and add to a list
## Script-Level: 3
## Script-Category: 
## Script-Language: Perl
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	PS Get all OPEN ports and add to a list

# Script-Description:
# 	'Run a show command to get the open ports and update a list with them'

# END-INTERNAL-SCRIPT-BLOCK

# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# END-SCRIPT-BLOCK

use strict;
use warnings;

use NetMRI_Easy;
my $wan_ip;
my @get_open_ports;
# Connect to the NetMRI
my $easy = new NetMRI_Easy;
our $name;
# get the device id from the job engine.
my $device_id = $easy->device_id;
my $open_port;
my $open_ports;
# retrieve the device
my $device = $easy->device;
#
# Create the custom field "Store WAN IP" if it does not already exist
#


foreach my $output_line (split /\r?\n/, $easy->send_command("sh control-plane host open-ports | i LISTEN"))  
{
# $easy->log_message('info', $output_line);
if ($output_line =~ m/(?<=\*:)(.*)(?=\*)/) {
                  my $wan_ip = $1;
 $wan_ip =~ s/\s+$//;;
 push (@get_open_ports, $wan_ip);
  
     
 $easy->log_message('info', , "Found an open port : $wan_ip");
  }
        }
$open_port = join(",",@get_open_ports);
$easy->log_message('info', , "Found an open port : $open_port");
 my $easy2 = $easy->broker->config_list;
 $easy2->create_row({
id => 56, 
'$my_name' => $name,
'$open_ports' => $open_port

});