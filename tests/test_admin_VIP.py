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


@pytest.fixture
def driver():
    """
    Настройка Selenium WebDriver с предустановленными Chromium и Chromedriver.
    """
    # Пути для Chromium и Chromedriver
    chrome_binary = "/usr/local/bin/chrome-linux64/chrome"
    chromedriver_path = "/usr/local/bin/chromedriver"

    # Проверка наличия файлов
    print("\n[DEBUG] Проверяем наличие бинарных файлов...")
    if not os.path.exists(chrome_binary):
        print(f"[ERROR] Chromium не найден по пути: {chrome_binary}")
    else:
        print(f"[DEBUG] Chromium найден по пути: {chrome_binary}")
        os.system(f"ls -l {chrome_binary}")
        os.system(f"{chrome_binary} --version || echo '[ERROR] Chromium не запускается'")

    if not os.path.exists(chromedriver_path):
        print(f"[ERROR] Chromedriver не найден по пути: {chromedriver_path}")
    else:
        print(f"[DEBUG] Chromedriver найден по пути: {chromedriver_path}")
        os.system(f"ls -l {chromedriver_path}")
        os.system(f"{chromedriver_path} --version || echo '[ERROR] Chromedriver не запускается'")

    # Если один из файлов отсутствует, выходим с ошибкой
    if not os.path.exists(chrome_binary):
        raise EnvironmentError(f"Chromium не найден по пути: {chrome_binary}")
    if not os.path.exists(chromedriver_path):
        raise EnvironmentError(f"Chromedriver не найден по пути: {chromedriver_path}")

    # Настройка WebDriver
    chrome_options = Options()
    chrome_options.binary_location = chrome_binary
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--headless")  # Включение headless режима для CI

    print("[DEBUG] Инициализируем WebDriver...")
    try:
        driver_service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    except Exception as e:
        print(f"[ERROR] Ошибка при инициализации WebDriver: {e}")
        raise

    yield driver
    print("[DEBUG] Закрываем WebDriver...")
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
