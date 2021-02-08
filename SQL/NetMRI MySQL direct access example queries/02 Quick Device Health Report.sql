
-- Quick Device Health Report

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
	
-- from DeviceEnvironmentMonitor table
	DevEnvMonID,
	DevEnvMonStartTime,
	DevEnvMonEndTime,
	DevEnvMonTimestamp,
	DevEnvMonChangedCols,
	DevEnvMonIndex,
	DevEnvMonType,
	DevEnvMonDescr,
	DevEnvMonState,
	DevEnvMonStatus,
	DevEnvMonMeasure,
	DevEnvMonLowWarnVal,
	DevEnvMonLowShutdown,
	DevEnvMonHighWarnVal,
	DevEnvMonHighShutdown,
	DevEnvMonStatusMessage,
	DevEnvMonStatusAlert

from report.Device
inner join report.DeviceEnvironmentMonitor

on report.Device.DeviceID = report.DeviceEnvironmentMonitor.DeviceID

where
	-- supress devices that are partially discovered.
	DeviceVendor is not NULL and
	DeviceVendor != 'unknown' and
	DeviceType != 'unknown'

and
	-- only report parameters that have changed.
	DevEnvMonChangedCols is not NULL

order by DeviceVendor ASC, DeviceType ASC, DeviceSysName ASC, DevEnvMonIndex ASC

;