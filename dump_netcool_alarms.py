import requests
from datetime import datetime, timedelta
import urllib3
import sys
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def dump_netcool_alerts(output_file="netcool_all_alarms.csv", days=1):
    print(f"Fetching Netcool alerts for the last {days} day(s)...")
    
    now = datetime.now()
    start_time = now - timedelta(days=days)
    
    sDate = start_time.strftime("%m/%d/%Y")
    eDate = now.strftime("%m/%d/%Y")
    sTime = start_time.strftime("%H:%M")
    eTime = now.strftime("%H:%M")
    
    # URL includes all severities (sev5=5&sev4=4&sev3=3&sev2=2&sev1=1&sev0=0)
    url = f"https://{{NETCOOL_FQDN}}/cgi-bin/Oracle/search_hist.cgi?OwnerGID=10&sev5=5&sev4=4&sev3=3&sev2=2&sev1=1&sev0=0&sDate={sDate}&sTime={sTime}&eDate={eDate}&eTime={eTime}&csv=1"
    
    print(f"Requesting data from: {url}")
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"Successfully dumped {max(0, len(response.text.splitlines()) - 1)} Netcool alarms to {output_file}")
    except Exception as e:
        print(f"Failed to dump alarms: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump Netcool alarms to CSV.")
    parser.add_argument("-o", "--output", default="netcool_all_alarms.csv", help="Output CSV filename")
    parser.add_argument("-d", "--days", type=int, default=1, help="Number of days to look back")
    args = parser.parse_args()
    
    dump_netcool_alerts(output_file=args.output, days=args.days)
