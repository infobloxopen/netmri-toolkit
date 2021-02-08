
-- Quick Device TCP/IP Port Report

select

-- from Device table
	DeviceStartTime,
	DeviceIPDotted,
	DeviceName,
	DeviceType,
	DeviceVendor,
	DeviceModel,
--	DeviceVersion,
--	DeviceSysLocation,
--	DeviceDNSName,
	
-- from DevicePort table
	DevicePortID,
	Port,
	PortProtocol,
	PortStartTime,
	PortEndTime,
	PortChangedCols,
	PortTimestamp,
	PortState,
	Service,
	ExpectedService,
	FirstOccurrence,
	ListenAddr

from report.Device
inner join report.DevicePort

on report.Device.DeviceID = report.DevicePort.DeviceID

where
	-- supress devices that are partially discovered.
	DeviceVendor is not NULL and
	DeviceVendor != 'unknown' and
	DeviceType != 'unknown'


order by DeviceVendor ASC, DeviceType ASC, DeviceSysName ASC

;