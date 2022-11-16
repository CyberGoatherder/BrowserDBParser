# BrowserDBParser

A small script to parse browsing and download activity from web browser SQLite DB files outputting to
a more friendly human-readable CSV format. Useful during IR investigations when looking to quickly review web browser activity. 

## Description

`BrowserDBParser.py` can be used to take an input of a web browser's `History` SQLite DB outputting two CSV files which detail web browsing and file download activity.

• Auto-detects browser type

• Converts Epoch / Webkit timestamps to human-readable time format

• Outputs relevant information to time-sorted .CSV files

Currently supports all Chromium-based (Chrome, Edge, Brave, Opera etc.) and Firefox-based (Firefox, Waterfox etc.) browsers. 


## Usage

```python
 _____                                  ____   _____  _____
| __  | ___  ___  _ _ _  ___  ___  ___ |    \ | __  ||  _  | ___  ___  ___  ___  ___
| __ -||  _|| . || | | ||_ -|| -_||  _||  |  || __ -||   __|| .'||  _||_ -|| -_||  _|
|_____||_|  |___||_____||___||___||_|  |____/ |_____||__|   |__,||_|  |___||___||_|
v1.0   @CyberGoatherder

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

```python
user@user: BrowserDBParser.py ~/Documents/Files/browser/History -o ~/Documents/Files/browser/ 
 _____                                  ____   _____  _____
| __  | ___  ___  _ _ _  ___  ___  ___ |    \ | __  ||  _  | ___  ___  ___  ___  ___
| __ -||  _|| . || | | ||_ -|| -_||  _||  |  || __ -||   __|| .'||  _||_ -|| -_||  _|
|_____||_|  |___||_____||___||___||_|  |____/ |_____||__|   |__,||_|  |___||___||_|
v1.0   @CyberGoatherder

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

~[1] Implement Safari support.~
