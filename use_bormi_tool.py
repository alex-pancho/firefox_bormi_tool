import shutil
import os
import json
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path

def get_firefox_profiles_path():
    if sys.platform == "win32":
        return Path(os.getenv("APPDATA")) / "Mozilla" / "Firefox" / "Profiles"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Firefox" / "Profiles"
    else:
        return Path.home() / ".mozilla" / "firefox"

def get_profiles_ini():
    profiles_ini_path = get_firefox_profiles_path().parent / "profiles.ini"
    if not profiles_ini_path.exists():
        print("Error: profiles.ini not found. Firefox profile directory may be incorrect.")
        sys.exit(1)
    return profiles_ini_path

def list_profiles():
    profiles_dir = get_firefox_profiles_path()
    profiles = [p for p in profiles_dir.iterdir() if p.is_dir()]
    return profiles

def copy_profile(old_profile, new_profile):
    files_to_copy = [
        "places.sqlite",  # Bookmarks and history
        "favicons.sqlite",  # Icons for bookmarks
        "cookies.sqlite",  # Cookies
        "logins.json",  # Saved logins
        "key4.db",  # Encryption key for logins
        "cert9.db",  # Certificates
        "permissions.sqlite",  # Site permissions
        "prefs.js",  # Preferences
        "extensions",  # Installed extensions
        "storage",  # Site data
        "sessionstore.jsonlz4"  # Open tabs and session
    ]
    
    for item in files_to_copy:
        src = old_profile / item
        dest = new_profile / item
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dest)
            print(f"Copied: {item}")
        else:
            print(f"Skipping missing: {item}")

def main():
    root = tk.Tk()
    root.withdraw()
    
    profiles = list_profiles()
    
    if len(profiles) < 2:
        messagebox.showerror("Error", "Not enough profiles found for migration.")
        return
    
    choices = [p.name for p in profiles]
    old_profile_name = simpledialog.askstring("Profile Selection", "Enter the name of the OLD profile:", initialvalue=choices[0])
    if old_profile_name not in choices:
        return
    old_profile = next(p for p in profiles if p.name == old_profile_name)
    
    new_profile_name = simpledialog.askstring("Profile Selection", "Enter the name of the NEW profile:", initialvalue=choices[1])
    if new_profile_name not in choices:
        return
    new_profile = next(p for p in profiles if p.name == new_profile_name)
    
    copy_profile(old_profile, new_profile)
    messagebox.showinfo("Success", "Migration completed successfully!")

if __name__ == "__main__":
    main()