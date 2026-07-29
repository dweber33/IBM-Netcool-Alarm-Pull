# Netcool Alarm Exporter (`dump_netcool_alarms.py`)
`dump_netcool_alarms.py` is a Python script that extracts historical Netcool alert data for a specified time window and exports the results to a CSV file for analysis and comparison.
---
## Features
- **Flexible Time Window**: Query historical alert data for any custom lookback period (default: 1 day).
- **All Severities Included**: Queries across all Netcool severity levels (0 through 5).
- **Direct CSV Export**: Saves the raw alarm dump directly to a CSV file.
---
## Prerequisites & Installation
Requires Python 3.x and the `requests` library.
```bash
pip install requests urllib3
Usage
Run the script from the command line:

bash
python dump_netcool_alarms.py [options]
Options
Flag	Parameter	Default	Description
-o	--output	netcool_all_alarms.csv	Output filename for the exported CSV data
-d	--days	1	Number of days to look back from the current time
Examples
Default 24-hour dump:

bash
python dump_netcool_alarms.py
Export the last 7 days to a custom file:

bash
python dump_netcool_alarms.py -d 7 -o netcool_7days.csv
How It Works
Netcool Query Mechanism
The script queries the Netcool system via its web CGI search gateway rather than directly connecting to the underlying database:

Endpoint: https://{{Netcool_FQDN}}/cgi-bin/Oracle/search_hist.cgi
HTTP Method: GET
SSL Verification: Disabled (verify=False) with suppressed warnings to accommodate internal certificates.
URL Query Parameters
Parameter	Value	Description
csv	1	Instructs the CGI backend to return raw CSV format instead of rendering an HTML page
sDate / sTime	MM/DD/YYYY / HH:MM	Start timestamp of the query window
eDate / eTime	MM/DD/YYYY / HH:MM	End timestamp of the query window
sev0–sev5	0 through 5	Includes all alert severity levels (Clear through Critical)
OwnerGID	10	Filters history by Group ID 10
