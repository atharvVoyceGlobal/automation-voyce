import os
import glob
import csv
import pandas as pd
import shutil
import logging
import time
import io
import allure
from collections import defaultdict
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


class Device_usage_NM(Graphs, Database):
    def __init__(self, driver, elements=None):  # elements теперь необязательный параметр
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver
        self.elements = elements if elements is not None else []

    def __getitem__(self, index):
        return self.elements[index]

    # Locators
    buttons = "//button[@class='ant-table-row-expand-icon ant-table-row-expand-icon-collapsed']"
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
    def get_buttons(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, self.buttons)))

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
        first_company = self.get_download_b()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK download button")

    def click_du(self):
        self.get_language_report_b().click()
        print("CLICK Device Usage page")

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

    def click_Last_month(self):
        self.get_Last_month().click()
        print("CLICK Last month")

    def click_Last_30_days(self):
        self.get_Last_30_days().click()
        print("CLICK Last 30 days")

    def press_return_key(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем нажатие на клавишу Return
        actions.send_keys(Keys.RETURN).perform()

        print("Pressed the Return key")

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

    def click_total_c(self):
        self.get_total_calls().click()
        print("CLICK Total calls filter")

    def click_lang_s(self):
        self.get_lang_s().click()
        print("CLICK language search")

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
        print("Список языков с веб-страницы:", languages)

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
                    error_message += f"БД: {db_lang}, Веб: {web_lang}\n"

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

    def select_time_period_and_wait_for_update(self, time_period, open_list=True):
        if open_list:
            self.click_list()  # Открытие списка только если это необходимо
            self.double_press_down_arrow()
        time.sleep(10)  # Короткая задержка, чтобы убедиться, что список открыт
        getattr(self, f"click_{time_period}")()
        self.click_buttons()
        time.sleep(30)
        self.click_download_b()

        download_folder = "/Users/nikitabarshchuk/Downloads"
        target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
        file_pattern = "Device_Report*.xlsx"
        moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)

        if moved_file_path:
            csv_data = self.read_csv_data(moved_file_path)
            website_data = self.fetch_website_data_for_devices1()
            self.compare_data_cvs(website_data, csv_data)
        # Ожидание обновления данных

    def take_data_for_device_period(self, time_period):
        # Особое внимание к периоду 'Last_year'
        self.select_time_period_and_wait_for_update(time_period)
        website_data = self.fetch_website_data_for_devices()
        db_data = self.query_get_devices_Indiana_for_periods(time_period)

        if not db_data:
            print(f"No database data found for period '{time_period}'")
            return 0, True  # Предполагаем, что расхождения есть

        return self.compare_device_data(website_data, db_data, time_period)

    def fetch_website_data_for_devices(self):
        # Перейдите к разделу устройств на сайте, если это необходимо
        # self.driver.get('URL_of_device_section')

        # Ожидание загрузки данных устройств
        rows = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ant-table-body > table > tbody > tr"))
        )

        # Извлечение данных устройств
        device_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:  # Проверка наличия ячеек, чтобы избежать ошибок с пустыми строками
                device_data.append({
                    "ClientSite": cells[0].text.strip(),  # Добавление данных ClientSite
                    "SerialNumber": cells[1].text.strip(),
                    # Исправлен индекс, предполагая, что Serial Number идет после ClientSite
                    "ServiceMinutes": cells[2].text.strip(),  # Адаптация под вашу структуру данных
                    "NumberOfTransactions": cells[3].text.strip(),  # Адаптация под вашу структуру данных
                    # Добавьте больше полей по мере необходимости
                })

        return device_data

    def compare_device_data(self, website_data, db_data, period):
        discrepancies = []

        # Преобразуем website_data в одноуровневый список словарей для упрощения обработки
        flat_website_data = []
        for site_data in website_data:
            for device in site_data.get('Devices', []):  # Получаем список устройств или пустой список, если ключа нет
                flat_website_data.append(device)  # Добавляем информацию об устройстве в общий список

        for sql_row in db_data:
            # Ищем совпадение по серийному номеру и ClientSite
            web_row = next((item for item in flat_website_data if
                            item.get('SerialNumber') == sql_row['IOSSerialNumber'] and item.get('ClientSite') ==
                            sql_row['ClientSite']), None)

            if web_row:
                # Сравнение данных
                if str(sql_row['ServiceMinutes']) != web_row.get('ServiceMinutes'):
                    discrepancies.append(
                        f"ServiceMinutes mismatch for SerialNumber {sql_row['IOSSerialNumber']} and ClientSite {sql_row['ClientSite']} in '{period}': DB({sql_row['ServiceMinutes']}) != Web({web_row.get('ServiceMinutes')})")
                if str(sql_row['TotalTransactions']) != web_row.get('NumberOfTransactions'):
                    discrepancies.append(
                        f"NumberOfTransactions mismatch for SerialNumber {sql_row['IOSSerialNumber']} and ClientSite {sql_row['ClientSite']} in '{period}': DB({sql_row['TotalTransactions']}) != Web({web_row.get('NumberOfTransactions')})")
            else:
                discrepancies.append(
                    f"Missing device on web for SerialNumber {sql_row['IOSSerialNumber']} and ClientSite {sql_row['ClientSite']} in '{period}'.")

        if discrepancies:
            # Обработка расхождений
            error_message = f"Discrepancies found for period '{period}':\n" + "\n".join(discrepancies)
            logging.error(error_message)
            # Дополнительная обработка ошибок
            return len(db_data) - len(discrepancies), False
        else:
            # Сообщение об успешном сравнении
            print(f"Data Between web and DB match for period '{period}'.")
            return len(db_data), True

    def fetch_website_data_for_devices1(self):
        # Ожидание загрузки данных о клиентских сайтах
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "tr.ant-table-row-level-0 > td.ant-table-cell.ant-table-row-expand-icon-cell"))
        )

        # Нахождение всех кнопок для расширения строки
        expand_buttons = self.driver.find_elements(
            By.CSS_SELECTOR, "tr.ant-table-row-level-0 > td.ant-table-cell.ant-table-row-expand-icon-cell")

        all_data = []
        for button in expand_buttons:
            # Находим название клиентского сайта, которое находится сразу после кнопки
            client_site_name = button.find_element(By.XPATH, "./following-sibling::td[1]").text.strip()

            # Получение строки с данными устройств, которая следует за названием сайта
            parent_row = button.find_element(By.XPATH, "./ancestor::tr")
            next_row = parent_row.find_element(By.XPATH, "./following-sibling::tr")

            # Получение данных устройств внутри расширенной строки
            devices_rows = next_row.find_elements(By.CSS_SELECTOR, "tr.ant-table-row-level-0")

            # Извлечение данных устройств
            device_data = []
            for row in devices_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 4:
                    device_data.append({
                        "ClientSite": client_site_name,
                        "SerialNumber": cells[0].text.strip(),
                        "ServiceMinutes": cells[1].text.strip(),
                        "DeviceOwner": cells[2].text.strip(),
                        "NumberOfTransactions": cells[3].text.strip()
                    })

            all_data.append({
                "ClientSite": client_site_name,
                "Devices": device_data
            })

        # print("WEBSITE DATA:", all_data)
        return all_data

    def execute_period_comparison(self):
        with allure.step("Compare data with DB by Periods"):
            time_periods = ['yesterday', 'This_week', 'last_week', 'this_month',
                            'Last_month', 'Last_30_days', 'This_year', 'Last_year']
            for time_period in time_periods:
                print(f"Processing period: {time_period}")
                self.select_time_period_and_wait_for_update(time_period)

                website_data = self.fetch_website_data_for_devices1()

                if time_period == 'Last_month':
                    db_data = self.query_get_devices_NM_for_last_month()

                elif time_period in ['Last_30_days', 'This_year', 'Last_year']:
                    if time_period == 'Last_30_days':
                        db_data = self.query_get_devices_NM_for_last_30_days()
                    elif time_period == 'This_year':
                        db_data = self.query_get_devices_NM_this_year()
                    elif time_period == 'Last_year':
                        db_data = self.query_get_devices_NM_last_year()

                else:
                    db_data = self.query_get_devices_NM_for_periods(time_period)

                if not db_data:
                    print(f"No data retrieved from SQL query for {time_period}.")
                    continue

                matched_count, data_match = self.compare_device_data(website_data, db_data, time_period)

                print(f"Period '{time_period}':")
                print(f"Total devices from SQL query: {len(db_data)}")
                if data_match:
                    print(f"All devices from SQL query matched with devices from the web page for this period.")
                else:
                    print(f"Discrepancies found for period '{time_period}'. Please check logs for more details.")

    def aggregate_results(self, results):
        aggregated_data = defaultdict(lambda: {'ServiceMinutes': 0, 'TotalTransactions': 0})
        for row in results:
            ios_serial = row['IOSSerialNumber']
            service_minutes = row['ServiceMinutes']
            total_transactions = row['TotalTransactions']  # Исправлено здесь
            aggregated_data[ios_serial]['ServiceMinutes'] += service_minutes
            aggregated_data[ios_serial]['TotalTransactions'] += total_transactions  # Исправлено здесь
        return aggregated_data

    def click_buttons(self):
        buttons = self.get_buttons()

        # Проходимся по каждой кнопке и кликаем на нее
        for button in buttons:
            button.click()

    def move_latest_file(self, download_folder, target_folder, file_pattern):
        try:
            if not os.path.exists(download_folder):
                print(f"Папка скачивания не существует: {download_folder}")
                return None
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)  # Создаём целевую папку, если она не существует

            files = glob.glob(os.path.join(download_folder, file_pattern))
            if not files:
                print(f"Файлы с шаблоном {file_pattern} не найдены в папке {download_folder}")
                return None

            latest_file = max(files, key=os.path.getctime)
            target_file = os.path.join(target_folder, os.path.basename(latest_file))

            shutil.move(latest_file, target_file)
            print(f"Файл {latest_file} был перемещен в {target_file}")
            return target_file
        except Exception as e:
            print(f"Ошибка при перемещении файла: {e}")
            return None

    def device_usage_page(self):
        with allure.step("Device_usage_NM"):
            Logger.add_start_step(method='Device_usage_NM')
            self.driver.maximize_window()
            self.click_drop_down()
            time.sleep(3)
            self.click_du()
            self.get_current_url()
            time.sleep(3)
            self.screenshot()
            time.sleep(3)
            self.click_and_check_sort()
            self.click_buttons()
            time.sleep(60)
            # logging.info("Starting to compare data with API.")
            # self.compare_devices_data1()
            # logging.info("Finished comparing data with API.")
            # logging.info("Starting to compare data with SQL.")
            # self.compare_devices_data_with_sql()
            # logging.info("Finished comparing data with SQL.")
            # Logger.add_end_step(url=self.driver.current_url, method='Device_usage_NM')
            # # # # TODO ЗДЕСЬ ОШИБКА С ФАЙЛОМ, ТАМ ТОЛЬКО ОБЩИЕ ЗНАЧЕНИЯ
            # self.click_download_b()
            # time.sleep(10)
            # download_folder = "/Users/nikitabarshchuk/Downloads"
            # target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
            # file_pattern = "Device_Report*.xlsx"
            # moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)
            #
            # if moved_file_path:
            #     csv_data = self.read_csv_data(moved_file_path)
            #     website_data = self.fetch_website_data_for_devices1()
            #     self.compare_data_cvs(website_data, csv_data)
            # self.execute_period_comparison()  ###TODO БАГ С ДУБЛИКАТАМИ
            self.click_and_check_sort1()

            ###TODO ДОБАВИТЬ ФИЛЬТРАЦИЮ

            # self.check_color_change(self.element_xpath, self.additional_xpath)

    def read_csv_data(self, file_path):
        data = []
        # Read all sheets in the Excel file except 'Overview'
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        sheets_to_read = {k: v for k, v in all_sheets.items() if k != 'Overview'}

        # Iterate over each sheet
        for sheet_name, df in sheets_to_read.items():
            print(f"Processing sheet: {sheet_name}")
            # Convert data to list of dictionaries
            for index, row in df.iterrows():
                if 'IOSSerialNumber' in row and row['IOSSerialNumber'] != "Total":
                    try:
                        # Remove commas from numbers and convert to numeric format
                        minutes_used = int(float(str(row.get('Minutes Used', '0')).replace(",", "")))
                        number_of_transactions = int(
                            float(str(row.get('Number of Transactions', '0')).replace(",", "")))
                    except ValueError as e:
                        print(f"Value error for row {index} in sheet {sheet_name}: {e}")
                        continue

                    row_data = {
                        'IOSSerialNumber': row.get('IOSSerialNumber'),
                        'Minutes Used': minutes_used,
                        'Number of Transactions': number_of_transactions,
                        'Client Site': row.get('Client Site', sheet_name)  # Use sheet name if 'Client Site' is missing
                    }
                    data.append(row_data)
                else:
                    print(f"Sheet {sheet_name} does not contain 'IOSSerialNumber' column.")

        return data

    def fetch_website_data_am_cvs(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0"))
        )
        website_data = []
        rows = self.driver.find_elements(By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:  # Убедитесь, что в строке достаточное количество ячеек
                serial_number = cells[0].text
                if not cells[1].text.replace(",",
                                             "").isdigit():  # Проверяем, является ли содержимое второй ячейки числом
                    continue  # Это заголовок клиента, пропускаем его
                minutes_used = int(cells[1].text.replace(",", ""))  # Преобразуем в число, убирая запятые
                device_owner = cells[2].text
                number_of_transactions = int(cells[3].text)
                website_data.append({
                    "IOSSerialNumber": serial_number,
                    "Minutes Used": minutes_used,
                    "Device Owner": device_owner,
                    "Number of Transactions": number_of_transactions
                })
        return website_data

    def compare_data_cvs(self, web_data, csv_data):
        all_data_matched = True
        for web_site_data in web_data:
            client_site_name = web_site_data['ClientSite']
            for web_device_data in web_site_data['Devices']:
                csv_row = next((item for item in csv_data if
                                item['IOSSerialNumber'] == web_device_data['SerialNumber'] and item[
                                    'Client Site'] == client_site_name), None)
                if csv_row:
                    # Сравните данные из веба и CSV, как ранее
                    web_minutes = int(web_device_data['ServiceMinutes'].replace(",", ""))
                    csv_minutes = csv_row['Minutes Used']
                    web_transactions = int(web_device_data['NumberOfTransactions'].replace(",", ""))
                    csv_transactions = csv_row['Number of Transactions']

                    if web_minutes != csv_minutes:
                        print(
                            f"Mismatch in Minutes Used for {web_device_data['SerialNumber']}: Web - {web_minutes}, CSV - {csv_minutes}")
                        all_data_matched = False

                    if web_transactions != csv_transactions:
                        print(
                            f"Mismatch in Number of Transactions for {web_device_data['SerialNumber']}: Web - {web_transactions}, CSV - {csv_transactions}")
                        all_data_matched = False
                else:
                    print(
                        f"Serial number {web_device_data['SerialNumber']} not found in CSV data for Client Site {client_site_name}.")
                    all_data_matched = False

        if all_data_matched:
            print("All downloaded data matches correctly.")

    def click_and_check_sort(self):
        """
        Method clicks on the sort buttons and checks if the data is sorted.
        """
        xpaths = [
            '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[1]/div/span[2]',
            '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[2]/div/span[2]',
            '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[3]/div/span[2]'
        ]

        for column_index, xpath in enumerate(xpaths, start=1):
            # Click on the sort button
            sort_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", sort_button)

            # Wait for the data to update after sorting

            # Check sorting in ascending order
            self.check_sorting(column_index, "asc")

            # Second click for sorting in descending order
            sort_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", sort_button)

            self.check_sorting(column_index, "desc")

    def check_sorting(self, column_index, order="asc"):
        """
        Method to check data sorting.
        """
        # Wait for the data to update
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, f'tr.ant-table-row-level-0 > td:nth-child({column_index})'))
        )

        # Extract data from the table column
        data_rows = self.driver.find_elements(By.CSS_SELECTOR,
                                              f'tr.ant-table-row-level-0 > td:nth-child({column_index})')
        data_values = [row.text for row in data_rows]

        if order == "asc":
            sorted_correctly = data_values == sorted(data_values)
        elif order == "desc":
            sorted_correctly = data_values == sorted(data_values, reverse=True)
        else:
            raise ValueError("Invalid order: must be 'asc' or 'desc'")

        if sorted_correctly:
            print(
                f"Data is sorted in {'ascending' if order == 'asc' else 'descending'} order for column {column_index}")
        else:
            print(
                f"Data sorting error in {'ascending' if order == 'asc' else 'descending'} order for column {column_index}")

    def click_and_check_sort1(self):
        """
        Method clicks on the sort buttons and checks if the data is sorted.
        """
        xpaths = [
            '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td/div/div/div/div/div[2]/div/table/thead/tr/th[1]/div/span[2]',
            '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td/div/div/div/div/div[2]/div/table/thead/tr/th[2]/div/span[2]',
            '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td/div/div/div/div/div[2]/div/table/thead/tr/th[4]/div/span[2]'
        ]

        for column_index, xpath in enumerate(xpaths, start=1):
            # Click on the sort button
            sort_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", sort_button)

            # Check sorting in ascending order
            self.check_sorting1(column_index, "asc", "devices")

            # Second click for sorting in descending order
            sort_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", sort_button)

            # Check sorting in descending order
            self.check_sorting1(column_index, "desc", "devices")

    def check_sorting1(self, column_index, order="asc", table="clients"):
        """
        Method to check data sorting.
        """
        if table == "clients":
            css_selector = f'tr.ant-table-row-level-0 > td:nth-child({column_index})'
        elif table == "devices":
            css_selector = f'tr.ant-table-row-level-0 > td:nth-child({column_index + 1})'  # adjust if needed

        data_rows = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
        data_values = [row.text for row in data_rows]

        if order == "asc":
            sorted_correctly = data_values == sorted(data_values)
        elif order == "desc":
            sorted_correctly = data_values == sorted(data_values, reverse=True)
        else:
            raise ValueError("Invalid order: must be 'asc' or 'desc'")

        if sorted_correctly:
            print(
                f"Data is sorted in {'ascending' if order == 'asc' else 'descending'} order for column {column_index} in the {table} table")
        else:
            print(
                f"Data sorting error in {'ascending' if order == 'asc' else 'descending'} order for column {column_index} in the {table} table")
