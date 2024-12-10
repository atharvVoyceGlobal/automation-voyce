import time

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base.base_class import Base
from utilities.logger import Logger


class Finish_screen(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators

    # Getters

    # Actions

    # METHODS
    def finish_screen_shot(self):
        with allure.step("Finish screen shot"):
            Logger.add_start_step(method='finish_screen_shot')
            self.get_current_url()
            self.assert_url("https://www.saucedemo.com/checkout-complete.html")
            self.screenshot()
            Logger.add_end_step(url=self.driver.current_url, method='finish_screen_shot')

        # error_button = WebDriverWait(self.driver, 30).until(
        #     EC.element_to_be_clickable((By.XPATH, "//*[@id='login_button_container']/div/form/div[3]")))
        # error_button1 = error_button.text
        # assert error_button1 == 'Epic sadface: Sorry, this user has been locked out.'
        # print('jopa')

        # if login == 'standard_user':
        #     user_name = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//input[@id = "
        #                                                                                            "'user-name']")))
        #     user_name.send_keys(login)
        #
        # button_login = WebDriverWait(self.driver, 30).until(
        #     EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']")))
        # button_login.click()
