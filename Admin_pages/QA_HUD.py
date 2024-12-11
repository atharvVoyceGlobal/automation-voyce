import string
import datetime
import random
import re
import string
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import unicodedata
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import threading
import shutil
import time
import re
import pytz
import pyautogui
import os
import glob
import csv
from datetime import datetime, timedelta

import math
import pandas as pd
import shutil
import time
import assertpy
import allure
import allure
from selenium.common import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from utilities.logger import Logger

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import logging

from selenium.webdriver.support.ui import WebDriverWait
from customer_pages.Graph_c import Graphs
import time

from datetime import timezone

import allure
import numpy as np
import pyautogui
from selenium.common import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from customer_pages.Graph_c import Graphs
from database.Database import Database
from utilities.logger import Logger


class Qa_hud(Graphs):

    def __init__(self, driver, time_zone='America/New_York'):
        Graphs.__init__(self, driver)
        Database.__init__(self)
        self.time_zone = pytz.timezone(time_zone)

    # Locators
    pages_100 = "//span[@class='ant-select-selection-item' and @title='100 / page']"
    pages_10 = "//div[@class='ant-select-item-option-content' and text()='10 / page']"
    pluses = "//button[@class='ant-table-row-expand-icon ant-table-row-expand-icon-collapsed' and @aria-label='Expand row']"

    Today_list = '//*[@id="header-container-id"]/div/div[3]/div/div/span[2]'
    id_field_watchlist = '//*[@id="active-session-table-expanded"]/div/div/table/tbody/tr[2]/td[1]/button'
    search_id_watchlist = '//*[@id="active-session-table-expanded"]/div/div/table/thead/tr/th[1]/div/span[2]/span'
    expand2 = '//*[@id="root"]/section/section/main/div/div/div/div/div[4]/div/div[1]/div/div[2]/button'
    remove_button = '(//*[@id="new-terp-expanded"]//tbody[contains(@class, "ant-table-tbody")]//button[span="Remove"])[1]'
    add_button = "(//*[@id='new-terp-expanded']//tbody//button[span='Add'])[1]"
    date_added = '//*[@id="new-terp-expanded"]/div/div/table/thead/tr/th[5]/div/span[1]'
    languages_f = '//*[@id="new-terp-expanded"]/div/div/table/thead/tr/th[4]/div/span[1]'
    languages_search = '//*[@id="new-terp-expanded"]/div/div/table/thead/tr/th[4]/div/span[2]/span'
    languages_input = "//input[@placeholder='Search Languages']"
    languages_field = '//*[@id="new-terp-expanded"]/div/div/table/tbody/tr[6]/td[4]'
    languages_field1 = '//*[@id="new-terp-expanded"]/div/div/table/tbody/tr[2]/td[4]'
    name_input = "//input[@placeholder='Search InterpreterName']"
    create_account_button = "//*[@id='root']/div/div[3]/div/div/div/div/div/div[2]/div[1]/div/button"
    first_name = "//*[@id='firstname']"
    last_name = "//*[@id='lastname']"
    activation_mail = "//div[contains(@class, 'ant-message-custom-content') and contains(@class, 'ant-message-success')]//span[contains(text(), 'We sent you an activation mail to')]"
    email_field = "//*[@id='email']"
    password_field = "//*[@id='password']"
    confirm_password = "//*[@id='confirm']"
    create_account_button2 = "//*[@id='root']/div/div[3]/div/div/div/div/div/form/div/div/div[7]/div/div/div/div/div/button"
    password_dont_math = "//*[@id='confirm_help']/div"
    password_dont_meet_criteria = "//*[@id='password_help']/div"
    qa_hud = '//*[@id="root"]/section/aside/div/ul/li[8]/div'
    qa_hud1 = "//li[@role='menuitem' and @sortlabel='Quality Assurance HUD' and contains(@class, 'ant-menu-item')]"
    id_f = "(//span[@class='ant-table-column-title' and text()='ID'])[3]"
    name_f = '//*[@id="new-terp-expanded"]/div/div/table/thead/tr/th[2]/div/span[1]'
    expand = '//*[@id="new-terp-unexpanded"]/div[1]/div/div[2]/button'
    id_field = '//*[@id="new-terp-expanded"]/div/div/table/tbody/tr[4]/td[1]'
    id_field1 = '//*[@id="new-terp-expanded"]/div/div/table/tbody/tr[2]/td[1]'
    name_field = '//*[@id="new-terp-expanded"]/div/div/table/tbody/tr[5]/td[2]'
    name_field1 = '//*[@id="new-terp-expanded"]/div/div/table/tbody/tr[2]/td[2]'
    search_id = '//*[@id="new-terp-expanded"]/div/div/table/thead/tr/th[1]/div/span[2]/span'
    search_name = '//*[@id="new-terp-expanded"]/div/div/table/thead/tr/th[2]/div/span[2]/span'
    id_input = "//input[@placeholder='Search InterpreterId' and contains(@class, 'ant-input')]"
    submit_search = "//button[contains(@class, 'ant-btn') and .//span[text()='Search']]"

    # Getters
    def get_date_added(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="new-terp-expanded"]/div/div/table/thead/tr/th[5]/div/span[1]')))

    # Метод клика для date_added
    def click_date_added(self):
        date_added_element = self.get_date_added()
        self.driver.execute_script("arguments[0].click();", date_added_element)
        print("CLICK date added")

    def get_expand2(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH,
             '//*[@id="root"]/section/section/main/div/div/div/div/div[4]/div/div/div/div/div[1]/div/div[3]/button')))

    def get_remove_button(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                '(//*[@id="new-terp-expanded"]//tbody[contains(@class, "ant-table-tbody")]//button[span="Remove"])[1]')))

    def get_add_button(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='new-terp-expanded']/div/div/table/tbody/tr[2]/td[6]/button/span")))

    def get_id_field_watchlist(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="active-session-table-expanded"]/div/div/table/tbody/tr[2]/td[1]')))

    def get_search_id_watchlist(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="active-session-table-expanded"]/div/div/table/thead/tr/th[1]/div/span[2]/span')))

    # Методы клика
    def click_expand2(self):
        self.get_expand2().click()

    def click_remove_button(self):
        self.get_remove_button().click()

    def click_add_button(self):
        first_company = self.get_add_button()
        self.driver.execute_script("arguments[0].click();", first_company)

    def get_search_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.search_name)))

    def get_search_id(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.search_id)))

    def get_qa_hud1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.qa_hud1)))

    def get_id_field1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.id_field1)))

    def get_id_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.id_field)))

    def get_name_field1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_field1)))

    def get_name_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_field)))

    def get_id_input(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.id_input)))

    def get_name_input(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_input)))

    def get_languages_f(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="new-terp-expanded"]/div/div/table/thead/tr/th[4]/div/span[1]')))

    def get_languages_search(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="new-terp-expanded"]/div/div/table/thead/tr/th[4]/div/span[2]/span')))

    def get_remove_b2(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="active-session-table-expanded"]/div/div/table/tbody/tr[2]/td[7]/button')))

    def get_languages_input(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Languages']")))

    def get_languages_field(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="new-terp-expanded"]/div/div/table/tbody/tr[6]/td[4]')))

    def get_languages_field1(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="new-terp-expanded"]/div/div/table/tbody/tr[2]/td[4]')))

    def get_expand(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.expand)))

    def get_id_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.id_f)))

    def get_name_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_f)))

    def get_qa_hud(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.qa_hud)))

    def get_create_account_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.create_account_button)))

    def get_first_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.first_name)))

    def get_last_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.last_name)))

    def get_email_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.email_field)))

    def get_password_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field)))

    def get_confirm_password(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.confirm_password)))

    def get_create_account_button2(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.create_account_button2)))

    def get_activation_mail(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.activation_mail)))

    def get_password_dont_math(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_dont_math)))

    def get_password_dont_meet_criteria(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.password_dont_meet_criteria)))

    def get_pages_100(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.pages_100)))

    def get_pages_10(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.pages_10)))

    def get_pluses(self):
        return WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, self.pluses)))

    def click_pluses(self):
        pluses = self.get_pluses()
        max_attempts = 3
        for plus in pluses:
            attempt = 0
            while attempt < max_attempts:
                try:
                    plus.click()
                    break  # Если клик успешен, выходим из цикла
                except WebDriverException as e:
                    print(f"Ошибка: {e}")
                    attempt += 1
                    if attempt < max_attempts:
                        print("Ожидаем и повторяем попытку...")
                        time.sleep(15)  # Ожидаем 5 секунд перед следующей попыткой
                    else:
                        print("Не удалось выполнить клик после нескольких попыток.")
        # Actions

    def click_pages_100(self):
        self.get_pages_100().click()
        print("100 clicked")

    def click_pages_10(self):
        languages_search = self.get_pages_10()
        self.driver.execute_script("arguments[0].click();", languages_search)
        print("")

    def input_first_name(self, user_name):
        self.get_first_name().send_keys(user_name)
        print("input first name")

    def input_last_name(self, user_password):
        self.get_last_name().send_keys(user_password)
        print("input last name")

    def input_id(self, user_password):
        self.get_id_input().send_keys(user_password)
        print("input id")

    def input_name(self, user_password):
        self.get_name_input().send_keys(user_password)
        print("input name")

    def input_email(self, user_password):
        self.get_email_field().send_keys(user_password)
        print("input email")

    def input_password_field(self, user_password):
        self.get_password_field().send_keys(user_password)
        print("input password")

    def input_confirm_password(self, user_password):
        self.get_confirm_password().send_keys(user_password)
        print("input confirm password")

    def click_qa_hud(self):
        self.get_qa_hud().click()
        print("CLICK QA HUD page")

    def click_qa_hud1(self):
        self.get_qa_hud1().click()
        print("CLICK QA HUD page")

    def click_by_css_selector(self, css_selector):
        element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        element.click()

    def click_id_f(self):
        first_company = self.get_id_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK id filter")

    def input_languages(self, value):
        self.get_languages_input().send_keys(value)
        print("input languages")

    def click_name_f(self):
        first_company = self.get_name_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK id filter")

    def click_last_month(self):
        # Ожидание появления элемента на странице
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='ant-select-item-option-content' and contains(text(), 'Last Month')]"))
        )

        # Находим элемент на странице
        this_month_element = self.driver.find_element(By.XPATH,
                                                      "//div[@class='ant-select-item-option-content' and contains(text(), 'Last Month')]")

        # Используем JavaScript для клика по элементу
        self.driver.execute_script("arguments[0].click();", this_month_element)
        print("Clicked on 'This Month'")

    def click_this_month(self):
        # Ожидание появления элемента на странице
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(text(), 'This Month')])[2]"))
        )

        # Находим элемент на странице
        this_month_element = self.driver.find_element(By.XPATH, "(//div[contains(text(), 'This Month')])[2]")

        # Используем JavaScript для клика по элементу
        self.driver.execute_script("arguments[0].click();", this_month_element)
        print("Clicked on 'This Month'")

    def click_languages_f(self):
        languages_f = self.get_languages_f()
        self.driver.execute_script("arguments[0].click();", languages_f)
        print("CLICK languages filter")

    def click_completed_tab(self):
        try:
            # Ожидание элемента и кликаем по нему
            completed_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//div[@data-node-key='Completed']/div[@role='tab' and @aria-selected='false' and @class='ant-tabs-tab-btn' and @tabindex='0']"))
            )
            self.driver.execute_script("arguments[0].click();", completed_tab)
            print("Clicked on the Completed tab.")
        except Exception as e:
            print(f"Error occurred while clicking on the Completed tab: {e}")

    def click_inprogress_tab(self):
        try:
            # Ожидание элемента и кликаем по нему
            completed_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//div[@data-node-key='In Progress']/div[@role='tab' and @aria-selected='false' and @class='ant-tabs-tab-btn' and @tabindex='0']"))
            )
            self.driver.execute_script("arguments[0].click();", completed_tab)
            print("Clicked on the Completed tab.")
        except Exception as e:
            print(f"Error occurred while clicking on the Completed tab: {e}")

    def click_element_by_xpath(self):
        # Ожидание появления элемента на странице
        element_to_click = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="root"]/section/section/main/div/div/div/div/div[3]/div'))
        )
        # Выполнение клика через JavaScript
        self.driver.execute_script("arguments[0].click();", element_to_click)
        print("CLICK on the specified XPath")

    # Клик по languages_search
    def click_languages_search(self):
        languages_search = self.get_languages_search()
        self.driver.execute_script("arguments[0].click();", languages_search)
        print("CLICK languages search")

    def click_search_id(self):
        first_company = self.get_search_id()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK search id")

    def click_search_id_w(self):
        first_company = self.get_search_id_watchlist()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK search id")

    def click_search_name(self):
        first_company = self.get_search_name()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK search name")

    def click_REMOVE_B2(self):
        first_company = self.get_remove_b2()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK remove b2")

    def click_create_account(self):
        self.get_create_account_button().click()
        print("CLICK Create an Account button")

    def press_return_key(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем нажатие на клавишу Return
        actions.send_keys(Keys.RETURN).perform()

        print("Pressed the Return key")

    def click_expand(self):
        first_company = self.get_expand()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Expand")

    def normalize_string(self, s):
        # Normalize to NFKD form, which separates letters and diacritics, and remove the diacritics
        return ''.join(c for c in unicodedata.normalize('NFKD', s) if unicodedata.category(c) != 'Mn')

    def is_sorted_ascending1(self, data):
        if not data:
            return True  # Consider an empty list as sorted

        # Exclude empty strings from processing
        processed_data = [self.process_item(item) for item in data if item.strip()]

        # Check if the data is sorted in ascending order considering type and value
        for i in range(len(processed_data) - 1):
            curr_type, curr_val = processed_data[i]
            next_type, next_val = processed_data[i + 1]

            if curr_type != next_type:
                continue  # Skip elements of different types (e.g., string and number)

            if curr_val > next_val:
                print(f"Error in sorting: {curr_val} should not be before {next_val}")
                return False  # Elements of the same type are not in the correct order

        return True

    def click_expand_qa_Analysis(self):
        try:
            # Ожидание элемента и кликаем по нему
            completed_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="qa-analysis-table-unexpanded"]/div[1]/div/div[2]/button/span'))
            )
            self.driver.execute_script("arguments[0].click();", completed_tab)
            print("Clicked expand_qa_Analysis.")
        except Exception as e:
            print(f"Error occurred while clicking on expand_qa_Analysis: {e}")

    def process_item(self, item):
        # Convert the string to lowercase, remove extra spaces, and normalize
        item = self.normalize_string(item.lower().strip())
        try:
            # Try to convert to a number
            value = float(item)
            return (type(value), value)
        except ValueError:
            # If conversion to number fails, treat as a string
            return (str, item)

    def normalize_language_string(self, lang_str):
        # Check if the input is a numpy array and convert it to a list if true
        if isinstance(lang_str, np.ndarray):
            lang_str = lang_str.tolist()

        # Join the list into a single string if it's not already a string
        if isinstance(lang_str, list):
            lang_str = ', '.join(lang_str)

        # Remove unwanted characters, keeping only letters, commas, parentheses, and spaces
        lang_str = re.sub(r"[^a-zA-Z,() ]", "", lang_str)

        # Split the cleaned string into a list, strip spaces, and sort the list
        cleaned_list = sorted(lang.strip() for lang in lang_str.split(','))

        # Return a comma-separated string of the sorted languages
        return ', '.join(cleaned_list)

    def normalize_name(self, name):
        # Remove excess whitespace and join name parts
        return " ".join(name.split())

    def compare_new_entries_with_db_data(self, web_data, db_data):
        print("Starting comparison of new entries with database data")
        discrepancies = []
        no_match_found = False

        keys_to_compare = {
            "ID": "InterpreterId",
            "Name": "InterpreterName",
            "Company Name": "CompanyCode",
            "Languages": "Languages",
        }

        for web_row in web_data:
            if not web_row.get("ID"):
                print("Empty ID found, skipping this row.")
                continue

            db_row = next((item for item in db_data if str(item['InterpreterId']) == web_row["ID"]), None)

            if db_row:
                for web_key, db_key in keys_to_compare.items():
                    web_value = web_row.get(web_key, '').strip()
                    db_value = getattr(db_row, db_key, '')

                    # Обработка и нормализация имён и языков
                    if web_key == "Languages":
                        db_value = ', '.join(db_value) if isinstance(db_value, list) else db_value
                        if self.normalize_language_string(db_value) != self.normalize_language_string(web_value):
                            discrepancies.append(
                                f"Discrepancy for ID {web_row['ID']}: {web_key} DB({db_value}) != Web({web_value})")
                    elif web_key == "Name":
                        if self.normalize_name(db_value) != self.normalize_name(web_value):
                            discrepancies.append(
                                f"Discrepancy for ID {web_row['ID']}: {web_key} DB({db_value}) != Web({web_value})")
                    else:
                        if str(db_value).strip() != str(web_value).strip():
                            discrepancies.append(
                                f"Discrepancy for ID {web_row['ID']}: {web_key} DB({db_value}) != Web({web_value})")
            else:
                no_match_found = True
                print(f"No matching data found in DB for ID: {web_row['ID']}")

        if discrepancies:
            print("Discrepancies found:")
            for discrepancy in discrepancies:
                print(discrepancy)
        else:
            print("All web data matches the database records.")

        if no_match_found:
            print("Some entries did not have matching data in DB.")

        return discrepancies

    def click_create_account_button2(self):
        self.get_create_account_button2().click()
        print("CLICK Create an Account button 2")

    # METHODS

    def refresh_and_click_force_login(self):
        # Обновляем страницу
        self.driver.refresh()
        time.sleep(5)  # Пауза, чтобы страница полностью обновилась

        try:
            # Проверяем, появился ли элемент на странице
            force_login_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[text()='Force Login']"))
            )
            # Кликаем по элементу, если он доступен
            force_login_button.click()
            print("Clicked on 'Force Login'")
        except TimeoutException:
            # Если элемент не появился в течение заданного времени
            print("The 'Force Login' button was not found after the page refresh.")

    def fetch_column_data(self, column_index):
        column_data = []
        try:
            # XPath to get the table body excluding the first row of measurements
            tbody_xpath = '//*[@id="new-terp-expanded"]/div/div/table/tbody'

            # Wait for the table body to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, tbody_xpath))
            )

            # Get all the data rows in the table, excluding the measurements row
            rows = self.driver.find_elements(By.XPATH, f"{tbody_xpath}/tr")

            # Iterate through the rows and extract data from the specified column
            for row in rows:
                try:
                    # Get the cell by column index and extract its text
                    cell = row.find_elements(By.XPATH, ".//td")[column_index]
                    column_data.append(cell.text)
                except StaleElementReferenceException:
                    print("Error accessing the element, the row has been changed.")
                except IndexError:
                    column_data.append("Error: index out of range")
        except Exception as e:
            print(f"An error occurred while fetching data from the column: {e}")

        return column_data

    def fetch_new_entries_from_table(self):
        # Ожидание загрузки таблицы на странице
        WebDriverWait(self.driver, 90).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='new-terp-expanded']/div/div/table/tbody"))
        )

        new_entries = []

        try:
            # Находим все строки в теле таблицы
            rows = WebDriverWait(self.driver, 90).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, "//*[@id='new-terp-expanded']/div/div/table/tbody/tr[position()>1]"))
            )

            for row in rows:
                # Получение значений ячеек для каждого столбца
                cells = row.find_elements(By.XPATH, ".//td")
                id = cells[0].text.strip()
                name = cells[1].text.strip()
                company_name = cells[2].text.strip()
                languages = cells[3].text.strip()
                date_added = cells[4].text.strip()

                new_entries.append({
                    "ID": id,
                    "Name": name,
                    "Company Name": company_name,
                    "Languages": languages,
                    "Date Added": date_added
                })
        except (NoSuchElementException, StaleElementReferenceException) as e:
            print("Ошибка при извлечении данных: ", e)

        return new_entries

    def get_Today_list(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Today_list)))

    def click_list(self):
        self.get_Today_list().click()
        print("CLICK list")

    def parse_monitor_history(self, detail_cells):
        # Обработка полученных данных из detail_cells
        transaction_id = detail_cells[0].text.strip()
        qa_name = detail_cells[1].text.strip()
        eval_minutes = detail_cells[3].text.strip()
        monitor_minutes = detail_cells[4].text.strip()
        monitor_start_time = datetime.datetime.strptime(detail_cells[5].text.strip(), '%Y-%m-%d %H:%M:%S')
        monitor_end_time = datetime.datetime.strptime(detail_cells[6].text.strip(), '%Y-%m-%d %H:%M:%S')

        return {
            "Transaction ID": transaction_id,
            "QA Name": qa_name,
            "Eval Minutes": eval_minutes,
            "Monitor Minutes": monitor_minutes,
            "Monitoring Start Time": monitor_start_time,
            "Monitoring End Time": monitor_end_time
        }

    def fetch_QAd(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="qad-table"]/div/div/table/tbody'))
        )

        all_data = []

        headers_first_level = self.driver.find_elements(By.XPATH, '//*[@id="qad-table"]/div/div/table/thead/tr/th')
        first_level_headers = [header.text for header in headers_first_level if header.text.strip() != '']

        for i in range(1, 21, 2):
            first_level_row_xpath = f'//*[@id="qad-table"]/div/div/table/tbody/tr[{i}]'
            first_level_cells = self.driver.find_elements(By.XPATH, f"{first_level_row_xpath}//td[position() > 1]")
            first_level_data = [cell.text.strip() for cell in first_level_cells]
            row_dict = dict(zip(first_level_headers, first_level_data))
            row_dict['second_level'] = []

            second_level_base_xpath = f'//*[@id="qad-table"]/div/div/table/tbody/tr[{i + 1}]'
            second_level_headers_xpath = f"{second_level_base_xpath}/td/div/div/div/div/div[2]/div/table/thead/tr/th"
            second_level_headers = self.driver.find_elements(By.XPATH, second_level_headers_xpath)
            second_level_headers_text = [header.text for header in second_level_headers if header.text.strip() != '']

            second_level_rows = self.driver.find_elements(By.XPATH,
                                                          f"{second_level_base_xpath}/td/div/div/div/div/div[2]/div/table/tbody/tr")
            for j in range(1, len(second_level_rows) + 1, 2):
                second_level_row_xpath = f"{second_level_base_xpath}/td/div/div/div/div/div[2]/div/table/tbody/tr[{j}]"
                second_level_cells = self.driver.find_elements(By.XPATH,
                                                               f"{second_level_row_xpath}//td[position() > 1]")
                second_level_data = [cell.text.strip() for cell in second_level_cells]
                second_level_row_dict = dict(zip(second_level_headers_text, second_level_data))
                second_level_row_dict['third_level'] = []

                third_level_rows_xpath = f"{second_level_base_xpath}/td/div/div/div/div/div[2]/div/table/tbody/tr[{j + 1}]/td/div/div/div/div/div/div/table/tbody/tr"
                third_level_rows = self.driver.find_elements(By.XPATH, third_level_rows_xpath)
                for third_level_row in third_level_rows:
                    third_level_headers_xpath = f"{second_level_base_xpath}/td/div/div/div/div/div[2]/div/table/tbody/tr[{j + 1}]/td/div/div/div/div/div/div/table/thead/tr/th"
                    third_level_headers = self.driver.find_elements(By.XPATH, third_level_headers_xpath)
                    third_level_headers_text = [header.text for header in third_level_headers if
                                                header.text.strip() != '']

                    third_level_cells = third_level_row.find_elements(By.XPATH, f".//td")
                    third_level_data = [cell.text.strip() for cell in third_level_cells]
                    third_level_row_dict = dict(zip(third_level_headers_text, third_level_data))

                    second_level_row_dict['third_level'].append(third_level_row_dict)

                row_dict['second_level'].append(second_level_row_dict)

            all_data.append(row_dict)
        return all_data

    def transform_data(self, data):
        results = []
        for item in data:
            interpreter_name = item['Interpreter Name']
            interpreter_id = item['Interpreter ID']
            main_score_data = item['Score']
            monthly_qa_status = item['QA Status']

            # Определяем, является ли основной score числом или меткой
            if '-' in main_score_data:
                score_label, score = main_score_data.split(' - ')
                score = int(score)  # Преобразуем строку в число
            else:
                score = int(main_score_data)
                score_label = None  # Метки нет

            for second_level in item['second_level']:
                qa_specialist_name = second_level['QA Name']
                qa_score = second_level['Score']  # Score на уровне QA

                # Проверка, является ли score второго уровня числом или текстом с меткой
                if '-' in qa_score:
                    qa_score_label, qa_score = qa_score.split(' - ')
                    qa_score = int(qa_score)
                else:
                    qa_score = int(qa_score)
                    qa_score_label = None  # Метки нет

                transaction_id = second_level['Transaction ID']
                for third_level in second_level['third_level']:
                    monitor_start_time = datetime.strptime(third_level['Monitoring Start Time'], '%Y-%m-%d %H:%M:%S')
                    monitor_end_time = datetime.strptime(third_level['Monitoring End Time'], '%Y-%m-%d %H:%M:%S')
                    total_monitor_seconds = (monitor_end_time - monitor_start_time).total_seconds()

                    result = {
                        'qaSpecialistName': qa_specialist_name,
                        'interpreterName': interpreter_name,
                        'interpreterId': int(interpreter_id),
                        'score': qa_score,  # Числовое значение score на уровне QA
                        'scoreLabel': qa_score_label if qa_score_label else score_label,  # Метка score если доступна
                        'monitorStartTime': monitor_start_time,
                        'requestId': int(transaction_id),
                        'monitorEndTime': monitor_end_time,
                        'totalMonitorSeconds': total_monitor_seconds,
                        'monthlyQaStatus': monthly_qa_status
                    }
                    results.append(result)
        return results

    def transform_data1(self, data):
        results = []
        for item in data:
            qa_name = item.get('QA Name')
            sessions = int(item.get('Sessions', 0))
            e_mins = int(item.get('E Mins', 0))
            m_mins = int(item.get('M Mins', 0))
            interpreters_monitored = int(item.get('Interpreters Monitored', 0))

            for second_level in item.get('second_level', []):
                if second_level['Transaction ID'] == '-' or second_level['Interpreter ID'] == '-':
                    continue

                transaction_id = int(second_level['Transaction ID'])
                interpreter_id = int(second_level['Interpreter ID'])
                interpreter_name = second_level['Interpreter Name']
                score = int(second_level['Score'])
                eval_minutes = int(second_level['Eval Minutes'])
                monitor_minutes = int(second_level['Monitor Minutes'])

                for third_level in second_level.get('third_level', []):
                    if third_level['Monitoring Start Time'] == '-' or third_level['Monitoring End Time'] == '-':
                        continue

                    monitor_start_time = datetime.strptime(third_level['Monitoring Start Time'], '%Y-%m-%d %H:%M:%S')
                    monitor_end_time = datetime.strptime(third_level['Monitoring End Time'], '%Y-%m-%d %H:%M:%S')
                    total_monitor_seconds = (monitor_end_time - monitor_start_time).total_seconds()

                    if third_level['Evaluation Start Time'] != '-':
                        evaluation_start_time = datetime.strptime(third_level['Evaluation Start Time'],
                                                                  '%Y-%m-%d %H:%M:%S')
                    else:
                        evaluation_start_time = None

                    if third_level['Evaluation Submit Time'] != '-':
                        evaluation_submit_time = datetime.strptime(third_level['Evaluation Submit Time'],
                                                                   '%Y-%m-%d %H:%M:%S')
                    else:
                        evaluation_submit_time = None

                    if third_level['Evaluation End Time'] != '-':
                        evaluation_end_time = datetime.strptime(third_level['Evaluation End Time'], '%Y-%m-%d %H:%M:%S')
                        total_evaluation_seconds = (
                                evaluation_end_time - evaluation_start_time).total_seconds() if evaluation_start_time else 0
                    else:
                        evaluation_end_time = None
                        total_evaluation_seconds = 0

                    result = {
                        'qaSpecialistName': qa_name,
                        'interpreterName': interpreter_name,
                        'interpreterId': interpreter_id,
                        'score': score,
                        'monitorStartTime': monitor_start_time,
                        'monitorEndTime': monitor_end_time,
                        'totalMonitorSeconds': total_monitor_seconds,
                        'totalEvaluationSeconds': total_evaluation_seconds,
                        'requestId': transaction_id,
                        'qaSpecialistId': None,  # Placeholder, as ID is not available from the frontend data
                        'sessions': sessions,
                        'monitorMinutes': monitor_minutes,
                        'evalMinutes': eval_minutes,
                        'Mmins': m_mins,
                        'Emins': e_mins,
                        'interpretersMonitored': interpreters_monitored
                    }
                    results.append(result)
        # print("transform_data1", results)
        return results

    def fetch_QA_analysis(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="qa-analysis-table-expanded"]/div/div/table/tbody'))
        )

        all_data = []

        headers_first_level = self.driver.find_elements(By.XPATH,
                                                        '//*[@id="qa-analysis-table-expanded"]/div/div/table/thead/tr/th')
        first_level_headers = [header.text for header in headers_first_level if header.text.strip() != '']

        for i in range(2, 300, 2):
            first_level_row_xpath = f'//*[@id="qa-analysis-table-expanded"]/div/div/table/tbody/tr[{i}]'
            first_level_cells = self.driver.find_elements(By.XPATH, f"{first_level_row_xpath}//td[position() > 1]")
            first_level_data = [cell.text.strip() for cell in first_level_cells]
            row_dict = dict(zip(first_level_headers, first_level_data))
            row_dict['second_level'] = []

            second_level_row_xpath_base = f'{first_level_row_xpath}/following-sibling::tr[1]/td/div/div/div/div/div[2]/div/table'
            second_level_headers = self.driver.find_elements(By.XPATH, f"{second_level_row_xpath_base}/thead/tr/th")
            second_level_headers_text = [header.text for header in second_level_headers if header.text.strip() != '']

            second_level_rows = self.driver.find_elements(By.XPATH, f"{second_level_row_xpath_base}/tbody/tr")
            for k in range(0, len(second_level_rows), 2):
                second_level_row_xpath = f"{second_level_row_xpath_base}/tbody/tr[{k + 1}]"
                second_level_cells = self.driver.find_elements(By.XPATH,
                                                               f"{second_level_row_xpath}//td[position() > 1]")
                second_level_data = [cell.text.strip() for cell in second_level_cells]
                if '-' in second_level_data:
                    continue  # Пропуск строк с '-'
                second_level_row_dict = dict(zip(second_level_headers_text, second_level_data))
                second_level_row_dict['third_level'] = []

                third_level_row_xpath_base = f"{second_level_row_xpath}/following-sibling::tr[1]/td/div/div/div/div/div/div/table"
                third_level_headers = self.driver.find_elements(By.XPATH, f"{third_level_row_xpath_base}/thead/tr/th")
                third_level_headers_text = [header.text for header in third_level_headers if header.text.strip() != '']

                third_level_rows = self.driver.find_elements(By.XPATH, f"{third_level_row_xpath_base}/tbody/tr")
                for j in range(len(third_level_rows)):
                    third_level_row_xpath = f"{third_level_row_xpath_base}/tbody/tr[{j + 1}]"
                    third_level_cells = self.driver.find_elements(By.XPATH, f"{third_level_row_xpath}//td")
                    third_level_data = [cell.text.strip() for cell in third_level_cells]
                    if '-' in third_level_data:
                        continue  # Пропуск строк с '-'
                    third_level_row_dict = dict(zip(third_level_headers_text, third_level_data))

                    second_level_row_dict['third_level'].append(third_level_row_dict)

                row_dict['second_level'].append(second_level_row_dict)

            all_data.append(row_dict)

        # print("fetch_QA_analysis", all_data)
        return all_data

    def drag_and_drop_by_coordinates(self, source_xpath):
        # Получите размер окна браузера и его позицию
        window_rect = self.driver.get_window_rect()
        window_x = window_rect['x']
        window_y = window_rect['y']

        # Найдите элемент, который вы хотите перетаскивать
        source_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, source_xpath))
        )
        # Прокрутите страницу до элемента
        self.driver.execute_script("arguments[0].scrollIntoView(true);", source_element)

        # Получите относительные координаты исходного элемента
        source_location = source_element.location
        source_x = window_x + source_location['x']
        source_y = window_y + source_location['y']

        # Найдите целевой элемент

        # Переместите мышь к исходному элементу и нажмите
        y_offset = 300
        x_offset = 100

        # Перемещение мыши и действия перетаскивания
        time.sleep(4)
        self.click_element_by_xpath()
        target_x = source_x + x_offset
        target_y = source_y + y_offset
        pyautogui.moveTo(target_x, target_y, duration=1)
        time.sleep(1)
        pyautogui.dragTo(target_x, target_y, duration=1, button='left')
        time.sleep(1)
        while not self.is_visible('//*[@id="qad-table"]/div/div/table/tbody'):
            pyautogui.mouseDown()
            time.sleep(3)
            pyautogui.mouseUp()
            time.sleep(3)

    def is_visible(self, xpath):
        try:
            element = WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except:
            return False

    def compare_data_for_periods(self):
        with allure.step("Compare data with DB by Periods"):
            time_periods = ['this_month']
            for period in time_periods:
                self.take_data_for_period_and_compare(period)

    def double_press_down_arrow(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем двойное нажатие на стрелку вверх
        actions.send_keys(Keys.ARROW_DOWN).perform()  # второе нажатие

        print("Pressed the Down arrow key")

    def take_data_for_period_and_compare(self, time_period):
        self.select_time_period_and_wait_for_update(time_period)  # Устанавливаем фильтр на веб-сайт
        time.sleep(30)
        website_data = self.fetch_new_entries_from_table()  # Получение данных с сайта

        # Выбор общего метода запроса в базе данных без учёта конкретных периодов 'last_month' и 'last_year'
        db_data = self.query_check_QA_HUD(time_period)

        if db_data and website_data:
            self.compare_new_entries_with_db_data(website_data, db_data)
        else:
            print(f"No data found for period '{time_period}'")

    def select_time_period_and_wait_for_update(self, time_period, open_list=True):
        if open_list:
            self.click_list()  # Открытие списка, если это необходимо
            self.double_press_down_arrow()
        time.sleep(10)  # Короткая задержка, чтобы убедиться, что список открыт
        getattr(self, f"click_{time_period}")()
        time.sleep(5)
        self.click_expand()
        time.sleep(10)  # Ожидание обновления данных

    def is_sorted_descending1(self, column_data):
        column_data_processed = []
        for data in column_data:
            if data:
                try:
                    # Пытаемся преобразовать строку в объект datetime
                    time = datetime.strptime(data, '%H:%M:%S')
                    column_data_processed.append(time)
                except ValueError:
                    # Если преобразование в datetime не удалось, обрабатываем как число
                    number = ''.join(filter(str.isdigit, data))
                    if number:
                        column_data_processed.append(int(number))
                    else:
                        # Если строка не содержит чисел, игнорируем её
                        continue

        # Проверяем, что каждый элемент больше или равен следующему
        for i in range(len(column_data_processed) - 1):
            # Для объектов datetime сравнение произойдет как временные метки
            # Для чисел - как целочисленные значения
            if column_data_processed[i] < column_data_processed[i + 1]:
                return False
        return True

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def fetch_all_data(self):
        collection = self.client["auth"]["InterpreterWatchlist"]

        cursor = collection.find(
            {})  # Использование find без фильтров, что эквивалентно db.getCollection("InterpreterWatchlist").find({})

        result_list = list(cursor)  # Преобразуем курсор в список для удобства работы с данными
        print(result_list)
        return result_list

    def adjust_time(self, time):
        if time == datetime.min:
            return time
        return time - timedelta(hours=4)

    def compare_data_QA_HUD(self, extracted_data, db_data):
        db_dict = {
            (
                item.get('interpreterName', 'N/A'),
                str(item.get('interpreterId', 'N/A')),
                self.adjust_time(item.get('monitorStartTime', datetime.min)).strftime('%Y-%m-%d %H:%M:%S'),
                self.adjust_time(item.get('monitorEndTime', datetime.min)).strftime('%Y-%m-%d %H:%M:%S')
            ): item
            for item in db_data
        }

        extracted_dict = {
            (
                item.get('Interpreter Name', 'N/A'),
                str(item.get('Interpreter ID', 'N/A')),
                item.get('Monitoring Start Time', 'N/A'),
                item.get('Monitoring End Time', 'N/A')
            ): item
            for item in extracted_data
        }

        for key, extracted_value in extracted_dict.items():
            db_value = db_dict.get(key)
            if not db_value:
                print(f'Нет соответствия в базе данных для KEY: {key}')
                print(f'Извлеченные данные: {extracted_value}')
                print(f'Данные из базы: {db_value}')
                print(f'Данные найдены и сошлись для {key}:')

    def compare_monitoring_records(self, frontend_data, db_data):
        found_records = []
        not_found_records = []
        time_difference = timedelta(hours=4)

        for index, record in enumerate(frontend_data):
            is_found = False
            frontend_start_time = record['monitorStartTime'].replace(microsecond=0)
            frontend_end_time = record['monitorEndTime'].replace(microsecond=0)

            for db_index, db_group in enumerate(db_data):
                for db_record in db_group.get('details', []):  # Используем .get для безопасного получения данных
                    try:
                        # Корректируем время из базы данных
                        db_start_time = (db_record['monitorStartTime'] - time_difference).replace(microsecond=0)
                        db_end_time = (db_record['monitorEndTime'] - time_difference).replace(microsecond=0)

                        # Сравниваем записи
                        if (record['qaSpecialistName'] == db_record['qaSpecialistName'] and
                                record['interpreterName'] == db_record['interpreterName'] and
                                record['interpreterId'] == db_record['interpreterId'] and
                                record['score'] == db_record['score'] and
                                record['requestId'] == db_record['requestId'] and
                                frontend_start_time == db_start_time and
                                frontend_end_time == db_end_time):
                            is_found = True
                            found_records.append(record)
                            print(
                                f"Match found for record {record['requestId'], frontend_start_time} with DB record {db_record['requestId'], db_start_time}")
                            break
                    except KeyError as e:
                        print(f"Key error: {e} in DB record {db_index + 1}")
                        continue

            if not is_found:
                not_found_records.append(record)
                print(f"No match found for record {record}")

        return found_records, not_found_records

    def process_qa_data(self, data):
        time_difference = timedelta(hours=4)  # Корректировка времени
        qa_specialists = {}

        for entry in data:
            for detail in entry['details']:
                # Корректировка времени для каждой записи
                detail['monitorStartTime'] -= time_difference
                detail['monitorEndTime'] -= time_difference

                qa_specialist = detail['qaSpecialistName']
                interpreter_id = detail['interpreterId']

                if qa_specialist not in qa_specialists:
                    qa_specialists[qa_specialist] = {
                        'Mmins': 0, 'Emins': 0, 'sessions': 0, 'interpreters': set()
                    }

                # Calculate Ceil(totalMonitorSeconds/60)
                monitor_minutes = math.ceil(detail['totalMonitorSeconds'] / 60)
                qa_specialists[qa_specialist]['Mmins'] += monitor_minutes

                # Calculate Ceil(totalEvaluationSeconds/60) if exists
                if 'totalEvaluationSeconds' in detail:
                    evaluation_minutes = math.ceil(detail['totalEvaluationSeconds'] / 60)
                    qa_specialists[qa_specialist]['Emins'] += evaluation_minutes
                    detail['evalMinutes'] = evaluation_minutes
                else:
                    detail['evalMinutes'] = 0

                detail['monitorMinutes'] = monitor_minutes

                # Sum totalQaSessions for the given qaSpecialistName
                qa_specialists[qa_specialist]['sessions'] += 1

                # Add interpreter ID to the set
                qa_specialists[qa_specialist]['interpreters'].add(interpreter_id)

        # Calculate interpretersMonitored and add it to the specialists data
        for qa_specialist in qa_specialists:
            qa_specialists[qa_specialist]['interpretersMonitored'] = len(qa_specialists[qa_specialist]['interpreters'])

        # Adding the calculated values back to the original data
        for entry in data:
            for detail in entry['details']:
                qa_specialist = detail['qaSpecialistName']
                detail['Mmins'] = qa_specialists[qa_specialist]['Mmins']
                detail['Emins'] = qa_specialists[qa_specialist]['Emins']
                detail['sessions'] = qa_specialists[qa_specialist]['sessions']
                detail['interpretersMonitored'] = qa_specialists[qa_specialist]['interpretersMonitored']

        print("DB DATA", data)
        return data

    def click_last_100_completed_in_table(self):
        try:
            # Находим все элементы с "Completed"
            completed_spans = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     '//*[@id="qad-table"]/div/div/table/tbody//span[contains(@style, "background-color: lightgreen;") and text() = "Completed"]'))
            )

            # Берем только последние 100 элементов
            if len(completed_spans) > 100:
                last_100_spans = completed_spans[-100:]
            else:
                last_100_spans = completed_spans

            # Кликаем по каждому найденному элементу, проверяя текст
            for completed_span in last_100_spans:
                if completed_span.text == 'Completed':
                    print("Completed span Checked")
                else:
                    print("Span text is not 'Completed':", completed_span.text)
        except Exception as e:
            print(f"Error occurred while clicking on the Completed span: {e}")

    def click_last_100_inprogress_in_table(self):
        try:
            # Находим все элементы с "Completed"
            completed_spans = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     "//div[@data-node-key='In Progress']/div[@role='tab' and @aria-selected='false' and @class='ant-tabs-tab-btn' and @tabindex='0'] | //div[@style='text-align: center; width: 100px;']/span[@style='background-color: yellow; padding: 2px 4px; border-radius: 4px; color: rgb(0, 0, 0); font-weight: bold;']"))
            )

            # Берем только последние 100 элементов
            if len(completed_spans) > 100:
                last_100_spans = completed_spans[-100:]
            else:
                last_100_spans = completed_spans

            # Кликаем по каждому найденному элементу, проверяя текст
            for completed_span in last_100_spans:
                if completed_span.text == 'In Progress':
                    print("Completed span Checked")
                else:
                    print("Span text is not 'Completed':", completed_span.text)
        except Exception as e:
            print(f"Error occurred while clicking on the Completed span: {e}")

    def match_data_F_DB(self, db_data, frontend_data):
        matched_data = []
        unmatched_data = []

        for frontend_entry in frontend_data:
            is_found = False
            # Нормализуем имена на фронте
            frontend_qa_specialist_name = re.sub(r'\s+', ' ', frontend_entry['qaSpecialistName']).strip()
            frontend_interpreter_name = re.sub(r'\s+', ' ', frontend_entry['interpreterName']).strip()
            frontend_start_time = frontend_entry['monitorStartTime'].replace(microsecond=0)
            frontend_end_time = frontend_entry['monitorEndTime'].replace(microsecond=0)

            for db_entry in db_data:
                for detail in db_entry['details']:
                    try:
                        if "  " in detail['qaSpecialistName']:
                            print("Double spaces found in DB qaSpecialistName:", detail['qaSpecialistName'])
                        if "  " in detail['interpreterName']:
                            print("Double spaces found in DB interpreterName:", detail['interpreterName'])

                        db_qa_specialist_name = re.sub(r'\s+', ' ', detail['qaSpecialistName']).strip()
                        db_interpreter_name = re.sub(r'\s+', ' ', detail['interpreterName']).strip()
                        db_start_time = detail['monitorStartTime'].replace(microsecond=0)
                        db_end_time = detail['monitorEndTime'].replace(microsecond=0)

                        if (db_qa_specialist_name == frontend_qa_specialist_name and
                                db_interpreter_name == frontend_interpreter_name and
                                detail['interpreterId'] == frontend_entry['interpreterId'] and
                                detail['score'] == frontend_entry['score'] and
                                detail['requestId'] == frontend_entry['requestId'] and
                                frontend_start_time == db_start_time and
                                frontend_end_time == db_end_time):
                            matched_data.append({
                                'db_data': detail,
                                'frontend_data': frontend_entry
                            })
                            is_found = True
                            # Вывод совпадающих данных
                            print("Match found:")
                            print("DB Data:")
                            for key, value in detail.items():
                                print(f"{key}: {value}")
                            print("\nFrontend Data:")
                            for key, value in frontend_entry.items():
                                print(f"{key}: {value}")
                            print("\n---\n")
                            break
                    except KeyError as e:
                        print(f"Key error: {e} in DB record")
                        continue

            if not is_found:
                unmatched_data.append(frontend_entry)
                # Вывод несовпадающих данных
                print("No match found for Frontend Data:")
                for key, value in frontend_entry.items():
                    print(f"{key}: {value}")
                print("\n---\n")

        return matched_data, unmatched_data


    def monitor(self):
        with allure.step("QA HUD"):
            Logger.add_start_step(method='QA HUD')
            self.click_qa_hud()
            time.sleep(3)
            self.click_qa_hud1()
            # time.sleep(3)
            # self.get_current_url()
            # self.assert_url('https://admin.vip.voyceglobal.com/hud/QA/')
            # time.sleep(3)
            # self.refresh_and_click_force_login()
            # self.click_expand()
            # time.sleep(3)
            # self.click_id_f()
            # time.sleep(10)
            # lang_data = self.fetch_column_data(column_index=0)
            # print("Data after first sort:", lang_data)
            # assert self.is_sorted_ascending1(lang_data), "Data is not sorted ascending."
            # self.click_id_f()
            # time.sleep(10)
            # lang_data = self.fetch_column_data(column_index=0)
            # print("Data after first sort:", lang_data)
            # assert self.is_sorted_descending1(lang_data), "Data is not sorted ascending."
            # self.click_search_id()
            # time.sleep(3)
            # id = self.get_id_field().text
            # time.sleep(3)
            # self.input_id(id)
            # time.sleep(3)
            # self.press_return_key()
            # time.sleep(3)
            # self.assert_word(self.get_id_field1(), id)
            # self.refresh_and_click_force_login()
            # time.sleep(10)
            # self.click_expand()
            # self.click_name_f()
            # time.sleep(10)
            # lang_data = self.fetch_column_data(column_index=1)
            # print("Data after first sort:", lang_data)
            # assert self.is_sorted_ascending1(lang_data), "Data is not sorted ascending."
            # self.click_name_f()
            # time.sleep(10)
            # lang_data = self.fetch_column_data(column_index=1)
            # print("Data after first sort:", lang_data)
            # assert self.is_sorted_descending1(lang_data), "Data is not sorted ascending."
            #
            # self.click_search_name()
            # time.sleep(3)
            # id = self.get_name_field().text
            # time.sleep(3)
            # self.input_name(id)
            # time.sleep(3)
            # self.press_return_key()
            # time.sleep(3)
            # self.assert_word(self.get_name_field1(), id)
            # self.refresh_and_click_force_login()
            # time.sleep(10)
            # self.click_expand()
            #
            # self.click_languages_f()
            # time.sleep(10)
            # lang_data = self.fetch_column_data(column_index=3)
            # print("Data after first sort:", lang_data)
            # assert self.is_sorted_ascending1(lang_data), "Data is not sorted ascending."
            # self.click_languages_f()
            # time.sleep(10)
            # lang_data = self.fetch_column_data(column_index=3)
            # print("Data after first sort:", lang_data)
            # assert self.is_sorted_descending1(lang_data), "Data is not sorted ascending."
            #
            # self.click_languages_search()
            # time.sleep(3)
            # id = self.get_languages_field().text
            # time.sleep(3)
            # self.input_languages(id)
            # time.sleep(3)
            # self.press_return_key()
            # time.sleep(3)
            # self.assert_word(self.get_languages_field1(), id)
            # self.refresh_and_click_force_login()
            # time.sleep(10)
            # self.click_expand()
            #
            # self.click_date_added()
            # time.sleep(10)
            # lang_data = self.fetch_column_data(column_index=4)
            # print("Data after first sort:", lang_data)
            # assert self.is_sorted_ascending1(lang_data), "Data is not sorted ascending."
            #
            # self.click_date_added()
            # time.sleep(10)
            # lang_data = self.fetch_column_data(column_index=4)
            # print("Data after first sort:", lang_data)
            # assert self.is_sorted_descending1(lang_data), "Data is not sorted ascending."
            # self.click_date_added()
            # time.sleep(10)
            # self.click_add_button()
            # time.sleep(10)
            # self.assert_word(self.get_remove_button(), 'Remove')
            # id = self.get_id_field1().text
            # self.refresh_and_click_force_login()
            # time.sleep(10)
            # self.click_expand2()
            # time.sleep(1)
            # self.click_search_id_w()
            # time.sleep(1)
            # self.input_id(id)
            # time.sleep(1)
            # self.press_return_key()
            # time.sleep(10)
            # self.assert_word(self.get_id_field_watchlist(), id)
            # self.click_REMOVE_B2()
            # self.refresh_and_click_force_login()
            # time.sleep(10)
            #
            # self.compare_data_for_periods()
            # self.refresh_and_click_force_login()
            # self.drag_and_drop_by_coordinates(
            #     source_xpath='//*[@id="root"]/section/section/main/div/div/div/div/div[3]/div')
            # time.sleep(3)
            # self.click_pages_100()
            # time.sleep(3)
            # self.click_pages_10()
            # time.sleep(3)
            # self.click_pluses()
            # time.sleep(20)
            # self.click_pluses()
            # time.sleep(3)
            # data = self.fetch_QAd()  # предполагается, что это ваш метод, который возвращает данные в текущем формате
            # transformed_data = self.transform_data(data)
            #
            #
            now = datetime.now(timezone.utc)
            start_of_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            start_of_last_month = (start_of_current_month - timedelta(days=1)).replace(day=1)
            end_of_last_month = start_of_current_month - timedelta(seconds=1)

            query = [
                {
                    "$match": {
                        "monitorStartTime": {
                            "$gte": start_of_last_month,
                            "$lte": end_of_last_month
                        },
                        "invalid": False,
                        "monitorEndTime": {"$ne": None}
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "interpreter": "$interpreterId"
                        },
                        "score": {
                            "$avg": {
                                "$cond": [
                                    {"$ne": [{"$ifNull": ["$evaluationSubmitTime", None]}, None]},
                                    "$score",
                                    None
                                ]
                            }
                        },
                        "totalQaSessions": {"$sum": 1},
                        "totalEvaluatedSessions": {
                            "$sum": {
                                "$cond": [
                                    {"$ne": [{"$ifNull": ["$evaluationSubmitTime", None]}, None]},
                                    1,
                                    0
                                ]
                            }
                        },
                        "details": {
                            "$push": {
                                "startTime": "$startTime",
                                "endTime": "$endTime",
                                "monitorStartTime": "$monitorStartTime",
                                "monitorEndTime": "$monitorEndTime",
                                "evaluationSubmitTime": "$evaluationSubmitTime",
                                "totalEvaluationSeconds": "$totalEvaluationSeconds",
                                "totalMonitorSeconds": "$totalMonitorSeconds",
                                "totalQaSeconds": "$totalQaSeconds",
                                "requestId": "$requestId",
                                "qaSpecialistId": "$qaSpecialistId",
                                "score": "$score",
                                "qaSpecialistName": "$qaSpecialistName",
                                "interpreterName": "$interpreterName",
                                "interpreterId": "$interpreterId"
                            }
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "score": 1,
                        "totalQaSessions": 1,
                        "details": 1,
                        "scoreLabel": {
                            "$switch": {
                                "branches": [
                                    {
                                        "case": {
                                            "$and": [
                                                {"$gte": ["$score", 0]},
                                                {"$lt": ["$score", 50]}
                                            ]
                                        },
                                        "then": "NI"
                                    },
                                    {
                                        "case": {
                                            "$and": [
                                                {"$gte": ["$score", 50]},
                                                {"$lt": ["$score", 55]}
                                            ]
                                        },
                                        "then": "LME"
                                    },
                                    {
                                        "case": {
                                            "$and": [
                                                {"$gte": ["$score", 55]},
                                                {"$lt": ["$score", 59]}
                                            ]
                                        },
                                        "then": "ME"
                                    },
                                    {
                                        "case": {"$gte": ["$score", 59]},
                                        "then": "EE"
                                    }
                                ],
                                "default": "Unknown"
                            }
                        },
                        "monthlyQaStatus": {
                            "$switch": {
                                "branches": [
                                    {"case": {"$eq": ["$totalEvaluatedSessions", 0]}, "then": "New"},
                                    {"case": {"$eq": ["$totalEvaluatedSessions", 1]}, "then": "In Progress"},
                                    {"case": {"$gt": ["$totalEvaluatedSessions", 1]}, "then": "Completed"}
                                ],
                                "default": "Unknown"
                            }
                        }
                    }
                }
            ]

            try:
                cursor = self.client["auth"]["InterpreterScore"].aggregate(query)
                db_data = list(cursor)
                # print(" "
                #       " "
                #       " "
                #       " "
                #       " "
                #       " "
                #       "Курсор успешно создан, документы загружены.", db_data)
            except Exception as e:
                print("Ошибка при выполнении запроса к базе данных:", e)

            # self.compare_monitoring_records(frontend_data=transformed_data, db_data=db_data)
            # self.click_completed_tab()
            # self.click_last_100_completed_in_table()
            # self.click_inprogress_tab()
            # self.click_last_100_inprogress_in_table()
            # self.driver.refresh()
            time.sleep(15)
            self.click_list()  # Открытие списка, если это необходимо
            self.double_press_down_arrow()
            time.sleep(10)  # Короткая задержка, чтобы убедиться, что список открыт
            self.click_last_month()
            self.click_expand_qa_Analysis()
            time.sleep(30)
            self.click_pluses()
            time.sleep(3)
            element = self.driver.find_element(By.XPATH,
                                               '//*[@id="qa-analysis-table-expanded"]/div/div/table/thead/tr/th[1]/div/span[1]')
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(40)
            self.click_pluses()
            time.sleep(100)
            data = self.fetch_QA_analysis()
            pdata = self.process_qa_data(db_data)
            tdata = self.transform_data1(data)
            self.match_data_F_DB(pdata, tdata)


# def run_authorization(driver, url, login, password):
#     try:
#         driver.get(url)
#         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "email"))).send_keys(login)
#         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
#         WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Sign In"]'))).click()
#         time.sleep(10)
#         WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section/aside/div/ul/li[9]/div'))).click()
#         time.sleep(10)
#         WebDriverWait(driver, 999).until(
#             EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'ant-menu-item') and .//a[text()='Quality Assurance HUD']]"))).click()
#         time.sleep(10)
#     finally:
#         driver.quit()
#
#
# def test_parallel_authorizations():
#     url = 'https://staging.admin.vip.voyceglobal.com/auth/login'
#     login = 'nikita.barshchuk'
#     password = 'Admin@123'
#     driver_path = '/Users/nikitabarshchuk/PycharmProjects/pythonProject3/chromedriver'
#
#     chrome_options = Options()
#     service = ChromeService(executable_path=driver_path)
#
#     # Создание потоков для параллельного выполнения
#     threads = []
#     for _ in range(2):
#         driver = webdriver.Chrome(service=service, options=chrome_options)
#         thread = threading.Thread(target=run_authorization, args=(driver, url, login, password))
#         threads.append(thread)
#         thread.start()
#
#     for thread in threads:
#         thread.join()


def run_authorization(driver_path, url, login, password, xpath):
    """Функция для выполнения авторизации и проверки результатов."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2
    })

    service = ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.ID, "email"))).send_keys(login)
        WebDriverWait(driver, 999).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
        WebDriverWait(driver, 999).until(
            EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Sign In"]]'))
        ).click()

        if not is_number_greater_than_zero(driver, xpath):
            raise Exception("Number in the element is not greater than zero or not present")
    finally:
        driver.quit()


def test_parallel_authorizations():
    url = 'https://staging.admin.vip.voyceglobal.com/auth/login'
    login = 'nikita.barshchuk'
    password = 'Admin@123'
    driver_path = '/Users/nikitabarshchuk/PycharmProjects/pythonProject3/chromedriver'
    xpath = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]'

    threads = []
    for _ in range(20):
        thread = threading.Thread(target=run_authorization, args=(driver_path, url, login, password, xpath))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    test_parallel_authorizations()

# Основная функция для запуска тестов
#
