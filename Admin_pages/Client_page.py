import time
import allure
from utilities.logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
import string
import random
from database.Database import Database, assert_equal
from customer_pages.Graph_c import Graphs

class Client_page(Graphs):

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver

    # Locators

    role_button = "//*[@id='root']/section/aside/div/ul/li[7]"
    name_filter = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]"
    name_filter2 = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]"
    search_name = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]/div/span[2]/span/svg"
    check_name = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]/div/span[3]"
    email_filter = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[2]"
    check_email = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]"
    role_filter = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[3]/div/span[1]/div/span[1]"
    check_role = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[3]"

    # email_field = "//*[@id='email']"
    # password_field = "//*[@id='password']"
    # confirm_password = "//*[@id='confirm']"
    # create_account_button2 = "//*[@id='root']/div/div[3]/div/div/div/div/div/form/div/div/div[7]/div/div/div/div/div/button"
    # password_dont_math = "//*[@id='confirm_help']/div"
    # password_dont_meet_criteria = "//*[@id='password_help']/div"

    # Getters
    def get_role_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.role_button)))

    def get_check_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_name)))

    def get_name_filter(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_filter)))

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

    def click_role_button(self):
        self.get_role_button().click()
        print("CLICK Role button")

    def click_name_filter(self):
        self.get_name_filter().click()
        print("CLICK name FILTER")

    def click_name_filter2(self):
        self.get_name_filter2().click()
        print("CLICK name FILTER2")

    def click_email_filter(self):
        self.get_email_filter().click()
        print("CLICK email FILTER")

    def click_role_filter(self):
        self.get_role_filter().click()
        print("CLICK role FILTER")

    # METHODS

    def client_page(self):
        with allure.step("Check filters"):
            Logger.add_start_step(method='Check filters')
            self.get_current_url()
            time.sleep(10)
            self.click_role_button()
<<<<<<< HEAD
            time.sleep(3)

            # MongoDB code for descending order
            collection1 = self.client1["auth"]["User"]
            query = {"isDeleted": False}



            sort = [(u"name", 1)]

            cursor = collection1.find(query, sort=sort, limit=1)
            name_from_db = None
            try:
                for doc in cursor:
                    name_from_db = doc["name"]
            except Exception as e:
                print(f"Error: {e}")

            assert_equal(name_from_db, self.get_check_name().text,
                         "The name from the database does not match the one on the webpage")
            print("data is correct")
            ###############################################TODO PPPPPPPPPPP
            self.click_name_filter2()

            collection1 = self.client1["auth"]["User"]
            query = {"isDeleted": False}

            sort = [(u"name", -1)]

            cursor = collection1.find(query, sort=sort, limit=1)
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
            self.click_email_filter()

            collection1 = self.client1["auth"]["User"]
            query = {"isDeleted": False}

            projection = {"email": u"$email", "_id": 0}

            sort = [(u"email", 1)]

            cursor = collection1.find(query, projection=projection, sort=sort, limit=1)
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
            collection1 = self.client1["auth"]["User"]
            query = {"isDeleted": False}

            projection = {"email": u"$email", "_id": 0}

            sort = [(u"email", -1)]

            cursor = collection1.find(query, projection=projection, sort=sort, limit=1)
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
            self.assert_word(self.get_check_role(), "Admin")
            self.click_role_filter()
            self.assert_word(self.get_check_role(), "")

            # MongoDB code for descending order
            collection = self.client["auth"]["User"]
            query = {"isDeleted": False}

            projection = {"role": u"$role", "_id": 0}

            sort = [(u"role", -1)]

            cursor = collection.find(query, projection=projection, sort=sort, limit=1)
            role_from_db_asc = None
            try:
                for doc in cursor:
                    role_from_db_asc = doc["role"]
            except Exception as e:
                print(f"Error: {e}")

            self.assert_equal(role_from_db_asc, self.get_check_role().text,
                              "The email from the database does not match the one on the webpage")
            print("correct data")
            ######################TODO PPPPPPPPPPPPPPPPPPPPPPPPPP
            self.click_role_filter()

            # MongoDB code for descending order
            collection = self.client["auth"]["User"]
            query = {"isDeleted": False}

            projection = {"role": u"$role", "_id": 0}

            sort = [(u"role", 1)]

            cursor = collection.find(query, projection=projection, sort=sort, limit=1)
            role_from_db_desc = None
            try:
                for doc in cursor:
                    role_from_db_desc = doc["role"]
            except Exception as e:
                print(f"Error: {e}")

            self.assert_equal(role_from_db_desc, self.get_check_role().text,
                              "The email from the database does not match the one on the webpage")
            print("correct data")
            #####################TODO PPPPPPPPPPPPPPPPPPPPPPPPPP
            self.close_connection()
            self.click_name_filter2()

    def close_connection(self):
        try:
            self.client1.close()
            print("Connection closed successfully")
        except Exception as e:
            print(f"Error closing connection: {e}")
=======
            # time.sleep(3)
            #
            # # MongoDB code for descending order
            # collection1 = self.client1["auth"]["User"]
            # query = {"isDeleted": False}
            #
            #
            #
            # sort = [(u"name", 1)]
            #
            # cursor = collection1.find(query, sort=sort, limit=1)
            # name_from_db = None
            # try:
            #     for doc in cursor:
            #         name_from_db = doc["name"]
            # except Exception as e:
            #     print(f"Error: {e}")
            #
            # assert_equal(name_from_db, self.get_check_name().text,
            #              "The name from the database does not match the one on the webpage")
            # print("data is correct")
            # ###############################################TODO PPPPPPPPPPP
            # self.click_name_filter2()
            #
            # collection1 = self.client1["auth"]["User"]
            # query = {"isDeleted": False}
            #
            # sort = [(u"name", -1)]
            #
            # cursor = collection1.find(query, sort=sort, limit=1)
            # name_from_db_desc = None
            # try:
            #     for doc in cursor:
            #         name_from_db_desc = doc["name"]
            # except Exception as e:
            #     print(f"Error: {e}")
            #
            # assert_equal(name_from_db_desc, self.get_check_name().text,
            #              "The name from the database does not match the one on the webpage")
            # print("correct data")
            # ######################TODO PPPPPPPPPPPPPPPP
            # self.click_email_filter()
            #
            # collection1 = self.client1["auth"]["User"]
            # query = {"isDeleted": False}
            #
            # projection = {"email": u"$email", "_id": 0}
            #
            # sort = [(u"email", 1)]
            #
            # cursor = collection1.find(query, projection=projection, sort=sort, limit=1)
            # email_from_db_asc = None
            # try:
            #     for doc in cursor:
            #         email_from_db_asc = doc["email"]
            # except Exception as e:
            #     print(f"Error: {e}")
            #
            # assert_equal(email_from_db_asc, self.get_check_email().text,
            #              "The email from the database does not match the one on the webpage")
            # print("correct data")
            # ######################TODO PPPPPPPPPPPPPPPPPPPPPPPPPP
            # self.click_email_filter()
            #
            # # MongoDB code for descending order
            # collection1 = self.client1["auth"]["User"]
            # query = {"isDeleted": False}
            #
            # projection = {"email": u"$email", "_id": 0}
            #
            # sort = [(u"email", -1)]
            #
            # cursor = collection1.find(query, projection=projection, sort=sort, limit=1)
            # email_from_db_asc = None
            # try:
            #     for doc in cursor:
            #         email_from_db_asc = doc["email"]
            # except Exception as e:
            #     print(f"Error: {e}")
            #
            # assert_equal(email_from_db_asc, self.get_check_email().text,
            #              "The email from the database does not match the one on the webpage")
            # print("correct data")
            #
            # ######################TODO PPPPPPPPPPPPPPPPPPPPPPPPPP
            # self.click_role_filter()
            # self.assert_word(self.get_check_role(), "Admin")
            # self.click_role_filter()
            # self.assert_word(self.get_check_role(), "")

            # # MongoDB code for descending order
            # collection = self.client["auth"]["User"]
            # query = {"isDeleted": False}
            #
            # projection = {"role": u"$role", "_id": 0}
            #
            # sort = [(u"role", -1)]
            #
            # cursor = collection.find(query, projection=projection, sort=sort, limit=1)
            # role_from_db_asc = None
            # try:
            #     for doc in cursor:
            #         role_from_db_asc = doc["role"]
            # except Exception as e:
            #     print(f"Error: {e}")
            #
            # self.assert_equal(role_from_db_asc, self.get_check_role().text,
            #                   "The email from the database does not match the one on the webpage")
            # print("correct data")
            # ######################TODO PPPPPPPPPPPPPPPPPPPPPPPPPP
            # self.click_role_filter()

            # # MongoDB code for descending order
            # collection = self.client["auth"]["User"]
            # query = {"isDeleted": False}
            #
            # projection = {"role": u"$role", "_id": 0}
            #
            # sort = [(u"role", 1)]
            #
            # cursor = collection.find(query, projection=projection, sort=sort, limit=1)
            # role_from_db_desc = None
            # try:
            #     for doc in cursor:
            #         role_from_db_desc = doc["role"]
            # except Exception as e:
            #     print(f"Error: {e}")
            #
            # self.assert_equal(role_from_db_desc, self.get_check_role().text,
            #                   "The email from the database does not match the one on the webpage")
            # print("correct data")
            ######################TODO PPPPPPPPPPPPPPPPPPPPPPPPPP
            # self.close_connection()
            # self.click_name_filter2()

    # def close_connection(self):
    #     try:
    #         self.client1.close()
    #         print("Connection closed successfully")
    #     except Exception as e:
    #         print(f"Error closing connection: {e}")
>>>>>>> 51a303e (Initial commit)
