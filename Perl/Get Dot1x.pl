###########################################################################
## Export of Script: PS Get Dot1x
## Script-Level: 3
## Script-Category: 
## Script-Language: Perl
###########################################################################

# BEGIN-INTERNAL-SCRIPT-BLOCK
# Script:
# 	PS Get Dot1x

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
my $Configs=$easy->send_command("sh dot1x all | i PortC|Dot1xDot1x");

my @output = split /\n/,$Configs;
my %ise;
our ($if_name);
foreach my $line (@output) {
                chomp $line;
                if ($line =~ /^Routed protocols on (\S+):/) {
                                ($if_name) = $line =~ /^Routed protocols on (\S+):/;
                                $ise{$if_name} = [()];
                } elsif ( $line =~ /ip/i ) {
                                my ($ip) = $line =~/(\S+)/;
                                push @{$ise{$if_name}}, $ip;
                }
}

foreach my $i (keys %ise) {
                my $id = $if_ids{$i};
                if (! exists $if_ids{$i}) {
                                print "Skipping interface $i, not in ISE \n";
                                next;                    
                }
                my @ise = @{$ise{$i}};
                if (! @ise ) {
                                print "Skipping interface $i no host-mode\n";
                                next;                    
                }
                print "Interface (name/id) ise => ($i,$id) " . join(",",@ise) . "\n";
                $easy->broker->interface->update({
                                # this uniquely identifies the interface in the NetMRI
                                InterfaceID   => $id,  
                                custom_ise    => join(",",@ise)
                });
}
