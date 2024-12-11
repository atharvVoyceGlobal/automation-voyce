import shutil
import time
import os
import glob
import csv
import math
import pandas as pd
import shutil
import time
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import assertpy
import allure
import allure
from selenium.webdriver.common.keys import Keys
from utilities.logger import Logger
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import logging
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from customer_pages.Graph_c import Graphs


class Interpreter_Dashboard(Graphs):

    def __init__(self, driver):
        super().__init__(driver)  # Это должно инициализировать метод __init__ класса Base
        self.driver = driver

    # Locators
    check_ser_m = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/tbody/tr[1]/td[8]/a'
    terp_b = '//*[@id="root"]/section/aside/div/ul/li[6]'
    interpreter_id_f = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/thead/tr/th[1]/div/span[1]'
    interpreter_name_f = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/thead/tr/th[2]/div/span[1]'
    calls_f = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/thead/tr/th[4]/div/span[1]'
    answered_f = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/thead/tr/th[5]/div/span[1]'
    missed_f = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/thead/tr/th[6]/div/span[1]'
    avg_wt_f = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/thead/tr/th[7]/div/span[1]'
    serviced_min_f = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/thead/tr/th[8]/div/span[1]'
    select_column = '//*[@id="root"]/section/section/main/div/div/div/div[1]/form/div/div/div/div[1]/div/div/div/div/div/div'
    interpreter_id = '//div[@class="ant-select-item-option-content" and text()="Interpreter ID"]'
    interpreter_name = '//div[@class="ant-select-item-option-content" and text()="Interpreter Name"]'
    language = '//div[@class="ant-select-item-option-content" and text()="Language"]'
    calls = '//div[@class="ant-select-item-option-content" and text()="# Calls"]'
    answered = '//div[@class="ant-select-item-option-content" and text()="Answered"]'
    missed = '//div[@class="ant-select-item-option-content" and text()="Missed %"]'
    avg_wt = '//div[@class="ant-select-item-option-content" and text()="Avg WT"]'
    serviced_min = '//div[@class="ant-select-item-option-content" and text()="Serviced Mins"]'
    enter_text_to_search = '//*[@id="text"]'
    save_b = '//*[@id="root"]/section/section/main/div/div/div/div[1]/form/div/div/div/div[3]/div/div/div/div/button/span[2]'
    search_b = '//*[@id="root"]/section/section/main/div/div/div/div[1]/form/div/div/div/div[3]/div/div/div/div/button/span[2]'

    download_b = "//*[@id='root']/section/section/main/div/div/div/div[1]/div[2]/button/span[2]"
    all_clients = '//*[@id="header-container-id"]/div/div[6]/div/div/span[2]'
    choose_company = "//div[@class='ant-select-item-option-content' and text()='CCH Internal']"
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
    Last_month = '//div[@title="Last Month"]'
    Last_30_days = '//div[@title="Last 30 Days"]'
    This_year = '//div[@title="This Year"]'
    Last_year = '//div[@title="Last Year"]'
    lang_field = '//*[@id="root"]/section/section/main/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]'
    element_xpath = "//*[@id='root']/section/section/main/div/div/div[2]/div/div/div/div/div/div[1]/div/div[1]/div/div/span[2]"
    additional_xpath = '//*[@id="root"]/section/aside/div/ul'
    field_1 = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/tbody/tr[1]/td[1]'
    name_cell = "//*[@id='root']/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/tbody/tr[1]/td[2]"
    lang_cell = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/tbody/tr[1]/td[3]'
    call_cell = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/tbody/tr[1]/td[4]'
    answered_cell = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/tbody/tr[1]/td[5]'
    missed_cell = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/tbody/tr[1]/td[6]'
    avg_wt_cell = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/tbody/tr[1]/td[7]'
    serv_mins_cell = '//*[@id="root"]/section/section/main/div/div/div/div[3]/div/div/div/div[1]/div/table/tbody/tr[1]/td[8]/div'
    reset_b = '//*[@id="root"]/section/section/main/div/div/div/div[1]/form/div/div/div/div[4]/div/div/div/div/button/span'

    # Getters
    def get_check_ser_m(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_ser_m)))
    def get_reset_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.reset_b)))
    def get_lang_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_cell)))

    def get_call_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.call_cell)))

    def get_answered_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.answered_cell)))

    def get_missed_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.missed_cell)))

    def get_avg_wt_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.avg_wt_cell)))

    def get_serv_mins_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.serv_mins_cell)))

    def get_name_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_cell)))

    def get_search_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.search_b)))

    def get_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.field_1)))

    def get_interpreter_name_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.interpreter_name_f)))

    def get_terp_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.terp_b)))

    def get_interpreter_id_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.interpreter_id_f)))

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
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.this_week)))

    def get_calls_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.calls_f)))

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

    def get_answered_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.answered_f)))

    def get_missed_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.missed_f)))

    def get_avg_wt_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.avg_wt_f)))

    def get_serviced_min_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.serviced_min_f)))

    def get_select_column(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.select_column)))

    def get_interpreter_id(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.interpreter_id)))

    def get_interpreter_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.interpreter_name)))

    def get_language(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.language)))

    def get_calls(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.calls)))

    def get_answered(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.answered)))

    def get_missed(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.missed)))

    def get_avg_wt(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.avg_wt)))

    def get_serviced_min(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.serviced_min)))

    def get_enter_text_to_search(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.enter_text_to_search)))

    def get_save_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.save_b)))

        # Actions

    def click_terp_b(self):
        self.get_terp_b().click()
        print("CLICK Terp button")

    def click_interpreter_id_f(self):
        self.get_interpreter_id_f().click()
        print("CLICK interpreter id filter")

    def click_interpreter_name_f(self):
        self.get_interpreter_name_f().click()
        print("CLICK interpreter name filter")

    def click_calls_f(self):
        self.get_calls_f().click()
        print("CLICK calls filter")

    def click_answered_f(self):
        self.get_answered_f().click()
        print("CLICK answered filter")

    def click_user(self):
        user_element = self.get_user_element()
        self.driver.execute_script("arguments[0].click();", user_element)
        print("Clicked on User")

    def click_missed_f(self):
        self.get_missed_f().click()
        print("click missed filter")

    def click_first_company(self):
        first_company = self.get_first_company()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("Clicked first_company")

    def click_all_clients(self):
        self.get_all_clients().click()
        print("CLICK all clients")

    def click_search_b(self):
        self.get_search_b().click()
        print("Search button")

    def click_avg_wt_f(self):
        self.get_avg_wt_f().click()
        print("CLICK avg wt filter")

    def click_serviced_min_f(self):
        self.get_serviced_min_f().click()
        print("CLICK serviced min filter")

    def click_select_column(self):
        self.get_select_column().click()
        print("CLICK info")

    def click_interpreter_id(self):
        first_company = self.get_interpreter_id()
        self.driver.execute_script("arguments[0].click();", first_company)

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

    def click_interpreter_name(self):
        self.get_interpreter_name().click()
        print("CLICK interpreter_name")

    def click_list(self):
        self.get_Today_list().click()
        print("CLICK list")

    def click_reset_b(self):
        self.get_reset_b().click()
        print("CLICK reset b")

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

    def double_press_down_arrow(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем двойное нажатие на стрелку вверх
        actions.send_keys(Keys.ARROW_DOWN).perform()  # второе нажатие

        print("Pressed the Down arrow key")

    def click_this_year(self):
        self.get_This_year().click()
        print("CLICK This year")

    def input_enter_text_to_search(self, language):
        self.get_enter_text_to_search().send_keys(language)
        print("Input Text")

    def click_check_ser_m(self):
        self.get_check_ser_m().click()
        print("CLICK SERVISED MINS")
    def click_language(self):
        self.get_language().click()
        print("CLICK language")

    def click_calls(self):
        self.get_calls().click()
        print("CLICK calls")

    def click_last_year(self):
        self.get_Last_year().click()
        print("CLICK Last year")

    def click_this_week(self):
        self.get_This_week().click()
        print("CLICK This week")

    def click_answered(self):
        self.get_answered().click()
        print("CLICK Answered")

    def click_missed(self):
        self.get_missed().click()
        print("CLICK missed")

    def click_avg_wt(self):
        self.get_avg_wt().click()
        print("CLICK avg wt")

    def click_serviced_min(self):
        self.get_serviced_min().click()
        print("CLICK serviced min")

    def click_save_b(self):
        self.get_save_b().click()
        print("CLICK missed")

    def click_download_b(self):
        self.get_download_b().click()
        print("CLICK Download")

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

    def fetch_website_data_int_d(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
            )
            # Обработка данных, как обычно
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table > tbody > tr")
            website_data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 7:
                    record = {
                        "InterpreterID": cells[0].text,
                        "InterpreterName": cells[1].text,
                        "Language": cells[2].text,
                        "TotalCalls": cells[3].text.replace(',', ''),
                        "Answered": cells[4].text.replace(',', ''),
                        "MissedPercent": cells[5].text.replace('%', '').strip(),
                        "AvgWT": cells[6].text.replace(',', ''),
                        "ServicedMins": cells[7].text.replace(',', '')
                    }
                    website_data.append(record)
                else:
                    print(f"Not enough cells in the row to extract data: {row.text}")
            return website_data
        except UnexpectedAlertPresentException:
            return None
        except TimeoutException:
            # Обработка случая, когда элементы не появляются в течение заданного времени
            print("Превышено время ожидания элементов")
            return None

    def fetch_api_data(self):
        token = self.get_token_from_session_storage()
        if not token:
            logging.error("No token found in session storage. Cannot proceed with the API call.")
            return None

        logging.info(f"Using token: {token}")
        url = 'https://api.staging.vip.voyceglobal.com/company/interpreter'
        headers = {
            'authority': 'api.staging.vip.voyceglobal.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'authorization': f'Bearer {token}',  # Используйте полученный токен
            'content-type': 'application/json',
            'origin': 'https://staging.vip.voyceglobal.com',
            'referer': 'https://staging.vip.voyceglobal.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        current_utc_date = datetime.utcnow()
        start_date = (current_utc_date - timedelta(hours=5)).strftime('%Y-%m-%dT05:00:00.000Z')
        end_date = (current_utc_date - timedelta(hours=5) + timedelta(days=1)).strftime('%Y-%m-%dT04:59:59.999Z')

        data = {
            'start': start_date,
            'end': end_date,
            'filterType': 'company',
            'id': 1604  # или другой ID
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            logging.error(
                f"Failed to get data from API. Status code: {response.status_code}. Response: {response.text}")
            return None
        print(response.text)
        return response.json()

    def fetch_website_data_am(self):
        rows = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
        )

        total_service_minutes = 0
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 11:  # Проверяем, что в строке есть хотя бы 10 ячеек
                service_minutes_text = cells[10].text.strip()  # Убедитесь, что индекс ячейки правильный
                # Проверяем, содержит ли ячейка "-", если да, считаем это значение как 0
                service_minutes = 0 if service_minutes_text == "-" else service_minutes_text
                try:
                    service_minutes = int(service_minutes)  # Преобразование текста в число
                    total_service_minutes += service_minutes
                except ValueError:
                    print(
                        f"Cannot convert to integer: {service_minutes_text}")  # Не удалось преобразовать текст в число
            else:
                print(f"Not enough cells in the row to extract data: {row.text}")

        print(f"Общее количество служебных минут: {total_service_minutes}")  # Печать финальной суммы
        return total_service_minutes

    def compare_data_dashboard_DB(self, website_data, db_data):
        for web_record in website_data:
            interpreter_id = web_record["InterpreterID"]
            matched_db_record = next((item for item in db_data if str(item.InterpreterId) == interpreter_id), None)

            if matched_db_record:
                # Сравнение InterpreterName
                print(
                    f"Comparing InterpreterName for ID {interpreter_id}: Web='{web_record['InterpreterName']}' vs DB='{matched_db_record.InterpreterName}'")
                assertpy.assert_that(web_record["InterpreterName"]).is_equal_to(matched_db_record.InterpreterName)

                # Сравнение Language
                web_languages = [lang.strip() for lang in web_record["Language"].split(',')]
                db_languages = matched_db_record.UniqueTargetLanguages.tolist()
                print(f"Comparing Language for ID {interpreter_id}: Web='{web_languages}' vs DB='{db_languages}'")
                for lang in web_languages:
                    assertpy.assert_that(db_languages).contains(lang)

                # Сравнение TotalCalls
                print(
                    f"Comparing TotalCalls for ID {interpreter_id}: Web='{web_record['TotalCalls']}' vs DB='{matched_db_record.TotalCalls}'")
                assertpy.assert_that(int(web_record["TotalCalls"])).is_equal_to(matched_db_record.TotalCalls)

                # Сравнение Answered
                print(
                    f"Comparing Answered for ID {interpreter_id}: Web='{web_record['Answered']}' vs DB='{matched_db_record.TotalCallsAnswered}'")
                assertpy.assert_that(int(web_record["Answered"])).is_equal_to(matched_db_record.TotalCallsAnswered)

                # Сравнение MissedPercent
                web_missed_percent = int(web_record["MissedPercent"])
                if matched_db_record.TotalCalls > 0:
                    db_missed_percent = self.custom_round(
                        matched_db_record.TotalCallsMissed * 100 / matched_db_record.TotalCalls)
                else:
                    db_missed_percent = 0
                print(
                    f"Comparing MissedPercent for ID {interpreter_id}: Web='{web_missed_percent}' vs DB='{db_missed_percent}'")
                assertpy.assert_that(web_missed_percent).is_equal_to(db_missed_percent)

                # Сравнение AvgWT (среднее время ожидания)
                web_avg_wt = int(web_record["AvgWT"])
                if matched_db_record.TotalCalls > 0 and matched_db_record.TotalWaitTime is not None:
                    db_avg_wt = self.custom_round(matched_db_record.TotalWaitTime / matched_db_record.TotalCalls)
                else:
                    db_avg_wt = 0
                print(f"Comparing AvgWT for ID {interpreter_id}: Web='{web_avg_wt}' vs DB='{db_avg_wt}'")
                assertpy.assert_that(web_avg_wt).is_equal_to(db_avg_wt)

                # Сравнение ServicedMins
                web_serviced_mins = int(web_record["ServicedMins"])
                db_serviced_mins = int(matched_db_record.TotalServiceMinutes)
                print(
                    f"Comparing ServicedMins for ID {interpreter_id}: Web='{web_serviced_mins}' vs DB='{db_serviced_mins}'")
                assertpy.assert_that(web_serviced_mins).is_equal_to(db_serviced_mins)

            else:
                print(f"No matching database record found for Interpreter ID: {interpreter_id}")

    def custom_round(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Value must be a number, got {type(value)}")
        if value - int(value) >= 0.5:
            return math.ceil(value)
        else:
            return math.floor(value)

    def compare_data_terp(self, website_data, api_data):
        for web_record in website_data:
            interpreter_id = str(web_record["InterpreterID"])
            matched_api_record = next((item for item in api_data if str(item["InterpreterId"]) == interpreter_id), None)

            if matched_api_record:
                # Сравнение InterpreterName
                print(
                    f"Comparing InterpreterName: Web='{web_record['InterpreterName']}' vs API='{matched_api_record['InterpreterName']}'")
                assert web_record["InterpreterName"] == matched_api_record[
                    "InterpreterName"], f"InterpreterName mismatch for {interpreter_id}"

                # Сравнение Language
                api_languages = matched_api_record["UniqueTargetLanguages"]
                web_languages = [lang.strip() for lang in web_record["Language"].split(',')]
                print(f"Comparing Language: Web='{web_languages}' vs API='{api_languages}'")
                assert all(lang in api_languages for lang in web_languages), f"Language mismatch for {interpreter_id}"

                # Сравнение TotalCalls
                print(
                    f"Comparing TotalCalls: Web='{web_record['TotalCalls']}' vs API='{matched_api_record['TotalCalls']}'")
                assert int(web_record["TotalCalls"]) == matched_api_record[
                    "TotalCalls"], f"TotalCalls mismatch for {interpreter_id}"

                # Сравнение Answered
                print(
                    f"Comparing Answered: Web='{web_record['Answered']}' vs API='{matched_api_record['TotalCallsAnswered']}'")
                assert int(web_record["Answered"]) == matched_api_record[
                    "TotalCallsAnswered"], f"Answered mismatch for {interpreter_id}"

                # Сравнение MissedPercent
                if matched_api_record["TotalCalls"] > 0:
                    missed_percent_api = self.custom_round(
                        float(matched_api_record["TotalCallsMissed"]) * 100 / float(matched_api_record["TotalCalls"]))
                else:
                    missed_percent_api = 0
                print(f"Comparing MissedPercent: Web='{web_record['MissedPercent']}' vs API='{missed_percent_api}'")
                assert int(
                    web_record["MissedPercent"]) == missed_percent_api, f"MissedPercent mismatch for {interpreter_id}"

                # Сравнение AvgWT
                if matched_api_record["TotalCalls"] > 0 and matched_api_record["TotalWaitTime"] is not None:
                    avg_wt_api = self.custom_round(
                        matched_api_record["TotalWaitTime"] / matched_api_record["TotalCalls"])
                else:
                    avg_wt_api = 0
                print(f"Comparing AvgWT: Web='{web_record['AvgWT']}' vs API='{avg_wt_api}'")
                assert int(web_record["AvgWT"]) == avg_wt_api, f"AvgWT mismatch for {interpreter_id}"

                # Сравнение ServicedMins
                print(
                    f"Comparing ServicedMins: Web='{web_record['ServicedMins']}' vs API='{matched_api_record['TotalServiceMinutes']}'")
                assert int(web_record["ServicedMins"]) == matched_api_record[
                    "TotalServiceMinutes"], f"ServicedMins mismatch for {interpreter_id}"

            else:
                print(f"No matching API record found for Interpreter ID: {interpreter_id}")

    def select_time_period_and_wait_for_update(self, time_period, open_list=True):
        if open_list:
            self.click_list()  # Открытие списка только если это необходимо
        time.sleep(10)  # Короткая задержка, чтобы убедиться, что список открыт
        self.double_press_down_arrow()
        time.sleep(3)
        getattr(self, f"click_{time_period}")()
        time.sleep(30)  # Ожидание обновления данных
        self.click_download_b()
        time.sleep(30)
        download_folder = "/Users/nikitabarshchuk/Downloads"
        target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
        file_pattern = "Interpreter_Report*.xlsx"

        moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)

        if moved_file_path:
            csv_data = self.read_csv_data(moved_file_path)
            website_data = self.fetch_website_data_int_d()
            self.compare_data_int(website_data, csv_data)


    def compare_data_for_periods(self):
        with allure.step("Compare data with DB by Periods"):
            time_periods = ['yesterday', 'this_week', 'last_week', 'this_month', 'last_month', 'last_30_days',
                            'this_year',
                            'last_year']
            for period in time_periods:
                success = self.take_data_for_period_and_compare(period)
                if period == 'last_year' and success:
                    break  # Завершаем цикл после успешной проверки для last_year

    def take_data_for_period_and_compare(self, time_period):
        self.select_time_period_and_wait_for_update(time_period)
        website_data = self.fetch_website_data_int_d()  # Получение данных с сайта для нового периода

        if time_period == 'last_year':
            db_data = self.query_interpreter_dashboard_periods1(time_period)
        else:
            db_data = self.query_interpreter_dashboard_periods(time_period)

        if not db_data or not website_data:
            print(f"No data found for period '{time_period}'")
            return False  # Данные не найдены

        # Выполнение сравнения данных
        self.compare_data_dashboard_DB_periods(website_data, db_data)
        return True  # Данные найдены и сравнение выполнено

    def compare_data_dashboard_DB_periods(self, website_data, db_data):
        for web_record in website_data:
            interpreter_id = web_record["InterpreterID"]
            matched_db_record = next((item for item in db_data if str(item.InterpreterId) == interpreter_id), None)

            if matched_db_record:
                self.compare_records(web_record, matched_db_record)
            else:
                print(f"No matching database record found for Interpreter ID: {interpreter_id}")

    def compare_records(self, web_record, db_record):
        discrepancies = []
        matches = []  # List for matching records

        # Check InterpreterName
        if web_record["InterpreterName"] != db_record.InterpreterName:
            discrepancies.append(
                f"InterpreterName mismatch: Web({web_record['InterpreterName']}) != DB({db_record.InterpreterName})")
        else:
            matches.append(
                f"InterpreterName matches: Web({web_record['InterpreterName']}) == DB({db_record.InterpreterName})")

        # Check Language
        if web_record["Language"] not in db_record.UniqueTargetLanguages:
            discrepancies.append(
                f"Language not found in DB: Web({web_record['Language']}) not in DB({db_record.UniqueTargetLanguages})")
        else:
            matches.append(
                f"Language matches: Web({web_record['Language']}) found in DB({db_record.UniqueTargetLanguages})")

        # Check TotalCalls
        if int(web_record["TotalCalls"]) != db_record.TotalCalls:
            discrepancies.append(
                f"TotalCalls mismatch: Web({web_record['TotalCalls']}) != DB({db_record.TotalCalls})")
        else:
            matches.append(f"TotalCalls matches: Web({web_record['TotalCalls']}) == DB({db_record.TotalCalls})")

        # Check Answered
        if int(web_record["Answered"]) != db_record.TotalCallsAnswered:
            discrepancies.append(
                f"Answered mismatch: Web({web_record['Answered']}) != DB({db_record.TotalCallsAnswered})")
        else:
            matches.append(f"Answered matches: Web({web_record['Answered']}) == DB({db_record.TotalCallsAnswered})")

        # Check MissedPercent
        web_missed_percent = int(web_record["MissedPercent"])
        db_missed_percent = self.calculate_missed_percent(db_record)
        if web_missed_percent != db_missed_percent:
            discrepancies.append(
                f"MissedPercent mismatch: Web({web_missed_percent}) != DB({db_missed_percent})")
        else:
            matches.append(f"MissedPercent matches: Web({web_missed_percent}) == DB({db_missed_percent})")

        # Check AvgWT (Average Wait Time)
        web_avg_wt = int(web_record["AvgWT"])
        db_avg_wt = self.calculate_avg_wait_time(db_record)
        if web_avg_wt != db_avg_wt:
            discrepancies.append(
                f"AvgWT mismatch: Web({web_avg_wt}) != DB({db_avg_wt})")
        else:
            matches.append(f"AvgWT matches: Web({web_avg_wt}) == DB({db_avg_wt})")

        # Check ServicedMins
        web_serviced_mins = int(web_record["ServicedMins"])
        db_serviced_mins = int(db_record.TotalServiceMinutes)
        if web_serviced_mins != db_serviced_mins:
            discrepancies.append(
                f"ServicedMins mismatch: Web({web_serviced_mins}) != DB({db_serviced_mins})")
        else:
            matches.append(f"ServicedMins matches: Web({web_serviced_mins}) == DB({db_serviced_mins})")

        # Output the results
        if matches:
            for match in matches:
                print(match)

        if discrepancies:
            for discrepancy in discrepancies:
                print(discrepancy)
        elif not matches:
            print("No data to compare.")
        else:
            print("All data matches between the web and the database.")

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

    def calculate_missed_percent(self, db_record):
        if db_record.TotalCalls > 0:
            return round(db_record.TotalCallsMissed * 100 / db_record.TotalCalls)
        else:
            return 0

    def calculate_avg_wait_time(self, db_record):
        if db_record.TotalCalls > 0 and db_record.TotalWaitTime is not None:
            return round(db_record.TotalWaitTime / db_record.TotalCalls)
        else:
            return 0

    def interpreter_dashboard(self):
        with allure.step("Interpreter Dashboard"):
            Logger.add_start_step(method='Interpreter Dashboard')
            self.driver.maximize_window()
            self.click_terp_b()
            self.get_current_url()
            time.sleep(3)
            self.screenshot()
            self.click_list()
            self.click_yesterday()
            time.sleep(30)
            serv_mins1 = self.get_check_ser_m().text
            print(serv_mins1)
            self.click_check_ser_m()
            time.sleep(10)
            serv_mins = self.fetch_website_data_am()
            time.sleep(3)
            self.assert_nums(serv_mins, serv_mins1)
            time.sleep(3)
            self.click_terp_b()
            self.driver.refresh()
            time.sleep(10)
            website_data = self.fetch_website_data_int_d()
            api_data = self.fetch_api_data()
            self.compare_data_terp(website_data, api_data)
            db_data = self.query_interpreter_dashboard()
            self.compare_data_dashboard_DB(website_data, db_data)
            self.compare_data_for_periods()  ###TODO historic data bug

            self.click_download_b()
            time.sleep(30)
            download_folder = "/Users/nikitabarshchuk/Downloads"
            target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
            file_pattern = "Interpreter_Report*.xlsx"

            moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)

            if moved_file_path:
                csv_data = self.read_csv_data(moved_file_path)
                website_data = self.fetch_website_data_int_d()
                self.compare_data_int(website_data, csv_data)

            self.click_interpreter_id_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            lang_data = self.fetch_column_data_total_calls(column_index=0)
            print("Data after first sort:", lang_data)
            assert self.is_sorted_ascending_l(lang_data), "Data is not sorted ascending."

            self.click_interpreter_id_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            lang_data = self.fetch_column_data_total_calls(column_index=0)
            print("Data after second sort:", lang_data)
            assert self.is_sorted_descending_l(lang_data), "Data is not sorted descending."

            self.click_interpreter_name_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            new_total_calls_data = self.fetch_column_data_total_calls(column_index=1)
            print("Data after first sort:", new_total_calls_data)
            assert self.is_sorted_ascending_l(new_total_calls_data), "Data is not sorted ascending."

            # Проверяем сортировку по убыванию
            self.click_interpreter_name_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            new_total_calls_data = self.fetch_column_data_total_calls(column_index=1)
            print("Data after second sort:", new_total_calls_data)
            assert self.is_sorted_descending_l(new_total_calls_data), "Data is not sorted descending."

            # Проверяем сортировку по возрастанию
            self.click_serviced_min_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки ###
            new_total_minutes_data = self.fetch_column_data_total_calls(column_index=7)
            print("Data after first sort (Total Minutes):", new_total_minutes_data)
            assert self.is_sorted_ascending(new_total_minutes_data), "Total Minutes data is not sorted ascending."

            self.click_serviced_min_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            new_total_minutes_data = self.fetch_column_data_total_calls(column_index=7)
            print("Data after second sort (Total Minutes):", new_total_minutes_data)
            assert self.is_sorted_descending(new_total_minutes_data), "Total Minutes data is not sorted descending."

            self.click_calls_f()
            time.sleep(2)  # Нажимаем на кнопку сортировки
            new_serviced_audio_calls_data = self.fetch_column_data_total_calls(column_index=3)
            print("Data after first sort (Serviced audio calls):", new_serviced_audio_calls_data)
            assert self.is_sorted_ascending(
                new_serviced_audio_calls_data), "Serviced audio calls data is not sorted ascending."

            self.click_calls_f()
            time.sleep(2)  # Нажимаем на кнопку сортировки еще раз
            new_serviced_audio_calls_data = self.fetch_column_data_total_calls(column_index=3)
            print("Data after second sort (Serviced audio calls):", new_serviced_audio_calls_data)
            assert self.is_sorted_descending(
                new_serviced_audio_calls_data), "Serviced audio calls data is not sorted descending."

            self.click_answered_f()
            time.sleep(2)  # Нажимаем на кнопку сортировки
            new_serviced_video_calls_data = self.fetch_column_data_total_calls(column_index=4)
            print("Data after first sort (Serviced video calls):", new_serviced_video_calls_data)
            assert self.is_sorted_ascending(
                new_serviced_video_calls_data), "Serviced video calls data is not sorted ascending."

            self.click_answered_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            new_serviced_video_calls_data = self.fetch_column_data_total_calls(column_index=4)
            print("Data after second sort (Serviced video calls):", new_serviced_video_calls_data)
            assert self.is_sorted_descending(
                new_serviced_video_calls_data), "Serviced video calls data is not sorted descending."

            # Проверка сортировки для "Average Wait Time"
            self.click_missed_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            avg_wait_time_data = self.fetch_column_data_total_calls(column_index=5)
            print("Data after first sort (Average Wait Time):", avg_wait_time_data)
            assert self.is_sorted_ascending(avg_wait_time_data), "Average Wait Time data is not sorted ascending."

            self.click_missed_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            avg_wait_time_data = self.fetch_column_data_total_calls(column_index=5)
            print("Data after second sort (Average Wait Time):", avg_wait_time_data)
            assert self.is_sorted_descending(avg_wait_time_data), "Average Wait Time data is not sorted ascending."

            # Проверка сортировки для "Average Call Length"
            self.click_avg_wt_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            avg_call_length_data = self.fetch_column_data_total_calls(column_index=6)
            print("Data after first sort (Average Call Length):", avg_call_length_data)
            assert self.is_sorted_ascending(avg_call_length_data), "Average Call Length data is not sorted ascending."

            self.click_avg_wt_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки еще раз
            avg_call_length_data = self.fetch_column_data_total_calls(column_index=6)
            print("Data after second sort (Average Call Length):", avg_call_length_data)
            assert self.is_sorted_descending(
                avg_call_length_data), "Average Call Length data is not sorted descending."

            self.click_select_column()
            self.click_interpreter_id()
            text = self.get_cell().text
            self.input_enter_text_to_search(text)
            self.click_search_b()
            time.sleep(1)
            self.assert_word(self.get_cell(), text)
            self.click_reset_b()

            self.click_select_column()
            self.click_interpreter_name()
            text1 = self.get_name_cell().text
            self.input_enter_text_to_search(text1)
            self.click_search_b()
            time.sleep(1)
            self.assert_word(self.get_name_cell(), text1)
            self.click_reset_b()

            self.click_select_column()
            self.click_language()
            text2 = self.get_lang_cell().text
            self.input_enter_text_to_search(text2)
            self.click_search_b()
            self.assert_word(self.get_lang_cell(), text2)
            self.click_reset_b()

            self.click_select_column()
            self.click_calls()
            text3 = self.get_call_cell().text
            self.input_enter_text_to_search(text3)
            self.click_search_b()
            self.assert_word(self.get_call_cell(), text3)
            self.click_reset_b()

            self.click_select_column()
            self.click_answered()
            text4 = self.get_answered_cell().text
            self.input_enter_text_to_search(text4)
            self.click_search_b()
            self.assert_word(self.get_answered_cell(), text4)
            self.click_reset_b()

            self.click_select_column()
            self.click_missed()
            text5 = self.get_missed_cell().text
            self.input_enter_text_to_search(text5)
            self.click_search_b()
            self.assert_word(self.get_missed_cell(), text5)
            self.click_reset_b()

            self.click_select_column()
            self.click_avg_wt()
            text6 = self.get_avg_wt_cell().text
            self.input_enter_text_to_search(text6)
            self.click_search_b()
            self.assert_word(self.get_avg_wt_cell(), text6)
            self.click_reset_b()

            self.click_select_column()
            self.click_serviced_min()
            text7 = self.get_check_ser_m().text
            self.input_enter_text_to_search(text7)
            self.click_search_b()
            self.assert_word(self.get_check_ser_m(), text7)
            self.click_reset_b()

    def compare_data_int(self, web_data_list, csv_data_list):
        with allure.step("Compare downloaded data with Web data"):
            print("Interpreter IDs in CSV:", [item['Interpreter ID'] for item in csv_data_list])
            print("Interpreter IDs on the website:", [data['InterpreterID'] for data in web_data_list])

            data_is_correct = True  # Флаг, отслеживающий корректность данных

            for web_data in web_data_list:
                if not web_data['InterpreterID']:
                    continue  # Пропускаем пустые строки

                matching_csv_data = next(
                    (item for item in csv_data_list if item['Interpreter ID'] == web_data['InterpreterID']),
                    None)
                if matching_csv_data:
                    if not self.compare_records_cvs(matching_csv_data, web_data):
                        print(f"Data mismatch for Interpreter ID: {web_data['InterpreterID']}")
                        data_is_correct = False  # Обнаружено несоответствие данных
                else:
                    print(f"No matching data found in CSV for Interpreter ID: {web_data['InterpreterID']}")
                    data_is_correct = False  # Обнаружено несоответствие данных

            if data_is_correct:
                print("Downloaded data is correct")  # Все данные совпадают

            return data_is_correct

    def normalize_number(self, number_str):
        """Удаление запятых из строки и преобразование в число."""
        try:
            return int(number_str.replace(',', ''))
        except ValueError:
            print(f"Ошибка преобразования: {number_str} не является числом")
            return None

    def compare_records_cvs(self, csv_data, web_data):
        is_match = True

        # Сравнение имени переводчика (игнорируя регистр)
        if csv_data['Name'].strip().lower() != web_data['InterpreterName'].strip().lower():
            print(
                f"Mismatch found for Interpreter Name: CSV '{csv_data['Name']}' vs Web '{web_data['InterpreterName']}'")
            is_match = False

        # Сравнение языка (игнорируя регистр и пробелы)
        csv_languages = set(map(str.strip, csv_data['Language'].strip().lower().split(',')))
        web_languages = set(map(str.strip, web_data['Language'].strip().lower().split(',')))
        if csv_languages != web_languages:
            print(f"Mismatch found for Language: CSV '{csv_data['Language']}' vs Web '{web_data['Language']}'")
            is_match = False

        # Сравнение общего числа вызовов
        if self.normalize_number(csv_data['# Calls']) != self.normalize_number(web_data['TotalCalls']):
            print(f"Mismatch found for Total Calls: CSV '{csv_data['# Calls']}' vs Web '{web_data['TotalCalls']}'")
            is_match = False

        # Сравнение числа отвеченных вызовов
        if self.normalize_number(csv_data['Answered']) != self.normalize_number(web_data['Answered']):
            print(f"Mismatch found for Answered Calls: CSV '{csv_data['Answered']}' vs Web '{web_data['Answered']}'")
            is_match = False

        # Сравнение процента пропущенных вызовов
        if self.normalize_number(csv_data['Missed %'].replace('%', '')) != self.normalize_number(
                web_data['MissedPercent']):
            print(
                f"Mismatch found for Missed Percent: CSV '{csv_data['Missed %']}' vs Web '{web_data['MissedPercent']}'")
            is_match = False

        # Сравнение обслуженных минут
        if self.normalize_number(csv_data['Serviced Mins']) != self.normalize_number(web_data['ServicedMins']):
            print(
                f"Mismatch found for Serviced Mins: CSV '{csv_data['Serviced Mins']}' vs Web '{web_data['ServicedMins']}'")
            is_match = False

        # Сравнение среднего времени ожидания
        if self.normalize_number(csv_data['Avg WT']) != self.normalize_number(web_data['AvgWT']):
            print(f"Mismatch found for Avg WT: CSV '{csv_data['Avg WT']}' vs Web '{web_data['AvgWT']}'")
            is_match = False

        return is_match

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

    def read_csv_data(self, file_path):
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

    def format_number(self, number_str):
        return number_str.replace(',', '').strip()

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
