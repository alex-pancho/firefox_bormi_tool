import shutil
import os
import sys
from pathlib import Path
import argparse
from gui_bormi_tool import gui_mode


def get_firefox_profiles_path():
    if sys.platform == "win32":
        return Path(os.getenv("APPDATA")) / "Mozilla" / "Firefox" / "Profiles"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Firefox" / "Profiles"
    else:
        return Path.home() / ".mozilla" / "firefox"


def check_profile_ini(firefox_profiles_path: Path):
    profiles_ini_path = firefox_profiles_path.parent / "profiles.ini"
    if not profiles_ini_path.exists():
        print(
            f"""Error: profiles.ini not found in
    {profiles_ini_path}
    Firefox profile directory may be incorrect."""
        )
        return False
    return True


def list_profiles():
    profiles_dir = get_firefox_profiles_path()
    check_profile_ini(profiles_dir)
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
        "sessionstore.jsonlz4",  # Open tabs and session
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


def text_mode():
    profiles = list_profiles()
    old_profile, new_profile = None, None

    if len(profiles) == 0:
        print("No profiles found in the default location.")
        old_profile_path = input("Enter the path to the OLD profile: ")
        new_profile_path = input("Enter the path to the NEW profile: ")
        old_profile = Path(old_profile_path)
        new_profile = Path(new_profile_path)
    elif len(profiles) == 1:
        response = input("Single Profile Found. Use this profile as OLD? (yes/NO): ")
        if response.lower() == "yes":
            old_profile = profiles[0]
            new_profile_path = input("Enter the path to the NEW profile: ")
            new_profile = Path(new_profile_path)
        else:
            new_profile = profiles[0]
            old_profile_path = input("Enter the path to the OLD profile: ")
            old_profile = Path(old_profile_path)
    elif len(profiles) >= 2:
        print("Available profiles:")
        for i, profile in enumerate(profiles):
            print(f"{i + 1}. {profile}")
        old_profile_index = int(input("Select the OLD profile (number): ")) - 1
        new_profile_index = int(input("Select the NEW profile (number): ")) - 1
        old_profile = profiles[old_profile_index]
        new_profile = profiles[new_profile_index]
    else:
        raise TypeError("Impossible get len of 'profiles' value")

    if old_profile and new_profile:
        copy_profile(old_profile, new_profile)
        print("Migration completed successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="Firefox Profile Backup or Migrate Tool"
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["gui", "text"],
        default="text",
        help="Run mode: 'gui' or 'text'",
    )
    args = parser.parse_args()

    if args.mode == "gui":
        gui_mode(list_profiles, copy_profile)
    else:
        text_mode()


if __name__ == "__main__":
    main()
