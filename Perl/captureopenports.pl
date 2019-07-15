# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# Script-Description:
#   This will capture all the open ports on a Cisco device and store it in a Custom Field
# END-SCRIPT-BLOCK

use strict;
use warnings;

use NetMRI_Easy;
my $port;
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
# Create the custom field "Open Ports" if it does not already exist
#
$easy->broker->custom_fields->create_field({
  model => 'Device',
  name  => 'Open Ports',
  type  => 'string',
});

foreach my $output_line (split /\r?\n/, $easy->send_command("sh control-plane host open-ports | i LISTEN"))  
{
# We are going to use the regex below to capture the open ports
#  tcp                        *:22                         *:0               SSH-Server   LISTEN
#  tcp                        *:23                         *:0                   Telnet   LISTEN
#  tcp                       *:179                         *:0                      BGP   LISTEN
#  udp                     *:54973                         *:0                  IP SNMP   LISTEN
#  udp                      *:4500                         *:0                   ISAKMP   LISTEN
#  udp                       *:161                         *:0                  IP SNMP   LISTEN
# $easy->log_message('info', $output_line);
if ($output_line =~ m/(tcp|udp).*(?<=\*:)(.*)(?=\*)/) {
                  my $proto = $1;
                  my $port = $2;
                  $port =~ s/\s+$//;;
                  $proto =~ s/\s+$//;;
                  my $string = join ":", $proto, $port;
                  push (@get_open_ports, $string);
                  $easy->log_message('info', , "Found an open port : $port \n");
                  }
}
$open_port = join(",",@get_open_ports);
$easy->log_message('info', , "All open ports : $open_port \n");
$easy->device->set_custom_field(open_ports => $open_port);
