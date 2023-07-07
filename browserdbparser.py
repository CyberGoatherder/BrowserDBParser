"""BrowserDBParser

A python script to parse relevant information from web browser DB files and
output to a more human-readable CSV format
"""

import argparse
import os
import re
import sqlite3
import sys
from time import sleep
import pandas as pd


print(r""" _____                                  ____   _____  _____
| __  | ___  ___  _ _ _  ___  ___  ___ |    \ | __  ||  _  | ___  ___  ___  ___  ___
| __ -||  _|| . || | | ||_ -|| -_||  _||  |  || __ -||   __|| .'||  _||_ -|| -_||  _|
|_____||_|  |___||_____||___||___||_|  |____/ |_____||__|   |__,||_|  |___||___||_|
v1.2   @CyberGoatherder
""")

### Set sleep time
delay = 0.15

### Set Args and DB file variable
parser = argparse.ArgumentParser(description="Browser History DB parser")
parser.add_argument("path", help="Input filepath, the DB file you want to parse")
parser.add_argument("-o", "--output", help="Output folder path", default=os.getcwd())
args = parser.parse_args()
args_path = str(args.path)
args_output = str(args.output)
if re.match(r".*\\.*[a-zA-Z0-9]$", args_output):
    args_output = args_output + "\\"
elif re.match(r".*/.*[a-zA-Z0-9]$", args_output):
    args_output = args_output + "/"
sleep(delay)
print("Selected DB File: '" + args_path + "'")
sleep(delay)
print("Selected Output Folder: '" + args_output + "'")
sleep(delay)

### Connect to DB and check version
sqlite_connection = sqlite3.connect(args_path, isolation_level=None,
                                    detect_types=sqlite3.PARSE_COLNAMES)
cursor = sqlite_connection.cursor()
sqlite_query = "select sqlite_version();"
cursor.execute(sqlite_query)
# Remove first 3 and last 4 characters from string for cleaner formatting.
result = str(cursor.fetchall())[3:-4]
print("\n[+] SQLite3 Version is:", result)
sleep(delay)

### Check table names to determine browser type
sqlite_query = "SELECT name FROM sqlite_master WHERE type='table';"
cursor.execute(sqlite_query)
browser = None
result = str(cursor.fetchall())
if "moz" in result:
    browser = "Mozilla-based"
elif "downloads_slices" in result:
    browser = "Chromium-based"
elif "history_visits" in result:
    browser = "Safari-based"
else:
    print("[+] A valid DB type could not be found, exiting")
    sleep(delay)
    sys.exit()

print("[+] Determined browser type: "+ browser + "\n")
sleep(delay)
print("[+] Connected to the SQLite DB\n")
sleep(0.6)

### Extract relevant info from DB fileconvert to human readable time and save to file
if browser == "Chromium-based":
    browsingfile = "Chromium_Browsing_History.csv"
    downloadfile = "Chromium_Download_History.csv"

    query = ("SELECT "
    + "datetime(visit_time / 1000000 + "
    + "(strftime('%s', '1601-01-01T00:00:00')), "
    + "'unixepoch') AS visit_time_UTC, "
    + "(visits.visit_duration / 3600 / 1000000) || ' h ' || "
    + "strftime('%M m %S s', visits.visit_duration / 1000000 / 86400.0) "
    + "AS visit_duration, "
    + "title, urls.url AS url "
    + "FROM urls "
    + "LEFT JOIN visits ON urls.id = visits.url "
    + "ORDER BY visit_time DESC;")
    db_browse = pd.read_sql_query(query, sqlite_connection)

    query = ("SELECT "
    + "datetime(start_time / 1000000 + "
    + "(strftime('%s', '1601-01-01T00:00:00')), "
    + "'unixepoch') AS download_start_UTC, "
    + "total_bytes, received_bytes, mime_type, current_path AS path, "
    + "tab_url, referrer "
    + "FROM downloads "
    + "ORDER BY start_time DESC;")
    db_download = pd.read_sql_query(query, sqlite_connection)
elif browser == "Mozilla-based":
    browsingfile = "Firefox_Browsing_History.csv"
    downloadfile = "Firefox_Download_History.csv"

    query = ("SELECT "
    + "datetime(last_visit_date / 1000000 + "
    + "(strftime('%s', '1970-01-01T00:00:00')), "
    + "'unixepoch') AS visit_time_UTC, "
    + "title, url "
    + "FROM moz_places "
    + "ORDER BY last_visit_date DESC;")
    db_browse = pd.read_sql_query(query, sqlite_connection)

    query = ("SELECT "
    + "datetime(dateAdded / 1000000 + "
    + "(strftime('%s', '1970-01-01T00:00:00')), "
    + "'unixepoch') AS download_start_UTC, content"
    + "FROM moz_annos "
    + "ORDER BY dateAdded DESC;")
    db_download = pd.read_sql_query(query, sqlite_connection)
elif browser == "Safari-based":
    browsingfile = "Safari_Browsing_History.csv"
    downloadfile = "N/A"

    query = ("SELECT "
    + "datetime(visit_time + (strftime('%s', '2001-01-01T00:00:00')), "
    + "'unixepoch') AS visit_time_UTC, title, url "
    + "FROM history_visits "
    + "INNER JOIN history_items "
    + "ON history_items.id = history_visits.history_item "
    + "ORDER BY visit_time DESC;")
    db_browse = pd.read_sql_query(query, sqlite_connection)

browsingoutput = args_output + browsingfile
downloadoutput = args_output + downloadfile

### Save data to CSV files
print("[+] Converting timestamps to human readable (UTC)")
sleep(delay)
db_browse.to_csv(browsingoutput, index=False)
print("[+] Browsing history saved to: '" + browsingoutput + "'")
sleep(delay)

if browser == "Safari-based":
    print("[!] Download history is not stored in an SQLite DB for this browser!")
    print("[!] Consider reviewing the 'Download.plist' file!")
    sleep(delay)
else:
    db_download.to_csv(downloadoutput, index=False)
    print("[+] Download history saved to: '" + downloadoutput + "'")
    sleep(delay)

# Close out DB connection
cursor.close()
sqlite_connection.close()
print("\n[+] Disconnected from SQLite DB")
sleep(delay)
# pylint: disable=invalid-name
