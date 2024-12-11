import os
import time
import allure
import json
import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import random
import pytest
import allure
from ev import EV
import string
import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Admin_pages.Create_an_account import Create_Account
from customer_pages.login_c_page import Login_c_page
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from customer_pages.forgot_c_password import Forgot_password
from customer_pages.Role_c import Client_page
from customer_pages.Edit_c_user import Edit_AAD_DELETE_user
from customer_pages.Add_an_user_c import Add_user
from customer_pages.Invoices_c import invoices
from customer_pages.Language_report_с import LR
from customer_pages.audio_vs_video_rep_c import Audio_vs_video_report
from customer_pages.Device_usage_c import Device_usage
from customer_pages.Device_usage_NM_C import Device_usage_NM
from customer_pages.Kanji import Login_Kanji
from customer_pages.Activity_monitor import Activity_monitor

from customer_pages.Interpreter_Dashboard_c import Interpreter_Dashboard
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from customer_pages.Transaction_page_c import Transaction_page
from customer_pages.Dashboard_c import Dashboard
from customer_pages.Widjets_test import Widjets
from customer_pages.Rep_password import Replace_password
from customer_pages.Rep_password2 import Replace_password2
from customer_pages.Device_usage_Yale_C import Device_usage_Yale
import allure
import pytest
import matplotlib.pyplot as plt
import subprocess
import shutil
import chromedriver_autoinstaller
from ev import EV


def generate_random_id(length=7):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


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


# Добавь фикстуру в класс
@pytest.mark.usefixtures("driver")
@allure.feature("Testing the administrative interface for VIP customers")
@allure.story("VIP Admin Test")
class TestVIPCustomer:

    @allure.description("VIP Customer TEST")
    @pytest.mark.run(order=1)
    def test_customer_VIP(self, driver):
        steps = [
            # self.perform_activity_monitor,
            # self.perform_nvp_authorization,
            # self.perform_forgot_password,
            # self.perform_replace_password,
            # self.perform_client_page,
            # self.perform_edit_user,
            # self.perform_add_user,
            # self.perform_check_company_authorization,
            # self.perform_invoice_page_check,
            # self.perform_language_report,
            # self.perform_audio_vs_video_report,
            # self.perform_kanji_login,
            # self.perform_device_usage_page,
            # self.perform_device_usage_nm_page,
            # self.perform_device_usage_Yale_page,
            # self.perform_interpreter_dashboard,
            # self.perform_transaction_page_test,
            # self.perform_dashboard_check,
            # self.perform_widgets_check
        ]

        for step in steps:
            # try:
            step(driver)
            # except Exception as e:
            #     allure.attach(str(e), name=f"Error in {step.__name__}", attachment_type=allure.attachment_type.TEXT)
            #     print(f"Error in {step.__name__}: {e}. Proceeding to the next step.")

    @allure.step("Performing Activity Monitor Check")
    def perform_activity_monitor(self, driver):
        login = Login_c_page(driver)
        login.authorization_new_york()
        # acm = Activity_monitor(driver)
        # acm.Activity_monitor()

    @allure.step("Performing NVP Authorization")
    def perform_nvp_authorization(self, driver):
        login = Login_c_page(driver)
        login.Log_out()
        login.NVP_authorization()

    @allure.step("Performing Forgot Password Process")
    def perform_forgot_password(self, driver):
        login = Login_c_page(driver)
        login.authorization()
        login.Log_out()
        fp = Forgot_password(driver)
        fp.Forgot_PD()

    @allure.step("Performing Replace Password Check")
    def perform_replace_password(self, driver):
        rp = Replace_password(driver)
        rp.Check_gmail()
        login = Login_c_page(driver)
        login.authorizationCOOK()
        rp2 = Replace_password2(driver)
        rp2.Forgot_PD2()
        login.authorizationCOOK2()

    @allure.step("Checking Client Page")
    def perform_client_page(self, driver):
        login = Login_c_page(driver)
        login.authorization()
        role = Client_page(driver)
        role.client_page()

    @allure.step("Editing User Information")
    def perform_edit_user(self, driver):
        eu = Edit_AAD_DELETE_user(driver)
        eu.edit_u()

    @allure.step("Adding New User")
    def perform_add_user(self, driver):
        au = Add_user(driver)
        au.add_user()
        login = Login_c_page(driver)
        login.Log_out()

    @allure.step("Checking Company Authorization")
    def perform_check_company_authorization(self, driver):
        login = Login_c_page(driver)
        login.authorization_check_company()
        login.Log_out()

    @allure.step("Invoice Page Check")
    def perform_invoice_page_check(self, driver):
        login = Login_c_page(driver)
        login.authorization_new_york()
        invoice = invoices(driver)
        invoice.invoice_p_check()

    @allure.step("Language Report Check")
    def perform_language_report(self, driver):
        lr = LR(driver)
        lr.language_rep()

    @allure.step("Audio vs Video Report Check")
    def perform_audio_vs_video_report(self, driver):
        avvs = Audio_vs_video_report(driver)
        avvs.audio_vs_video_rep()
        login = Login_c_page(driver)
        login.Log_out()

    @allure.step("Kanji Login Check")
    def perform_kanji_login(self, driver):
        kanji = Login_Kanji(driver)
        kanji.Kanji()

    @allure.step("Device Usage Page Check")
    def perform_device_usage_page(self, driver):
        login = Login_c_page(driver)
        login.authorization_new_york()
        dev_u = Device_usage(driver)
        dev_u.device_usage_page()
        login.Log_out()

    @allure.step("Device Usage NM Page Check")
    def perform_device_usage_nm_page(self, driver):
        login = Login_c_page(driver)
        login.authorization()
        dev_nm = Device_usage_NM(driver)
        dev_nm.device_usage_page()
        login.Log_out()

    @allure.step("Device Usage Yale Page Check")
    def perform_device_usage_Yale_page(self, driver):
        login = Login_c_page(driver)
        login.authorization_Yale()
        dev_yale = Device_usage_Yale(driver)
        dev_yale.device_usage_page()

    @allure.step("Interpreter Dashboard Check")
    def perform_interpreter_dashboard(self, driver):
        login = Login_c_page(driver)
        login.authorization_new_york()
        id = Interpreter_Dashboard(driver)
        id.interpreter_dashboard()

    @allure.step("Transaction Page Test")
    def perform_transaction_page_test(self, driver):
        tp = Transaction_page(driver)
        tp.transaction_page_test()
        login = Login_c_page(driver)
        login.Log_out()

    @allure.step("Dashboard Check")
    def perform_dashboard_check(self, driver):
        login = Login_c_page(driver)
        login.authorization_EST()
        dashboard = Dashboard(driver)
        dashboard.dashboard_check()
        login.Log_out()

    @allure.step("Widgets Check")
    def perform_widgets_check(self, driver):
        login = Login_c_page(driver)
        login.authorization_for_widjets()
        widgets = Widjets(driver)
        widgets.widgets_check()

    @pytest.fixture(scope="session", autouse=True)
    def analyze_and_report(self, request):
        def finalizer():
            current_directory = os.path.dirname(os.path.abspath(__file__))
            results_directory = os.path.join(current_directory, 'test_results2')

            # Убедитесь, что директория существует
            if not os.path.exists(results_directory):
                os.makedirs(results_directory)

            # Использование пути в analyze_allure_results
            self.analyze_allure_results(results_directory)
            self.create_graph_and_attach_to_allure()

        request.addfinalizer(finalizer)

    def analyze_allure_results(self, directory):
        step_results = {}  # Словарь для хранения результатов каждого шага

        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as file:
                    try:
                        results = json.load(file)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file: {filepath}")
                        continue

                    steps = results.get('steps', [])
                    for step in steps:
                        step_name = step['name']
                        if step_name not in step_results:
                            step_results[step_name] = {'total': 0, 'failed': 0}
                        step_results[step_name]['total'] += 1
                        if step.get('status') in ['failed', 'broken']:
                            step_results[step_name]['failed'] += 1

        self.step_results = step_results

    def create_graph_and_attach_to_allure(self):
        # Получение пути текущей директории
        current_directory = os.path.dirname(os.path.abspath(__file__))
        downloads_directory = os.path.join(current_directory, "Downloads")
    
        # Создание папки "Downloads", если она не существует
        if not os.path.exists(downloads_directory):
            os.makedirs(downloads_directory)
    
        # Создание общего графика для всех результатов
        total_steps = sum(result['total'] for result in self.step_results.values())
        total_failed = sum(result['failed'] for result in self.step_results.values())
        total_successful = total_steps - total_failed
    
        overall_graph_path = os.path.join(downloads_directory, "overall_results_graph.png")
        self.create_and_save_graph(
            'Overall Test Results',
            ['Successful Steps', 'Failed Steps'],
            [total_successful, total_failed],
            overall_graph_path
        )
    
        # Создание индивидуальных графиков для каждого метода
        for step_name, results in self.step_results.items():
            successful_steps = results['total'] - results['failed']
            failed_steps = results['failed']
            step_graph_path = os.path.join(downloads_directory, f"{step_name}_results_graph.png")
            self.create_and_save_graph(
                f'{step_name} Results',
                ['Successful Steps', 'Failed Steps'],
                [successful_steps, failed_steps],
                step_graph_path
            )

    def create_and_save_graph(self, title, labels, values, graph_path):
        success_percentage = (values[0] / sum(values) * 100) if sum(values) != 0 else 0
        failure_percentage = (values[1] / sum(values) * 100) if sum(values) != 0 else 0

        fig, ax = plt.subplots()
        ax.bar(labels, values, color=['green', 'red'])
        plt.xlabel('Types of Results')
        plt.ylabel('Count')
        plt.title(f'{title}: {values[0]} Successful, {values[1]} Failed\n'
                  f'Success: {success_percentage:.2f}%, Failure: {failure_percentage:.2f}%')
        fig.savefig(graph_path)

        with open(graph_path, 'rb') as file:
            allure.attach(file.read(), name=f'{title}', attachment_type=allure.attachment_type.PNG)
