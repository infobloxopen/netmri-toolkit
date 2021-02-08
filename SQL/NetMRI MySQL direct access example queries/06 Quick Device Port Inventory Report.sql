
-- Quick Device Port Report
--
-- (Components where PhysicalClass = "port")
--

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
	
-- from DevicePhysical table
DevicePhysicalID,
-- DataSourceID,
-- DeviceID,
PhysicalIndex,
PhysicalStartTime,
PhysicalEndTime,
PhysicalChangedCols,
PhysicalTimestamp,
PhysicalDescr,
PhysicalVendorType,
PhysicalContainedIn,
PhysicalClass,
PhysicalParentRelPos,
PhysicalName,
PhysicalHardwareRev,
PhysicalFirmwareRev,
PhysicalSoftwareRev,
PhysicalSerialNum,
PhysicalMfgName,
PhysicalModelName,
PhysicalAlias,  -- NOTE:  This is the ifIndex of the port on the device.
PhysicalAssetID,
UnitState

from report.Device
inner join report.DevicePhysical

on report.Device.DeviceID = report.DevicePhysical.DeviceID

where	
	-- supress devices that are partially discovered.
	DeviceVendor is not NULL and
	DeviceVendor != 'unknown' and
	DeviceType != 'unknown' and
	PhysicalClass = "port"

order by DeviceVendor ASC, DeviceType ASC, DeviceSysName ASC, PhysicalContainedIn ASC

;