# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#	($Vendor eq "Cisco" and $SysDescr like /NX-OS/)
#
# END-SCRIPT-BLOCK

#This script shows an example on how to deal with prompts
#Thanks @CLenner - https://community.infoblox.com/t5/Network-Change-Configuration/How-to-handle-the-RSA-key-fingerprint-prompt-message/m-p/17652#M2831 

# these variables you should be able to use as they are
use strict;
use warnings;
use NetMRI_Easy;
my $easy = new NetMRI_Easy({ api_version => 3.0 });

# you'll need to modify the values given to these variables so they match your environment:
my $sftp_user = "username";
my $sftp_server = "ip_address";
my $target_path = "/directory/filename.bin";
my $sftp_password = "password";

# copy files with RSA Prompt
$easy->send_command("clear ssh hosts"); # Ensures consistency between switches regardless of SSH/SFTP/SCP history (makes sure the "are you sure" prompt always shows up).
$easy->send_command("copy sftp://$sftp_user\@$sftp_server$target_path bootflash: vrf default","Are you sure you want to continue connecting (yes/no)?"); # issue copy command
$easy->send_command("yes","password:"); #answer the "are you sure" prompt
$easy->send_async_command("$sftp_password",10); # answer the password prompt, and the copy then begins
# unless we tune a custom COPP - the actual copy will always take too long to wait for, short timeout for async command is so we're not sitting around waiting
# (but it takes more than 10 seconds to timeout, so maybe this value is below some minimum allowed)
