###########################################################################
## Export of Script: PS Adds Device Memory to Data Field
## Script-Level: 3
## Script-Category: 
## Script-Language: Perl
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	PS Adds Device Memory to Data Field

# Script-Description:
# 	'This will run a sh ver | inc "bytes of memory" command (
Cisco 3725 (R7000) processor (revision 0.1) with 124928K/6144K bytes of memory.) and format it to fit 124928K/6144K into a Device Data Field'

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

my $mem_line;
my @mem_array;
# Connect to the NetMRI
my $easy = new NetMRI_Easy;

# get the device id from the job engine.
my $device_id = $easy->device_id;

# retrieve the device
my $device = $easy->device;
#
# Create the custom field called memory if it does not already exist
#
$easy->broker->custom_fields->create_field({
  model => 'Device',
  name  => 'DRAM',
  type  => 'string',
});

foreach my $output_line (split /\r?\n/, $easy->send_command("show version"))  
{
#	$easy->log_message('info', $output_line);
	if ($output_line =~ m/bytes of memory/) {
		  $easy->log_message('info', $output_line);
#		  my @mem_array = split (/(?<=with\s)(.*)(?=\sbytes)/, $output_line);
   	  	  $easy->log_message('info', , "updated chasis serial number $mem_array[1]");
		  $easy->device->set_custom_field(dram => $mem_array[1]);
}
}