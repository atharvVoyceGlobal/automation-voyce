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
from playwright.sync_api import sync_playwright
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

@staticmethod
def install_browser_and_driver():
    installation_path = os.path.join(os.getcwd(), "chrome_installation")
    os.makedirs(installation_path, exist_ok=True)

    try:
        print("Installing Chrome...")
        subprocess.run(
            [
                "npx", "@puppeteer/browsers", "install", "chrome@stable",
                "--path", installation_path
            ],
            check=True
        )
        print("Chrome installed successfully!")

        chrome_binary_path = os.path.join(
            installation_path,
            "chrome",
            "mac_arm-131.0.6778.87",
            "chrome-mac-arm64",
            "Google Chrome for Testing.app",
            "Contents",
            "MacOS",
            "Google Chrome for Testing"
        )

        if not os.path.exists(chrome_binary_path):
            raise FileNotFoundError(f"Chrome binary not found at {chrome_binary_path}")

        print("Fetching Chrome version...")
        version_output = subprocess.run(
            [chrome_binary_path, "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        chrome_version = version_output.stdout.strip().split(" ")[-1]
        print(f"Installed Chrome version: {chrome_version}")

        print(f"Installing ChromeDriver for version {chrome_version}...")
        subprocess.run(
            [
                "npx", "@puppeteer/browsers", "install", f"chromedriver@{chrome_version}",
                "--path", installation_path
            ],
            check=True
        )
        print("ChromeDriver installed successfully!")

        chromedriver_path = os.path.join(
            installation_path,
            "chromedriver",
            f"mac_arm-{chrome_version}",
            "chromedriver-mac-arm64",
            "chromedriver"
        )

        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")

        print(f"Chrome binary: {chrome_binary_path}")
        print(f"ChromeDriver binary: {chromedriver_path}")

        return chrome_binary_path, chromedriver_path
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during installation: {e}")
        raise

@pytest.fixture
def driver():

    """
    Настройка Selenium WebDriver с установленными Chrome и ChromeDriver.
    """
    chrome_binary, chromedriver_path = install_browser_and_driver()

    chrome_options = Options()
    chrome_options.binary_location = chrome_binary
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    # chrome_options.add_argument("--headless")  # Включение headless режима

    driver_service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    pid = driver.service.process.pid
    os.system(f'echo {EV.my_password1} | sudo -S renice -n -10 -p {pid}')

    yield driver
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
