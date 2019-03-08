###########################################################################
## Export of Script: PS Add VTP Info to Custom Field
## Script-Level: 3
## Script-Category: Uncategorized
## Script-Language: Perl
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	PS Add VTP Info to Custom Field

# Script-Description:
# 	''Add VTP Info to Custom Field''

# END-INTERNAL-SCRIPT-BLOCK

###########################################################################
## Export of Script: PS Add VTP Info to Custom Field
## Script-Level: 3
## Script-Category: 
###########################################################################


# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     true
#
# END-SCRIPT-BLOCK

use strict;
use warnings;

use NetMRI_Easy;
use XML::Simple;

my $mem_line;
# Connect to the NetMRI
my $easy = new NetMRI_Easy;

# get the device id from the job engine.
my $device_id = $easy->device_id;

# retrieve the device
my $device = $easy->device;
#
# Create the custom fields for VTP if they do not already exist
#
$easy->broker->custom_fields->create_field({
  model => 'Device',
  name  => 'vtpMode',
  type  => 'string',
});

$easy->broker->custom_fields->create_field({
  model => 'Device',
  name  => 'vtpDomain',
  type  => 'string',
});
$easy->broker->custom_fields->create_field({
  model => 'Device',
  name  => 'vtp_Pass',
  type  => 'string',
});

foreach my $output_line (split /\r?\n/, $easy->send_command("show vtp status"))  
{
#	$easy->log_message('info', $output_line);
	if ($output_line =~ m/VTP Domain Name\s+:\s+(\w+)/) {
		  $easy->log_message('info', $output_line);
		  my @mem_array = split (/VTP Domain Name\s+:\s+(\w+)/, $output_line);
   	  	  $easy->log_message('info', , "updated vtp domain name[1]");
#		  $easy->device->set_custom_field(vtpDomain => $mem_array[1]);
}
	if ($output_line =~ m/VTP Operating Mode\s+:\s+(\w+)/) {
		  $easy->log_message('info', $output_line);
		  my @mem_array = split (/VTP Operating Mode\s+:\s+(\w+)/, $output_line);
   	  	  $easy->log_message('info', , "updated vtp domain name[1]");
#		  $easy->device->set_custom_field(vtpMode => $mem_array[1]);
}
}
foreach my $output_line (split /\r?\n/, $easy->send_command("show vtp password"))  
{
#	$easy->log_message('info', $output_line);
	if ($output_line =~ m/Password\s+:\s+(\w+)/) {
		  $easy->log_message('info', $output_line);
		  my @mem_array = split (/Password\s+:\s+(\w+)/, $output_line);
   	  	  $easy->log_message('info', , "updated vtp domain name[1]");
#		  $easy->device->set_custom_field(vtpPass => $mem_array[1]);
}
}

