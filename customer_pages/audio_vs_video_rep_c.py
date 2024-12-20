import math
import os
import glob
import csv
import pandas as pd
import shutil
import time
import allure
import threading
from selenium.webdriver.chrome.service import Service
from selenium.common import TimeoutException
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


class Audio_vs_video_report(Graphs, Database, EV):
    def __init__(self, driver, elements=None):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver
        # Инициализация elements как списка, если он не предоставлен
        self.elements = elements if elements is not None else []

    def __getitem__(self, index):
        # Убедитесь, что self.elements определен и доступен
        if hasattr(self, 'elements') and self.elements is not None:
            return self.elements[index]
        else:
            raise AttributeError("The 'elements' attribute is not initialized or is set to None.")


    # Locators
    last_pages = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/ul/li[8]'
    ten_tr_per_page = "//div[contains(@class, 'ant-select-item-option-content') and contains(text(), '10 / page')]"
    pages = "//span[@class='ant-select-selection-item' and text()='100 / page']"
    completed_calls_check = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[8]/a'
    dropdown_list = '//*[@id="root"]/section/aside/div/ul/li[4]/div'
    language_report_b = "//a[@href='/pages/reports/audio-report']"
    download_b = "//*[@id='root']/section/section/main/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/button"
    all_clients = '//*[@id="header-container-id"]/div/div[6]/div/div/span[2]'
    choose_company = '//div[@class="ant-select-item-option-content" and text()="46700"]'
    Today_list = '//*[@id="header-container-id"]/div/div[5]/div/div/span[2]'
    yesterday = "//div[contains(@class, 'ant-select-item-option-content') and contains(text(), 'Yesterday')]"
    Custom = "//div[contains(@class, 'ant-select-item-option-content') and text()='Custom Date']"
    last_week = "//div[@title='Last Week']"
    this_week = "//div[@title='This Week']"
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
    last_month = '//div[@title="Last Month"]'
    last_30_days = '//div[@title="Last 30 Days"]'
    this_year = '//div[@title="This Year"]'
    last_year = '//div[@title="Last Year"]'
    lang_field = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]'
    element_xpath = "//*[@id='root']/section/section/main/div/div/div[2]/div/div/div/div/div/div[1]/div/div[1]/div/div/span[2]"
    additional_xpath = '//*[@id="root"]/section/aside/div/ul'

    # Getters
    def get_pages(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.pages)))
    def get_avg_call_length(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.minutes_by_v)))

    def get_lang_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_field)))

    def get_Last_month(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.last_month)))

    def get_Last_30_days(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.last_30_days)))

    def get_This_year(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.this_year)))

    def get_Last_year(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.last_year)))

    def get_This_month(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.this_month)))

    def get_This_week(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.this_week)))

    def get_completed_calls(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.completed_calls)))

    def get_download_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.download_b)))

    def get_all_clients(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.all_clients)))

    def get_choose_company(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.choose_company)))

    def get_Yesterday(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.yesterday)))

    def get_Today_list(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Today_list)))

    def get_Custom(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Custom)))

    def get_Last_week(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.last_week)))

    def get_start_date(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.start_date)))

    def get_end_date(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.end_date)))

    def get_no_data(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.no_data)))

    def get_lang_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_f)))

    def get_lang_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_s_f)))

    def get_lang_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_s)))

    def get_completed_calls_check(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.completed_calls_check)))

    def get_last_pages(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.last_pages)))

    def get_total_calls(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.total_calls)))

    def get_total_minutes(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.total_minutes)))

    def get_ser_audio_c(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ser_audio_c)))
    def get_ten_tr_per_page(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ten_tr_per_page)))

    def get_ser_video_c(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ser_video_c)))

    def get_avg_rating(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.avg_rating)))

    def get_avg_wait_time(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.minutes_by_a)))

    def get_drop_download(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.drop_download)))

    def get_dropdown_list(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.dropdown_list)))

    def get_language_report_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.language_report_b)))

    def get_pdf(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.pdf)))

        # Actions

    def click_last_pages(self):
        self.get_last_pages().click()
        print("CLICK last pages")
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

    def click_lr(self):
        self.get_language_report_b().click()
        print("CLICK info")

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

    def click_yesterday(self):
        self.get_Yesterday().click()
        print("CLICK yesterday")

    def click_last_week(self):
        self.get_Last_week().click()
        print("CLICK last week")

    def click_this_month(self):
        self.get_This_month().click()
        print("CLICK This month")

    def click_last_month(self):
        self.get_Last_month().click()
        print("CLICK Last month")

    def click_last_30_days(self):
        self.get_Last_30_days().click()
        print("CLICK Last 30 days")

    def press_return_key(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем нажатие на клавишу Return
        actions.send_keys(Keys.RETURN).perform()

        print("Pressed the Return key")
    def click_ten_tr_per_page(self):
        self.get_ten_tr_per_page().click()
        print("CLICK ten_tr_per_page")
    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolling to the bottom of the page is performed")

    def double_press_down_arrow(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем двойное нажатие на стрелку вверх
        actions.send_keys(Keys.ARROW_DOWN).perform()  # второе нажатие

        print("Pressed the Down arrow key")

    def click_this_year(self):
        self.get_This_year().click()
        print("CLICK This year")

    def input_lang_sf(self, language):
        self.get_lang_s_f().send_keys(language)
        print("Input language")

    def click_pages(self):
        self.get_pages().click()
        print("CLICK pages")

    def click_completed_calls_check(self):
        self.get_completed_calls_check().click()
        print("CLICK completed_calls_check")

    def click_total_c(self):
        first_company = self.get_total_calls()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Total calls filter")

    def click_lang_s(self):
        first_company = self.get_lang_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK language search")

    def click_last_year(self):
        self.get_Last_year().click()
        print("CLICK Last year")

    def click_this_week(self):
        self.get_This_week().click()
        print("CLICK This week")

    def click_lang_f(self):
        first_company = self.get_lang_f()
        self.driver.execute_script("arguments[0].click();", first_company)
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

    def compare_language_lists(self, list_from_db, list_from_web):
        # Сравнение двух списков языков
        if list_from_db == list_from_web:
            print("Languages is good.")
        else:
            error_message = "Filter is not working.\nРазличия:\n"
            discrepancies_found = False

            for db_lang, web_lang in zip(list_from_db, list_from_web):
                if db_lang != web_lang:
                    discrepancies_found = True
                    error_message += f"DB: {db_lang}, web: {web_lang} \ n"

            if discrepancies_found:
                raise Exception(error_message)

    def audio_vs_video_rep(self):
        with allure.step("Audio vs Video Report"):
            Logger.add_start_step(method='Audio vs Video Report')
            self.driver.maximize_window()

            self.click_drop_down()
            time.sleep(10)
            self.click_drop_down()
            self.click_lr()
            self.get_current_url()
            time.sleep(3)
            self.screenshot()
            time.sleep(3)
            # self.click_completed_calls_check()
            # time.sleep(10)
            # self.scroll_to_bottom()
            # time.sleep(4)
            # self.click_pages()
            # time.sleep(3)
            # self.click_ten_tr_per_page()
            # time.sleep(10)
            # self.click_last_pages()
            # time.sleep(10)
            # transactions_per_page = 10
            # last_page_text = self.get_last_pages().text
            # if last_page_text.isdigit():
            #     last_page_number = int(last_page_text)
            #
            #     # Вычитаем 1 из номера последней страницы и умножаем на количество транзакций на странице
            #     total_pages = math.ceil(last_page_number - 1) * transactions_per_page
            #
            #     # Получаем количество строк на текущей странице
            #     rows = self.driver.find_elements(By.XPATH, "//div[@class='ant-table-container']//table/tbody/tr")
            #     rows_count = len(rows) - 1
            #
            #     # Добавляем количество строк к общему числу страниц
            #     total_pages += rows_count
            #
            # self.click_drop_down()
            # time.sleep(10)
            # self.click_drop_down()
            # self.click_lr()
            # cc = int(self.get_completed_calls_check().text)
            # self.assert_word(cc, total_pages) #TODO BUG
            self.get_current_url()
            time.sleep(3)

            sorted_api_data = self.language_report_test_today()  # Сохранение возвращаемых данных
            self.compare_avsv_rep(sorted_api_data)
            self.click_download_b()
            time.sleep(10)
            download_folder = "/Users/nikitabarshchuk/Downloads"
            target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
            file_pattern = "Audio_Video_Report*.xlsx"

            moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)

            if moved_file_path:
                csv_data = self.read_excel_data(moved_file_path)
                website_data = self.fetch_website_data12()
                self.compare_data12(website_data, csv_data)
            self.click_lang_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            lang_data = self.fetch_column_data_total_calls(column_index=0)
            print("Data after first sort:", lang_data)
            assert self.is_sorted_ascending_l(lang_data), "Data is not sorted ascending."

            self.click_lang_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            lang_data = self.fetch_column_data_total_calls(column_index=0)
            print("Data after second sort:", lang_data)
            assert self.is_sorted_descending_l(lang_data), "Data is not sorted descending."
            self.click_lang_f()
            time.sleep(3)
            self.click_all_clients()
            self.click_choose_company()
            time.sleep(10)
            self.compare_data1234()
            self.click_download_b()
            time.sleep(10)
            download_folder = "/Users/nikitabarshchuk/Downloads"
            target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
            file_pattern = "Audio_Video_Report*.xlsx"

            moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)

            if moved_file_path:
                csv_data = self.read_excel_data(moved_file_path)
                website_data = self.fetch_website_data12()
                self.compare_data12(website_data, csv_data)
            self.compare_data_for_periods()
            self.driver.refresh()
            time.sleep(20)
            self.click_lang_s()
            self.input_lang_sf(' spanish ')  ###TODO должна быть проверка на пробелы до и после названия языка
            self.press_return_key()
            self.assert_word(self.get_lang_field(), "Spanish")
            self.driver.refresh()
            time.sleep(20)
            self.click_lang_f()
            time.sleep(5)

            # Проверяем сортировку по возрастанию
            self.click_total_c()
            time.sleep(5)  # Нажимаем на кнопку сортировки
            new_total_calls_data = self.fetch_column_data_total_calls(column_index=1)
            print("Data after first sort:", new_total_calls_data)
            assert self.is_sorted_ascending(new_total_calls_data), "Data is not sorted ascending."

            # Проверяем сортировку по убыванию
            self.click_total_c()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            new_total_calls_data = self.fetch_column_data_total_calls(column_index=1)
            print("Data after second sort:", new_total_calls_data)
            assert self.is_sorted_descending(new_total_calls_data), "Data is not sorted descending."

            # Проверяем сортировку по возрастанию
            self.click_total_minutes()
            time.sleep(1)  # Нажимаем на кнопку сортировки ###
            new_total_minutes_data = self.fetch_column_data_total_calls(column_index=2)
            print("Data after first sort (Total Minutes):", new_total_minutes_data)
            assert self.is_sorted_ascending(new_total_minutes_data), "Total Minutes data is not sorted ascending."

            self.click_total_minutes()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            new_total_minutes_data = self.fetch_column_data_total_calls(column_index=2)
            print("Data after second sort (Total Minutes):", new_total_minutes_data)
            assert self.is_sorted_descending(new_total_minutes_data), "Total Minutes data is not sorted descending."

            self.click_ser_audio_c()
            time.sleep(2)  # Нажимаем на кнопку сортировки
            new_serviced_audio_calls_data = self.fetch_column_data_total_calls(column_index=3)
            print("Data after first sort (Serviced audio calls):", new_serviced_audio_calls_data)
            assert self.is_sorted_ascending(
                new_serviced_audio_calls_data), "Serviced audio calls data is not sorted ascending."

            self.click_ser_audio_c()
            time.sleep(2)  # Нажимаем на кнопку сортировки еще раз
            new_serviced_audio_calls_data = self.fetch_column_data_total_calls(column_index=3)
            print("Data after second sort (Serviced audio calls):", new_serviced_audio_calls_data)
            assert self.is_sorted_descending(
                new_serviced_audio_calls_data), "Serviced audio calls data is not sorted descending."

            self.click_ser_video_c()
            time.sleep(2)  # Нажимаем на кнопку сортировки
            new_serviced_video_calls_data = self.fetch_column_data_total_calls(column_index=4)
            print("Data after first sort (Serviced video calls):", new_serviced_video_calls_data)
            assert self.is_sorted_ascending(
                new_serviced_video_calls_data), "Serviced video calls data is not sorted ascending."

            self.click_ser_video_c()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            new_serviced_video_calls_data = self.fetch_column_data_total_calls(column_index=4)
            print("Data after second sort (Serviced video calls):", new_serviced_video_calls_data)
            assert self.is_sorted_descending(
                new_serviced_video_calls_data), "Serviced video calls data is not sorted descending."

            # Проверка сортировки для "Average Wait Time"
            self.click_avg_wait_time()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            avg_wait_time_data = self.fetch_column_data_total_calls(column_index=5)
            print("Data after first sort (Average Wait Time):", avg_wait_time_data)
            assert self.is_sorted_ascending1(avg_wait_time_data), "Average Wait Time data is not sorted ascending."

            self.click_avg_wait_time()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            avg_wait_time_data = self.fetch_column_data_total_calls(column_index=5)
            print("Data after second sort (Average Wait Time):", avg_wait_time_data)
            assert self.is_sorted_descending1(avg_wait_time_data), "Average Wait Time data is not sorted ascending."

            # Проверка сортировки для "Average Call Length"
            self.click_avg_call_length()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            avg_call_length_data = self.fetch_column_data_total_calls(column_index=6)
            print("Data after first sort (Average Call Length):", avg_call_length_data)
            assert self.is_sorted_ascending1(avg_call_length_data), "Average Call Length data is not sorted ascending."

            self.click_avg_call_length()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            avg_call_length_data = self.fetch_column_data_total_calls(column_index=6)
            print("Data after second sort (Average Call Length):", avg_call_length_data)
            assert self.is_sorted_descending1(
                avg_call_length_data), "Average Call Length data is not sorted descending."

            # Проверка сортировки для "Rating"

            self.check_color_change(self.element_xpath, self.additional_xpath)
            self.driver.refresh()

    def check_color_change(self, element_xpath, additional_xpath):
        with allure.step("Change Color"):
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, element_xpath)))
            additional_element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, additional_xpath)))
            old_color = element.value_of_css_property('background-color')
            additional_old_color = additional_element.value_of_css_property('background-color')

            # Кликаем, чтобы сменить тему
            self.click_light()

            # Проверка изменения цвета для обоих элементов
            WebDriverWait(self.driver, 30).until_not(
                lambda d: element.value_of_css_property('background-color') == old_color and
                          additional_element.value_of_css_property('background-color') == additional_old_color)

            # Вывод результатов
            new_color = element.value_of_css_property('background-color')
            additional_new_color = additional_element.value_of_css_property('background-color')
            print(f"Main element color changed from {old_color} to {new_color}")
            print(f"Additional element color changed from {additional_old_color} to {additional_new_color}")

    def click_light(self):
        # Предположим, что переключатель темы имеет id 'theme-toggle'
        theme_toggle_xpath = "//span[text()='Light']"
        theme_toggle = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, theme_toggle_xpath)))
        theme_toggle.click()
        print("Theme changed to light.")

    # @staticmethod
    # def run_with_timeout(func, args=(), timeout=300):
    #     result = [None]  # Обёртка для результата, чтобы можно было изменить внутри функции
    #     exception = [None]  # Обёртка для исключений
    #
    #     def target():
    #         try:
    #             result[0] = func(*args)  # Попытка выполнить функцию
    #         except Exception as e:
    #             exception[0] = e
    #
    #     thread = threading.Thread(target=target)
    #     thread.start()
    #
    #     thread.join(timeout)  # Ожидаем выполнения потока до истечения таймаута
    #
    #     if thread.is_alive():
    #         print(f"Terminating due to timeout: {timeout} seconds.")
    #         thread.join()  # В некоторых случаях вы можете попробовать thread.terminate() или подобные методы в зависимости от реализации
    #         raise TimeoutError(f"Function exceeded the maximum timeout of {timeout} seconds.")
    #
    #     if exception[0]:
    #         raise exception[0]  # Если было исключение, поднимаем его
    #
    #     return result[0]  # Возвращаем результат функции

    def compare_data_for_period1(self, website_data, time_period):
        languages = self.query_lang_rep1()  # Получение списка языков
        discrepancies = []  # Инициализация переменной здесь

        for lang in languages:
            language_name = lang[0]
            try:
                db_data = self.query_language_stats_CHH1(language_name, time_period)
            except Exception as e:
                print(f"An error occurred while executing the query for {language_name}: {e}")
                continue

            if db_data:
                for row in db_data:
                    # Инициализация списка расхождений перед проверкой условий
                    discrepancies = []
                    web_rows = [item for item in website_data if item["LanguageName"] == language_name]

                    if web_rows:
                        print(f"Comparing data for language: {language_name}")

                        # Инициализация и вычисление общих значений для веб-данных
                        total_calls_web = sum(int(item["TotalCalls"]) for item in web_rows)
                        total_minutes_web = sum(int(item["TotalMinutes"]) for item in web_rows)
                        serviced_audio_calls_web = sum(int(item["CallsbyAudio"]) for item in web_rows)
                        serviced_video_calls_web = sum(int(item["CallsbyVideo"]) for item in web_rows)
                        minutes_by_audio_web = sum(
                            int(item["MinutesbyAudio"].replace(' minutes', '')) for item in web_rows)
                        minutes_by_video_web = sum(
                            int(item["MinutesbyVideo"].replace(' minutes', '')) for item in web_rows)

                        # Обработка случая с None
                        db_total_calls = 0 if row.TotalCalls is None else row.TotalCalls
                        db_total_minutes = 0 if row.ServiceMinutes is None else row.ServiceMinutes
                        db_serviced_audio_calls = 0 if row.CountSuccessAudioCalls is None else row.CountSuccessAudioCalls
                        db_serviced_video_calls = 0 if row.CountSuccessVideoCalls is None else row.CountSuccessVideoCalls
                        db_count_video_minute = 0 if row.CountVideoMinute is None else row.CountVideoMinute
                        db_count_audio_minute = 0 if row.CountAudioMinute is None else row.CountAudioMinute

                        # Сравнение значений
                        if str(db_total_calls) != str(total_calls_web):
                            discrepancies.append(f"Total Calls: DB({db_total_calls}) != Web({total_calls_web})")
                        if str(db_total_minutes) != str(total_minutes_web):
                            discrepancies.append(f"Total Minutes: DB({db_total_minutes}) != Web({total_minutes_web})")
                        if str(db_serviced_audio_calls) != str(serviced_audio_calls_web):
                            discrepancies.append(
                                f"Serviced Audio Calls: DB({db_serviced_audio_calls}) != Web({serviced_audio_calls_web})")
                        if str(db_serviced_video_calls) != str(serviced_video_calls_web):
                            discrepancies.append(
                                f"Serviced Video Calls: DB({db_serviced_video_calls}) != Web({serviced_video_calls_web})")
                        if str(db_count_audio_minute) != str(minutes_by_audio_web):
                            discrepancies.append(
                                f"CountAudioMinute: DB({db_count_audio_minute}) != Web({minutes_by_audio_web})")
                        if str(db_count_video_minute) != str(minutes_by_video_web):
                            discrepancies.append(
                                f"CountVideoMinute: DB({db_count_video_minute}) != Web({minutes_by_video_web})")

                        # Вывод результатов сравнения
                        if discrepancies:
                            discrepancy_messages = "\n".join(discrepancies)
                            print(f"Discrepancies found for language {language_name}:\n{discrepancy_messages}")
                        else:
                            print("No discrepancies found for this language.")

        return bool(discrepancies)
#
    def select_time_period_and_wait_for_update(self, time_period, open_list=True):
        if open_list:
            self.click_list()
        time.sleep(3)
        self.double_press_down_arrow()
        time.sleep(10)  # Короткая задержка, чтобы убедиться, что список открыт
        getattr(self, f"click_{time_period}")()
        time.sleep(60)
        self.click_download_b()
        time.sleep(30)
        download_folder = "/Users/nikitabarshchuk/Downloads"
        target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
        file_pattern = "Audio_Video_Report*.xlsx"

        moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)

        if moved_file_path:
            csv_data = self.read_excel_data(moved_file_path)
            website_data = self.fetch_website_data12()
            self.compare_data12(website_data, csv_data)
        # Ожидание обновления данных

    def compare_data_for_periods(self):
        with allure.step("Compare data with DB by Periods"):

            languages = self.query_lang_rep1()
            time_periods = ['last_30_days', 'yesterday', 'this_week', 'this_month', 'last_week', 'last_month', 'this_year', 'last_year']
            should_continue = True  # Флаг для контроля продолжения цикла

            for lang in languages:
                if not should_continue:  # Проверяем, должен ли цикл продолжаться
                    break

                language_name = lang[0]
                for period in time_periods:
                    if not self.take_data_for_period(period, language_name):
                        print(f"Discrepancies found for language {language_name} and period '{period}'.")
                    if period == 'last_year':
                        should_continue = False  # Установка флага в False после обработки 'Last_year'
                        break

    def take_data_for_period(self, time_period, language_name):
        if time_period == 'last_year':
            # Открываем список и нажимаем стрелку вниз, только если период - Last_year
            self.click_list()
            self.double_press_down_arrow()
            self.select_time_period_and_wait_for_update(time_period, open_list=False)
            time.sleep(30)
        elif time_period == 'this_year':
            # Открываем список и нажимаем стрелку вниз, только если период - Last_year
            self.select_time_period_and_wait_for_update(time_period)
            time.sleep(30)
        else:
            # В других случаях просто выбираем период и ждём обновления
            self.select_time_period_and_wait_for_update(time_period)

        website_data = self.fetch_website_data12()  # Получение данных с сайта для нового периода

        db_data = self.query_language_stats_CHH1(language_name, time_period)
        if not db_data:
            print(f"No database data found for language {language_name} and period '{time_period}'")
            return False

        return self.compare_data_for_period1(website_data, time_period)

    def read_excel_data(self, file_path):
        def format_value(value):
            if pd.isna(value) or value in ['invalid date', 'None', '-', '']:
                return None
            if isinstance(value, str):
                return value.strip().lower()
            return str(value).lower()

        df = pd.read_excel(file_path)
        formatted_data = []

        for index, row in df.iterrows():
            processed_row = {key: format_value(value) for key, value in row.items()}
            formatted_data.append(processed_row)

        return formatted_data

    def compare_data12(self, web_data_list, csv_data_list):
        with allure.step("Compare downloaded data with Web data"):
            if csv_data_list is None:
                print("Error: CSV data list is None")
                return False

            # Приведение языковых названий к верхнему регистру для сравнения
            csv_languages = {self.format_string(item['Language Name']): item for item in csv_data_list}
            web_languages = {self.format_string(data['LanguageName']): data for data in web_data_list if
                             data['LanguageName'].strip()}

            print("Languages ​​in CSV:", list(csv_languages.keys()))
            print("Languages ​​on the site:", list(web_languages.keys()))

            data_is_correct = True  # Флаг, отслеживающий корректность данных

            for language_name, web_data in web_languages.items():
                matching_csv_data = csv_languages.get(language_name, None)
                if matching_csv_data:
                    if not self.compare_records(matching_csv_data, web_data):
                        print(f"Data mismatch for language: {web_data['LanguageName']}")
                        data_is_correct = False  # Обнаружено несоответствие данных
                else:
                    print(f"No matching data found in CSV for language: {web_data['LanguageName']}")
                    data_is_correct = False  # Обнаружено несоответствие данных

            if data_is_correct:
                print("Downloaded data is correct")  # Все данные совпадают

            return data_is_correct

    def format_number(self, number_str):
        if number_str is None:
            return 0
        return float(number_str.replace(',', '').strip())

    def format_string(self, string):
        if string is None:
            return ''
        return string.strip().upper()

    def compare_records(self, csv_record, web_record):
        keys_to_compare = ['Total Calls', 'Total Minutes', 'Calls by Audio', 'Calls by Video']
        is_match = True
        for key in keys_to_compare:
            web_key = key.replace(' ', '')
            csv_value = self.format_number(csv_record.get(key, '0'))
            web_value = self.format_number(web_record.get(web_key, '0'))
            if round(csv_value, 2) != round(web_value, 2):
                print(f"Mismatch in {key}: CSV - {csv_value}, Web - {web_value}")
                is_match = False
            else:
                print(f"Match found for {key}: CSV - {csv_value}, Web - {web_value}")
        return is_match

    def move_latest_file(self, download_folder, target_folder, file_pattern):
        try:
            if not os.path.exists(download_folder):
                print(f"The download folder does not exist: {download_folder}")
                return None
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)  # Создаём целевую папку, если она не существует

            files = glob.glob(os.path.join(download_folder, file_pattern))
            if not files:
                print(f"Files with a template {File_pattern} were not found in the folder {download_folder}")
                return None

            latest_file = max(files, key=os.path.getctime)
            target_file = os.path.join(target_folder, os.path.basename(latest_file))

            shutil.move(latest_file, target_file)
            print(f"The file {Latest_file} was moved to {target_file}")
            return target_file
        except Exception as e:
            print(f"Error when moving the file: {e}")
            return None

    def fetch_column_data_total_calls(self, column_index):
        rows = WebDriverWait(self.driver, 300).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
        )

        column_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > column_index:
                column_data.append(cells[column_index].text.replace(',', ''))
            else:
                print(f"Not enough cells in the row to extract data: {row.text}")
        return column_data

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

    def is_sorted_ascending1(self, column_data):
        # Убираем все нечисловые символы и преобразуем строки в целые числа
        column_data_int = []
        for data in column_data:
            # Извлекаем только числовую часть строки
            number = ''.join(filter(str.isdigit, data))
            # Если строка не пустая, преобразуем в число и добавляем в список
            if number:
                column_data_int.append(int(number))

        # Проверяем, что каждый элемент меньше или равен следующему
        return all(column_data_int[i] <= column_data_int[i + 1] for i in range(len(column_data_int) - 1))

    def is_sorted_descending1(self, column_data):
        # Убираем все нечисловые символы и преобразуем строки в целые числа
        column_data_int = []
        for data in column_data:
            # Извлекаем только числовую часть строки
            number = ''.join(filter(str.isdigit, data))
            # Если строка не пустая, преобразуем в число и добавляем в список
            if number:
                column_data_int.append(int(number))

        # Проверяем, что каждый элемент больше или равен следующему
        return all(column_data_int[i] >= column_data_int[i + 1] for i in range(len(column_data_int) - 1))

    def is_sorted_ascending_l(self, column_data):
        # Убеждаемся, что значения не пустые
        filtered_data = [x for x in column_data if x]

        # Проверяем, отсортированы ли значения по возрастанию
        return filtered_data == sorted(filtered_data)

    def is_sorted_descending_l(self, column_data):
        # Убеждаемся, что значения не пустые
        filtered_data = [x for x in column_data if x]

        # Проверяем, отсортированы ли значения по убыванию
        return filtered_data == sorted(filtered_data, reverse=True)
