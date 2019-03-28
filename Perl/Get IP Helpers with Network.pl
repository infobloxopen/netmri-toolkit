###########################################################################
## Export of Script: PS Get IP Helpers with Network
## Script-Level: 3
## Script-Category: 
## Script-Language: Perl
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	PS Get IP Helpers with Network

# END-INTERNAL-SCRIPT-BLOCK

# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
# $Vendor eq "Cisco"
#
# Script-Login:false
#
# Script-Variables:
#
##
# END-SCRIPT-BLOCK
use strict;
use warnings;
 
use NetMRI_Easy;
my $easy = new NetMRI_Easy;
my $device_id = $easy->device_id;
my $device = $easy->device;
print $device->DeviceID . " " . $device->DeviceName . "\n";
my %if_ids = map { $_->ifDescrRaw => $_->InterfaceID }  $easy->broker->interface->index({ DeviceID => $device_id });
my $Configs=$easy->broker->device->running_config_text(DeviceID=>$device_id)->{running_config_text};
my @output = split /\n/,$Configs;
my %helpers = ();
my %subrange = ();

our ($if_name);

# Create the custom field called IP Helpers if it does not already exist
#
$easy->broker->custom_fields->create_field({
  model => 'Interface',
  name  => 'IP Helpers',
  type  => 'string',
});
$easy->broker->custom_fields->create_field({
  model => 'Interface',
  name  => 'Subnet',
  type  => 'string',
});
foreach my $line (@output) {
                chomp $line;
                if ($line =~ /^interface (\S+)/) {
                                ($if_name) = $line =~ /^interface (\S+)/;
                                $helpers{$if_name} = [()];
                                $subrange{$if_name} = [()];
                } elsif ( $line =~ /ip dhcp relay address /i ) {
                                my ($ip) = $line =~ /ip dhcp relay address (\S+)/;
                                push @{$helpers{$if_name}}, $ip;
                } elsif ( $line =~ /ip helper-address /i ) {
                                my ($ip) = $line =~ /ip helper-address (\S+)/;
                                push @{$helpers{$if_name}}, $ip;

		} elsif ( $line =~ /ip address /i ) {
                                my ($subnet) = $line =~ /ip address (.*)/;
				my $test = $line =~ /ip address (.+)/;
				print "$test test\n";
                                push @{$subrange{$if_name}}, $subnet;
                }             
}
foreach my $i (keys %helpers) {
                my $id = $if_ids{$i};
                if (! exists $if_ids{$i}) {
                                print "Skipping interface $i, not in IDs table\n";
                                next;                    
                }
                my @helpers = @{$helpers{$i}};
                if (! @helpers ) {
                                print "Skipping interface $i no helpers\n";
                                next;                    
                }
                print "Interface (name/id) helpers => ($i,$id) " . join(",",@helpers) . "\n";
                $easy->broker->interface->update({
                                # this uniquely identifies the interface in the NetMRI
                                InterfaceID   => $id,  
                                custom_ip_helpers    => join(",",@helpers)
                });
}

foreach my $i (keys %subrange) {
                my $id = $if_ids{$i};
                if (! exists $if_ids{$i}) {
                                print "Skipping interface $i, not in IDs table\n";
                                next;                    
                }
                my @subrange = @{$subrange{$i}};
                if (! @subrange) {
                                print "Skipping interface $i no helpers\n";
                                next;                    
                }
                print "Interface (name/id) helpers => ($i,$id) " . join(",",@subrange) . "\n";
                $easy->broker->interface->update({
                                # this uniquely identifies the interface in the NetMRI
                                InterfaceID   => $id,  
                                custom_subnet   => join(",",@subrange)
                });
}