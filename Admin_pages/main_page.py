import time



import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base.base_class import Base
from utilities.logger import Logger


class Main_page(Base):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators

    product_1 = "//button[@id='add-to-cart-sauce-labs-backpack']"
    product_2 = "//*[@id='add-to-cart-sauce-labs-bike-light']"
    product_3 = "//*[@id='add-to-cart-sauce-labs-bolt-t-shirt']"
    cart = "//*[@id='shopping_cart_container']/a"
    burger_button = '//*[@id="react-burger-menu-btn"]'
    link_about = "//*[@id='about_sidebar_link']"

    # Getters
    def get_cart(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.cart)))

    def get_product_1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.product_1)))

    def get_product_2(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.product_2)))

    def get_product_3(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.product_3)))

    def get_burger_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.burger_button)))

    def get_link_about(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.link_about)))

    # Actions

    def click_select_product_1(self):
        self.get_product_1().click()
        print("CLICK product1")

    def click_select_product_2(self):
        self.get_product_2().click()
        print("CLICK product2")

    def click_select_product_3(self):
        self.get_product_2().click()
        print("CLICK product3")

    def click_cart(self):
        self.get_cart().click()
        print("CLICK product")

    def click_burger_button(self):
        self.get_burger_button().click()
        print("CLICK menu")

    def click_link_about(self):
        self.get_link_about().click()
        print("CLICK about")

    # METHODS
    def select_product(self):
        with allure.step("Select product"):
            Logger.add_start_step(method='select_product')
            self.get_current_url()
            self.click_select_product_1()
            self.click_cart()
            Logger.add_end_step(url=self.driver.current_url, method='select_product')

    def select_product_2(self):
        self.get_current_url()
        self.click_select_product_2()
        self.click_cart()

    def select_product_3(self):
        self.get_current_url()
        self.click_select_product_3()
        self.click_cart()

    def select_menu_about(self):
        with allure.step("select menu about"):
            self.click_burger_button()
            self.get_current_url()
            self.click_link_about()
            self.assert_url("https://saucelabs.com/")

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
