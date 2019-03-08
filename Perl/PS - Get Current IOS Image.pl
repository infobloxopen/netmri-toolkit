###########################################################################
## Export of Script: PS - Get Current IOS Image
## Script-Level: 3
## Script-Category: 
## Script-Language: Perl
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	PS - Get Current IOS Image

# Script-Description:
# 	'Get the current IOS image from a "show version" and update a custom field called "IOS Image"'

# END-INTERNAL-SCRIPT-BLOCK

# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#     $vendor eq "Cisco" and $sysdescr like /IOS/
#
# END-SCRIPT-BLOCK

use strict;
use warnings;

use NetMRI_Easy;

# Connect to the NetMRI
my $easy = new NetMRI_Easy;
my $system_image;

# Create the custom field called IOS Image if it does not already exist
$easy->broker->custom_fields->create_field({
	model => 'Device',
	name  => 'IOS Image',
	type  => 'string'
});

foreach my $output_line (split /\r?\n/, $easy->send_command("show version"))  
{
#	For each line in the ourput we will search and until we match a line that starts with "System image file is"
	if ($output_line =~ m/System image file is/) {
		$easy->log_message('info', $output_line);
		# This is a regex that will parse the line and puting the location and image into the 2nd slot of the array
		my @system_image = split (/(?<=System image file is\s\\")(.*)(?=\\")|(?<=System image file is ")(.*)(?=")/, $output_line);
		# This will generate the Custom Log Message to confim that it's capturing the correct data in the array slot 1
		$easy->log_message('info', , "[+] Updated Custom Field IOS Image : $system_image[1]");
   	  	# This will send update the custom field we created called "IOS Image"
   	  	### NOTE ### the fact it's all lower case with "_" for the space
		$easy->device->set_custom_field(ios_image => $system_image[1]);
	}
}
