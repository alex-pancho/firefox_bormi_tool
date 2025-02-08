import shutil
import os
import json
import sys
import wx
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
    app = wx.App(False)
    frame = wx.Frame(None, wx.ID_ANY, "Firefox Profile Migrator", size=(400, 300))
    panel = wx.Panel(frame)
    
    profiles = list_profiles()
    
    if len(profiles) < 2:
        wx.MessageBox("Error: Not enough profiles found for migration.", "Error", wx.OK | wx.ICON_ERROR)
        return
    
    choices = [p.name for p in profiles]
    old_profile_choice = wx.SingleChoiceDialog(frame, "Select the OLD profile:", "Profile Selection", choices)
    if old_profile_choice.ShowModal() != wx.ID_OK:
        return
    old_profile = profiles[old_profile_choice.GetSelection()]
    
    new_profile_choice = wx.SingleChoiceDialog(frame, "Select the NEW profile:", "Profile Selection", choices)
    if new_profile_choice.ShowModal() != wx.ID_OK:
        return
    new_profile = profiles[new_profile_choice.GetSelection()]
    
    copy_profile(old_profile, new_profile)
    wx.MessageBox("Migration completed successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
    
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
