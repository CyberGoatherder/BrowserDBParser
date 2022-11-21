# BrowserDBParser

A small script to parse browsing and download activity from web browser SQLite DB files outputting to
a more friendly human-readable CSV format. Useful during IR investigations when looking to quickly review web browser activity. 

## Description

`BrowserDBParser.py` can take a web browser's `History` SQLite DB as input outputting two CSV files which detail web browsing and file download activity.

• Auto-detects browser type

• Converts Epoch / Webkit / Apple Cocoa Core Data timestamps to human-readable time format

• Outputs relevant information to time-sorted .CSV files

Currently supports all Chromium-based (Chrome, Edge, Brave, Opera etc.), Firefox-based (Firefox, Waterfox etc.) and Safari browsers. 

## Common History File Locations

Quick reference for some of the most common browsers

```
Windows:

Chrome: C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\History
E.G. C:\Users\Bob\AppData\Local\Google\Chrome\User Data\Default\History

Firefox: C:\Users\<username>\AppData\Roaming\Mozilla\Firefox\Profiles\<profile folder>\places.sqlite
E.G. C:\Users\Alice\AppData\Roaming\Mozilla\Firefox\Profiles\gq4yx1bn.default-release\places.sqlite

Edge: C:\Users\<username>\AppData\Local\Microsoft\Edge\User Data\Default\History
E.G. C:\Users\Bob\AppData\Local\Microsoft\Edge\User Data\Default\History
```
```
Mac:

Chrome: /Users/$USER/Library/Application Support/Google/Chrome/Default/History
Firefox: /Users/<username>/Library/Application Support/Firefox/Profiles/<profile folder>/places.sqlite
Safari: ~/Library/Safari/History.db
```
```
Linux:

Chrome: ~/.config/google-chrome/Default/History
Firefox: /home/<username>/.mozilla/firefox/<profile folder>/places.sqlite
```
:bulb: **Tip:** Remember that for Chromium based browsers \Default\ is only valid if nobody has 'signed in' to the browser. Signing into the browser will create a new profile at \Profile1\ instead of \Default\\\.

## Sample
A sample file has been provided. 

**Scenario**: It's been reported that malware stored inside of a .ZIP has been executed on a machine. Can you use the sample file provided to determine where the .ZIP was downloaded from? At what time? And what actions lead to the user landing on the page serving malware?

## Requirements

Just one.

```
pip install pandas
```

## Usage

```
 _____                                  ____   _____  _____
| __  | ___  ___  _ _ _  ___  ___  ___ |    \ | __  ||  _  | ___  ___  ___  ___  ___
| __ -||  _|| . || | | ||_ -|| -_||  _||  |  || __ -||   __|| .'||  _||_ -|| -_||  _|
|_____||_|  |___||_____||___||___||_|  |____/ |_____||__|   |__,||_|  |___||___||_|
v1.1   @CyberGoatherder

usage: parser.py [-h] [-o OUTPUT] path

Browser History DB parser

positional arguments:
  path                  Input filepath, the DB file you want to parse

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output folder path

Example:
python BrowserDBParser.py /path/to/DB/file -o /path/to/DB/output
```

### Example

```
user@user: BrowserDBParser.py ~/Documents/Files/browser/History -o ~/Documents/Files/browser/ 
 _____                                  ____   _____  _____
| __  | ___  ___  _ _ _  ___  ___  ___ |    \ | __  ||  _  | ___  ___  ___  ___  ___
| __ -||  _|| . || | | ||_ -|| -_||  _||  |  || __ -||   __|| .'||  _||_ -|| -_||  _|
|_____||_|  |___||_____||___||___||_|  |____/ |_____||__|   |__,||_|  |___||___||_|
v1.1   @CyberGoatherder

Selected DB File: '/home/user/Documents/Files/browser/History'
Selected Output Folder: '/home/user/Documents/Files/browser/'

[+] SQLite3 Version is: 3.39.4
[+] Determined browser type: Chromium-based

[+] Connected to SQLite DB

[+] Converting timestamps to human readable (Matching current system timezone)
[+] Browsing history saved to: '/home/user/Documents/Files/browser/Chromium_Browsing_History.csv'
[+] Download history saved to: '/home/user/Documents/Files/browser/Chromium_Download_History.csv'

[+] Disconnected from SQLite DB
```


### Roadmap

~[1] Implement Safari support~

~[2] Add a sample file~
