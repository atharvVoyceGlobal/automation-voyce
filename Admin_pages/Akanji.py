import os
import time
import allure
from utilities.logger import Logger
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
from database.Databricks import Databricks
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from ev import EV


class Login_Kanji(Base, Databricks, EV):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        Databricks.__init__(self)

    # Locators
    blueprint = '//*[@id="sidebarItemblueprints"]'
    devices = "//a[@class='bl-blueprint-list__item decorate-off']//p[contains(@class, 'b-txt-light') and contains(., 'Devices')]"
    login_b = '//*[@id="app"]/div/div[1]/button[1]'
    login_field = "//*[@id='identifierId']"
    next = '//*[@id="identifierNext"]/div/button/span'
    next2 = '//*[@id="passwordNext"]/div/button/span'
    password_field = "//*[@id='password']/div[1]/div/div[1]/input"
    continue_login = "//div[contains(@class, 'ccaa66e69')]/button[contains(@class, 'c6141592f')]"
    main_word = "//*[@id='header-container-id']/div/div[1]/div"
    error_email = "//*[@id='email_help']/div"
    error_password = "//*[@id='password_help']/div"
    no_valid_password = "/html/body/div[2]/div/div/div/span[2]"
    no_valid_email = "//span[text()='User not found']"
    log_out = "//*[@id='root']/section/aside/div/div[3]/div/div/span/span"
    log_out2 = "//span[@class='ant-dropdown-menu-title-content' and text()='Logout']"
    main_word2 = "//div[contains(@class, 'rc-virtual-list-holder-inner')]"
    tam = "//span[text()='Try another method']"
    rec_code = '//*[@id="with-selector-list"]/li[2]/form/button'
    code_f = '//*[@id="code"]'
    continue_rec_code = "//button[@type='submit'][@name='action'][@value='default'][contains(@class, 'c6141592f')][@data-action-button-primary='true' and text()='Continue']"
    google = "//span[text()='Continue with Google']"
    filter = '//*[@id="showFiltersTooltip"]/div'
    filter2 = "//section[contains(@class, 'sc-cCVOAp') and contains(@class, 'sc-kAdXeD') and contains(@class, 'sc-hCaUpS') and contains(@class, 'sc-bvTASY') and contains(@class, 'hrLCxu') and text()='Filter']"
    filter3 = "//section[contains(@class, 'sc-hcnlBt') and contains(@class, 'sc-hkbPbT') and contains(@class, 'sc-jRhVzh') and contains(@class, 'gAwVam') and contains(@class, 'cursor-pointer') and @title='Blueprint']"
    filter4 = "//section[@class='sc-cCVOAp sc-kAdXeD sc-hCaUpS sc-bvTASY hrLCxu' and text()='includes any']"
    filter5 = "//section[@class='sc-hcnlBt sc-hkbPbT sc-jRhVzh gAwVam cursor-pointer' and text()='contains']"
    filter_field = "//input[@name='filters[0].value']"
    galka = "//i[@class='far fa-check']"
    three = "//button[@class='sc-dxgOiQ dEBpxt' and text()='300']"

    # Getters
    def get_blueprint(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.blueprint)))

    def get_three(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.three)))

    def get_galka(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.galka)))

    def get_filter_field(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter_field)))

    def get_filter5(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter5)))

    def get_filter4(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter4)))

    def get_filter3(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter3)))

    def get_filter2(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter2)))

    def get_filter(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter)))

    def get_next2(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.next2)))

    def get_next(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.next)))

    def get_google(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.google)))

    def get_continue_rec_code(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.continue_rec_code)))

    def get_code_f(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.code_f)))

    def get_rec_code(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.rec_code)))

    def get_tam(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.tam)))

    def get_login_b(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.login_b)))

    def get_main_word2(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.main_word2)))

    def get_all_clients(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.all_clients)))

    def get_log_out(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.log_out)))

    def get_log_out2(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.log_out2)))

    def get_login_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.login_field)))

    def get_password_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field)))

    def get_no_valid_password(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.no_valid_password)))

    def get_no_valid_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.no_valid_email)))

    def get_button_login(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.continue_login)))

    def get_main_word(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.main_word)))

    def get_error_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_email)))

    def get_error_password(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_password)))

        # Actions

    def input_code(self):
        # Путь к файлу с кодом
        file_path = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/customer_pages/code"
        # Считывание кода из файла
        with open(file_path, 'r') as file:
            code = file.read().strip()  # .strip() удалит пробелы и переводы строки по краям строки
        # Вводим считанный код в поле ввода
        self.get_code_f().send_keys(code)
        print("input code")

    def input_filter_field(self, name):
        self.get_filter_field().send_keys(name)
        print("Input company NAME")

    def click_300(self):
        self.get_three().click()
        print("Click three")

    def click_filter5(self):
        self.get_filter5().click()
        print("Click Filter")

    def click_galka(self):
        self.get_galka().click()
        print("Click Galka")

    def click_filter4(self):
        self.get_filter4().click()
        print("Click Filter")

    def click_filter3(self):
        self.get_filter3().click()
        print("Click Filter")

    def click_filter2(self):
        self.get_filter2().click()
        print("Click Filter")

    def click_filter(self):
        self.get_filter().click()
        print("Click Filter")

    def click_google(self):
        self.get_google().click()
        print("Click Google")

    def click_next2(self):
        self.get_next2().click()
        print("Click next")

    def click_next(self):
        self.get_next().click()
        print("Click next")

    def click_blueprint(self):
        self.get_blueprint().click()
        print("Click blueprint")

    def click_continue_rec_code(self):
        self.get_continue_rec_code().click()
        print("Click recover code")

    def click_rec(self):
        self.get_rec_code().click()
        print("Click recover code")

    def click_tam(self):
        self.get_tam().click()
        print("Click Try another methood")

    def click_login(self):
        self.get_login_b().click()
        print("Click Log in button")

    def input_login(self, user_name):
        self.get_login_field().send_keys(user_name)
        print("input user name")

    def input_password(self, user_password):
        self.get_password_field().send_keys(user_password)
        print("input password")

    def click_button_continue(self):
        self.get_button_login().click()
        print("CLICK login button")

    def click_all_clients(self):
        self.get_all_clients().click()
        print("Click All Clients")

    def click_log_out(self):
        self.get_log_out().click()
        print("CLICK logs out")

    def click_log_out2(self):
        self.get_log_out2().click()
        print("CLICK logs out 2")

    # METHODS
    def scroll_to_bottom(self, delay=1.0):
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # SCROLL DOWN
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(delay)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def extract_base_name(self, name):
        """
        Extracts the base name, considering the condition of four characters and spaces. If the word has fewer than 4 characters, it uses the first word.
        """
        cleaned_name = name.replace(" ", "")
        if len(cleaned_name) < 4:
            return name.split(' ')[0]
        else:
            return cleaned_name[:4]

    def collect_blueprints_info(self):
        """
        Gathers information about projects (blueprints) and groups them by the first four characters of the name, ignoring spaces. Excludes entries with 0 devices. Then writes the collected information to a file.
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".bl-blueprint-list__item"))
        )

        blueprint_items = self.driver.find_elements(By.CSS_SELECTOR, ".bl-blueprint-list__item")
        blueprints_info = {}

        for item in blueprint_items:
            name = item.find_element(By.CSS_SELECTOR, ".bl-blueprint-list__item-name").text
            device_count_text = item.find_element(By.CSS_SELECTOR, ".bl-blueprint-list__item-counts p").text
            device_count = int(device_count_text.split()[0])

            if device_count == 0:
                continue

            base_name = self.extract_base_name(name)
            if base_name in blueprints_info:
                blueprints_info[base_name]['device_count'] += device_count

                if len(name.replace(" ", "")) > len(blueprints_info[base_name]['name'].replace(" ", "")):
                    blueprints_info[base_name]['name'] = name
            else:
                blueprints_info[base_name] = {'name': name, 'device_count': device_count}

        file_path = '/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Admin_pages/Kanji_devices_Admin'
        with open(file_path, 'w') as file:
            for info in blueprints_info.values():
                line = f"{info['name']}, {info['device_count']}\n"
                file.write(line)

        print(list(blueprints_info.values()))
        return list(blueprints_info.values())

    def Kanji(self):
        with allure.step("Log In Kanji"):
            Logger.add_start_step(method='VALID_authorization')
        self.driver.get(self.url_Kanji)
        self.click_login()
        self.click_google()
        self.input_login(self.my_accaunt)
        self.click_next()
        self.input_password(self.my_password)
        self.click_next2()
        time.sleep(10)
        self.click_blueprint()
        self.scroll_to_bottom()
        self.collect_blueprints_info()

    def get_devices_info(self):
        with allure.step("Get Kanji devices data"):
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".react-bs-container-body table tbody"))
            )
            rows = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".react-bs-container-body .table tbody tr"))
            )

            file_path = os.path.join(
                '/Users/nikitabarshchuk/PycharmProjects/pythonProject3/customer_pages/Kanji_devices')

            with open(file_path, 'w') as file:
                for row in rows:
                    try:
                        device_name = WebDriverWait(row, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(4) span"))
                        ).get_attribute('title').strip()

                        serial_number = WebDriverWait(row, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(7) span"))
                        ).get_attribute('title').strip()

                        line = f"Device Name: {device_name}, Serial Number: {serial_number}\n"

                        file.write(line)

                    except Exception as e:
                        print(f"It was not possible to extract data for the line: {row.text}.Error: {e}")
