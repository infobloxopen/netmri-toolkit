
-- Quick Device CPU Util Report

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
	
-- from DeviceCpuStats_D_20210125 table
	DeviceCpuStatsID,
	StartTime,
	EndTime,
	CpuIndex,
	CpuBusy

from report.Device
inner join report.DeviceCpuStats_D_20210125

on report.Device.DeviceID = report.DeviceCpuStats_D_20210125.DeviceID

where
	-- supress devices that are partially discovered.
	DeviceVendor is not NULL and
	DeviceVendor != 'unknown' and
	DeviceType != 'unknown'

-- optionally select only one device.
-- and report.Device.DeviceID = 1

order by
	DeviceVendor ASC, DeviceType ASC, DeviceSysName ASC,
	 CpuIndex ASC, StartTime ASC
;