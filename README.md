# Mozilla Firefox BORMI tool

Python script for **B**ackup **OR** **MI**grate from old to new Mozilla Firefox profile.

## Description
This script allows users to easily back up or migrate their Mozilla Firefox profiles using a graphical user interface (GUI) built with TkInter.

## Based on
- [Profiles - Where Firefox stores user data](https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data)
- [Back up and restore information in Firefox profiles](https://support.mozilla.org/en-US/kb/back-and-restore-information-firefox-profiles)

## Features
- Detects available Firefox profiles
- Allows users to select old and new profiles via GUI
- Copies essential profile data (bookmarks, cookies, extensions, etc.)
- Ensures data integrity during migration

## Requirements
- ONLY Python 3.x  (no pypy library dependencies)
- Exsist at least two Mozilla Firefox profiles - new and old

## Usage
Run the script and follow the prompts to back up or migrate your Firefox profile.

### Text Mode (default)
```bash
python use_bormi_tool.py
```

### GUI Mode 
```bash
python use_bormi_tool.py -m gui
```

Next, you will be given the opportunity to specify the Firefox profiles for backup or migrate.
