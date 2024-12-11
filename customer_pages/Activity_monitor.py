import shutil
import time
import pyautogui
import os
import glob
import csv
import math
import pandas as pd
import shutil
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import functools
import time
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


def is_equivalent_service_minutes(db_value, web_value):
    if (db_value in [None, '-', 0] and web_value in ['', '-', '0']) or str(db_value) == web_value:
        return True
    return False


class Activity_monitor(Graphs):

    def __init__(self, driver):
        super().__init__(driver)  # Это должно инициализировать метод __init__ класса Base
        self.driver = driver

    # Locators
    lang_f_ASL = '//*[@id="header-container-id"]/div/div[4]/div/label[4]/span[1]'
    lang_f_LOTS = '//*[@id="header-container-id"]/div/div[4]/div/label[3]'
    lang_f_Spanish = '//*[@id="header-container-id"]/div/div[4]/div/label[2]'
    check_in_id = "//*[@id='root']/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td/div/div/div/div/div[2]/div/table/tbody/tr/td[1]"
    check_in_name = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td/div/div/div/div/div[2]/div/table/tbody/tr/td[2]'

    plus = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]/button'
    buttons = "//button[@class='ant-table-row-expand-icon ant-table-row-expand-icon-collapsed' and @type='button']"
    activity_m_b = '//*[@id="root"]/section/aside/div/ul/li[3]'
    select_columns = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[1]/div/div[1]/button/span'
    service_s_t_column = '//div[@data-rbd-draggable-id="Service Start Time"]'
    cancel_c = "//div[@data-rbd-draggable-id='Time Zone']"
    target_column_xpath = '//div[text()="Transaction ID"]'
    ok = "//span[text()='OK']"
    check_added_c = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[1]'

    Service_Start_Time_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[1]'
    Transaction_ID_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[2]/div/span[1]/div/span[1]'
    Transaction_ID_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[2]/div/span[2]'
    Transaction_ID_s_f = "//input[@placeholder='Search ReferenceTransactionId']"
    Product_Name_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[3]/div/span[1]'
    Product_Name_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[3]/div/span[2]/span'
    Product_Name_s_f = "//input[@placeholder='Search RequestProductName']"
    Request_Date_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[4]/div/span[1]/div/span[1]'
    Request_Date_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[4]/div/span[2]/span'
    Request_Date_s_f = "//input[@placeholder='Search RequestDate']"
    Request_Time_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[5]/div/span[2]/span'
    start_time = "//input[@placeholder='Start Time']"
    end_time = "//input[@placeholder='End Time']"
    Request_Time_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[5]/div/span[1]/div/span[1]'
    Client_name_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[6]/div/span[1]/div'
    Client_name_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[6]/div/span[2]/span'
    Clirnt_name_s_f = "//input[@placeholder='Search ClientName' and @type='text']"
    Client_name_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[7]'
    Client_name_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[7]'
    Target_Language_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[7]/div/span[1]'
    Target_Language_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[7]/div/span[2]/span'
    Target_Language_s_f = "//input[@placeholder='Search TargetLanguage']"
    Target_Language_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[8]'
    Target_Language_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[8]'
    Audio_video_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[8]/div/span[1]/div'
    Audio_video_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[8]/div/span[2]/span'
    Audio_video_s_f = "//input[@placeholder='Search VideoOption']"
    Audio_video_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[9]'
    Audio_video_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[9]'
    WaitingSeconds_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[10]/div/span[1]'
    WaitingSeconds_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[10]/div/span[2]/span'
    WaitingSeconds_s_f = "//input[@placeholder='Search WaitingSeconds']"
    WaitingSeconds_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[11]'
    WaitingSeconds_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[11]'
    service_minutes_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[11]/div/span[2]'
    service_minutes_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[11]/div/span[2]/span'
    service_minutes_s_f = "//input[@placeholder='Search ServiceMinutes']"
    service_minutes_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[12]'
    service_minutes_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[12]'
    first_object = "//span[@class='ant-radio-inner']"

    Interpriter_Name_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[12]/div/span[2]/span'
    Interpriter_Name_s_f = "//input[@placeholder='Search InterpreterFirstName']"
    Interpriter_Name_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[13]'
    Interpriter_Name_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[13]'

    serial_number_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[18]/div/span[2]/span'
    serial_number_s_f = "//input[@placeholder='Search IOSSerialNumber']"
    serial_number_cell = '//*[@id="scrollableDiv"]/div/div/div/label[1]/span[2]/span/strong'
    serial_number_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[19]'

    Client_User_Name_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[19]/div/span[1]/div'
    Client_User_Name_s_f = "//input[@placeholder='Search UserName']"
    Client_User_Name_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[19]/div/span[2]/span'
    Client_User_Name_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[20]'
    Client_User_Name_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[20]'

    Interpriter_id_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[13]/div/span[1]/div'
    Interpriter_id_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[13]/div/span[2]/span'
    Interpriter_id_s_f = "//input[@placeholder='Search InterpreterId']"
    Interpriter_id_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[14]'
    Interpriter_id_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[14]'
    Cancel_time_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[14]/div/span[1]'
    Caller_id_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[17]/div/span[2]/span'
    Caller_id_s_f = "//input[@placeholder='Search CallerID']"
    Caller_id_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[18]'
    Caller_id_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[18]'

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
    search_b = "//span[text()='Search']"

    download_b = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[1]/div/div[3]/div/div[2]/button'
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
    element_xpath = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[1]/div/div[1]/button'
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
    tr_id_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[3]'
    tr_id_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[3]'
    pr_n_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[4]'
    pr_n_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[4]'
    req_d_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[5]'
    req_d_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[5]'
    r_time_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[6]'
    r_time_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[6]'
    status_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[9]/div/span[2]/span'
    status_s_f = "//input[@placeholder='Search Status']"
    status_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[10]'
    status_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[10]'
    search_sf = "//button[span[contains(text(), 'Search')]]"

    # Getters
    def get_search_sf(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.search_sf)))

    def get_lang_f_ASL(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_f_ASL)))

    def get_lang_f_LOTS(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_f_LOTS)))

    def get_lang_f_Spanish(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.lang_f_Spanish)))

    def get_check_in_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_in_name)))

    def get_check_in_id(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_in_id)))

    def get_plus(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.plus)))

    def get_Interpriter_Name_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Interpriter_Name_s)))

    def get_Interpriter_Name_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Interpriter_Name_s_f)))

    def get_Interpriter_Name_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Interpriter_Name_cell)))

    def get_Interpriter_Name_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Interpriter_Name_cell1)))

    def get_status_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.status_cell)))

    def get_status_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.status_cell1)))

    def get_status_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.status_s_f)))

    def get_status_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.status_s)))

    def get_Client_name_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Client_name_f)))

    def get_Client_name_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Client_name_s)))

    def get_Clirnt_name_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Clirnt_name_s_f)))

    def get_Client_name_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Client_name_cell)))

    def get_Client_name_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Client_name_cell1)))

    def get_r_time_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.r_time_cell1)))

    def get_r_time_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.r_time_cell)))

    def get_req_d_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.req_d_cell1)))

    def get_target_column(self):
        return WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.target_column_xpath)))

    def get_req_d_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.req_d_cell)))

    def get_pr_n_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.pr_n_cell1)))

    def get_pr_n_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.pr_n_cell)))

    def get_tr_id_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.tr_id_cell)))

    def get_tr_id_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.tr_id_cell1)))

    def get_buttons(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.buttons)))

    def get_check_added_c(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_added_c)))

    def get_ok(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ok)))

    def get_reset_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.reset_b)))

    def get_select_columns(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.select_columns)))

    def get_service_s_t_column(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.service_s_t_column)))

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

    def get_Transaction_ID_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Transaction_ID_f)))

    def get_activity_m_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.activity_m_b)))

    def get_Transaction_ID_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Transaction_ID_s_f)))

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

    def get_Transaction_ID_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Transaction_ID_s)))

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

    def get_Service_Start_Time_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Service_Start_Time_f)))

    def get_Product_Name_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Product_Name_f)))

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

    def get_Product_Name_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Product_Name_s)))

    def get_Product_Name_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Product_Name_s_f)))

    def get_Request_Date_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Request_Date_f)))

    def get_Request_Date_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Request_Date_s)))

    def get_Request_Date_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Request_Date_s_f)))

    def get_Request_Time_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Request_Time_s)))

    def get_start_time(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.start_time)))

    def get_end_time(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.end_time)))

    def get_Request_Time_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Request_Time_f)))

    def get_Target_Language_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Target_Language_f)))

    def get_Target_Language_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Target_Language_s)))

    def get_Target_Language_s_f(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.Target_Language_s_f)))

    def get_Target_Language_cell(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.Target_Language_cell)))

    def get_Target_Language_cell1(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.Target_Language_cell1)))

    def get_Audio_video_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Audio_video_f)))

    def get_Audio_video_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Audio_video_s)))

    def get_first_object(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.first_object)))

    def get_Audio_video_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Audio_video_s_f)))

    def get_Audio_video_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Audio_video_cell)))

    def get_Audio_video_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Audio_video_cell1)))

    def get_WaitingSeconds_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.WaitingSeconds_f)))

    def get_WaitingSeconds_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.WaitingSeconds_s)))

    def get_WaitingSeconds_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.WaitingSeconds_s_f)))

    def get_WaitingSeconds_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.WaitingSeconds_cell)))

    def get_WaitingSeconds_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.WaitingSeconds_cell1)))

    def get_service_minutes_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.service_minutes_f)))

    def get_service_minutes_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.service_minutes_s)))

    def get_service_minutes_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.service_minutes_s_f)))

    def get_service_minutes_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.service_minutes_cell)))

    def get_service_minutes_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.service_minutes_cell1)))

    def get_Interpriter_id_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Interpriter_id_f)))

    def get_Interpriter_id_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Interpriter_id_s)))

    def get_Interpriter_id_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Interpriter_id_s_f)))

    def get_Interpriter_id_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Interpriter_id_cell)))

    def get_Interpriter_id_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Interpriter_id_cell1)))

    def get_Cancel_time_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Cancel_time_f)))

    def get_Caller_id_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Caller_id_s)))

    def get_Caller_id_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Caller_id_s_f)))

    def get_Caller_id_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Caller_id_cell)))

    def get_Caller_id_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Caller_id_cell1)))

    def get_serial_number_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.serial_number_s)))

    def get_serial_number_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.serial_number_s_f)))

    def get_serial_number_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.serial_number_cell)))

    def get_serial_number_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.serial_number_cell1)))

    def get_Client_User_Name_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Client_User_Name_f)))

    def get_Client_User_Name_s(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Client_User_Name_s)))

    def get_Client_User_Name_s_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Client_User_Name_s_f)))

    def get_Client_User_Name_cell(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Client_User_Name_cell)))

    def get_Client_User_Name_cell1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Client_User_Name_cell1)))

    # Actions
    def click_Client_User_Name_f(self):
        self.get_Client_User_Name_f().click()
        print("CLICK Client_User_Name_f")

    def click_Client_User_Name_s(self):
        first_company = self.get_Client_User_Name_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Client_User_Name_s")

    def input_Client_User_Name(self, user_name):
        self.get_Client_User_Name_s_f().send_keys(user_name)
        print("Input Client User Name")

    def click_serial_number_s(self):
        self.get_serial_number_s().click()
        print("CLICK serial_number Search")

    def input_serial_number(self, number):
        self.get_serial_number_s_f().send_keys(number)
        print("Input Serial Number")

    def click_Caller_id_s(self):
        first_company = self.get_Caller_id_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Caller_id Search")

    def input_Caller_id(self, id):
        self.get_Caller_id_s_f().send_keys(id)
        print("Input Caller ID")

    def click_Cancel_time_f(self):
        self.get_Cancel_time_f().click()
        print("CLICK Cancel_time_f")

    def click_Interpriter_id_f(self):
        first_company = self.get_Interpriter_id_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Interpriter_id_f")

    def click_Interpriter_id_s(self):
        first_company = self.get_Interpriter_id_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Interpriter_id_s")

    def input_Interpriter_id(self, id):
        self.get_Interpriter_id_s_f().send_keys(id)
        print("Input Interpreter ID")

    def click_service_minutes_f(self):
        first_company = self.get_service_minutes_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK service_minutes_f")

    def click_service_minutes_s(self):
        self.get_service_minutes_s().click()
        print("CLICK service_minutes_s")

    def input_service_minutes(self, minutes):
        self.get_service_minutes_s_f().send_keys(minutes)
        print("Input Service Minutes")

    def click_WaitingSeconds_f(self):
        first_company = self.get_WaitingSeconds_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK WaitingSeconds_f")

    def click_WaitingSeconds_s(self):
        self.get_WaitingSeconds_s().click()
        print("CLICK WaitingSeconds_s")

    def input_WaitingSeconds(self, waiting_time):
        self.get_WaitingSeconds_s_f().send_keys(waiting_time)
        print("Input Waiting Seconds")

    def click_Audio_video_f(self):
        first_company = self.get_Audio_video_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Audio_video_f")

    def click_Audio_video_s(self):
        self.get_Audio_video_s().click()
        print("CLICK Audio_video_s")

    def input_Audio_video(self, video_option):
        self.get_Audio_video_s_f().send_keys(video_option)
        print("Input Video Option")

    def clear_input_field(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click()
        actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND)
        actions.send_keys(Keys.DELETE)
        actions.perform()

    def click_Target_Language_f(self):
        self.get_Target_Language_f().click()
        print("CLICK Target_Language_f")

    def click_Target_Language_s(self):
        first_company = self.get_Target_Language_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Target_Language_s")

    def input_Target_Language(self, language):
        self.get_Target_Language_s_f().send_keys(language)
        print("Input Target Language")

    def click_ok(self):
        self.get_ok().click()
        print("CLICK Ok")

    def click_activity_m_b(self):
        self.get_activity_m_b().click()
        print("CLICK Terp button")

    def click_select_columns(self):
        self.get_select_columns().click()
        print("CLICK select columns button")

    def get_element_coordinates(self, xpath):
        element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
        location = element.location
        size = element.size
        x_center = location['x'] + size['width'] / 2
        y_center = location['y'] + size['height'] / 2
        print(f"Центр элемента находится на координатах X: {x_center}, Y: {y_center}")
        return x_center, y_center

    def click_calls_f(self):
        self.get_calls_f().click()
        print("CLICK calls filter")

    def click_first_object(self):
        first_company = self.get_first_object()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK calls filter")

    def click_answered_f(self):
        self.get_answered_f().click()
        print("CLICK answered filter")

    def click_Service_Start_Time_f(self):
        first_company = self.get_Service_Start_Time_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("click Service Start Time filter")

    def click_first_company(self):
        first_company = self.get_first_company()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("Clicked first_company")

    def click_all_clients(self):
        self.get_all_clients().click()
        print("CLICK all clients")

    def click_Client_name_f(self):
        first_company = self.get_Client_name_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Client_name_f")

    def click_Client_name_s(self):
        self.get_Client_name_s().click()
        print("CLICK Client_name_s")

    def input_Client_name(self, name):
        self.get_Clirnt_name_s_f().send_keys(name)
        print("Input Client Name")

    def click_Transaction_ID_s(self):
        first_company = self.get_Transaction_ID_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Transaction_ID_s")

    def click_Transaction_ID_f(self):
        self.get_Transaction_ID_f().click()
        print("CLICK Transaction_ID_f")

    def click_Interpriter_Name_s(self):
        self.get_Interpriter_Name_s().click()
        print("CLICK Interpriter_Name Search")

    def input_Interpriter_Name(self, name):
        self.get_Interpriter_Name_s_f().send_keys(name)
        print("Input Interpreter Name")

    def click_Product_Name_f(self):
        first_company = self.get_Product_Name_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Product_Name_f")

    def click_Product_Name_s(self):
        first_company = self.get_Product_Name_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Product_Name_s")

    def click_Request_Date_f(self):
        self.get_Request_Date_f().click()
        print("CLICK Request_Date_f")

    def click_Request_Date_s(self):
        first_company = self.get_Request_Date_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Request_Date_s")

    def click_Request_Time_s(self):
        first_company = self.get_Request_Time_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Request_Time_s")

    def click_status_s(self):
        first_company = self.get_status_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Status Search icon")

    def click_plus(self):
        self.get_plus().click()
        print("CLICK Plus")

    def click_Request_Time_f(self):
        first_company = self.get_Request_Time_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Request_Time_f")

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
        self.get_interpreter_id().click()
        print("CLICK interpreter id")

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

    def input_status(self, language):
        self.get_status_s_f().send_keys(language)
        print("Input Text")

    def input_start_time(self, language):
        self.get_start_time().send_keys(language)
        print("Input Text")

    def input_end_time(self, language):
        self.get_end_time().send_keys(language)
        print("Input Text")

    def input_tr_id(self, language):
        self.get_Transaction_ID_s_f().send_keys(language)
        print("Input Text")

    def input_pr_n(self, language):
        self.get_Product_Name_s_f().send_keys(language)
        print("Input Text")

    def input_date(self, language):
        self.get_Request_Date_s_f().send_keys(language)
        print("Input Text")

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

    def click_lang_f_Spanish(self):
        first_company = self.get_lang_f_Spanish()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK lang_f_Spanish")

    def click_lang_f_LOTS(self):
        first_company = self.get_lang_f_LOTS()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK lang_f_LOTS")

    def click_lang_f_ASL(self):
        first_company = self.get_lang_f_ASL()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK lang_f_ASL")

    def click_download_b(self):
        first_company = self.get_download_b()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Download")

    def click_buttons(self):
        buttons = self.get_buttons()

        # Проходимся по каждой кнопке и кликаем на нее
        for button in buttons:
            button.click()

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

    def fetch_website_data_am_cvs(self):
        rows = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
        )

        website_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            # Убедитесь, что в строке достаточно ячеек для извлечения данных
            if len(cells) >= 17:
                website_data.append({
                    "TransactionID": cells[1].text.strip(),
                    "ProductName": cells[2].text.strip(),
                    "RequestDate": cells[3].text.strip(),
                    "RequestTime": cells[4].text.strip(),
                    "ClientName": cells[5].text.strip(),
                    "TargetLanguage": cells[6].text.strip(),
                    "AudioVideo": cells[7].text.strip(),
                    "Status": cells[8].text.strip(),
                    "WaitingSeconds": cells[9].text.strip(),
                    "ServiceMinutes": cells[10].text.strip() if cells[10].text.strip() else None,
                    "InterpreterName": cells[11].text.strip(),
                    "InterpreterID": cells[12].text.strip(),
                    "CancelTime": cells[13].text.strip(),
                    "Cost": cells[14].text.strip(),
                    "StarRating": cells[15].text.strip(),
                    "CallerID": cells[16].text.strip(),
                    "SerialNumber": cells[17].text.strip(),
                    "ClientUserName": cells[18].text.strip() if len(cells) > 18 else None,
                })
            else:
                print(f"Not enough cells in the row to extract data: {row.text}")

        return website_data

    def fetch_website_data_am1(self):
        rows = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
        )

        website_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 10:  # Убедитесь, что в строке достаточно ячеек для извлечения данных
                target_language = cells[6].text.strip()
                if target_language:  # Проверяем, что поле языка не пустое
                    website_data.append({
                        "TransactionID": cells[1].text.strip(),
                        "ProductName": cells[2].text.strip(),
                        "RequestDate": cells[3].text.strip(),
                        "RequestTime": cells[4].text.strip(),
                        "ClientName": cells[5].text.strip(),
                        "TargetLanguage": cells[6].text.strip(),
                        "AudioVideo": cells[7].text.strip(),
                        "Status": cells[8].text.strip(),
                        "WaitingSeconds": cells[9].text.strip(),
                        "ServiceMinutes": cells[10].text.strip() if len(cells) > 10 else None,
                        # Проверяем, есть ли данные в 13-й ячейке
                    })
                print(f"{target_language}")
            else:
                print("None Language")

        return website_data

    def is_equivalent_servic(self, db_value, web_value):
        if (db_value in [None, '-', 0] and web_value in ['', '-', '0']) or str(db_value) == web_value:
            return True
        return False

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

    def compare_data_am_t(self, web_data, db_data):
        if db_data is None:
            raise ValueError("db_data не может быть None")

        discrepancies = []
        for web_row in web_data:
            db_row = next((item for item in db_data if str(item.ReferenceTransactionId) == web_row["TransactionID"]),
                          None)

            if db_row:
                if db_row.RequestProductName != web_row["ProductName"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: ProductName DB({db_row.RequestProductName}) != Web({web_row['ProductName']})")
                if db_row.Date.strftime('%Y-%m-%d') != web_row["RequestDate"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: RequestDate DB({db_row.Date.strftime('%Y-%m-%d')}) != Web({web_row['RequestDate']})")

                db_time = datetime.strptime(db_row.ExtractedTime, '%H:%M:%S')
                db_time_adjusted = db_time - timedelta(hours=4)  # Вычитаем 5 часов
                web_time = datetime.strptime(web_row["RequestTime"], '%H:%M:%S')

                if db_time_adjusted.time() != web_time.time():
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: RequestTime DB({db_time_adjusted.strftime('%H:%M:%S')}) != Web({web_row['RequestTime']})")
                if db_row.ClientName != web_row["ClientName"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: ClientName DB({db_row.ClientName}) != Web({web_row['ClientName']})")
                if db_row.TargetLanguage != web_row["TargetLanguage"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: TargetLanguage DB({db_row.TargetLanguage}) != Web({web_row['TargetLanguage']})")
                if db_row.VideoOption.lower() != web_row["AudioVideo"].lower():
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: AudioVideo DB({db_row.VideoOption}) != Web({web_row['AudioVideo']})")
                if db_row.Status != web_row["Status"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: Status DB({db_row.Status}) != Web({web_row['Status']})")
                if str(db_row.WaitingSeconds) != web_row["WaitingSeconds"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: WaitingSeconds DB({db_row.WaitingSeconds}) != Web({web_row['WaitingSeconds']})")
                if not is_equivalent_service_minutes(db_row.ServiceMinutes, web_row["ServiceMinutes"]):
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: ServiceMinutes DB({db_row.ServiceMinutes if db_row.ServiceMinutes is not None else '-'}) != Web({web_row['ServiceMinutes']})")

        if discrepancies:
            for discrepancy in discrepancies:
                print(discrepancy)
            raise AssertionError("Discrepancies were found during the data comparison.")
        else:
            print("No discrepancies found.")

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

        website_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 10:  # Убедитесь, что в строке достаточно ячеек для извлечения данных
                website_data.append({
                    "TransactionID": cells[1].text.strip(),
                    "ProductName": cells[2].text.strip(),
                    "RequestDate": cells[3].text.strip(),
                    "RequestTime": cells[4].text.strip(),
                    "ClientName": cells[5].text.strip(),
                    "TargetLanguage": cells[6].text.strip(),
                    "AudioVideo": cells[7].text.strip(),
                    "Status": cells[8].text.strip(),
                    "WaitingSeconds": cells[9].text.strip(),
                    "ServiceMinutes": cells[10].text.strip() if len(cells) > 10 else None,
                    # Проверяем, есть ли данные в 13-й ячейке
                })
            else:
                print(f"Not enough cells in the row to extract data: {row.text}")
        return website_data

    def compare_data_dashboard_DB(self, website_data, db_data):
        for web_record in website_data:
            interpreter_id = web_record["InterpreterID"]
            matched_db_record = next((item for item in db_data if str(item.InterpreterID) == interpreter_id), None)

            if matched_db_record:
                # Сравнение InterpreterName
                print(
                    f"Comparing InterpreterName for ID {interpreter_id}: Web='{web_record['InterpreterName']}' vs DB='{matched_db_record.InterpreterName}'")
                assertpy.assert_that(web_record["InterpreterName"]).is_equal_to(matched_db_record.InterpreterName)

                # Сравнение Language
                web_language = web_record["Language"]
                db_languages = matched_db_record.UniqueTargetLanguages
                print(f"Comparing Language for ID {interpreter_id}: Web='{web_language}' vs DB='{db_languages}'")
                assertpy.assert_that(db_languages).contains(web_language)

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

                if matched_db_record.TotalCalls > 0:
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
                print(f"Comparing Language: Web='{web_record['Language']}' vs API='{api_languages}'")
                assert web_record["Language"] in api_languages, f"Language mismatch for {interpreter_id}"

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
                if matched_api_record["TotalCalls"] > 0:
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
            self.double_press_down_arrow()
        time.sleep(10)  # Короткая задержка, чтобы убедиться, что список открыт
        getattr(self, f"click_{time_period}")()
        time.sleep(30)  # Ожидание обновления данных

    def compare_data_for_periods(self):
        with allure.step("Compare data with DB by Periods"):
            time_periods = ['last_30_days', 'this_week', 'this_month', 'this_year', 'last_week', 'yesterday',
                            'last_month', 'last_year']
            for period in time_periods:
                self.take_data_for_period_and_compare(period)

    def take_data_for_period_and_compare(self, time_period):
        self.select_time_period_and_wait_for_update(time_period)  # Устанавливаем фильтр на веб-сайте
        website_data = self.fetch_website_data_am()  # Получение данных с сайта
        db_data = self.query_activity_m_periods(time_period)  # Получение данных из базы данных

        if db_data and website_data:
            self.compare_data_am_t_periods(website_data, db_data)
        else:
            print(f"No data found for period '{time_period}'")

    def compare_data_am_t_periods(self, web_data, db_data):
        discrepancies = []

        for web_row in web_data:
            db_row = next((item for item in db_data if str(item.ReferenceTransactionId) == web_row["TransactionID"]),
                          None)

            if db_row:
                if db_row.RequestProductName != web_row["ProductName"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: ProductName DB({db_row.RequestProductName}) != Web({web_row['ProductName']})")
                if db_row.Date.strftime('%Y-%m-%d') != web_row["RequestDate"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: RequestDate DB({db_row.Date.strftime('%Y-%m-%d')}) != Web({web_row['RequestDate']})")

                db_time = datetime.strptime(db_row.ExtractedTime, '%H:%M:%S')
                db_time_adjusted = db_time - timedelta(hours=5)  # Вычитаем 5 часов
                web_time = datetime.strptime(web_row["RequestTime"], '%H:%M:%S')

                if db_time_adjusted.time() != web_time.time():
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: RequestTime DB({db_time_adjusted.strftime('%H:%M:%S')}) != Web({web_row['RequestTime']})")
                if db_row.ClientName != web_row["ClientName"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: ClientName DB({db_row.ClientName}) != Web({web_row['ClientName']})")
                if db_row.TargetLanguage != web_row["TargetLanguage"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: TargetLanguage DB({db_row.TargetLanguage}) != Web({web_row['TargetLanguage']})")
                if db_row.VideoOption.lower() != web_row["AudioVideo"].lower():
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: AudioVideo DB({db_row.VideoOption}) != Web({web_row['AudioVideo']})")
                if db_row.Status != web_row["Status"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: Status DB({db_row.Status}) != Web({web_row['Status']})")
                if str(db_row.WaitingSeconds) != web_row["WaitingSeconds"]:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: WaitingSeconds DB({db_row.WaitingSeconds}) != Web({web_row['WaitingSeconds']})")

                db_service_minutes = str(db_row.ServiceMinutes) if db_row.ServiceMinutes is not None else "-"
                web_service_minutes = web_row["ServiceMinutes"] if web_row["ServiceMinutes"] != '0' else "-"

                if db_service_minutes != web_service_minutes:
                    discrepancies.append(
                        f"Discrepancy for {web_row['TransactionID']}: ServiceMinutes DB({db_service_minutes}) != Web({web_service_minutes})")

        if discrepancies:
            for discrepancy in discrepancies:
                print(discrepancy)
            print("Discrepancies were found during the data comparison.")
        else:
            print("No discrepancies found.")

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

    def calculate_missed_percent(self, db_record):
        if db_record.TotalCalls > 0:
            return round(db_record.TotalCallsMissed * 100 / db_record.TotalCalls)
        else:
            return 0

    def calculate_avg_wait_time(self, db_record):
        if db_record.TotalCalls > 0:
            return round(db_record.TotalWaitTime / db_record.TotalCalls)
        else:
            return 0

    def check_language_sorted_S(self, website_data):
        # Язык для проверки
        language_to_check = 'Spanish'
        # Проверяем, что язык каждой транзакции - Spanish
        check_result = all(item['TargetLanguage'] == language_to_check for item in website_data)
        return check_result, language_to_check

    def check_language_sorted_ASL(self, website_data):
        # Язык для проверки
        language_to_check = 'American Sign Language (ASL)'
        # Проверяем, что язык каждой транзакции - ASL
        check_result = all(item['TargetLanguage'] == language_to_check for item in website_data)
        return check_result, language_to_check

    def check_language_sorted_LOTS(self, website_data):
        # Языки для исключения
        languages_to_exclude = ['Spanish', 'American Sign Language (ASL)']
        # Проверяем, что язык каждой транзакции не является Spanish или ASL
        check_result = all(item['TargetLanguage'] not in languages_to_exclude for item in website_data)
        return check_result, languages_to_exclude

    def drag_and_drop_by_coordinates(self, source_xpath, target_xpath):
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
        target_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, target_xpath))
        )
        target_location = target_element.location
        target_x = window_x + target_location['x']
        target_y = window_y + target_location['y']

        # Переместите мышь к исходному элементу и нажмите
        y_offset = 210
        x_offset = 100
        # Перемещение мыши и действия перетаскивания
        time.sleep(5)
        pyautogui.moveTo(source_x + x_offset, source_y + y_offset, duration=1)
        time.sleep(5)
        pyautogui.mouseDown()
        time.sleep(5)
        pyautogui.moveTo(target_x + x_offset, target_y + y_offset, duration=1)
        time.sleep(5)
        pyautogui.mouseUp()

    def drag_and_drop_by_coordinates1(self, source_xpath, target_xpath):
        # Получите размер окна браузера и его позицию
        window_rect = self.driver.get_window_rect()
        window_x = window_rect['x']
        window_y = window_rect['y']

        # Найдите элемент, который вы хотите перетаскивать
        source_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, source_xpath))
        )

        # Получите относительные координаты исходного элемента
        source_location = source_element.location
        source_x = window_x + source_location['x']
        source_y = window_y + source_location['y']

        # Найдите целевой элемент
        target_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, target_xpath))
        )
        target_location = target_element.location
        target_x = window_x + target_location['x']
        target_y = window_y + target_location['y']

        # Переместите мышь к исходному элементу и нажмите
        y_offset = 210
        x_offset = 100
        # Перемещение мыши и действия перетаскивания
        time.sleep(4)
        pyautogui.moveTo(source_x + x_offset, source_y + y_offset, duration=1)
        time.sleep(4)
        pyautogui.mouseDown()
        time.sleep(4)
        pyautogui.moveTo(target_x + x_offset, target_y + y_offset, duration=1)
        time.sleep(5)
        pyautogui.mouseUp()

    def move_to_element_and_click_js(self, element_xpath):
        # Ожидание появления элемента и получение его
        element_to_click = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )

        # Прокрутка страницы к элементу с помощью JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element_to_click)

        # Ожидание, чтобы убедиться, что элемент в видимой области и может быть кликнут
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, element_xpath))
        )

        # Выполнение клика с помощью JavaScript
        self.driver.execute_script("arguments[0].click();", element_to_click)

        print("Выполнен клик на элемент с помощью JavaScript")

    def extract_column_names(self, xpath):
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        return [element.text for element in elements]

    def compare_columns_and_click_ok(self):
        first_element_xpath = "//div[@data-rbd-droppable-id='selected' and @data-rbd-droppable-context-id='0']"
        second_element_xpath = "//*[@id='root']/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]"

        first_column_names = self.extract_column_names(first_element_xpath)
        self.click_ok()  # Предполагая, что метод click_ok() уже определен в классе
        # Ожидание обновления страницы
        time.sleep(3)  # Пример задержки, настраивается по необходимости
        second_column_names = self.extract_column_names(second_element_xpath)

        if first_column_names == second_column_names:
            print("Column names match.")
        else:
            print("Column names NOT match.")

    # def drag_and_drop_by_coordinates(self, source_xpath, target_xpath):
    #     # Найдите элемент, который вы хотите перетаскивать
    #     source_element = self.driver.find_element(By.XPATH, source_xpath)
    #     # Прокрутите страницу до элемента
    #     self.driver.execute_script("arguments[0].scrollIntoView(true);", source_element)
    #     # Ожидание, чтобы убедиться, что элемент видим и можно с ним взаимодействовать
    #     WebDriverWait(self.driver, 10).until(EC.visibility_of(source_element))
    #
    #     # Получите координаты и размеры исходного элемента
    #     source_location = source_element.location
    #     source_size = source_element.size
    #     source_x_center = source_size['width'] // 2
    #     source_y_center = source_size['height'] // 2
    #
    #     # Кликните по элементу, чтобы сфокусироваться на нем
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element_with_offset(source_element, source_x_center, source_y_center)
    #     actions.click().perform()
    #
    #     # Найдите элемент, куда вы хотите перетаскивать
    #     target_element = self.driver.find_element(By.XPATH, target_xpath)
    #     # Ожидание, чтобы убедиться, что элемент видим и можно с ним взаимодействовать
    #     WebDriverWait(self.driver, 10).until(EC.visibility_of(target_element))
    #
    #     # Получите координаты и размеры целевого элемента
    #     target_location = target_element.location
    #     target_size = target_element.size
    #     target_x_center = target_location['x'] + target_size['width'] // 2
    #     target_y_center = target_location['y'] + target_size['height'] // 2
    #
    #     # Вычислите смещение от исходного элемента к центру целевого элемента
    #     offset_x = target_x_center - (source_location['x'] + source_x_center)
    #     offset_y = target_y_center - (source_location['y'] + source_y_center)
    #
    #     # Нажмите на исходный элемент, удерживайте и перетащите его в центр целевого элемента
    #     actions.click_and_hold(source_element)
    #     actions.move_by_offset(offset_x, offset_y)
    #     actions.release().perform()

    def extract_full_text(self, xpath):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text

    def compare_data_cvs(self, web_data_list, csv_data_list):
        data_is_correct = True

        # Перебираем данные с вебсайта
        for web_data in web_data_list:
            transaction_id = web_data['TransactionID']

            # Пропускаем запись, если TransactionID пустой
            if not transaction_id.strip():
                continue

            matching_csv_data = next(
                (item for item in csv_data_list if str(item['ReferenceTransactionId']) == transaction_id), None)

            if matching_csv_data:
                if not self.compare_records_cvs(matching_csv_data, web_data):
                    print(f"Data mismatch for transaction ID: {transaction_id}")
                    data_is_correct = False
            else:
                print(f"No matching data found in CSV for transaction ID: {transaction_id}")
                data_is_correct = False

        if data_is_correct:
            print("All data matches correctly")

        return data_is_correct

    def click_role_dropdown(self):
        user_element = self.get_service_minutes_cell()
        self.driver.execute_script("arguments[0].scrollIntoView(true);", user_element)
        location = user_element.location
        size = user_element.size
        window_x = self.driver.get_window_rect()['x']
        window_y = self.driver.get_window_rect()['y']
        x = window_x + location['x'] + size['width'] / 2
        y = window_y + location['y'] + size['height'] / 2
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.click()
        print("CLICK role dropdown")

        # Нажать клавишу стрелки вправо 40 раз
        for _ in range(40):
            pyautogui.press('right')
        print("Pressed right arrow key 40 times")

        # Прокрутить страницу к самому верху
        self.driver.execute_script("window.scrollTo(0, 0);")
        print("Scrolled to the top")


    def scroll_to_right(self):
        # Имитация нажатия стрелки вниз на клавиатуре
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(5)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(5)

        # Ожидание появления ползунка скроллбара и получение его
        scrollbar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='root']/section/section/main/div/div/div/div/div/div/div/div[2]/div[3]/div"))
        )

        # Создание объекта ActionChains
        actions = ActionChains(self.driver)

        # Выполнение действия перетаскивания
        actions.click_and_hold(scrollbar).move_by_offset(600, 0).release().perform()

        print("Ползунок прокручен")

    def move_to_element_and_click(self):
        # Ожидание появления элемента и получение его
        element_xpath = "//*[@id='root']/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]/button"
        element_to_click = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, element_xpath))
        )

        # Создание объекта ActionChains
        actions = ActionChains(self.driver)

        # Перемещение к элементу и клик
        actions.move_to_element(element_to_click).click().perform()

        print("Курсор мыши был перемещен на элемент, и был выполнен клик")

    def compare_records_cvs(self, csv_record, web_record):
        keys_to_compare = {
            "ProductName": "RequestProductName",
            "RequestDate": "RequestTime",
            "RequestTime": "ExtractedTime",
            "ClientName": "ClientName",
            "TargetLanguage": "TargetLanguage",
            "AudioVideo": "VideoOption",
            "Status": "Status",
            "WaitingSeconds": "WaitingSeconds",
            "ServiceMinutes": "ServiceMinutes",
            "InterpreterName": "InterpreterFirstName",
            "InterpreterID": "InterpreterId",  # Исправлено здесь
            "CancelTime": "ServiceCancelTime",
            "Cost": "TotalPrice",  # Исправлено здесь
            "StarRating": "CallQualityRatingStar",
            "CallerID": "CallerID",
            "SerialNumber": "IOSSerialNumber",
            "ClientUserName": "UserName"
        }
        def format_value(value):
            if isinstance(value, str):
                value = value.strip()
            if value in ['invalid date', 'None', '-', '', '0']:  # добавлено '0'
                return None
            return value.lower()

        is_match = True
        for web_key, csv_key in keys_to_compare.items():
            csv_value = format_value(csv_record[csv_key]) if csv_key in csv_record and csv_record[csv_key] else None
            web_value = format_value(web_record[web_key]) if web_key in web_record and web_record[web_key] else None

            if csv_value != web_value:
                print(f"Mismatch in {web_key}: CSV - '{csv_value}', Web - '{web_value}'")
                is_match = False
            else:
                print(f"Match found for {web_key}: CSV - '{csv_value}', Web - '{web_value}'")  # Сообщение о совпадении

        return is_match

    def compare_columns_and_click_ok1(self):
        first_element_xpath = "//div[@data-rbd-droppable-id='selected' and @data-rbd-droppable-context-id='0']"
        second_element_xpath = "//*[@id='root']/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr"

        first_column_names = self.extract_column_names(first_element_xpath)
        print("Первый набор имен колонок:", first_column_names)

        self.click_ok()  # Предполагая, что метод click_ok() уже определен в классе
        self.driver.execute_script("document.body.style.zoom='50%'")

        # Ожидание обновления страницы
        time.sleep(10)  # Пример задержки, настраивается по необходимости

        second_column_names = self.extract_column_names(second_element_xpath)
        print("Второй набор имен колонок:", second_column_names)

        # Обработка специального случая, когда отсутствует перенос строки
        first_column_names = self.adjust_column_names(first_column_names)
        second_column_names = self.adjust_column_names(second_column_names)

        if first_column_names != second_column_names:
            raise AssertionError("Column names do NOT match.")
        print("Column names match.")

    def adjust_column_names(self, column_names):
        adjusted_names = []
        for name in column_names:
            # Разделяем строки, если 'Star Rating' не начинается с новой строки
            if 'Star Rating' in name and not name.startswith('Star Rating'):
                parts = name.split('Star Rating')
                adjusted_names.append(parts[0].strip())
                adjusted_names.append('Star Rating' + parts[1])
            else:
                adjusted_names.append(name)
        return adjusted_names
    def Activity_monitor(self):
        with allure.step("Activity Monitor"):
            Logger.add_start_step(method='Activity Monitor')
            self.driver.maximize_window()
            self.click_activity_m_b()
            self.get_current_url()
            time.sleep(3)
            self.screenshot()
            time.sleep(10)
            try:
                # Попытка проверить, был ли уже добавлен нужный столбец
                self.assert_word(self.get_check_added_c(), 'Service Start Time')
            except AssertionError:
                self.click_select_columns()
                self.drag_and_drop_by_coordinates(self.service_s_t_column, self.target_column_xpath)
                time.sleep(3)
                self.click_ok()
                time.sleep(5)
                self.assert_word(self.get_check_added_c(), 'Service Start Time')
            self.click_Service_Start_Time_f()
            time.sleep(3)  # Нажимаем на кнопку сортировки
            lang_data = self.fetch_column_data(column_index=1)
            print("Data after first sort:", lang_data)
            assert self.is_sorted_ascending1(lang_data), "Data is not sorted ascending."

            self.click_Service_Start_Time_f()
            time.sleep(6)  # Нажимаем на кнопку сортировки еще раз
            lang_data = self.fetch_column_data(column_index=1)
            print("Data after second sort:", lang_data)
            assert self.is_sorted_descending1(lang_data), "Data is not sorted descending."
            time.sleep(3)

            self.click_Transaction_ID_f()
            time.sleep(5)  # Нажимаем на кнопку сортировки
            lang_data = self.fetch_column_data(column_index=2)
            print("Data after first sort:", lang_data)
            assert self.is_sorted_ascending1(lang_data), "Data is not sorted ascending."

            self.click_Transaction_ID_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            lang_data = self.fetch_column_data(column_index=2)
            print("Data after first sort:", lang_data)
            assert self.is_sorted_descending1(lang_data), "Data is not sorted descending."
            time.sleep(3)
            self.click_Transaction_ID_s()
            time.sleep(2)
            id = self.get_tr_id_cell().text
            self.input_tr_id(id)
            time.sleep(3)
            self.get_search_sf().click()
            time.sleep(3)
            self.click_first_object()
            time.sleep(3)
            self.assert_word(self.get_tr_id_cell1(), id)
            self.driver.refresh()
            time.sleep(10)

            self.click_Product_Name_f()
            time.sleep(3)  # Нажимаем на кнопку сортировки
            lang_data = self.fetch_column_data(column_index=3)
            print("Data after first sort:", lang_data)
            assert self.is_sorted_ascending_l(lang_data), "Data is not sorted ascending."

            self.click_Product_Name_f()
            time.sleep(3)  # Нажимаем на кнопку сортировки
            lang_data = self.fetch_column_data(column_index=3)
            print("Data after first sort:", lang_data)
            assert self.is_sorted_descending_l(lang_data), "Data is not sorted descending."
            self.click_Product_Name_s()
            time.sleep(20)
            name = self.get_pr_n_cell().text
            time.sleep(5)
            self.get_Product_Name_s_f().click()
            time.sleep(5)
            self.input_pr_n(name)
            time.sleep(7)
            self.get_search_sf().click()
            time.sleep(7)
            self.click_first_object()
            time.sleep(5)
            self.assert_word(self.get_pr_n_cell1(), name)
            self.driver.refresh()
            time.sleep(10)

            self.click_Request_Date_s()
            date = self.get_req_d_cell().text
            self.input_date(date)
            time.sleep(3)
            self.get_search_sf().click()
            time.sleep(3)
            self.click_first_object()
            time.sleep(3)
            self.assert_word(self.get_req_d_cell1(), date)
            self.driver.refresh()
            time.sleep(10)

            self.click_Request_Time_f()
            time.sleep(1)  # Нажимаем на кнопку сортиров
            # ки
            lang_data = self.fetch_column_data(column_index=5)
            print("Data after first sort:", lang_data)
            assert self.is_sorted_ascending1(lang_data), "Data is not sorted ascending."

            self.click_Request_Time_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            lang_data = self.fetch_column_data(column_index=5)
            print("Data after first sort:", lang_data)
            assert self.is_sorted_descending1(lang_data), "Data is not sorted descending."
            # self.click_Request_Time_s()
            # st = self.get_r_time_cell().text
            # self.input_start_time(st)
            # self.input_end_time(st)
            # self.press_return_key()
            # time.sleep(1)
            # self.click_search_b()
            # time.sleep(8)
            # self.assert_word(self.get_r_time_cell1(), st)
            self.driver.refresh()
            time.sleep(10)

            self.click_Client_name_f()
            time.sleep(5)  # Нажимаем на кнопку сортировки
            client_name_data = self.fetch_column_data(column_index=6)  # Измените индекс столбца при необходимости
            print("Data after first sort:", client_name_data)
            assert self.is_sorted_ascending1(client_name_data), "Data is not sorted ascending."

            self.click_Client_name_f()
            time.sleep(5)  # Нажимаем на кнопку сортировки
            client_name_data = self.fetch_column_data(column_index=6)  # Измените индекс столбца при необходимости
            print("Data after second sort:", client_name_data)
            assert self.is_sorted_descending1(client_name_data), "Data is not sorted descending."
            time.sleep(10)
            self.click_Client_name_s()
            client_name = self.get_Client_name_cell().text
            time.sleep(5)
            self.input_Client_name(client_name)
            time.sleep(7)
            self.get_search_sf().click()
            time.sleep(7)
            self.click_first_object()
            time.sleep(3)
            self.assert_word(self.get_Client_name_cell1(), client_name)
            self.driver.refresh()
            time.sleep(15)

            self.click_Target_Language_f()
            time.sleep(5)  # Нажимаем на кнопку сортировки
            target_language_data = self.fetch_column_data(column_index=7)  # Измените индекс столбца при необходимости
            print("Data after first sort:", target_language_data)
            assert self.is_sorted_ascending1(target_language_data), "Data is not sorted ascending."
            time.sleep(1)

            self.click_Target_Language_f()
            time.sleep(6)  # Нажимаем на кнопку сортировки
            target_language_data = self.fetch_column_data(column_index=7)  # Измените индекс столбца при необходимости
            print("Data after second sort:", target_language_data)
            assert self.is_sorted_descending1(target_language_data), "Data is not sorted descending."

            self.click_Target_Language_s()
            time.sleep(20)
            target_language = self.get_Target_Language_cell().text
            time.sleep(5)
            self.get_Target_Language_s_f().click()
            time.sleep(10)
            self.input_Target_Language(target_language)
            time.sleep(7)
            self.get_search_sf().click()
            time.sleep(7)
            self.click_first_object()
            time.sleep(2)
            self.assert_word(self.get_Target_Language_cell1(), target_language)
            self.driver.refresh()
            time.sleep(10)

            self.click_Audio_video_f()
            time.sleep(10)  # Нажимаем на кнопку сортировки
            audio_video_data = self.fetch_column_data(column_index=8)  # Измените индекс столбца при необходимости
            print("Data after first sort:", audio_video_data)
            assert self.is_sorted_ascending1(audio_video_data), "Data is not sorted ascending."

            self.click_Audio_video_f()
            time.sleep(5)  # Нажимаем на кнопку сортировки
            audio_video_data = self.fetch_column_data(column_index=8)  # Измените индекс столбца при необходимости
            print("Data after second sort:", audio_video_data)
            assert self.is_sorted_descending1(audio_video_data), "Data is not sorted descending."
            time.sleep(3)
            audio_video_option = self.get_Audio_video_cell().text
            time.sleep(3)
            self.click_Audio_video_s()
            time.sleep(10)
            self.input_Audio_video(audio_video_option)
            time.sleep(7)
            self.get_search_sf().click()
            time.sleep(7)
            self.click_first_object()
            time.sleep(10)
            self.assert_word(self.get_Audio_video_cell1(), audio_video_option)
            self.driver.refresh()
            time.sleep(20)
            self.click_status_s()  ###TODO BUG
            status = self.get_status_cell().text
            time.sleep(3)
            # self.input_status(status)
            self.click_first_object()
            time.sleep(10)
            # self.assert_word(self.get_status_cell1(), status)
            self.driver.refresh()
            time.sleep(10)
            self.click_WaitingSeconds_f()
            time.sleep(10)  # Нажимаем на кнопку сортировки
            waiting_seconds_data = self.fetch_column_data(column_index=10)
            print("Data after first sort:", waiting_seconds_data)
            assert self.is_sorted_ascending1(waiting_seconds_data), "Data is not sorted ascending."

            self.click_WaitingSeconds_f()
            time.sleep(3)  # Нажимаем на кнопку сортировки
            waiting_seconds_data = self.fetch_column_data(column_index=10)
            print("Data after second sort:", waiting_seconds_data)
            assert self.is_sorted_descending1(waiting_seconds_data), "Data is not sorted descending."

            time.sleep(15)

            self.click_service_minutes_f()
            time.sleep(4)  # Нажимаем на кнопку сортировки
            service_minutes_data = self.fetch_column_data(column_index=11)
            print("Data after first sort:", service_minutes_data)
            assert self.is_sorted_ascending1(service_minutes_data), "Data is not sorted ascending."

            self.click_service_minutes_f()
            time.sleep(4)  # Нажимаем на кнопку сортировки
            service_minutes_data = self.fetch_column_data(column_index=11)
            print("Data after second sort:", service_minutes_data)
            assert self.is_sorted_descending1(service_minutes_data), "Data is not sorted descending."

            time.sleep(10)
            self.click_role_dropdown()
            time.sleep(5)
            self.click_Interpriter_Name_s()
            time.sleep(10)
            interpreter_name = self.get_Interpriter_Name_cell1().text
            time.sleep(10)
            self.input_Interpriter_Name(interpreter_name)
            time.sleep(7)
            self.get_search_sf().click()
            time.sleep(7)
            self.click_first_object()
            time.sleep(6)
            self.assert_word(self.get_Interpriter_Name_cell1(), interpreter_name)
            self.driver.refresh()
            time.sleep(15)
            self.click_role_dropdown()
            self.click_Interpriter_id_f()
            time.sleep(6)  # Нажимаем на кнопку сортировки
            interpriter_id_data = self.fetch_column_data(column_index=13)
            print("Data after first sort:", interpriter_id_data)
            assert self.is_sorted_ascending1(interpriter_id_data), "Data is not sorted ascending."

            self.click_Interpriter_id_f()
            time.sleep(6)  # Нажимаем на кнопку сортировки
            interpriter_id_data = self.fetch_column_data(column_index=13)
            print("Data after second sort:", interpriter_id_data)
            assert self.is_sorted_descending1(interpriter_id_data), "Data is not sorted descending."

            self.click_Interpriter_id_s()
            interpriter_id = self.get_Interpriter_id_cell().text
            self.input_Interpriter_id(interpriter_id)
            time.sleep(7)
            self.get_search_sf().click()
            time.sleep(7)
            self.click_first_object()
            time.sleep(8)
            self.assert_word(self.get_Interpriter_id_cell1(), interpriter_id)
            time.sleep(3)
            self.driver.refresh()
            time.sleep(6)
            self.click_role_dropdown()
            time.sleep(1)
            caller_id = self.get_Caller_id_cell().text
            time.sleep(5)
            self.click_Caller_id_s()
            time.sleep(10)
            self.get_Caller_id_s_f().click()
            time.sleep(10)
            self.input_Caller_id(caller_id)
            time.sleep(7)
            self.get_search_sf().click()
            time.sleep(7)
            self.click_first_object()
            time.sleep(5)
            self.assert_word(self.get_Caller_id_cell1(), caller_id)
            self.driver.refresh()
            time.sleep(15)
            self.click_role_dropdown()
            time.sleep(3)
            self.click_serial_number_s()
            time.sleep(3)
            serial_number = self.get_serial_number_cell().text
            self.input_serial_number(serial_number)
            time.sleep(7)
            self.get_search_sf().click()
            time.sleep(7)
            self.click_first_object()
            time.sleep(10)

            self.assert_word(self.get_serial_number_cell1(), serial_number)
            self.driver.refresh()
            time.sleep(10)
            self.click_role_dropdown()
            time.sleep(3)
            self.click_Client_User_Name_f()
            time.sleep(5)  # Нажимаем на кнопку сортировки
            client_user_name_data = self.fetch_column_data(column_index=19)
            print("Data after first sort:", client_user_name_data)
            assert self.is_sorted_ascendingA(client_user_name_data), "Data is not sorted ascending."
            time.sleep(3)
            self.click_Client_User_Name_f()
            time.sleep(1)  # Нажимаем на кнопку сортировки
            client_user_name_data = self.fetch_column_data(column_index=19)
            print("Data after second sort:", client_user_name_data)
            assert self.is_sorted_descendingA(client_user_name_data), "Data is not sorted descending."
            time.sleep(3)
            self.click_Client_User_Name_s()
            time.sleep(3)
            client_user_name = self.get_Client_User_Name_cell().text
            self.input_Client_User_Name(client_user_name)
            time.sleep(7)
            self.get_search_sf().click()
            time.sleep(7)
            self.click_first_object()
            time.sleep(5)
            self.assert_word(self.get_Client_User_Name_cell1(), client_user_name)
            self.driver.refresh()
            time.sleep(3)
            self.click_role_dropdown()
            time.sleep(3)
            self.click_plus()
            self.assert_word(self.get_check_in_id(), self.get_Interpriter_id_cell1().text)
            self.assert_word(self.get_check_in_name(), self.get_Interpriter_Name_cell1().text)

            self.driver.refresh()
            time.sleep(10)
            self.click_select_columns()
            time.sleep(5)
            first_company = self.get_service_s_t_column()
            self.driver.execute_script("arguments[0].click();", first_company)
            time.sleep(20)
            self.drag_and_drop_by_coordinates1(self.service_s_t_column, self.cancel_c)
            time.sleep(5)
            self.click_ok()
            time.sleep(5)
            self.assert_word(self.get_check_added_c(), 'Transaction ID')
            time.sleep(5)
            self.click_select_columns()
            time.sleep(5)
            self.compare_columns_and_click_ok1()
            time.sleep(3)
            self.driver.refresh()
            time.sleep(15)
            web_data = self.fetch_website_data_am1()
            db_data = self.query_activity_m()
            self.compare_data_am_t(web_data, db_data)
            self.driver.refresh()
            time.sleep(15)
            self.click_lang_f_Spanish()
            time.sleep(5)  # Ожидаем обновления данных на странице
            website_data = self.fetch_website_data_am1()
            time.sleep(5)
            result_s, language_s = self.check_language_sorted_S(website_data)
            assert result_s, "Ошибка: данные не соответствуют языку Spanish"

            # Клик по фильтру ASL и проверка данных
            self.click_lang_f_ASL()
            time.sleep(5)  # Ожидаем обновления данных на странице
            website_data = self.fetch_website_data_am1()
            time.sleep(5)
            result_asl, language_asl = self.check_language_sorted_ASL(website_data)
            assert result_asl, "Ошибка: данные не соответствуют языку ASL"

            # Клик по фильтру LOTS (языки, отличные от Spanish и ASL) и проверка данных
            self.click_lang_f_LOTS()
            time.sleep(5)  # Ожидаем обновления данных на странице
            website_data = self.fetch_website_data_am1()
            time.sleep(5)
            result_lots, excluded_languages_lots = self.check_language_sorted_LOTS(website_data)
            assert result_lots, "Ошибка: данные соответствуют языкам Spanish или ASL"
            self.driver.refresh()
            time.sleep(20)
            self.click_download_b()
            time.sleep(3)
            download_folder = "/Users/nikitabarshchuk/Downloads"
            target_folder = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Downloads"
            file_pattern = "Activity_Monitor_Records*.xlsx"

            moved_file_path = self.move_latest_file(download_folder, target_folder, file_pattern)

            if moved_file_path:
                csv_data = self.read_excel_data(moved_file_path)
                website_data = self.fetch_website_data_am_cvs()
                self.compare_data_cvs(website_data, csv_data)

            self.check_color_change(self.element_xpath, self.additional_xpath)

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

    def fetch_column_data(self, column_index):
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

    def is_sorted_ascendingA(self, column_data):
        # Отфильтровываем строки, которые не содержат 'Ascension Indiana'
        filtered_data = [x for x in column_data if 'Ascension Indiana' in x]

        # Проверяем, отсортированы ли значения по возрастанию
        return filtered_data == sorted(filtered_data)

    def is_sorted_descendingA(self, column_data):
        # Отфильтровываем строки, которые не содержат 'Ascension Indiana'
        filtered_data = [x for x in column_data if 'Ascension Indiana' in x]

        # Проверяем, отсортированы ли значения по убыванию
        return filtered_data == sorted(filtered_data, reverse=True)
