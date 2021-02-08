
-- get the column names for report.Device.

SELECT concat(column_name, ",") as "-- comment"
from information_schema.columns 
where table_schema = "report" and table_name = "Device";

 