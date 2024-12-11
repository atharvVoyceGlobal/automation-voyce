import time
import re
import allure
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from utilities.logger import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
from database.Database import Database, assert_equal
from database.Databricks import Databricks
from customer_pages.Graph_c import Graphs
from ev import EV

class Devices_Check(Graphs, EV):

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver
        Databricks.__init__(self)

    # Locators

    source_xpath = "//span[@class='ant-divider-inner-text' and text()='Total']"
    num_of_dev = '//*[@id="root"]/section/section/main/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div/div[2]'
    dashboard_button = "//*[@id='root']/section/aside/div/ul/li[1]"
    email = "//*[@id='email']"
    submit_button = "//*[@id='root']/div/div[3]/div/div/div/div/div/form/div/div/div[2]/div/div/div/div/div/button"
    successful_send = "/html/body/div[2]/div/div/div/span[2]"
    error_massage = "/html/body/div[2]/div/div/div/span[2]"
    active_carts = '//*[@id="root"]/section/section/main/div/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div'
    vod = '//*[@id="root"]/section/section/main/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div'
    cod = '//*[@id="root"]/section/section/main/div/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div'
    min_used = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]'
    avg_wait_sec_video_sp = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[3]/div/div[2]/div/div[2]'
    avg_wait_sec_video_lots = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div[2]'
    avg_call_lenght_mins = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[5]/div/div[2]/div/div[2]'
    total_calls_serv = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[6]/div/div[2]/div/div[2]'
    compl_video_calls = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[7]/div/div[2]/div/div[2]'
    compl_audio_calls = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[8]/div/div[2]/div/div[2]'
    total_requests = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[9]/div/div[2]/div/div[2]'
    cancelled = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[10]/div/div[2]/div/div[2]'
    est_cost = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[11]/div/div[2]/div/div[2]'
    new = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[12]/div/div[2]/div/div[2]'
    pending = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[14]/div/div[2]/div/div[2]'
    in_serv = '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[13]/div/div[2]/div/div[2]'
    ast_pages = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/ul/li[8]'
    ten_tr_per_page = "//div[contains(@class, 'ant-select-item-option-content') and contains(text(), '10 / page')]"
    pages = "//span[@class='ant-select-selection-item' and text()='100 / page']"
    cost_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[15]/div'
    lang_f_ASL = '//*[@id="header-container-id"]/div/div[4]/div/label[4]/span[1]'
    lang_f_LOTS = '//*[@id="header-container-id"]/div/div[4]/div/label[3]'
    lang_f_Spanish = '//*[@id="header-container-id"]/div/div[4]/div/label[2]'
    check_in_id = "//*[@id='root']/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td/div/div/div/div/div[2]/div/table/tbody/tr/td[1]"
    check_in_name = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td/div/div/div/div/div[2]/div/table/tbody/tr/td[2]'

    plus = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]/button'
    buttons = "//button[@class='ant-table-row-expand-icon ant-table-row-expand-icon-collapsed' and @type='button']"
    activity_m_b = '//*[@id="root"]/section/aside/div/ul/li[2]'
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
    Product_Name_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[3]/div/span[1]/div/span[2]'
    Product_Name_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[3]/div/span[2]/span'
    Product_Name_s_f = "//input[@placeholder='Search RequestProductName']"
    Request_Date_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[4]/div/span[1]/div/span[1]'
    Request_Date_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[4]/div/span[2]/span'
    Request_Date_s_f = "//input[@placeholder='Search RequestDate']"
    Request_Time_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[5]/div/span[2]/span'
    start_time = "//input[@placeholder='Start Time']"
    end_time = "//input[@placeholder='End Time']"
    Request_Time_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[5]/div/span[1]'
    Client_name_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[6]/div/span[1]'
    Client_name_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[6]/div/span[2]/span'
    Clirnt_name_s_f = "//input[@placeholder='Search ClientName' and @type='text']"
    Client_name_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[6]/td[7]'
    Client_name_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[7]'
    Target_Language_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[7]/div/span[1]'
    Target_Language_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[7]/div/span[2]/span'
    Target_Language_s_f = "//input[@placeholder='Search TargetLanguage']"
    Target_Language_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[5]/td[8]'
    Target_Language_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[8]'
    Audio_video_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[8]/div/span[1]'
    Audio_video_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[8]/div/span[2]/span'
    Audio_video_s_f = "//input[@placeholder='Search VideoOption']"
    Audio_video_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[5]/td[9]'
    Audio_video_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[9]'
    WaitingSeconds_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[10]/div/span[1]/div/span[2]'
    WaitingSeconds_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[10]/div/span[2]/span'
    WaitingSeconds_s_f = "//input[@placeholder='Search WaitingSeconds']"
    WaitingSeconds_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[11]'
    WaitingSeconds_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[11]'
    service_minutes_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[11]/div/span[1]/div'
    service_minutes_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[11]/div/span[2]/span'
    service_minutes_s_f = "//input[@placeholder='Search ServiceMinutes']"
    service_minutes_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[12]'
    service_minutes_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[12]'

    Interpriter_Name_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[12]/div/span[2]/span'
    Interpriter_Name_s_f = "//input[@placeholder='Search InterpreterFirstName']"
    Interpriter_Name_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[5]/td[13]'
    Interpriter_Name_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[13]'

    serial_number_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[18]/div/span[2]/span'
    serial_number_s_f = "//input[@placeholder='Search IOSSerialNumber']"
    serial_number_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[19]'
    serial_number_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[19]'

    Client_User_Name_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[19]/div/span[1]/div'
    Client_User_Name_s_f = "//input[@placeholder='Search UserName']"
    Client_User_Name_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[19]/div/span[2]/span'
    Client_User_Name_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[20]'
    Client_User_Name_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[20]'

    Interpriter_id_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[14]/div/span[1]/div'
    Interpriter_id_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[13]/div/span[2]/span'
    Interpriter_id_s_f = "//input[@placeholder='Search InterpreterId']"
    Interpriter_id_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[14]'
    Interpriter_id_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[14]'
    Cancel_time_f = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[14]/div/span[1]'
    Caller_id_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[17]/div/span[2]/span'
    Caller_id_s_f = "//input[@placeholder='Search CallerID']"
    Caller_id_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[18]'
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
    search_b = "//div[contains(@class, 'ant-dropdown') and contains(@class, 'css-1tx2tgg') and contains(@class, 'ant-dropdown-placement-bottomRight')]//button[contains(@class, 'ant-btn') and contains(@class, 'css-1tx2tgg') and contains(@class, 'ant-btn-primary') and contains(@class, 'ant-btn-sm')]//span[text()='Search']"

    download_b = "//button[span[text()='Download']]"
    all_clients = '//*[@id="header-container-id"]/div/div[6]/div/div/span[2]'
    choose_company = "//div[@class='ant-select-item-option-content' and text()='CCH Internal']"
    Today_list = "(//span[@class='ant-select-selection-item'])[2]"
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
    tr_id_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[3]'
    tr_id_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[3]'
    pr_n_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[5]/td[4]'
    pr_n_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[4]'
    req_d_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[5]'
    req_d_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[5]'
    r_time_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[6]'
    r_time_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[6]'
    status_s = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[9]/div/span[2]'
    status_s_f = "//input[@placeholder='Search Status']"
    status_cell = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[10]'
    status_cell1 = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[10]'

    # Getters

    def get_ten_tr_per_page(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ten_tr_per_page)))

    def get_pages(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.pages)))

    def get_cost(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.cost_f)))

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
        return WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, self.Today_list)))

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
        self.get_Caller_id_s().click()
        print("CLICK Caller_id Search")

    def input_Caller_id(self, id):
        self.get_Caller_id_s_f().send_keys(id)
        print("Input Caller ID")

    def click_Cancel_time_f(self):
        element = self.get_Cancel_time_f()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK Cancel_time_f")

    def click_Interpriter_id_f(self):
        self.get_Interpriter_id_f().click()
        print("CLICK Interpriter_id_f")

    def click_Interpriter_id_s(self):
        element = self.get_Interpriter_id_s()  # Замените на ваш селектор
        self.driver.execute_script("arguments[0].click();", element)
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

    def click_Cost_f(self):
        self.get_cost().click()
        print("CLICK cost")

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
        self.get_Target_Language_s().click()
        print("CLICK Target_Language_s")

    def input_Target_Language(self, language):
        self.get_Target_Language_s_f().send_keys(language)
        print("Input Target Language")

    def click_ok(self):
        self.get_ok().click()
        print("CLICK Ok")

    def click_transaction_b(self):
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
        print(f"Center of element X: {x_center}, Y: {y_center}")
        return x_center, y_center

    def click_calls_f(self):
        self.get_calls_f().click()
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
        self.get_Transaction_ID_s().click()
        print("CLICK Transaction_ID_s")

    def click_Transaction_ID_f(self):
        self.get_Transaction_ID_f().click()
        print("CLICK Transaction_ID_f")

    def click_Interpriter_Name_s(self):
        first_company = self.get_Interpriter_Name_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Interpriter_Name Search")

    def input_Interpriter_Name(self, name):
        self.get_Interpriter_Name_s_f().send_keys(name)
        print("Input Interpreter Name")

    def click_Product_Name_f(self):
        first_company = self.get_Product_Name_f()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Product_Name_f")

    def click_Product_Name_s(self):
        self.get_Product_Name_s().click()
        print("CLICK Product_Name_s")

    def click_Request_Date_f(self):
        self.get_Request_Date_f().click()
        print("CLICK Request_Date_f")

    def click_Request_Date_s(self):
        first_company = self.get_Request_Date_s()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK Request_Date_s")

    def click_Request_Time_s(self):
        # Поиск элемента по CSS селектору
        request_time_s_element = self.driver.find_element(By.CSS_SELECTOR,
                                                          "#root > section > section > main > div > div > div > div > div > div > div > div.ant-table-container > div.ant-table-header.ant-table-sticky-holder > table > thead > tr > th:nth-child(6) > div > span.ant-dropdown-trigger.ant-table-filter-trigger > span")
        # Нажатие на элемент
        request_time_s_element.click()
        print("CLICK Request_Time_s")

    def click_status_s(self):
        self.get_status_s().click()
        print("CLICK Status Search icon")

    def click_plus(self):
        self.get_plus().click()
        print("CLICK Plus")

    def click_Request_Time_f(self):
        self.get_Request_Time_f().click()
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

    def press_return_key(self):
        actions = ActionChains(self.driver)

        actions.send_keys(Keys.RETURN).perform()

        print("Pressed the Return key")

    def clear_input_field(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click()
        time.sleep(2)
        actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND)
        time.sleep(2)
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
        css_selector = "#header-container-id > div > div:nth-child(4) > div > div > span.ant-select-selection-item"
        element_to_click = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        self.driver.execute_script("arguments[0].click();", element_to_click)
        print("CLICK list")

    def click_list1(self):
        first_company = self.get_Today_list()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK list")

    def input_company(self, company):
        try:
            input_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ant-select-selection-search-input"))
            )
            if len(input_elements) > 1:
                input_element = input_elements[1]
                input_element.send_keys(company)
                print("Input Company Name:", company)
            else:
                print("Not enough elements found for input.")
        except TimeoutException:
            print("The elements for entering the company name did not become available within the specified timeout period.")

    def click_last_pages(self):
        first_company = self.get_last_pages()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK last pages")

    def click_reset_b(self):
        self.get_reset_b().click()
        print("CLICK reset b")

    def click_yesterday(self):
        self.get_Yesterday().click()
        print("CLICK yesterday")

    def click_last_year(self):
        self.get_Last_year().click()
        print("CLICK yesterday")

    def click_ten_tr_per_page(self):
        self.get_ten_tr_per_page().click()
        print("CLICK ten_tr_per_page")

    def click_pages(self):
        self.get_pages().click()
        print("CLICK pages")

    def click_last_week(self):
        self.get_Last_week().click()
        print("CLICK last week")

    def click_this_month(self):
        self.get_This_month().click()
        print("CLICK This month")

    def click_this_week(self):
        self.get_This_week().click()
        print("CLICK This week")

    def click_last_month(self):
        self.get_Last_month().click()
        print("CLICK Last month")

    def click_last_30_days(self):
        self.get_Last_30_days().click()
        print("CLICK Last 30 days")

    # Getters

    def get_active_carts(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div')))

    def get_vod(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,
                                                                                '//*[@id="root"]/section/section/main/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div')))

    def get_cod(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,
                                                                                '//*[@id="root"]/section/section/main/div/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div')))

    def get_min_used(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]')))

    def get_avg_wait_sec_video_sp(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[3]/div/div[2]/div/div[2]')))

    def get_avg_wait_sec_video_lots(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[4]/div/div[2]/div/div[2]')))

    def get_avg_call_lenght_mins(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[5]/div/div[2]/div/div[2]')))

    def get_total_calls_serv(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[6]/div/div[2]/div/div[2]')))

    def get_compl_video_calls(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[7]/div/div[2]/div/div[2]')))

    def get_compl_audio_calls(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[8]/div/div[2]/div/div[2]')))

    def get_total_requests(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[9]/div/div[2]/div/div[2]')))

    def get_cancelled(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[10]/div/div[2]/div/div[2]')))

    def get_est_cost(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[11]/div/div[2]/div/div[2]')))

    def get_new(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[12]/div/div[2]/div/div[2]')))

    def get_pending(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[14]/div/div[2]/div/div[2]')))

    def get_in_serv(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div[2]/div/div[13]/div/div[2]/div/div[2]')))

    def get_dashboard_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.dashboard_button)))

    def get_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.email)))

    def get_submit_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.submit_button)))

    def get_successful_send(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.successful_send)))

    def get_error_massage(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_massage)))

        # Actions

    def click_active_carts(self):
        element = self.get_active_carts()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK active_carts")

    def click_vod(self):
        element = self.get_vod()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK vod")

    def click_cod(self):
        element = self.get_cod()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK cod")

    def click_min_used(self):
        element = self.get_min_used()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK min_used")

    def click_avg_wait_sec_video_sp(self):
        element = self.get_avg_wait_sec_video_sp()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK avg_wait_sec_video_sp")

    def click_avg_wait_sec_video_lots(self):
        element = self.get_avg_wait_sec_video_lots()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK avg_wait_sec_video_lots")

    def click_avg_call_length_mins(self):
        element = self.get_avg_call_lenght_mins()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK avg_call_length_mins")

    def click_total_calls_serv(self):
        element = self.get_total_calls_serv()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK total_calls_serv")

    def click_compl_video_calls(self):
        element = self.get_compl_video_calls()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK compl_video_calls")

    def click_compl_audio_calls(self):
        element = self.get_compl_audio_calls()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK compl_audio_calls")

    def click_total_requests(self):
        element = self.get_total_requests()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK total_requests")

    def click_cancelled(self):
        element = self.get_cancelled()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK cancelled")

    def click_est_cost(self):
        element = self.get_est_cost()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK est_cost")

    def click_new(self):
        element = self.get_new()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK new")

    def click_this_year(self):
        self.get_This_year().click()
        print("CLICK This year")

    def click_pending(self):
        element = self.get_pending()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK pending")

    def click_in_serv(self):
        element = self.get_in_serv()
        self.driver.execute_script("arguments[0].click();", element)
        print("CLICK in_serv")

    def click_dashboard_button(self):
        self.get_dashboard_button().click()
        print("CLICK Dashboard")

    def input_email(self, user_password):
        self.get_email().send_keys(user_password)
        print("input email")

    def click_submit_button(self):
        self.get_submit_button().click()
        print("CLICK submit button")

    # METHODS

    def move_cursor_and_click_with_pyautogui_11am(self, source_xpath):
        window_rect = self.driver.get_window_rect()
        window_x = window_rect['x']
        window_y = window_rect['y']

        source_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, source_xpath))
        )

        source_location = source_element.location
        source_x = window_x + source_location['x']
        source_y = window_y + source_location['y']


        y_offset = 170
        x_offset = 5


        pyautogui.moveTo(source_x + x_offset, source_y + y_offset, duration=1)
        pyautogui.mouseDown()
        pyautogui.mouseUp()

    def compare_data_with_api(self, db_data, api_data):
        discrepancies = []

        for db_row in db_data:
            language_name = db_row['TargetLanguage']
            api_row = next((item for item in api_data if item['TargetLanguage'] == language_name), None)

            if api_row:
                if db_row['ServiceMinutes'] != api_row['ServiceMinutes']:
                    discrepancies.append(
                        f"ServiceMinutes mismatch for language {language_name}: DB({db_row['ServiceMinutes']}) != API({api_row['ServiceMinutes']})")
                if db_row['CountAudioMinute'] != api_row['CountAudioMinute']:
                    discrepancies.append(
                        f"CountAudioMinute mismatch for language {language_name}: DB({db_row['CountAudioMinute']}) != API({api_row['CountAudioMinute']})")
                if db_row['CountVideoMinute'] != api_row['CountVideoMinute']:
                    discrepancies.append(
                        f"CountVideoMinute mismatch for language {language_name}: DB({db_row['CountVideoMinute']}) != API({api_row['CountVideoMinute']})")
                if db_row['WaitingSeconds'] != api_row['WaitingSeconds']:
                    discrepancies.append(
                        f"WaitingSeconds mismatch for language {language_name}: DB({db_row['WaitingSeconds']}) != API({api_row['WaitingSeconds']})")
                if db_row['TotalCalls'] != api_row['TotalCalls']:
                    discrepancies.append(
                        f"TotalCalls mismatch for language {language_name}: DB({db_row['TotalCalls']}) != API({api_row['TotalCalls']})")
                if db_row['CountSuccessAudioCalls'] != api_row['CountSuccessAudioCalls']:
                    discrepancies.append(
                        f"CountSuccessAudioCalls mismatch for language {language_name}: DB({db_row['CountSuccessAudioCalls']}) != API({api_row['CountSuccessAudioCalls']})")
                if db_row['CountSuccessVideoCalls'] != api_row['CountSuccessVideoCalls']:
                    discrepancies.append(
                        f"CountSuccessVideoCalls mismatch for language {language_name}: DB({db_row['CountSuccessVideoCalls']}) != API({api_row['CountSuccessVideoCalls']})")
                if db_row['CallQualityRatingStar'] != api_row['CallQualityRatingStar']:
                    discrepancies.append(
                        f"CallQualityRatingStar mismatch for language {language_name}: DB({db_row['CallQualityRatingStar']}) != API({api_row['CallQualityRatingStar']})")
                if db_row['CountRatingStarCalls'] != api_row['CountRatingStarCalls']:
                    discrepancies.append(
                        f"CountRatingStarCalls mismatch for language {language_name}: DB({db_row['CountRatingStarCalls']}) != API({api_row['CountRatingStarCalls']})")

        return discrepancies

    def compare_data_with_api_lang_by_hour(self, db_data, api_data):
        discrepancies = []

        api_data_dict = {item['languageName']: item for item in api_data}

        for db_row in db_data:
            language_name = db_row['languageName']
            api_row = api_data_dict.get(language_name)

            if api_row:
                if db_row['TotalCalls'] != api_row['TotalCalls']:
                    discrepancies.append(
                        f"TotalCalls mismatch for language {language_name}: DB({db_row['TotalCalls']}) != API({api_row['TotalCalls']})")

                api_hours_dict = {hour['hour']: hour for hour in api_row['hours']}

                for db_hour in db_row['hours']:
                    api_hour = api_hours_dict.get(db_hour['hour'])

                    if api_hour:
                        if db_hour['ServiceMinutes'] != api_hour['ServiceMinutes']:
                            discrepancies.append(
                                f"ServiceMinutes mismatch for language {language_name} at hour {db_hour['hour']}: DB({db_hour['ServiceMinutes']}) != API({api_hour['ServiceMinutes']})")
                        if db_hour['CountAudioMinute'] != api_hour['CountAudioMinute']:
                            discrepancies.append(
                                f"CountAudioMinute mismatch for language {language_name} at hour {db_hour['hour']}: DB({db_hour['CountAudioMinute']}) != API({api_hour['CountAudioMinute']})")
                        if db_hour['CountVideoMinute'] != api_hour['CountVideoMinute']:
                            discrepancies.append(
                                f"CountVideoMinute mismatch for language {language_name} at hour {db_hour['hour']}: DB({db_hour['CountVideoMinute']}) != API({api_hour['CountVideoMinute']})")
                        if db_hour['WaitingSeconds'] != api_hour['WaitingSeconds']:
                            discrepancies.append(
                                f"WaitingSeconds mismatch for language {language_name} at hour {db_hour['hour']}: DB({db_hour['WaitingSeconds']}) != API({api_hour['WaitingSeconds']})")
                        if db_hour['CountSuccessAudioCalls'] != api_hour['CountSuccessAudioCalls']:
                            discrepancies.append(
                                f"CountSuccessAudioCalls mismatch for language {language_name} at hour {db_hour['hour']}: DB({db_hour['CountSuccessAudioCalls']}) != API({api_hour['CountSuccessAudioCalls']})")
                        if db_hour['CountSuccessVideoCalls'] != api_hour['CountSuccessVideoCalls']:
                            discrepancies.append(
                                f"CountSuccessVideoCalls mismatch for language {language_name} at hour {db_hour['hour']}: DB({db_hour['CountSuccessVideoCalls']}) != API({api_hour['CountSuccessVideoCalls']})")
                        if db_hour['CallQualityRatingStar'] != api_hour['CallQualityRatingStar']:
                            discrepancies.append(
                                f"CallQualityRatingStar mismatch for language {language_name} at hour {db_hour['hour']}: DB({db_hour['CallQualityRatingStar']}) != API({api_hour['CallQualityRatingStar']})")
                        if db_hour['CountRatingStarCalls'] != api_hour['CountRatingStarCalls']:
                            discrepancies.append(
                                f"CountRatingStarCalls mismatch for language {language_name} at hour {db_hour['hour']}: DB({db_hour['CountRatingStarCalls']}) != API({api_hour['CountRatingStarCalls']})")
                    else:
                        discrepancies.append(
                            f"Hour {db_hour['hour']} data for language {language_name} found in DB but not in API data")
            else:
                discrepancies.append(f"Language {language_name} found in DB but not in API data")

        return discrepancies

    def double_press_down_arrow(self):
        actions = ActionChains(self.driver)

        actions.send_keys(Keys.ARROW_DOWN).perform()

        print("Pressed the Down arrow key")

    def assert_word111(self, word, result):
        if hasattr(word, 'text'):
            value_word = word.text
        else:
            value_word = word

        value_word_str = str(value_word).replace(',', '').strip()
        result_str = str(result).replace(',', '').strip()

        print(f"Actual text: '{value_word_str}', Expected text: '{result_str}'")
        assert value_word_str == result_str, f" '{result_str}', ASSERT '{value_word_str}'"
        print("good word")

    def compare_data_for_periods(self):
        with allure.step("Compare data with DB by Periods"):
            time_periods = ['last_30_days', 'yesterday', 'this_week', 'this_month', 'last_week', 'last_month',
                            'this_year', 'last_year']
            for period in time_periods:
                self.take_data_for_period_and_compare(period)

    def select_time_period_and_wait_for_update(self, time_period, open_list=True):
        if open_list:
            self.click_list()
            self.double_press_down_arrow()
        time.sleep(10)
        getattr(self, f"click_{time_period}")()
        time.sleep(30)

    def get_num_of_dev(self):
        element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.num_of_dev)))
        text = element.text
        print(text)
        return text

    def get_company_data(self):
        company_data_list = []
        try:
            collection = self.client["your_database_name"]["Company"]

            query = {}

            projection = {"CompanyName": 1, "CompanyCode": 1, "_id": 0}

            cursor = collection.find(query, projection)

            for document in cursor:
                company_data_list.append(document)

            for company_data in company_data_list:
                print(company_data)

        except Exception as e:
            print(f"Error: {e}")

        return company_data_list

    def take_data_for_period_and_compare(self, time_period):
        self.select_time_period_and_wait_for_update(time_period)

        (total_price_sum, spanish_audio_video_calls_count, other_languages_video_calls_count,
         pending, new, in_service, serviced, cancelled, total_calls_serviced, completed_audio_calls,
         minutes_used, average_waiting_time_per_spanish_video_call, avg_waiting_seconds_video_ol,
         avg_call_length_mins) = self.query_all_data_widgets_by_periods(time_period)

        # self.assert_word(self.get_est_cost().text, total_price_sum)
        # self.assert_word(self.get_avg_wait_sec_video_sp().text, average_waiting_time_per_spanish_video_call)
        # self.assert_word(self.get_avg_wait_sec_video_lots().text, avg_waiting_seconds_video_ol)
        self.assert_word111(self.get_pending().text, pending)
        self.assert_word111(self.get_new().text, new)
        self.assert_word111(self.get_in_serv().text, in_service)
        self.assert_word111(self.get_total_calls_serv().text, serviced)
        self.assert_word111(self.get_cancelled().text, cancelled)
        self.assert_word111(self.get_total_requests().text, total_calls_serviced)
        self.assert_word111(self.get_compl_video_calls().text,
                            spanish_audio_video_calls_count + other_languages_video_calls_count)
        self.assert_word111(self.get_compl_audio_calls().text, completed_audio_calls)
        self.assert_word111(self.get_min_used().text, minutes_used)
        self.assert_word111(self.get_avg_call_lenght_mins().text, avg_call_length_mins)

    def extract_base_name(self, name):
        return name.split(' ')[0]

    def compare_device_counts(self, company_devices_count_list, matched_companies):
        matched_companies_dict = {item['CompanyName']: item['DeviceCount'] for item in matched_companies}

        for company_name, expected_dev_count in company_devices_count_list:
            actual_dev_count = matched_companies_dict.get(company_name)

            if actual_dev_count is not None:
                if actual_dev_count == expected_dev_count:
                    print(f"Match for {company_name}: {expected_dev_count} devices")
                else:
                    print(f"Discrepancy for {company_name}: expected {expected_dev_count}, found {actual_dev_count}")
            else:
                print(f"Company {company_name} not found in the matched data")

    def extract_base_name1(self, name):
        """
        Extracts the base name, taking into account various formatting conditions of the titles.
        """
        original_name = name.replace('-', ' ')
        name = original_name.split()[0]

        if re.match(r'^[A-Z]+[a-z]+', name) or name.isupper():
            base_name = name
        else:
            match = re.search(r'[a-z][A-Z]', name)
            if match:
                base_name = name[:match.start() + 1]
            else:
                base_name = name

        print(f"Original: {original_name}, Base: {base_name}")
        return base_name.lower()

    def map_blueprints_and_create_list(self, company_data_list):
        file_path = '/Users/nikitabarshchuk/PycharmProjects/pythonProject3/Admin_pages/Kanji_devices_Admin'
        matched_companies = []
        unmatched_blueprints = []
        matched_company_names = []
        code_usage = {}

        with open(file_path, 'r') as file:
            blueprint_data_from_file = [line.strip().split(', ') for line in file.readlines()]

        processed_names = {self.extract_base_name1(line[0]): int(line[1]) for line in blueprint_data_from_file}

        for company in company_data_list:
            company_name_processed = self.extract_base_name1(company['CompanyCode'])
            if company_name_processed in processed_names:
                matched_companies.append({
                    'CompanyName': company['CompanyName'],
                    'CompanyCode': company['CompanyCode'],
                    'DeviceCount': processed_names[company_name_processed]
                })
                matched_company_names.append(company['CompanyName'])
                code_usage[company_name_processed] = code_usage.get(company_name_processed, 0) + 1

        unmatched_blueprints = list(set(processed_names.keys()) - set(code_usage.keys()))

        print("\nMatched companies:")
        for company in matched_companies:
            print(f"CompanyName: {company['CompanyName']}, DeviceCount: {company['DeviceCount']}")

        print("\nUnmatched names from the file:")
        for unmatched in unmatched_blueprints:
            print(unmatched)

        print("\nCodes used more than once:")
        for code, usage in code_usage.items():
            if usage > 1:
                print(f"Code: {code}, Used: {usage} times")

        print("\nMatched company names:")
        for name in matched_company_names:
            print(name)

        return matched_companies, matched_company_names

    def normalize_string(self, s):
        s = re.sub(r'\s+', '', s).lower()
        if "mercytn" in s or "srhc" in s or "srhca" in s:
            return s
        if "cooper" in s:
            return "cooper"
        elif "stjohn" in s:
            return "stjohn"
        return s

    def find_key_word(self, s):
        s_lower = s.lower()
        if "mercytn" == s_lower or "srhc" == s_lower or "srhca" == s_lower:
            return s
        key_word = s.split(' ')[0].lower()
        if "cooper" in key_word:
            return "cooper"
        elif "stjohn" in key_word:
            return "stjohn"
        return key_word

    def normalize_and_track_original_names(self, device_info_data):
        normalized_to_original = {}
        for info in device_info_data:
            original_name = info.get('blueprintName', '')
            if original_name == "Unity Health Toronto":
                if original_name in normalized_to_original:
                    normalized_to_original[original_name].add(original_name)
                else:
                    normalized_to_original[original_name] = {original_name}
            else:
                processed_name = original_name.replace(" Tst", "")
                key_word = self.find_key_word(processed_name)
                normalized_name = self.normalize_string(key_word)
                if normalized_name in normalized_to_original:
                    normalized_to_original[normalized_name].add(processed_name)
                else:
                    normalized_to_original[normalized_name] = {processed_name}
        return normalized_to_original

    def find_matching_and_non_matching_companies(self):
        company_collection = self.client["reporting"]["Company"]
        device_info_collection = self.client["reporting"]["DeviceInformation"]

        company_data = list(company_collection.find({}, {"CompanyName": 1, "CompanyCode": 1, "_id": 0}))
        device_info_data = list(device_info_collection.find({}, {"blueprintName": 1, "_id": 0}))

        normalized_company_codes = {self.normalize_string(self.find_key_word(company['CompanyCode'])): company for
                                    company in company_data}
        normalized_blueprint_names = self.normalize_and_track_original_names(device_info_data)

        matched_companies = []
        matched_company_names = []
        unmatched_company_codes = set(normalized_company_codes.keys())
        unmatched_blueprint_names = set(normalized_blueprint_names.keys())

        for normalized_blueprint, original_names in normalized_blueprint_names.items():
            for company_code, company in normalized_company_codes.items():
                if normalized_blueprint.startswith(company_code) or company_code.startswith(normalized_blueprint):
                    company_name = company['CompanyName']

                    if "MercyTN" in original_names:
                        company_name = "Mercy Community Healthcare"

                    if "unity" in company_name.lower():
                        company_name = "Unity Health Toronto"
                    elif company_name.endswith(" Tst"):
                        company_name = company_name[:-4]

                    if "srhc" in company_name.lower() or "srhca" in company_name.lower():
                        company_name = company['CompanyName']

                    matched_companies.append({
                        "CompanyName": company_name,
                        "CompanyCode": company_code,
                        "BlueprintNames": original_names
                    })
                    matched_company_names.append(company_name)
                    unmatched_company_codes.discard(company_code)
                    unmatched_blueprint_names.discard(normalized_blueprint)
                    break

        print("Matching CompanyName and BlueprintName:")
        for match in matched_companies:
            print(f"{match['CompanyName']} ({', '.join(match['BlueprintNames'])})")


        print("\nUnmatched CompanyCode and corresponding CompanyName:")
        for code in unmatched_company_codes:
            print(f"{code}: {normalized_company_codes[code]['CompanyName']}")


        print("\nUnmatched blueprintName and their originals:")
        for normalized_name in unmatched_blueprint_names:
            original_names = ', '.join(normalized_blueprint_names[normalized_name])
            print(f"{normalized_name} (Originals: {original_names})")

        return matched_companies, matched_company_names

    def aggregate_and_combine_blueprints(self):
        collection = self.client["reporting"]["DeviceInformation"]


        pipeline = [
            {
                "$group": {
                    "_id": "$blueprintName",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}}
        ]

        aggregated_data = list(collection.aggregate(pipeline))
        combined_names = {}

        for item in aggregated_data:
            name = item["_id"]
            count = item["count"]


            key_word = self.normalize_string(self.find_key_word(name))

            if key_word in combined_names:

                combined_names[key_word]["count"] += count
                combined_names[key_word]["original_names"].add(name)
            else:

                combined_names[key_word] = {"count": count, "original_names": {name}}


        print("United Blueprint Names and their total quantity:")
        for key, info in combined_names.items():
            print(f"Key: {key}, Count: {info['count']}, Original Names: {', '.join(info['original_names'])}")

        return combined_names

    def click_on_company_name(self, company_name):
        try:
            elements = WebDriverWait(self.driver, 160).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ant-select-item.ant-select-item-option"))
            )
            company_found = False
            for element in elements:
                if element.get_attribute("title").strip() == company_name.strip():
                    element.click()
                    company_found = True
                    if company_name.strip() in ["Mercy Medical Center", "Northwestern Memorial Healthcare"]:
                        self.double_press_down_arrow()
                        self.press_return_key()
                    break

            if not company_found:
                print(f"The company '{company_name}' was not found on the list.")
                self.press_return_key()
                if company_name.strip() in ["Mercy Medical Center", "Northwestern Memorial Healthcare"]:
                    self.double_press_down_arrow()

        except TimeoutException:
            print(f"Elements with the names of companies were not found for a given time.")
            self.press_return_key()
            if company_name.strip() in ["Mercy Medical Center", "Northwestern Memorial Healthcare"]:
                self.double_press_down_arrow()
    def update_web_device_data(self, web_device_data, matched_companies):
        company_to_blueprint = {}
        for company in matched_companies:
            if 'CompanyName' in company and 'BlueprintNames' in company:
                company_to_blueprint[company['CompanyName']] = company.get('BlueprintNames', [])

        for device in web_device_data:
            company_name = device.get('company_name')
            if company_name in company_to_blueprint:
                device['BlueprintNames'] = company_to_blueprint[company_name]
            else:
                device.setdefault('BlueprintNames', [])

        return web_device_data

    def devices_check(self):
        with allure.step("devices_check"):
            Logger.add_start_step(method='devices_check')
            self.get_current_url()
            self.assert_url('https://admin.vip.voyceglobal.com/pages')
            time.sleep(10)
            self.find_matching_and_non_matching_companies()
            self.aggregate_and_combine_blueprints()
            matched_companies, matched_company_names = self.find_matching_and_non_matching_companies()
            combined_names = self.aggregate_and_combine_blueprints()



            # Перебираем названия компаний из списка совпадений
            web_device_data = []
            for company_name in matched_company_names:
                self.click_list1()
                time.sleep(3)
                self.input_company(company_name)
                time.sleep(2)  # Возможно, потребуется корректировка задержки
                # Кликаем по компании в выпадающем списке после ввода названия
                self.click_on_company_name(company_name)
                time.sleep(2)
                num_of_dev = self.get_num_of_dev()

                web_device_data.append({"company_name": company_name, "num_of_dev": num_of_dev})
            self.update_web_device_data(web_device_data, matched_companies)
            web_device_data = self.update_web_device_data(web_device_data, matched_companies)

                # Сравнение данных из веб-интерфейса с агрегированными данными
            self.compare_web_and_database_data(web_device_data, combined_names)

    def compare_web_and_database_data(self, web_device_data, combined_names):
        for web_data in web_device_data:
            blueprint_names = web_data["BlueprintNames"]  # Теперь используем BlueprintNames из web_device_data
            num_of_dev_web = web_data["num_of_dev"]

            match_found = False
            for key, info in combined_names.items():
                # Проверяем, есть ли пересечение между BlueprintNames из web и Original Names из db
                if set(blueprint_names).intersection(info["original_names"]):
                    match_found = True
                    num_of_dev_db = info["count"]
                    if num_of_dev_web == num_of_dev_db:
                        print(f"MATCH: {', '.join(blueprint_names)} web: {num_of_dev_web}, db: {num_of_dev_db}")
                    else:
                        print(f"MISMATCH: {', '.join(blueprint_names)} web: {num_of_dev_web}, db: {num_of_dev_db}")
                    break  # Прерываем цикл, если нашли хотя бы одно совпадение

            if not match_found:
                print(f"NO MATCH FOUND FOR: {', '.join(blueprint_names)}")
# Получаем количество устройств для текущей компании

                # Добавляем информацию в список для сравнения
            #     company_devices_count_list.append((company_name, num_of_dev))
            #
            # # Сравниваем полученные данные по устройствам с ожидаемыми
            # self.compare_device_counts(company_devices_count_list, matched_companies)

