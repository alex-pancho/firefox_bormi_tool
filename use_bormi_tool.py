import shutil
import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
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
        print(
            "Error: profiles.ini not found. Firefox profile directory may be incorrect."
        )
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
        src = Path(old_profile) / item
        dest = Path(new_profile) / item
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dest)
            print(f"Copied: {item}")
        else:
            print(f"Skipping missing: {item}")


def ask_directories_profile(is_old_known: bool = False, is_new_known: bool = False):
    old_profile = None
    new_profile = None

    if not is_old_known:
        old_profile_path = filedialog.askdirectory(
            title="Select OLD Firefox profile folder"
        )
        if not old_profile_path:
            return None, None
        old_profile = Path(old_profile_path)
    if not is_new_known:
        new_profile_path = filedialog.askdirectory(
            title="Select NEW Firefox profile folder"
        )
        if not new_profile_path:
            return None, None
        new_profile = Path(new_profile_path)

    return old_profile, new_profile


def select_profiles_gui(profiles):
    def on_submit():
        nonlocal old_dropdown, new_dropdown
        old_profile = profiles_dict[old_dropdown.get()]
        new_profile = profiles_dict[new_dropdown.get()]
        old_profile_label.config(text=old_profile)
        new_profile_label.config(text=new_profile)
        root.quit()

    root = tk.Tk()
    root.title("Select Firefox Profiles")

    profiles_dict = {p.name: p for p in profiles}
    # Label to display the returned value
    old_profile_label = tk.Label(root, 
                                 text="""
    """)
    old_profile_label.pack()

    tk.Label(root, text="Select OLD Profile:").pack()
    old_profile_var = tk.StringVar()
    old_dropdown = ttk.Combobox(
        root,
        textvariable=old_profile_var,
        values=list(profiles_dict.keys())
    )
    old_dropdown.pack()

    tk.Label(root, text="Select NEW Profile:").pack()
    new_profile_var = tk.StringVar()
    new_dropdown = ttk.Combobox(
        root,
        textvariable=new_profile_var,
        values=list(profiles_dict.keys())
    )
    new_dropdown.pack()
    
    # Label to display the returned value
    new_profile_label = tk.Label(root, 
                                 text="""
    """)
    new_profile_label.pack()

    tk.Button(root, text="Start Migration", command=on_submit).pack()
    root.mainloop()

    return old_profile_label.cget("text"), new_profile_label.cget("text")


def main():
    root = tk.Tk()
    root.withdraw()

    profiles = list_profiles()
    old_profile, new_profile = None, None

    if len(profiles) == 0:
        messagebox.showwarning(
            "Warning", "No profiles found in the default location."
        )
        old_profile, new_profile = ask_directories_profile()
    elif len(profiles) == 1:
        response = messagebox.askquestion(
            "Single Profile Found", "Can I use this profile as OLD?"
        )
        if response == "yes":
            old_profile = profiles[0]
            new_profile, _ = ask_directories_profile(is_old_known=True)
        else:
            new_profile = profiles[0]
            old_profile, _ = ask_directories_profile(is_new_known=True)
    elif len(profiles) >= 2:
        old_profile, new_profile = select_profiles_gui(profiles)
    else:
        raise TypeError("Impossible get len of 'profiles' value")

    if old_profile and new_profile:
        copy_profile(old_profile, new_profile)
        messagebox.showinfo("Success", "Migration completed successfully!")


if __name__ == "__main__":
    main()
