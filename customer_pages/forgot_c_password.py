import time
import allure
from utilities.logger import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
from database.Database import Database, assert_equal
from ev import EV

class Forgot_password(Base, Database, EV):

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver

    # Locators

    forgot_password_button = "/html/body/div/div/div[3]/div/div/div/div/div/p/i/a"
    email = "//*[@id='email']"
    submit_button = "//*[@id='root']/div/div[3]/div/div/div/div/div/form/div/div/div[2]/div/div/div/div/div/button"
    successful_send = "/html/body/div[2]/div/div/div/span[2]"
    error_massage = "/html/body/div[2]/div/div/div/span[2]"

    # Getters
    def get_forgot_password_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.forgot_password_button)))

    def get_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.email)))

    def get_submit_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.submit_button)))

    def get_successful_send(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.successful_send)))

    def get_error_massage(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_massage)))

        # Actions

    def click_forgot_password_button(self):
        self.get_forgot_password_button().click()
        print("CLICK Forgot password")

    def input_email(self, user_password):
        self.get_email().send_keys(user_password)
        print("input email")

    def click_submit_button(self):
        self.get_submit_button().click()
        print("CLICK submit button")

    # METHODS

    def Forgot_PD(self):
        with allure.step("Forgot password"):
            Logger.add_start_step(method='Forgot password with no valid data')
            self.click_forgot_password_button()
            self.get_current_url()
            self.assert_url("https://staging.vip.voyceglobal.com/auth/forgot-password")
            self.input_email("Skubi.DO")
            self.click_submit_button()
            self.assert_word(self.get_error_massage(), "Email is not available on the server")
            self.driver.refresh()
            with allure.step("Forgot password with no valid data"):
                Logger.add_end_step(url=self.driver.current_url, method='Forgot password with no valid data')
            self.click_forgot_password_button()
            self.get_current_url()
            self.assert_url("https://staging.vip.voyceglobal.com/auth/forgot-password")
            with allure.step("Forgot password with valid data"):
                Logger.add_start_step(method='Forgot password with no valid data')
            self.input_email(self.my_accaunt)
            self.click_submit_button()
            self.assert_word(self.get_successful_send(),
                             f"Email has been successfully sent to {self.my_accaunt}")

            database = self.client["auth-customer"]
            collection = database["Email"]

            # Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

            query = {}
            projection = {"email": u"$email", "_id": 0}
            sort = [(u"createdAt", -1)]
            cursor = collection.find(query, projection=projection, sort=sort, limit=1)

            latest_email = None
            try:
                for doc in cursor:
                    print(doc)
                    latest_email = doc.get('email')
            finally:
                self.client.close()

            assert_equal(latest_email, self.my_accaunt, "The latest email in the database does not "
                                                                           "match the expected email")
            print("data is correct")
#