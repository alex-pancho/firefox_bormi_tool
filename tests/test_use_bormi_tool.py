import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

try:
    from use_bormi_tool import get_firefox_profiles_path, check_profile_ini
    from use_bormi_tool import list_profiles, copy_profile
except ImportError:
    sys.path.append(str(Path(__file__).parent.parent))
    from use_bormi_tool import get_firefox_profiles_path, check_profile_ini
    from use_bormi_tool import list_profiles, copy_profile


class TestBormiTool(unittest.TestCase):
    @patch("os.getenv")
    @patch("sys.platform", "win32")
    def test_get_firefox_profiles_path_windows(self, mock_getenv):
        """Test get_firefox_profiles_path on Windows"""
        mock_getenv.return_value = "C:\\Users\\TestUser\\AppData\\Roaming"
        expected_path = Path(
            "C:/Users/TestUser/AppData/Roaming/Mozilla/Firefox/Profiles"
        )
        self.assertEqual(get_firefox_profiles_path(), expected_path)

    @patch("sys.platform", "darwin")
    def test_get_firefox_profiles_path_mac(self):
        """Test get_firefox_profiles_path on macOS"""
        expected_path = (
            Path.home() / "Library" / "Application Support" / "Firefox" / "Profiles"
        )
        self.assertEqual(get_firefox_profiles_path(), expected_path)

    @patch("sys.platform", "linux")
    def test_get_firefox_profiles_path_linux(self):
        """Test get_firefox_profiles_path on Linux"""
        expected_path = Path.home() / ".mozilla" / "firefox"
        self.assertEqual(get_firefox_profiles_path(), expected_path)

    @patch("pathlib.Path.exists")
    def test_check_profile_ini_exists(self, mock_exists):
        """Test check_profile_ini when profiles.ini exists"""
        is_exist_file = False
        mock_exists.return_value = True
        firefox_profiles_path = Path("/mock/path")
        try:
            is_exist_file = check_profile_ini(firefox_profiles_path)
        except SystemExit:
            self.fail("check_profile_ini() raised SystemExit unexpectedly!")
        self.assertTrue(is_exist_file)

    @patch("pathlib.Path.exists")
    def test_check_profile_ini_not_exists(self, mock_exists):
        """Test check_profile_ini when profiles.ini does not exist"""
        is_exist_file = True
        mock_exists.return_value = False
        firefox_profiles_path = Path("/mock/path")
        try:
            is_exist_file = check_profile_ini(firefox_profiles_path)
        except SystemExit:
            self.fail("check_profile_ini() raised SystemExit unexpectedly!")
        self.assertFalse(is_exist_file)

    @patch("use_bormi_tool.get_firefox_profiles_path")
    @patch("pathlib.Path.iterdir")
    def test_list_profiles(self, mock_iterdir, mock_get_firefox_profiles_path):
        """Test list_profiles when profiles exist"""
        mock_get_firefox_profiles_path.return_value = Path("/mock/path")
        mock_profile1 = MagicMock(spec=Path)
        mock_profile1.is_dir.return_value = True
        mock_profile2 = MagicMock(spec=Path)
        mock_profile2.is_dir.return_value = True
        mock_iterdir.return_value = [mock_profile1, mock_profile2]

        profiles = list_profiles()
        self.assertEqual(len(profiles), 2)
        self.assertIn(mock_profile1, profiles)
        self.assertIn(mock_profile2, profiles)

    @patch("use_bormi_tool.get_firefox_profiles_path")
    @patch("pathlib.Path.iterdir")
    def test_list_profiles_no_profiles(
        self, mock_iterdir, mock_get_firefox_profiles_path
    ):
        """Test list_profiles when no profiles exist"""
        mock_get_firefox_profiles_path.return_value = Path("/mock/path")
        mock_iterdir.return_value = []

        profiles = list_profiles()
        self.assertEqual(len(profiles), 0)

    # @patch('shutil.copy2')
    # @patch('shutil.copytree')
    # @patch('pathlib.Path.exists')
    # @patch('pathlib.Path.is_dir')
    # def test_copy_profile(self, mock_is_dir, mock_exists, mock_copytree, mock_copy2):
    #     """ Test copy_profile """
    #     mock_exists.return_value = True
    #     def mock_is_dir(p):
    #         return p.name in ["extensions", "storage"]
    #     mock_is_dir.side_effect = mock_is_dir(Path('/mock/old_profile'))

    #     old_profile = Path('/mock/old_profile')
    #     new_profile = Path('/mock/new_profile')

    #     copy_profile(old_profile, new_profile)

    #     expected_files = [
    #         "places.sqlite", "favicons.sqlite", "cookies.sqlite", "logins.json",
    #         "key4.db", "cert9.db", "permissions.sqlite", "prefs.js",
    #         "extensions", "storage", "sessionstore.jsonlz4"
    #     ]

    #     for item in expected_files:
    #         src = old_profile / item
    #         dest = new_profile / item
    #         if item in ["extensions", "storage"]:
    #             mock_copytree.assert_any_call(src, dest, dirs_exist_ok=True)
    #         else:
    #             mock_copy2.assert_any_call(src, dest)

    # @patch('shutil.copy2')
    # @patch('shutil.copytree')
    # @patch('pathlib.Path.exists')
    # @patch('pathlib.Path.is_dir')
    # def test_copy_profile_missing_files(self, mock_is_dir, mock_exists, mock_copytree, mock_copy2):
    #     """ Test copy_profile with missing files """
    #     mock_exists.side_effect = lambda p: p.name not in ["cookies.sqlite", "logins.json"]
    #     mock_is_dir.side_effect = lambda p: p.name in ["extensions", "storage"]

    #     old_profile = Path('/mock/old_profile')
    #     new_profile = Path('/mock/new_profile')

    #     copy_profile(old_profile, new_profile)

    #     expected_files = [
    #         "places.sqlite", "favicons.sqlite", "cookies.sqlite", "logins.json",
    #         "key4.db", "cert9.db", "permissions.sqlite", "prefs.js",
    #         "extensions", "storage", "sessionstore.jsonlz4"
    #     ]

    #     for item in expected_files:
    #         src = old_profile / item
    #         dest = new_profile / item
    #         if item in ["extensions", "storage"]:
    #             mock_copytree.assert_any_call(src, dest, dirs_exist_ok=True)
    #         elif item not in ["cookies.sqlite", "logins.json"]:
    #             mock_copy2.assert_any_call(src, dest)
    #         else:
    #             mock_copy2.assert_not_called_with(src, dest)


if __name__ == "__main__":
    unittest.main()
