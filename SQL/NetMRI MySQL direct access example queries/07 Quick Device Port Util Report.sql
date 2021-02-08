
-- Quick Device Port Daily Util Report
--
-- (Components where PhysicalClass = "port")
--   X
-- (ifPerfDaily_M_[DATE])
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
	UnitState,

-- from ifPerfDaily_M_[DATE] table
	StartTime,
	EndTime,
	ifIndex,  -- NOTE: Join attribute to the DevicePhysicals table.
	ifTotalChanges,
	ifInOctets,
	ifInUcastPkts,
	ifInNUcastPkts,
	ifInMulticastPkts,
	ifInBroadcastPkts,
	ifInDiscards,
	ifInErrors,
	ifOutOctets,
	ifOutUcastPkts,
	ifOutNUcastPkts,
	ifOutMulticastPkts,
	ifOutBroadcastPkts,
	ifOutDiscards,
	ifOutErrors,
	ifAlignmentErrors,
	ifFCSErrors,
	ifLateCollisions,
	InThru,
	OutThru,
	TotalThru,
	InUtil,
	OutUtil,
	TotalUtil,
	InErrorPct,
	OutErrorPct,
	TotalErrorPct,
	InBcastPct,
	OutBcastPct,
	TotalBcastPct,
	InDiscardPct,
	OutDiscardPct,
	TotalDiscardPct

-- Device X DevicePhysical(ports)
from report.Device
inner join report.DevicePhysical
on report.Device.DeviceID = report.DevicePhysical.DeviceID

-- DevicePhysical(ports) X ifPerfDaily_M_[DATE]
inner join report.ifPerfDaily_M_20210101
on PhysicalAlias = ifIndex and
	report.Device.DeviceID = report.ifPerfDaily_M_20210101.DeviceID

where
	-- pick one device and port for demonstration purposes.
	report.Device.DeviceID = 7
	and PhysicalAlias = 10148 
	and
	
	-- supress devices that are partially discovered.
	DeviceVendor is not NULL and
	DeviceVendor != 'unknown' and
	DeviceType != 'unknown' and
	PhysicalClass = "port"

order by
	DeviceVendor ASC, DeviceType ASC, DeviceSysName ASC,
	PhysicalAlias ASC, StartTime ASC
	
;