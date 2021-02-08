
-- An Advisor Lifecycle Report Example.

SELECT
	`report`.`InfraDevice`.DeviceID
	, `report`.`InfraDevice`.`DeviceVendor`
	, `report`.`InfraDevice`.`DeviceName`
	, `report`. `InfraDevice`.`DeviceIPDotted`
	, `report`.`InfraDevice`.`DeviceType`
	, IFNULL(dp.PhysicalModelName, `report`.`InfraDevice`.`DeviceModel`) 'DeviceModel'
	, `config`.`device_metas`.`eox_status`
	, `config`.`device_metas`.`end_of_sale`
	, `config`.`device_metas`.`end_of_software_maintenance`
	, `config`.`device_metas`.`end_of_vulnerability_security_support`
	, `config`.`device_metas`.`end_of_support`
FROM
	`report`.`InfraDevice`
LEFT JOIN (
SELECT *
FROM
	`report`.`DevicePhysical`
WHERE
	`report`.`DevicePhysical`.`PhysicalClass` = 'Chassis'
) dp
USING(`DeviceID`)
LEFT JOIN
	`config`.`device_metas`
ON
	`DeviceID` = `device_id`

-- filter out devices who have not yet had EoX dates announced.
WHERE eox_status IS NOT NULL

ORDER BY
	`report`.`InfraDevice`.`DeviceIPNumeric`;