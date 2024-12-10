import time
import allure
from bson import Int64
from selenium.webdriver.common.action_chains import ActionChains
from utilities.logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
from selenium.webdriver.common.keys import Keys
import string
import random
from database.Database import Database, assert_equal


class Client_page(Base, Database):

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver

    # Locators
    reset_c = "//button[@type='button' and contains(@class, 'ant-btn') and contains(@class, 'ant-btn-link') and contains(@class, 'ant-btn-sm') and @disabled and ./span[text()='Reset']]"
    clients_field = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[4]"
    fc = "//span[contains(@class, 'ant-dropdown-menu-title-content')]/span[text()='Northwestern Memorial Healthcare']"
    ok_b = "//button[@type='button' and contains(@class, 'ant-btn') and contains(@class, 'ant-btn-primary') and contains(@class, 'ant-btn-sm')]/span[text()='OK']"
    choose_company = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[4]/div/span[2]"
    search_e = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[2]/div/span[2]"
    name_field = "//input[@type='text' and contains(@class, 'ant-input css-1tx2tgg')]"
    email_field = "//input[@placeholder='Search email' and contains(@class, 'ant-input') and @type='text']"
    search_button = "//span[text()='Search']"
    reset_button = "//button[@type='button' and contains(@class, 'ant-btn') and contains(@class, 'css-1tx2tgg') and contains(@class, 'ant-btn-default') and contains(@class, 'ant-btn-sm')]/span[text()='Reset']"
    role_button = "//*[@id='root']/section/aside/div/ul/li[6]"
    name_filter = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]"
    name_filter2 = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]"
    search_name = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[2]/span/svg"
    check_name = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]/div/span/span[2]"
    email_filter = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[2]"
    check_email = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]"
    role_filter = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[3]/div/span[1]/div/span[1]"
    check_role = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[3]"
    search_n = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[2]"

    # email_field = "//*[@id='email']"
    # password_field = "//*[@id='password']"
    # confirm_password = "//*[@id='confirm']"
    # create_account_button2 = "//*[@id='root']/div/div[3]/div/div/div/div/div/form/div/div/div[7]/div/div/div/div/div/button"
    # password_dont_math = "//*[@id='confirm_help']/div"
    # password_dont_meet_criteria = "//*[@id='password_help']/div"

    # Getters

    def get_reset_c(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.reset_c)))

    def get_clients_f(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.clients_field)))

    def get_ok_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.ok_b)))

    def get_fc(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.fc)))

    def get_choose_company(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.choose_company)))

    def get_search_e(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.search_e)))

    def get_email_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.email_field)))

    def get_name_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_field)))

    def get_search_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.search_button)))

    def get_reset_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.reset_button)))

    def get_role_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.role_button)))

    def get_check_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_name)))

    def get_name_filter(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_filter)))

    def get_search_n(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.search_n)))

    def get_name_filter2(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_filter2)))

    def get_email_filter(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.email_filter)))

    def get_check_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_email)))

    def get_role_filter(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.role_filter)))

    def get_check_role(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_role)))

    # ACTIONS

    def input_email(self, email):
        self.get_email_field().send_keys(email)
        print("input email")

    def input_name(self, user_name):
        self.get_name_field().send_keys(user_name)
        print("input first name")

    def click_search_button(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        print("Pressed Return key")

    def click_reset_button(self):
        self.get_reset_button().click()
        print("CLICK Reset button")

    def click_role_button(self):
        self.get_role_button().click()
        print("CLICK Role button")

    def click_search_e(self):
        self.get_search_e().click()
        print("CLICK search email")

    def click_name_filter(self):
        self.get_name_filter().click()
        print("CLICK name FILTER")

    def click_choose_c(self):
        self.get_choose_company().click()
        print("Click choose_company")

    def click_search_n(self):
        self.get_search_n().click()
        print("Click search")

    def click_name_filter2(self):
        self.get_name_filter2().click()
        print("CLICK name FILTER2")

    def click_ok_b(self):
        self.get_ok_b().click()
        print("CLICK OK")

    def click_fc(self):
        self.get_fc().click()
        print("Choose First Company")

    def click_email_filter(self):
        self.get_email_filter().click()
        print("CLICK email FILTER")

    def click_reset_c(self):
        self.get_reset_c().click()
        print("CLICK reset company")

    def click_role_filter(self):
        self.get_role_filter().click()
        print("CLICK role FILTER")

    # METHODS

    def client_page(self):
        with allure.step("Check filters"):
            Logger.add_start_step(method='Check filters')
            self.get_current_url()
            self.click_role_button()
            time.sleep(5)
            self.assert_url('https://staging.vip.voyceglobal.com/pages/role-hierarchy')
            ###############################################TODO PPPPPPPPPPP

            collection = self.client["auth-customer"]["User"]
            query = {
                "isDeleted": False,
                "company": Int64(1598),
                "role": "User"  # убрал u перед строкой, в Python 3 все строки в unicode по умолчанию
            }
            sort = [("name", 1)]

            cursor = collection.find(query, sort=sort, limit=1)
            name_from_db_desc = None
            try:
                for doc in cursor:
                    name_from_db_desc = doc["name"]
            except Exception as e:
                print(f"Error: {e}")

            assert_equal(name_from_db_desc, self.get_check_name().text,
                         "The name from the database does not match the one on the webpage")
            print("correct data")

            # TODO
            self.click_name_filter()
            element_text = self.get_check_name().text
            self.assert_word(element_text[:3], 'zzz')
            collection = self.client["auth-customer"]["User"]
            query = {"isDeleted": False, "company": Int64(1598)}

            sort = [(u"name", -1)]

            cursor = collection.find(query, sort=sort, limit=1)
            name_from_db_desc = None
            try:
                for doc in cursor:
                    name_from_db_desc = doc["name"]
            except Exception as e:
                print(f"Error: {e}")

            assert_equal(name_from_db_desc, self.get_check_name().text,
                         "The name from the database does not match the one on the webpage")
            print("correct data")
            ######################TODO PPPPPPPPPPPPPPPP
            self.click_search_n()
            self.input_name('zzzz')
            self.click_search_button()
            element_text = self.get_check_name().text
            self.assert_word(element_text[:4], 'zzzz')
            self.driver.refresh()
            # self.click_reset_button()
            self.click_search_e()
            self.input_email('bbb')
            self.click_search_button()
            self.assert_word(self.get_check_email(), 'bbb@voyceglobal.com')
            self.driver.refresh()
            # self.click_search_e()
            # self.click_reset_button()

            self.click_email_filter()

            collection = self.client["auth-customer"]["User"]

            query = {"isDeleted": False, "company": Int64(1598)}

            projection = {"email": u"$email", "_id": 0}

            sort = [(u"email", 1)]

            cursor = collection.find(query, projection=projection, sort=sort, limit=1)
            email_from_db_asc = None
            try:
                for doc in cursor:
                    email_from_db_asc = doc["email"]
            except Exception as e:
                print(f"Error: {e}")

            assert_equal(email_from_db_asc, self.get_check_email().text,
                         "The email from the database does not match the one on the webpage")
            print("correct data")
            ######################TODO PPPPPPPPPPPPPPPPPPPPPPPPPP
            self.click_email_filter()

            # MongoDB code for descending order
            collection = self.client["auth-customer"]["User"]

            query = {"isDeleted": False, "company": Int64(1598)}

            projection = {"email": u"$email", "_id": 0}

            sort = [(u"email", -1)]

            cursor = collection.find(query, projection=projection, sort=sort, limit=1)
            email_from_db_asc = None
            try:
                for doc in cursor:
                    email_from_db_asc = doc["email"]
            except Exception as e:
                print(f"Error: {e}")

            assert_equal(email_from_db_asc, self.get_check_email().text,
                         "The email from the database does not match the one on the webpage")
            print("correct data")

            ######################TODO PPPPPPPPPPPPPPPPPPPPPPPPPP
            self.click_role_filter()
            self.assert_word(self.get_check_role(), "User")
            self.click_role_filter()
            self.click_choose_c()
            self.click_fc()
            self.click_ok_b()
            self.assert_word(self.get_clients_f(), 'Northwestern Memorial Healthcare')
            self.driver.refresh()
            self.click_name_filter()

