import urllib.request
import zipfile
import time
import allure
import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Admin_pages.Create_an_account import Create_Account
from Admin_pages.LOGIN_test import Login_page
from Admin_pages.Widjets_admin import Widjets
from Admin_pages.Forgot_password import Forgot_password
from Admin_pages.Client_page import Client_page
from Admin_pages.finish_screenshot import Finish_screen
from Admin_pages.edit_user import Edit_AAD_DELETE_user
from Admin_pages.Devices_check import Devices_Check
from Admin_pages.Transaction_page_Admin import Transaction_page_A
import allure
import pytest
from Admin_pages.Akanji import Login_Kanji
from Admin_pages.QA_HUD import Qa_hud
from customer_pages.login_c_page import Login_c_page
from selenium.webdriver.chrome.options import Options
import subprocess
import os
import shutil
import chromedriver_autoinstaller
from ev import EV



def log_and_run(command):
    """Helper function to log and execute shell commands."""
    print(f"[DEBUG] Running command: {command}")
    result = os.system(command)
    if result != 0:
        print(f"[ERROR] Command failed: {command}")
    return result

def download_and_install_chrome():
    """Download and install Chrome from the official .deb package."""
    import os
    import urllib.request
    import subprocess

    chrome_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
    deb_path = "google-chrome-stable_current_amd64.deb"

    if not os.path.exists("/usr/bin/google-chrome"):
        print("[INFO] Chrome not found. Downloading...")
        try:
            # Download the .deb package
            urllib.request.urlretrieve(chrome_url, deb_path)
            print(f"[INFO] Downloaded Chrome .deb package to {deb_path}")

            # Install the .deb package using dpkg
            print("[INFO] Installing Chrome...")
            subprocess.run(["sudo", "dpkg", "-i", deb_path], check=True)

            # Fix any missing dependencies
            subprocess.run(["sudo", "apt-get", "-f", "install", "-y"], check=True)

            # Verify installation
            if os.path.exists("/usr/bin/google-chrome"):
                print("[INFO] Chrome is successfully installed.")
            else:
                raise FileNotFoundError("[ERROR] Chrome installation failed.")

        except Exception as e:
            print(f"[ERROR] Failed to download or install Chrome: {e}")
            raise
        finally:
            # Clean up the .deb package
            if os.path.exists(deb_path):
                os.remove(deb_path)

@pytest.fixture
def driver():
    import os
    import pytest
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options

    chromedriver_path = "chromedriver"  # Ensure chromedriver is in the project

    # Ensure Chrome is installed
    if not os.path.exists("/usr/bin/google-chrome"):
        download_and_install_chrome()

    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"[ERROR] Chromedriver not found at: {chromedriver_path}")

    # Set executable permission for Chromedriver
    if not os.access(chromedriver_path, os.X_OK):
        print("[INFO] Setting execute permissions for Chromedriver...")
        os.chmod(chromedriver_path, 0o755)

    # Check if Chrome is executable
    if not os.access("/usr/bin/google-chrome", os.X_OK):
        raise PermissionError("[ERROR] Google Chrome is not executable at /usr/bin/google-chrome")

    # Configure WebDriver
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--headless")

    try:
        driver_service = ChromeService(executable_path=os.path.abspath(chromedriver_path))
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)
        print("[INFO] WebDriver initialized successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to initialize WebDriver: {e}")
        raise

    yield driver
    print("[INFO] Closing WebDriver...")
    driver.quit()


@allure.feature("Testing the administrative interface for VIP customers")
@allure.story("VIP Admin Test")
class TestVIPAdmin24:
    @allure.title("VIP Admin TEST")
    @pytest.mark.run(order=1)
    def test_admin_VIP(self, driver):
        login = Login_page(driver)
        # login1 = Login_c_page(driver)
        # login1.authorization1()
        login.authorization()
        # wid = Widjets(driver)
        # wid.widgets_check()
        # login.authorization_PROD()
        tra = Transaction_page_A(driver)
        tra.transaction_page_test()
        # login.authorization_PROD()
        # DC = Devices_Check(driver)
        # DC.devices_check()
        # login.NVP_authorization()
        # login.authorization()
        # login.Log_out()
        #
        # ac = Create_Account(driver)
        # ac.ACC()
        # fp = Forgot_password(driver)
        # fp.Forgot_PD()
        #
        # login.authorization()
        # cp = Client_page(driver)
        # cp.client_page()
        # ac = Create_Account(driver)
        # ac.ACC()
        #
        # eu = Edit_AAD_DELETE_user(driver)
        # eu.edit_u()
        #
        # login.authorization_QA_HUD()
        # MONITOR = Qa_hud(driver)
        # MONITOR.monitor()
