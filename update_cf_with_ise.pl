# BEGIN-SCRIPT-BLOCK
#
# Script-Filter:
# $Vendor eq "Cisco"
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
my $Configs=$easy->send_command("sh dot1x all | i PortC|Dot1x");
my @output = split /\n/,$Configs;
my %ise = ();
our ($if_name);
foreach my $line (@output) {
                chomp $line;
                if ($line =~ /^Dot1x Info for (\S+)/) {
                                ($if_name) = $line =~ /^Dot1x Info for (\S+)/;
                                $ise{$if_name} = [()];
                } elsif ( $line =~ /PortControl =/i ) {
                                my ($ip) = $line =~ /PortControl \s.+ = /i;
                                if ($ip !~ m/AUTO/){
                                push @{$ise{$if_name}}, $ip;
                                }
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
 
