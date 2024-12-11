import math
import os
import glob
import csv
import pandas as pd
import shutil
import logging
import time
import allure
from collections import defaultdict
from selenium.webdriver.chrome.service import Service
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium import webdriver
from utilities.logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
import string
import random
from database.Databricks import Databricks
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from database.Database import Database
import requests
from customer_pages.Graph_c import Graphs
from operator import itemgetter
from ev import EV

class Device_usage(Graphs, Database, EV):
    def __init__(self, driver, elements=None):  # elements теперь необязательный параметр
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver
        self.elements = elements if elements is not None else []

    def __getitem__(self, index):
        return self.elements[index]

    # Locators
    last_pages = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/ul/li[8]'
    ten_tr_per_page = "//div[contains(@class, 'ant-select-item-option-content') and contains(text(), '10 / page')]"
    pages = "//span[@class='ant-select-selection-item' and text()='100 / page']"
    completed_calls_check = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[6]/a'
    mac_assert_f = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[3]'
    serial_assert_f = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]'
    dev_name_assert = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]'
    n_of_t = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[6]/div/span[1]'
    min_u = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[4]/div/span[1]'
    mac_sf = "//input[@class='ant-input css-1tx2tgg' and @type='text' and @placeholder='Search macAddress']"
    mac_s = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[3]/div/span[2]/span'
    ser_nub_sf = "//input[@class='ant-input css-1tx2tgg' and @type='text' and @placeholder='Search IOSSerialNumber']"
    ser_nub_s = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[2]/div/span[2]/span'
    ser_nub_f = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[2]/div/span[1]/div/span[1]'
    dev_name_sf = "//input[@placeholder='Search deviceName']"
    dev_name_s = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[2]/span'
    dev_name_f = "//*[@id='root']/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[1]/div/span[1]"
    dropdown_list = '//*[@id="root"]/section/aside/div/ul/li[4]/div'
    device_usage_b = "//a[@href='/pages/reports/device-usage' and text()='Device Usage']"
    download_b = "//*[@id='root']/section/section/main/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/button"
    all_clients = '//*[@id="header-container-id"]/div/div[6]/div/div/span[2]'
    choose_company = "//div[@class='ant-select-item-option-content' and text()='CCH Internal']"
    Today_list = '//*[@id="header-container-id"]/div/div[5]/div/div/span[2]'
    Yesterday = "//div[contains(@class, 'ant-select-item-option-content') and contains(text(), 'Yesterday')]"
    Custom = "//div[contains(@class, 'ant-select-item-option-content') and text()='Custom Date']"
    Last_week = "//div[@title='Last Week']"
    This_week = "//div[@title='This Week']"
    start_date = '//*[@id="header-container-id"]/div/div[5]/div/div/div[1]/input'
    end_date = '//*[@id="header-container-id"]/div/div[5]/div/div/div[3]/input'
    no_data = '//*[@id="root"]/section/section/main/div/div/div[3]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td/div/div[2]'
    lang_f = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[1]/div/span[1]'
    lang_s = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[2]/span'
    lang_s_f = "//input[@placeholder='Search TargetLanguage']"
    total_calls = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[2]/div/span[1]'
    total_minutes = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[3]/div/span[1]'
    ser_audio_c = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[4]/div/span[1]'
    ser_video_c = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[5]/div/span[1]'
    minutes_by_a = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[6]/div/span[1]'
    minutes_by_v = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[7]/div/span[1]'
    avg_rating = '//*[@id="root"]/section/section/main/div/div/div[3]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[8]/div/span[1]'
    drop_download = '//*[@id="root"]/section/section/main/div/div/div[3]/div/div/div/div/div/div[1]/div/div[1]/div/div/span[2]'
    pdf = "//div[@title='PDF']"
    completed_calls = '//*[@id="root"]/section/section/main/div/div/div[3]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[9]/a'
    this_month = '//div[@title="This Month"]'
    Last_month = '//div[@title="Last Month"]'
    Last_30_days = '//div[@title="Last 30 Days"]'
    This_year = '//div[@title="This Year"]'
    Last_year = '//div[@title="Last Year"]'
    lang_field = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]'
    element_xpath = "//td[@class='ant-table-cell' and contains(text(), ' minutes')]"
    additional_xpath = '//*[@id="root"]/section/aside/div/ul'

    # Getters
    def get_mac_assert_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.mac_assert_f)))

    def get_serial_assert_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.serial_assert_f)))

    def get_dev_name_assert(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.dev_name_assert)))

    def get_n_of_t(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.n_of_t)))

    def get_min_u(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.min_u)))

    def get_mac_sf(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.mac_sf)))

    def get_mac_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.mac_s)))

    def get_ser_nub_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ser_nub_s)))

    def get_ser_nub_sf(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ser_nub_sf)))

    def get_ser_nub_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ser_nub_f)))

    def get_name_search_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.dev_name_sf)))

    def get_name_search(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.dev_name_s)))

    def get_name_filter(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.dev_name_f)))

    def get_pages(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.pages)))

    def get_avg_call_length(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.minutes_by_v)))

    def get_lang_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_field)))

    def get_Last_month(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Last_month)))

    def get_Last_30_days(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Last_30_days)))

    def get_This_year(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.This_year)))

    def get_Last_year(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Last_year)))

    def get_This_month(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.this_month)))

    def get_This_week(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.This_week)))

    def get_completed_calls(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.completed_calls)))

    def get_download_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.download_b)))

    def get_all_clients(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.all_clients)))

    def get_ten_tr_per_page(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ten_tr_per_page)))

    def get_choose_company(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.choose_company)))

    def get_Yesterday(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Yesterday)))

    def get_Today_list(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Today_list)))

    def get_Custom(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Custom)))

    def get_Last_week(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Last_week)))

    def get_start_date(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.start_date)))

    def get_end_date(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.end_date)))

    def get_no_data(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.no_data)))

    def get_lang_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_f)))

    def get_last_pages(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.last_pages)))

    def get_lang_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_s_f)))

    def get_lang_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_s)))

    def get_total_calls(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.total_calls)))

    def get_total_minutes(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.total_minutes)))

    def get_ser_audio_c(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ser_audio_c)))

    def get_ser_video_c(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ser_video_c)))

    def get_completed_calls_check(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.completed_calls_check)))

    def get_avg_rating(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.avg_rating)))

    def get_avg_wait_time(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.minutes_by_a)))

    def get_drop_download(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.drop_download)))

    def get_dropdown_list(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.dropdown_list)))

    def get_language_report_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.device_usage_b)))

    def get_pdf(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.pdf)))

        # Actions

    def input_mac(self, user_name):
        self.get_mac_sf().send_keys(user_name)
        print("input Mac Number")

    def click_mac_sf(self):
        self.get_mac_sf().click()
        print("CLICK Mac Search ")

    def click_mac_s(self):
        self.get_mac_s().click()
        print("CLICK Mac Search ")

    def click_ser_nub_s(self):
        self.get_ser_nub_s().click()
        print("CLICK Serial Number Search")

    def input_ser_num(self, user_name):
        self.get_ser_nub_sf().send_keys(user_name)
        print("input Serial Number")

    def input_dev_name(self, user_name):
        self.get_name_search_field().send_keys(user_name)
        print("input Device name")

    def click_dev_n_s(self):
        self.get_name_search().click()
        print("CLICK Device Name Search")

    def click_n_of_t(self):
        self.get_n_of_t().click()
        print("CLICK Number of Transactions filter")

    def click_min_u(self):
        self.get_min_u().click()
        print("CLICK Used Minutes filter")

    def click_ser_nub_f(self):
        self.get_ser_nub_f().click()
        print("CLICK Serial Number filter")

    def click_dev_name_filter(self):
        try:
            element = self.get_name_filter()
            element.click()
            print("CLICK Device Name filter")
        except StaleElementReferenceException:
            # Повторно получаем элемент и пытаемся кликнуть
            element = self.get_name_filter()
            element.click()

    def click_avg_wait_time(self):
        self.get_avg_wait_time().click()
        print("CLICK avg wait_time")

    def click_avg_call_length(self):
        self.get_avg_call_length().click()
        print("CLICK avg call length")

    def click_rating(self):
        self.get_avg_rating().click()
        print("CLICK avg rating")

    def click_ser_audio_c(self):
        self.get_ser_audio_c().click()
        print("CLICK SERVICED_Audio CALLS")

    def click_ser_video_c(self):
        self.get_ser_video_c().click()
        print("CLICK SERVICED_Video CALLS")

    def click_user(self):
        user_element = self.get_user_element()
        self.driver.execute_script("arguments[0].click();", user_element)
        print("Clicked on User")

    def click_select_role_button(self):
        self.get_select_role_button().click()
        print("click select_role_button")

    def click_first_company(self):
        first_company = self.get_first_company()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("Clicked first_company")

    def click_all_clients(self):
        self.get_all_clients().click()
        print("CLICK all clients")

    def click_total_minutes(self):
        self.get_total_minutes().click()
        print("CLICK total minutes filter")

    def click_download_b(self):
        self.get_download_b().click()
        print("CLICK download button")

    def click_du(self):
        self.get_language_report_b().click()
        print("CLICK Device Usage page")

    def click_last_pages(self):
        self.get_last_pages().click()
        print("CLICK last pages")

    def click_drop_down(self):
        self.get_dropdown_list().click()
        print("CLICK dropdown list")

    def clear_input_field(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click()
        actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND)
        actions.send_keys(Keys.DELETE)
        actions.perform()

    def click_choose_company(self):
        self.get_choose_company().click()
        print("CLICK choose company")

    def click_select_company(self):
        SC = self.get_select_company()
        action = ActionChains(self.driver)
        action.move_to_element(SC).click().perform()
        print("click select company")

    def click_all_companies(self):
        self.get_select_all_companies().click()
        print("CLICK all companies")

    def click_list(self):
        self.get_Today_list().click()
        print("CLICK list")

    def press_return_key(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем нажатие на клавишу Return
        actions.send_keys(Keys.RETURN).perform()

        print("Pressed the Return key")

    def click_yesterday(self):
        self.get_Yesterday().click()
        print("CLICK yesterday")

    def click_last_week(self):
        self.get_Last_week().click()
        print("CLICK last week")

    def click_this_month(self):
        self.get_This_month().click()
        print("CLICK This month")

    def click_Last_month(self):
        self.get_Last_month().click()
        print("CLICK Last month")

    def click_Last_30_days(self):
        self.get_Last_30_days().click()
        print("CLICK Last 30 days")

    def double_press_down_arrow(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем двойное нажатие на стрелку вверх
        actions.send_keys(Keys.ARROW_DOWN).perform()  # второе нажатие

        print("Pressed the Down arrow key")

    def click_This_year(self):
        self.get_This_year().click()
        print("CLICK This year")


    def input_lang_sf(self, language):
        self.get_lang_s_f().send_keys(language)
        print("Input language")

    def click_completed_calls_check(self):
        self.get_completed_calls_check().click()
        print("CLICK completed_calls_check")

    def click_pages(self):
        self.get_pages().click()
        print("CLICK pages")

    def click_total_c(self):
        self.get_total_calls().click()
        print("CLICK Total calls filter")

    def click_lang_s(self):
        self.get_lang_s().click()
        print("CLICK language search")

    def click_ten_tr_per_page(self):
        self.get_ten_tr_per_page().click()
        print("CLICK ten_tr_per_page")

    def click_Last_year(self):
        self.get_Last_year().click()
        print("CLICK Last year")

    def click_This_week(self):
        self.get_This_week().click()
        print("CLICK This week")

    def click_lang_f(self):
        self.get_lang_f().click()
        print("CLICK Language Filter")

    def click_add(self):
        ad = self.get_add()
        action = ActionChains(self.driver)
        action.move_to_element(ad).click().perform()
        print("click Add")

    # METHODS

    def fetch_sorted_languages_from_web(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr > td:nth-child(1)"))
        )
        # Извлекаем все элементы, содержащие названия языков
        language_elements = self.driver.find_elements(By.CSS_SELECTOR, "table > tbody > tr > td:nth-child(1)")

        # Предположим, что первый элемент в списке - это ненужный элемент (например, заголовок),
        # поэтому начнем с индекса 1 вместо 0, чтобы пропустить его
        languages = [element.text.strip() for element in language_elements[1:]]  # начинаем со второго элемента
        print("List of languages ​​from the web page:", languages)

        return languages

    def move_latest_file(self, download_folder, target_folder, file_pattern):
        try:
            if not os.path.exists(download_folder):
                print(f"The download folder does not exist: {download_folder}")
                return None
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)  # Создаём целевую папку, если она не существует

            files = glob.glob(os.path.join(download_folder, file_pattern))
            if not files:
                print(f"Files with a template {file_pattern} were not found in the folder {download_folder}")
                return None

            latest_file = max(files, key=os.path.getctime)
            target_file = os.path.join(target_folder, os.path.basename(latest_file))

            shutil.move(latest_file, target_file)
            print(f"The file {latest_file} was moved to {target_file}")
            return target_file
        except Exception as e:
            print(f"Error when moving the file: {e}")
            return None

    def compare_language_lists(self, list_from_db, list_from_web):
        # Сравнение двух списков языков
        if list_from_db == list_from_web:
            print("Languages is good.")
        else:
            error_message = "Filter is not working. \ Nras: \ n"
            discrepancies_found = False

            for db_lang, web_lang in zip(list_from_db, list_from_web):
                if db_lang != web_lang:
                    discrepancies_found = True
                    error_message += f"DB: {db_lang}, web: {web_lang} \ n"

            if discrepancies_found:
                raise Exception(error_message)

    def compare_device_data_for_periods(self):
        time_periods = ['yesterday', 'This_week', 'last_week', 'this_month',
                        'Last_month', 'Last_30_days', 'This_year', 'Last_year']
        for period in time_periods:
            print(f"Processing period: {period}")
            matched_count, has_discrepancies = self.take_data_for_device_period(period)
            # Сюда нужно добавить логику получения общего числа устройств из db_data
            total_devices = "Implement logic to fetch total devices"  # Измените это на соответствующий код
            print(f"Period '{period}':")
            print(f"Total devices from SQL query: {total_devices}")
            print(f"Total matched devices: {matched_count}")

            if has_discrepancies:
                print(
                    f"There is a mismatch in the number of devices between SQL query and web page for period '{period}'.")
            else:
                print("All devices from SQL query matched with devices from the web page for this period.")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolling to the bottom of the page is performed")

    def select_time_period_and_wait_for_update(self, time_period, open_list=True):
        if open_list:
            self.click_list()  # Открытие списка только если это необходимо
            self.double_press_down_arrow()
        time.sleep(10)  # Короткая задержка, чтобы убедиться, что список открыт
        getattr(self, f"click_{time_period}")()
        time.sleep(30)  # Ожидание обновления данных
        self.click_download_b()
        time.sleep(10)
        download_folder = "/Users/nikitabarshchuk/Downloads"
        target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
        file_pattern = "Device_Usage_Report*.xlsx"

        moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)
        time.sleep(60)

        if moved_file_path:
            time.sleep(30)
            csv_data = self.read_csv_device_usage_data(moved_file_path)
            website_data = self.fetch_website_data_for_devices1()
            assert self.compare_device_usage_data(website_data, csv_data_list=csv_data), "Data mismatch found."

    def fetch_website_data_for_devices1(self):
        # Ожидание загрузки данных устройств
        rows = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ant-table-tbody > tr"))
        )

        # Извлечение данных устройств
        device_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 6:  # Убедитесь, что в строке есть достаточно ячеек
                row_data = {
                    "devicename": cells[0].text.strip(),
                    "serialnumber": cells[1].text.strip(),
                    "macaddress": cells[2].text.strip(),
                    "minutesused": cells[3].text.strip(),
                    "deviceowner": cells[4].text.strip(),
                    "numberoftransactions": cells[5].text.strip(),
                }
                device_data.append(row_data)
            else:
                print(f"Not enough cells in the row to extract data: {row.text}")

        print("All device data:", device_data)  # Вывод всех данных устройств
        return device_data

    def take_data_for_device_period(self, time_period):
        # Особое внимание к периоду 'Last_year'
        self.select_time_period_and_wait_for_update(time_period)
        website_data = self.fetch_website_data_for_devices()
        db_data = self.query_get_devices_Indiana_for_periods(time_period)

        if not db_data:
            print(f"No database data found for period '{time_period}'")
            return 0, True  # Предполагаем, что расхождения есть

        return self.compare_device_data(website_data, db_data)

    def fetch_website_data_for_devices(self):
        # Перейдите к разделу устройств на сайте, если это необходимо
        # self.driver.get('URL_of_device_section')

        # Ожидание загрузки данных устройств, предполагаем, что они находятся в таблице
        rows = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
        )

        # Извлечение данных устройств
        device_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            # Предположим, что структура строки таблицы соответствует следующему формату:
            # | Serial Number | Service Minutes | Number of Services | ... |
            device_data.append({
                "SerialNumber": cells[1].text.strip(),  # Индекс может варьироваться
                "ServiceMinutes": cells[3].text.strip(),  # Индекс может варьироваться
                "NumberOfServices": cells[5].text.strip(),  # Индекс может варьироваться
                # Добавьте больше полей по мере необходимости
            })

        return device_data

    def compare_device_data(self, website_data, db_data, period):
        discrepancies = []

        for sql_row in db_data:
            web_row = next((item for item in website_data if item['SerialNumber'] == sql_row['IOSSerialNumber']), None)

            if web_row:
                device_discrepancies = []

                if str(sql_row['ServiceMinutes']) != web_row['ServiceMinutes']:
                    device_discrepancies.append(
                        f"ServiceMinutes mismatch: DB({sql_row['ServiceMinutes']}) != Web({web_row['ServiceMinutes']})")
                if str(sql_row['NumberOfServices']) != web_row['NumberOfServices']:
                    device_discrepancies.append(
                        f"NumberOfServices mismatch: DB({sql_row['NumberOfServices']}) != Web({web_row['NumberOfServices']})")

                if device_discrepancies:
                    discrepancy_message = f"Discrepancies for SerialNumber {sql_row['IOSSerialNumber']} in '{period}':\n" + "\n".join(
                        device_discrepancies)
                    discrepancies.append(discrepancy_message)
            else:
                discrepancies.append(
                    f"Missing device on web for SerialNumber {sql_row['IOSSerialNumber']} in '{period}'.")

        if discrepancies:
            error_message = f"Discrepancies found for period '{period}':\n" + "\n".join(discrepancies)
            logging.error(error_message)
            # Ваш код для обработки ошибок и логирования
        else:
            # Ваш код в случае, если ошибок не обнаружено
            print(f"All devices matched perfectly for period '{period}'.")

        return len(db_data) - len(discrepancies), bool(discrepancies)

    def execute_period_comparison(self):

        with allure.step("Compare data with DB by Periods"):
            time_periods = ['yesterday', 'This_week', 'last_week', 'this_month', 'Last_month', 'Last_30_days', 'This_year', 'Last_year']
            for time_period in time_periods:
                print(f"Processing period: {time_period}")
                self.select_time_period_and_wait_for_update(time_period)
#
                # Инициализация переменной для хранения данных
                db_data = []

                # Получение и сравнение данных для каждого периода
                website_data = self.fetch_website_data_for_devices()  # Получение данных с сайта

                if time_period == 'Last_month':
                    db_data = self.query_get_devices_Indiana_for_periods(time_period)
                    historic_data = self.query_get_devices_Indiana_for_last_month()
                    if historic_data:
                        db_data += historic_data
                    aggregated_data = self.aggregate_results(db_data)
                    db_data = [{'IOSSerialNumber': ios_serial, 'ServiceMinutes': data['ServiceMinutes'],
                                'NumberOfServices': data['NumberOfServices']} for ios_serial, data in
                               aggregated_data.items()]

                elif time_period in ['Last_30_days', 'This_year', 'Last_year']:
                    # Для данных периодов нет необходимости агрегации
                    if time_period == 'Last_30_days':
                        db_data = self.query_get_devices_Indiana_for_last_30_days()
                    elif time_period == 'This_year':
                        db_data = self.query_get_devices_Indiana_this_year()
                    elif time_period == 'Last_year':
                        db_data = self.query_get_devices_Indiana_last_year()

                else:
                    # Остальные периоды без изменений
                    db_data = self.query_get_devices_Indiana_for_periods(time_period)

                if not db_data:
                    print(f"No data retrieved from SQL query for {time_period}.")
                    continue

                # Продолжение обработки данных для сравнения, вывода и т.д.
                matched_count = self.compare_device_data(website_data, db_data, time_period)

                # Вывод информации о совпадениях
                print(f"Period '{time_period}':")
                print(f"Total devices from SQL query: {len(db_data)}")

                if matched_count == len(db_data):
                    print("All devices from SQL query matched with devices from the web page for this period.")
                else:
                    print("Tying to compare data from db and web site...")

    def aggregate_results(self, results):
        aggregated_data = defaultdict(lambda: {'ServiceMinutes': 0, 'NumberOfServices': 0})
        for row in results:
            ios_serial = row['IOSSerialNumber']
            service_minutes = row['ServiceMinutes']
            number_of_services = row['NumberOfServices']
            aggregated_data[ios_serial]['ServiceMinutes'] += service_minutes
            aggregated_data[ios_serial]['NumberOfServices'] += number_of_services
        return aggregated_data

    def fetch_column_data(self, column_index):
        # Ожидание загрузки всех строк таблицы
        rows = WebDriverWait(self.driver, 300).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
        )

        # Извлечение данных из указанного столбца каждой строки
        column_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > column_index:
                column_data.append(cells[column_index].text.replace(',', ''))
            else:
                print(f"Not enough cells in the row to extract data: {row.text}")
        return column_data

    def is_sorted_ascending_str(self, column_data):
        # Убираем пустые строки и специальные случаи
        column_data_filtered = [x for x in column_data if x and "AscensionIndiana" in x]
        # Проверяем, что каждый элемент меньше или равен следующему
        return column_data_filtered == sorted(column_data_filtered)

    def is_sorted_descending_str(self, column_data):
        # Убираем пустые строки и специальные случаи
        column_data_filtered = [x for x in column_data if x and "AscensionIndiana" in x]
        # Проверяем, что каждый элемент больше или равен следующему
        return column_data_filtered == sorted(column_data_filtered, reverse=True)

    def is_sorted_ascending_serial(self, column_data):
        # Убираем пустые строки
        column_data_filtered = [x for x in column_data if x]
        # Извлекаем первую букву каждой строки для сравнения
        first_letters = [x[0] for x in column_data_filtered]
        # Проверяем, что каждый элемент меньше или равен следующему
        return first_letters == sorted(first_letters)

    def is_sorted_descending_serial(self, column_data):
        # Убираем пустые строки
        column_data_filtered = [x for x in column_data if x]
        # Извлекаем первую букву каждой строки для сравнения
        first_letters = [x[0] for x in column_data_filtered]
        # Проверяем, что каждый элемент больше или равен следующему
        return first_letters == sorted(first_letters, reverse=True)

    def is_sorted_ascending(self, column_data):
        # Отфильтровываем пустые строки и преобразуем остальные в числа
        column_data_int = [int(x) for x in column_data if x]

        # Проверяем, отсортированы ли значения по возрастанию
        return column_data_int == sorted(column_data_int)

    def is_sorted_descending(self, column_data):
        # Отфильтровываем пустые строки и преобразуем остальные в числа
        column_data_int = [int(x) for x in column_data if x]

        # Проверяем, отсортированы ли значения по убыванию
        return column_data_int == sorted(column_data_int, reverse=True)

    def read_csv_device_usage_data(self, file_path):
        print(f"Reading Excel data from: {file_path}")  # Добавлено для отладки
        df = pd.read_excel(file_path)  # Не пропускаем строки

        # Определяем названия полей, которые соответствуют столбцам в Excel файле
        fieldnames = [
            'Device Name', 'Serial Number', 'Mac Address',
            'Minutes Used', 'Device Owner', 'Number of Transactions'
        ]

        # Приведение названий столбцов к стандартному формату
        df.columns = [col.strip() for col in df.columns]

        data = []
        for index, row in df.iterrows():
            clean_row = {
                fieldnames[i].replace(' ', '').lower(): str(row[fieldnames[i]]).strip() if pd.notna(
                    row[fieldnames[i]]) else None
                for i in range(len(fieldnames))
            }
            print(f"Row data: {clean_row}")  # Вывод каждой строки для отладки
            data.append(clean_row)

        return data

    def assert_nums(self, actual_text, expected_text):
        # Преобразование чисел в строки
        actual_text_str = str(actual_text)
        expected_text_str = str(expected_text)

        # Проверка, что обе строки достаточно длинные для сравнения
        if len(actual_text_str) > 1 and len(expected_text_str) > 1:
            # Исключение последнего символа из каждой строки
            actual_text_trimmed = actual_text_str[:-1]
            expected_text_trimmed = expected_text_str[:-1]

            # Сравнение обрезанных строк
            assert actual_text_trimmed == expected_text_trimmed, f"Actual text: '{actual_text_trimmed}', Expected text: '{expected_text_trimmed}'"
        else:
            # Если строки слишком короткие для сравнения, используем исходное сравнение
            assert actual_text_str == expected_text_str, f"Actual text: '{actual_text_str}', Expected text: '{expected_text_str}'"

    def compare_device_usage_data(self, web_data_list, csv_data_list):
        print("Starting comparison...")  # For debugging
        data_is_correct = True

        for web_data in web_data_list:
            serial_number = web_data['serialnumber'].strip()

            # Skip iteration if serial_number is empty
            if not serial_number:
                print("Serial number is missing in web data:", web_data)
                continue

            matching_csv_data = next((item for item in csv_data_list if item['serialnumber'].strip() == serial_number),
                                     None)

            if not matching_csv_data:
                print(f"Serial number {serial_number} not found in CSV")
                data_is_correct = False
                continue

            # Data comparison
            for key in web_data:
                web_value = web_data[key] if web_data[key] else 'None'
                csv_value = matching_csv_data[key] if matching_csv_data[key] else 'None'

                # Treat 'None' and 'undefined' as equal
                if (csv_value in ['None', 'undefined'] and web_value in ['None', 'undefined']):
                    continue

                # Convert strings containing numbers for comparison
                try:
                    web_numeric_value = float(web_value.replace(',', ''))
                    csv_numeric_value = float(csv_value.replace(',', ''))

                    if web_numeric_value != csv_numeric_value:
                        print(f"Mismatch for {key} with serial number: {serial_number}")
                        print(f"CSV value: '{csv_value}' vs Web value: '{web_value}'")
                        data_is_correct = False
                except ValueError:
                    # If conversion to float fails, fall back to string comparison
                    if web_value != csv_value:
                        print(f"Mismatch for {key} with serial number: {serial_number}")
                        print(f"CSV value: '{csv_value}' vs Web value: '{web_value}'")
                        data_is_correct = False

        # Check if all data was correct
        if data_is_correct:
            print("Downloaded data is correct")

        return data_is_correct

    def device_usage_page(self):
        with allure.step("Device usage page CHECK"):
            Logger.add_start_step(method='Device usage page CHECK')
            self.driver.maximize_window()

            self.click_drop_down()
            self.click_du()
            # self.get_current_url()
            # time.sleep(5)
            # self.click_n_of_t()
            # time.sleep(1)
            # self.click_n_of_t()
            # self.click_completed_calls_check()
            # time.sleep(10)
            # rows = self.driver.find_elements(By.XPATH, "//tbody[@class='ant-table-tbody']/tr")
            # rows_count = len(rows) - 1
            # print(rows_count)
            # self.click_drop_down()
            # self.click_du()
            # self.click_n_of_t()
            # time.sleep(1)
            # self.click_n_of_t()
            # cc = int(self.get_completed_calls_check().text)
            # print(cc)
            # self.assert_nums(cc, rows_count)
            # time.sleep(10)
            # self.screenshot()
            # time.sleep(10)
            # self.compare_devices_data()
            file_path = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/customer_pages/Kanji_devices"
            # self.compare_devices(file_path)
            # self.compare_devices_with_web(file_path)
            # time.sleep(10)
            # self.execute_comparison()
            self.execute_period_comparison()
            self.driver.refresh()
            time.sleep(30)
            self.click_dev_name_filter()
            time.sleep(5)  # Ждем, пока таблица обновится после сортировки

            # Получаем данные после первой сортировки
            device_name_data = self.fetch_column_data(column_index=0)  # 0 - индекс столбца "Device Name"
            print("Data after first sort:", device_name_data)
            assert self.is_sorted_ascending_str(device_name_data), "Data is not sorted ascending."

            # Нажимаем на фильтр второй раз для сортировки в обратном порядке
            self.click_dev_name_filter()
            time.sleep(5)  # Ждем, пока таблица обновится после сортировки

            # Получаем данные после второй сортировки
            device_name_data_desc = self.fetch_column_data(column_index=0)
            print("Data after second sort:", device_name_data_desc)
            assert self.is_sorted_descending_str(device_name_data_desc), "Data is not sorted descending."

            self.click_ser_nub_f()
            device_name_data = self.fetch_column_data(column_index=1)  # 0 - индекс столбца "Device Name"
            print("Data after first sort:", device_name_data)
            assert self.is_sorted_ascending_serial(device_name_data), "Data is not sorted ascending."

            # Нажимаем на фильтр второй раз для сортировки в обратном порядке
            self.click_ser_nub_f()
            time.sleep(1)  # Ждем, пока таблица обновится после сортировки

            # Получаем данные после второй сортировки
            device_name_data_desc = self.fetch_column_data(column_index=1)
            print("Data after second sort:", device_name_data_desc)
            assert self.is_sorted_descending_serial(device_name_data_desc), "Data is not sorted descending."

            self.click_min_u()
            time.sleep(1)  # Ждем, пока таблица обновится после сортировки

            # Получаем данные после первой сортировки
            device_name_data = self.fetch_column_data(column_index=3)  # 0 - индекс столбца "Device Name"
            print("Data after first sort:", device_name_data)
            assert self.is_sorted_ascending(device_name_data), "Data is not sorted ascending."

            # Нажимаем на фильтр второй раз для сортировки в обратном порядке
            self.click_min_u()
            time.sleep(1)  # Ждем, пока таблица обновится после сортировки

            # Получаем данные после второй сортировки
            device_name_data_desc = self.fetch_column_data(column_index=3)
            print("Data after second sort:", device_name_data_desc)
            assert self.is_sorted_descending(device_name_data_desc), "Data is not sorted descending."

            self.click_n_of_t()
            time.sleep(1)  # Ждем, пока таблица обновится после сортировки

            # Получаем данные после первой сортировки
            device_name_data = self.fetch_column_data(column_index=5)  # 0 - индекс столбца "Device Name"
            print("Data after first sort:", device_name_data)
            assert self.is_sorted_ascending(device_name_data), "Data is not sorted ascending."

            # Нажимаем на фильтр второй раз для сортировки в обратном порядке
            self.click_n_of_t()
            time.sleep(1)  # Ждем, пока таблица обновится после сортировки

            # Получаем данные после второй сортировки
            device_name_data_desc = self.fetch_column_data(column_index=5)
            print("Data after second sort:", device_name_data_desc)
            assert self.is_sorted_descending(device_name_data_desc), "Data is not sorted descending."
            self.click_list()
            self.click_last_week()
            self.click_dev_n_s()
            self.input_dev_name('AscensionIndiana 001')
            time.sleep(10)
            self.press_return_key()
            self.assert_word(self.get_dev_name_assert(), 'AscensionIndiana 001')
            self.driver.refresh()
            time.sleep(15)
            self.click_list()
            time.sleep(2)
            self.click_last_week()
            time.sleep(2)
            self.click_ser_nub_s()
            self.input_ser_num('KW97RYQF17')
            self.press_return_key()
            self.assert_word(self.get_serial_assert_f(), 'KW97RYQF17')
            self.driver.refresh()
            time.sleep(3)
            self.click_list()
            time.sleep(2)
            self.click_last_week()
            time.sleep(2)
            self.click_mac_s()
            self.input_mac('2c:32:6a:67:06:ee')
            self.press_return_key()
            self.assert_word(self.get_mac_assert_f(), '2c:32:6a:67:06:ee')
            self.driver.refresh()
            time.sleep(3)
            self.click_download_b()
            time.sleep(10)
            download_folder = "/Users/nikitabarshchuk/Downloads"
            target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
            file_pattern = "Device_Usage_Report*.xlsx"

            moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)
            time.sleep(60)

            if moved_file_path:
                time.sleep(30)
                csv_data = self.read_csv_device_usage_data(moved_file_path)
                website_data = self.fetch_website_data_for_devices1()
                assert self.compare_device_usage_data(website_data, csv_data_list=csv_data), "Data mismatch found."
