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
    """Загрузка и установка Chrome из официального .deb пакета для Linux."""
    chrome_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
    deb_path = "google-chrome-stable_current_amd64.deb"

    if not os.path.exists("/usr/bin/google-chrome"):
        print("[INFO] Chrome не найден. Загружается...")
        urllib.request.urlretrieve(chrome_url, deb_path)
        print(f"[INFO] Загружен пакет Chrome .deb в {deb_path}")

        print("[INFO] Установка Chrome...")
        subprocess.run(["sudo", "dpkg", "-i", deb_path], check=True)
        os.remove(deb_path)
        print("[INFO] Chrome успешно установлен.")
    else:
        print("[INFO] Chrome уже установлен.")

def download_and_install_chromedriver():
    """Загрузка и установка последней стабильной версии ChromeDriver."""
    chromedriver_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = urllib.request.urlopen(chromedriver_url)
    version_number = response.read().decode('utf-8').strip()
    chromedriver_link = f"https://chromedriver.storage.googleapis.com/{version_number}/chromedriver_linux64.zip"

    chromedriver_zip = "chromedriver_linux64.zip"
    if not os.path.exists("chromedriver"):
        print("[INFO] ChromeDriver не найден. Загружается...")
        urllib.request.urlretrieve(chromedriver_link, chromedriver_zip)

        subprocess.run(["unzip", "-o", chromedriver_zip], check=True)
        subprocess.run(["chmod", "+x", "chromedriver"], check=True)
        os.remove(chromedriver_zip)
        print("[INFO] ChromeDriver установлен и готов к использованию.")
    else:
        print("[INFO] ChromeDriver уже установлен.")

@pytest.fixture
def driver():
    download_and_install_chrome()
    download_and_install_chromedriver()

    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--headless")

    driver_service = ChromeService(executable_path=os.path.abspath("chromedriver"))
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
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
