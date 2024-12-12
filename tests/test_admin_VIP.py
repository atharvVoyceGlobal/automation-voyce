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

def download_and_extract_chrome():
    """Download and extract Chrome from the given URL."""
    chrome_url = "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/linux64/chrome-linux64.zip"
    zip_path = "chrome-linux64.zip"
    extract_path = "chrome-linux64"

    if not os.path.exists("chrome"):
        print("[INFO] Chrome binary not found. Downloading...")
        try:
            urllib.request.urlretrieve(chrome_url, zip_path)
            print(f"[INFO] Downloaded Chrome to {zip_path}")

            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                print(f"[INFO] Extracted Chrome to {extract_path}")

            # Locate the extracted Chrome binary
            chrome_binary = os.path.join(extract_path, "chrome")
            if os.path.exists(chrome_binary):
                os.rename(chrome_binary, "chrome")
                os.chmod("chrome", 0o755)
                print("[INFO] Chrome binary is ready.")
            else:
                raise FileNotFoundError("[ERROR] Chrome binary not found after extraction.")
        except Exception as e:
            print(f"[ERROR] Failed to download or extract Chrome: {e}")
            raise
        finally:
            # Clean up the zip file
            if os.path.exists(zip_path):
                os.remove(zip_path)

@pytest.fixture
def driver():
    chrome_assembled = "chrome"
    chromedriver_path = "chromedriver"  # Ensure chromedriver is in the project

    # Ensure Chrome is downloaded and available
    if not os.path.exists(chrome_assembled):
        download_and_extract_chrome()

    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"[ERROR] Chromedriver not found at: {chromedriver_path}")

    log_and_run(f"ls -l {chrome_assembled}")
    log_and_run(f"ls -l {chromedriver_path}")

    # Check versions
    log_and_run(f"{chrome_assembled} --version || echo '[ERROR] Cannot fetch Chrome version'")
    log_and_run(f"{chromedriver_path} --version || echo '[ERROR] Cannot fetch Chromedriver version'")

    # Configure WebDriver
    chrome_options = Options()
    chrome_options.binary_location = os.path.abspath(chrome_assembled)
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
        log_and_run("ps -ef | grep chrome")
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
