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

def log_and_run(command):
    """Helper function to log and execute shell commands."""
    print(f"[DEBUG] Running command: {command}")
    result = os.system(command)
    if result != 0:
        print(f"[ERROR] Command failed: {command}")
    return result

@pytest.fixture
def driver():
    """
    Configure Selenium WebDriver using pre-stored Chromium and Chromedriver binaries.
    """
    # Define file paths inside the project
    chrome_parts = ["chrome_part_aa", "chrome_part_ab", "chrome_part_ac"]
    chrome_assembled = "chrome"
    chromedriver_path = "chromedriver"

    # Assemble Chrome binary if not already assembled
    if not os.path.exists(chrome_assembled):
        print("[INFO] Assembling Chrome binary from parts...")
        try:
            with open(chrome_assembled, "wb") as assembled_file:
                for part in chrome_parts:
                    if not os.path.exists(part):
                        raise FileNotFoundError(f"[ERROR] Part file {part} is missing.")
                    print(f"[DEBUG] Adding {part} to {chrome_assembled}.")
                    with open(part, "rb") as part_file:
                        assembled_file.write(part_file.read())
            os.chmod(chrome_assembled, 0o755)
            print("[INFO] Chrome binary assembled successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to assemble Chrome binary: {e}")
            raise
    else:
        print(f"[INFO] Chrome binary already assembled at: {os.path.abspath(chrome_assembled)}")

    # Ensure Chromedriver exists
    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"Chromedriver not found at: {chromedriver_path}")
    else:
        print(f"[INFO] Chromedriver binary found at: {os.path.abspath(chromedriver_path)}")

    # Check file permissions
    log_and_run(f"ls -l {chrome_assembled}")
    log_and_run(f"ls -l {chromedriver_path}")

    # Check versions
    log_and_run(f"{os.path.abspath(chrome_assembled)} --version || echo '[ERROR] Cannot fetch Chrome version'")
    log_and_run(f"{os.path.abspath(chromedriver_path)} --version || echo '[ERROR] Cannot fetch Chromedriver version'")

    # Configure WebDriver
    chrome_options = Options()
    chrome_options.binary_location = os.path.abspath(chrome_assembled)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--headless")  # Enable headless mode for CI

    print("[INFO] Initializing WebDriver...")
    try:
        driver_service = ChromeService(executable_path=os.path.abspath(chromedriver_path))
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)
        print("[INFO] WebDriver initialized successfully.")
    except Exception as e:
        print(f"[ERROR] Error initializing WebDriver: {e}")
        print("[DEBUG] Retrying with additional diagnostics...")
        log_and_run(f"ps -ef | grep {os.path.basename(chrome_assembled)}")
        raise

    yield driver

    print("[INFO] Closing WebDriver...")
    driver.quit()
    print("[INFO] WebDriver closed successfully.")


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
