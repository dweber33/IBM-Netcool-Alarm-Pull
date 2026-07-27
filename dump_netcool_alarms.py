import requests
from datetime import datetime, timedelta
import urllib3
import sys
import argparse
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def dump_netcool_alerts(output_file="netcool_all_alarms.csv", total_days=1, chunk_days=7):
    print(f"Fetching Netcool alerts for the last {total_days} day(s)...")
    if total_days > chunk_days:
        print(f"Querying in chunks of {chunk_days} days to prevent server timeouts.")
    
    now = datetime.now()
    end_time = now
    start_time = now - timedelta(days=total_days)
    
    current_start = start_time
    first_chunk = True
    total_lines_written = 0
    
    with open(output_file, 'w', encoding='utf-8') as f:
        while current_start < end_time:
            current_end = current_start + timedelta(days=chunk_days)
            if current_end > end_time:
                current_end = end_time
                
            sDate = current_start.strftime("%m/%d/%Y")
            eDate = current_end.strftime("%m/%d/%Y")
            sTime = current_start.strftime("%H:%M")
            eTime = current_end.strftime("%H:%M")
            
            url = f"https://{NETCOOL_FQDN}/cgi-bin/Oracle/search_hist.cgi?OwnerGID=10&sev5=5&sev4=4&sev3=3&sev2=2&sev1=1&sev0=0&sDate={sDate}&sTime={sTime}&eDate={eDate}&eTime={eTime}&csv=1"
            
            print(f"Fetching chunk from {sDate} to {eDate}...")
            
            try:
                # Adding a timeout so it doesn't hang indefinitely
                response = requests.get(url, verify=False, timeout=120)
                response.raise_for_status()
                
                # Split lines so we can strip the header on subsequent chunks
                lines = response.text.splitlines()
                
                if lines:
                    if first_chunk:
                        # Write the header and the data
                        f.write('\n'.join(lines) + '\n')
                        total_lines_written += max(0, len(lines) - 1)
                        first_chunk = False
                    else:
                        # Skip the first line (header) for all subsequent chunks
                        if len(lines) > 1:
                            f.write('\n'.join(lines[1:]) + '\n')
                            total_lines_written += (len(lines) - 1)
                
            except requests.exceptions.Timeout:
                print(f" -> ERROR: Timeout while fetching chunk {sDate} to {eDate}. Data for this period will be missing.")
            except Exception as e:
                print(f" -> ERROR: Failed to fetch chunk {sDate} to {eDate}: {e}")
            
            current_start = current_end
            
            # Brief pause to avoid slamming the server
            if current_start < end_time:
                time.sleep(1)
            
    print(f"\nFinished! Successfully dumped {total_lines_written} Netcool alarms to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump Netcool alarms to CSV.")
    parser.add_argument("-o", "--output", default="netcool_all_alarms.csv", help="Output CSV filename")
    parser.add_argument("-d", "--days", type=int, default=1, help="Number of days to look back")
    parser.add_argument("-c", "--chunk", type=int, default=7, help="Days per request chunk (to avoid timeouts)")
    args = parser.parse_args()
    
    dump_netcool_alerts(output_file=args.output, total_days=args.days, chunk_days=args.chunk)
