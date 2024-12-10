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
from Admin_pages.Forgot_password import Forgot_password
from Admin_pages.Client_page import Client_page
from Admin_pages.finish_screenshot import Finish_screen
from Admin_pages.edit_user import Edit_AAD_DELETE_user
from Admin_pages.Devices_check import Devices_Check
from Admin_pages.Transaction_page_Admin import Transaction_page_A
from Admin_pages.Widjets_admin import Widjets
from Admin_pages.Dashboard import Dashboard
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

@pytest.fixture(scope="session")
def driver():
    # Удалить папку с драйверами перед установкой
    chromedriver_dir = os.path.expanduser("~/.wdm")
    if os.path.exists(chromedriver_dir):
        shutil.rmtree(chromedriver_dir)

    # Автоматическая установка ChromeDriver
    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    # chrome_options.add_argument("--headless=new")  # Включение headless режима

    driver = webdriver.Chrome(options=chrome_options)
    pid = driver.service.process.pid  # Получение PID процесса драйвера

    os.system(f'echo {EV.my_password1} | sudo -S renice -n -10 -p {pid}')

    yield driver
    driver.quit()


# @pytest.fixture
# def driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-extensions")
# 
#     driver_service = ChromeService(executable_path='/Users/nikitabarshchuk/PycharmProjects/pythonProject3/chromedriver')
#     chrome_options.binary_location = '/Users/nikitabarshchuk/PycharmProjects/pythonProject3/chrome/mac_arm-130.0.6723.58/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
#     driver = webdriver.Chrome(service=driver_service, options=chrome_options)
#     pid = driver.service.process.pid  # Получение PID процесса драйвера
# 
#     # Выполнение команды с вводом пароля
#     os.system(f'echo {EV.my_password1} | sudo -S renice -n -10 -p {pid}')
# 
#     yield driver
#     driver.quit()

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
        dsh = Dashboard(driver)
        dsh.dashboard_check()
        widjet = Widjets(driver)
        widjet.widgets_check()
        # login.authorization_PROD()
        # tra = Transaction_page_A(driver)
        # tra.transaction_page_test()
        # login.authorization_PROD()
        # DC = Devices_Check(driver)
        # DC.devices_check()
        # login.NVP_authorization()
        # login.authorization()
        # login.Log_out()
        #
        ac = Create_Account(driver)
        ac.ACC()
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
