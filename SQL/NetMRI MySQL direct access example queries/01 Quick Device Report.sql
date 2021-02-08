
-- Quick Device Inventory Report

select

	DataSourceID,
	DeviceID,
	DeviceStartTime,
	DeviceEndTime,
	DeviceChangedCols,
	DeviceIPDotted,
	DeviceIPNumeric,
	DeviceName,
	DeviceType,
	DeviceAssurance,
	DeviceVendor,
	DeviceModel,
	DeviceVersion,
	DeviceSysName,
	DeviceSysDescr,
	DeviceSysLocation,
	DeviceSysContact,
	DeviceDNSName,
	DeviceFirstOccurrenceTime,
	DeviceTimestamp,
	DeviceAddlInfo,
	DeviceMAC,
	ParentDeviceID,
	DeviceNetBIOSName,
	DeviceOUI,
	MgmtServerDeviceID,
	InfraDeviceInd,
	NetworkDeviceInd,
	VirtualInd,
	VirtualNetworkID,
	DeviceUniqueKey

from report.Device

where
	DeviceVendor is not NULL and
	DeviceVendor != 'unknown' and
	DeviceType != 'unknown'

order by DeviceVendor ASC, DeviceType ASC

;