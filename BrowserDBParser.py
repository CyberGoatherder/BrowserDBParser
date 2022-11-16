import sqlite3
import argparse
import re
from time import sleep
import pandas as pd
from sys import exit
import os

print("""
 _____                                  ____   _____  _____
| __  | ___  ___  _ _ _  ___  ___  ___ |    \ | __  ||  _  | ___  ___  ___  ___  ___
| __ -||  _|| . || | | ||_ -|| -_||  _||  |  || __ -||   __|| .'||  _||_ -|| -_||  _|
|_____||_|  |___||_____||___||___||_|  |____/ |_____||__|   |__,||_|  |___||___||_|
v1.0   @CyberGoatherder
""")

### Set sleep time
delay = 0.15

### Set Args and DB file variable
parser = argparse.ArgumentParser(description="Browser History DB parser")
parser.add_argument("path", help="Input filepath, the DB file you want to parse")
parser.add_argument("-o", "--output", help="Output folder path", default = os.getcwd())
args = parser.parse_args()
args_path = (str(args.path))
args_output = (str(args.output))
if re.match(r".*\\.*[a-zA-Z0-9]$", args_output):
    args_output = args_output + "\\"
elif re.match(r".*/.*[a-zA-Z0-9]$", args_output):
    args_output = args_output + "/"
sleep(delay)
print("Selected DB File: '" + args_path + "'");sleep(delay)
print("Selected Output Folder: '" + args_output + "'");sleep(delay)

### Connect to DB and check version
sqliteConnection = sqlite3.connect(args_path,isolation_level=None,detect_types=sqlite3.PARSE_COLNAMES)
cursor = sqliteConnection.cursor()
sqlite_Query = "select sqlite_version();"
cursor.execute(sqlite_Query)
result = (str(cursor.fetchall())[3:-4]) # Remove first 3 and last 4 characters from string for cleaner formatting.
print("\n[+] SQLite3 Version is:", result);sleep(delay)

### Check table names to determine browser type
sqlite_Query = "SELECT name FROM sqlite_master WHERE type='table';"
cursor.execute(sqlite_Query)
result = str(cursor.fetchall())
if "moz" in result:
    browser = "Mozilla-based"
elif "downloads_slices" in result:
    browser = "Chromium-based"
elif "history_visits" in result:
    browser = "Safari-based"
else:
    print("[+] A valid DB type could not be found, exiting");sleep(delay)
    exit()
print("[+] Determined browser type: "+ browser + "\n");sleep(delay)
print("[+] Connected to the SQLite DB\n");sleep(0.6)

### Extract relevant info from DB file convert to human readable time and save to file
if browser == "Chromium-based":
    browsingfile = "Chromium_Browsing_History.csv"
    downloadfile = "Chromium_Download_History.csv"
    db_browse = pd.read_sql_query("SELECT datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') AS last_visit_time, title, url FROM urls ORDER BY last_visit_time DESC;", sqliteConnection)
    db_download = pd.read_sql_query("SELECT datetime((start_time/1000000)-11644473600, 'unixepoch', 'localtime') AS start_time, current_path, tab_url, referrer, total_bytes FROM downloads ORDER BY start_time DESC;", sqliteConnection)
elif browser == "Mozilla-based":
    browsingfile = "Firefox_Browsing_History.csv"
    downloadfile = "Firefox_Download_History.csv"
    db_browse = pd.read_sql_query("SELECT datetime(last_visit_date/1000000, 'unixepoch', 'localtime') AS last_visit_date, title, url FROM moz_places ORDER BY last_visit_date DESC;", sqliteConnection)
    db_download = pd.read_sql_query("SELECT datetime(dateAdded/1000000, 'unixepoch', 'localtime') AS dateAdded, content FROM moz_annos ORDER BY dateAdded DESC;", sqliteConnection)
elif browser == "Safari-based":
    browsingfile = "Safari_Browsing_History.csv"
    downloadfile = "N/A"
    db_browse = pd.read_sql_query("SELECT datetime(visit_time + 978307200, 'unixepoch', 'localtime') AS visit_time, title, url FROM history_visits INNER JOIN history_items ON history_items.id = history_visits.history_item ORDER BY visit_time DESC;", sqliteConnection)
browsingoutput = args_output + browsingfile
downloadoutput = args_output + downloadfile

### Save data to CSV files
print("[+] Converting timestamps to human readable (Matching current system timezone)");sleep(delay)
db_browse.to_csv(browsingoutput, index=False)
print("[+] Browsing history saved to: '" + browsingoutput + "'");sleep(delay)
if browser == "Chromium-based" or browser == "Mozilla-based":
    db_download.to_csv(downloadoutput, index=False)
    print("[+] Download history saved to: '" + downloadoutput + "'");sleep(delay)
elif browser == "Safari-based":
    print("[!] Download history is not stored in an SQLite DB for this browser, consider reviewing the 'Download.plist' file!");sleep(delay)
# Close out DB connection
cursor.close()
sqliteConnection.close()
print("\n[+] Disconnected from SQLite DB");sleep(delay)
