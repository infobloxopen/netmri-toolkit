###########################################################################
## Export of Script: PS Get IPAM DHCP Range and Ignore
## Script-Level: 3
## Script-Category: IPAM
## Script-Language: Perl
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	PS Get IPAM DHCP Range and Ignore

# Script-Description:
# 	'Pull DHCP Ranges from IPAM and add them to NetMRI as Rnages to be ignore'

# END-INTERNAL-SCRIPT-BLOCK


# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
#    true
#
# Script-Login: 
#    true
#
# Script-Variables:
#     $gmuser string "Grid Master Username"
#     $gmpassword password "Grid Master Password"
#     $gmipaddress string "GM IP Address"
# 
# END-SCRIPT-BLOCK
use strict;
use warnings;
use NetMRI_Easy;

our $gmipaddress;
our $gmuser;
our $gmpassword;

my $easy = new NetMRI_Easy;

# Connect to the NetMRI
my $easyddi = new NetMRI_Easy({ 
nios_api => 1,
nios_ipaddress => "$gmipaddress",
nios_username  => "$gmuser",
nios_password  => "$gmpassword"
});

# Connect to DDI
my $ddi_session = $easyddi->nios_session;
#check for error
if ($ddi_session->status_code()) 
{
  $easy->log_message('error', 'Construct session failed: ' . $ddi_session->status_code() . ':' . $ddi_session->status_detail());  exit 1;
}
# or note success
$easy->log_message('info', 'Session created successfully');

# log the DDI version
my $ddi_version = $ddi_session->server_version();
$easy->log_message('info', 'Version: '.$ddi_version."/n");

my @all_range_objs = $ddi_session->search(
    object       => "Infoblox::DHCP::Range",
    network      => "2\..*",
);
foreach my $range_obj (@all_range_objs) {
    my $range_val = sprintf("%s-%s", $range_obj->start_addr(), $range_obj->end_addr());
    $easy->log_message('info', 'DHCP Range to Ignore: '.$range_val."\n");
#    my $devices = $easy->broker->discovery_settings->create({
#    range_value    => '$range_val',
#    range_type     => 'RANGE',
#    discovery_status => 'IGNORE',
#});
}