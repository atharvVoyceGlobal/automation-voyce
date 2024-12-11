import time
import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from utilities.logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
from selenium.webdriver.common.action_chains import ActionChains
import string
import random
from database.Database import Database
from selenium.webdriver.support.ui import WebDriverWait


class Edit_AAD_DELETE_user(Base, Database):

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver

    # Locators
    successful_changes = "//div[contains(@class, 'ant-message-custom-content ant-message-success')]"
    check_role = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[3]"
    no_first_name = "//*[@id='firstname_help']/div"
    no_last_name = "//*[@id='lastname_help']/div"
    super_admin_element = '//div[contains(@class, "ant-select-item-option-content") and text()="Super Admin"]'
    edit_button = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[5]/div/button[1]"
    name_field = "//*[@id='firstname']"
    last_name_field = "//*[@id='lastname']"
    select_role_button = "//*[@id='rc-tabs-0-panel-accountInfo']/form/div[4]/div/div/div/div/div/div"
    admin_element = '//div[contains(@class, "ant-select-item-option-content") and text()="Admin"]'
    user_element = '//div[contains(@class, "ant-select-item-option-content") and text()="User"]'
    save_button = '//button[contains(@class, "ant-btn") and contains(@class, "ant-btn-round") and contains(@class, "ant-btn-primary") and .//span[text()="Save"]]'
    scroll = '//div[contains(@class, "rc-virtual-list-scrollbar-thumb")]'

    Accessibility_button = '//div[@data-node-key="accessibility"]'
    name_filter2 = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[1]/table/thead/tr/th[1]"
    cancel_button = "/html/body/div[3]/div/div[2]/div/div[2]/div[3]/button[1]"
    select_company = '//*[@id="rc-tabs-0-panel-accessibility"]/div[1]/div/div'
    select_all = "//*[@id='rc-tabs-0-panel-accessibility']/div[2]/button[1]"
    clear_companies = "//*[@id='rc-tabs-0-panel-accessibility']/div[2]/button[2]"
    first_company = '//div[contains(@class, "ant-select-item-option-content") and text()="180 Health Partners in Tennessee"]'
    last_company = '//div[contains(@class, "ant-select-item-option-content") and text()="美域翻译"]'
    x1C_for_assert = "//*[@id='rc-tabs-0-panel-accessibility']/div[1]/div/div/div[1]/span/span[1]"
    x2C_for_assert = '//span[text()="美域翻译"]'

    ACC = '//div[contains(@class, "ant-tabs-tab-btn") and text()="Accessibility"]'

    email_field = "//*[@id='email']"
    password_field = "//*[@id='password']"
    confirm_password = "//*[@id='confirm']"

    activation_mail = "/html/body/div[2]/div/div/div/span[2]"
    password_dont_math = "//*[@id='confirm_help']/div"
    password_dont_meet_criteria = "//*[@id='password_help']/div"

    # Getters
    def get_email_value(self):
        check_email_element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]"))
        )
        return check_email_element.text

    def form_message_with_email(self, email_value):
        return f"User: {email_value} has been updated."

    def get_scroll(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.scroll)))

    def assert_email_message(self):
        email_value = self.get_email_value()
        expected_message = self.form_message_with_email(email_value)
        self.assert_word(self.get_suc_changes(), expected_message)

    def get_ACC(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.ACC)))

    def get_name_filter2(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_filter2)))

    def get_suc_changes(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.successful_changes)))

    def get_clear(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.clear_companies)))

    def get_x2C_for_assert(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.x2C_for_assert)))

    def get_first_company(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.first_company)))

    def get_last_company(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.last_company)))

    def get_check_role(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.check_role)))

    def get_no_first_name(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.no_first_name)))

    def get_no_last_name(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.no_last_name)))

    def get_super_admin_element(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.super_admin_element)))

    def get_find_admin(self):
        return WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'User')]")))

    def get_edit_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.edit_button)))

    def get_name_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.name_field)))

    def get_last_name_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.last_name_field)))

    def get_select_role_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.select_role_button)))

    def get_save_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.save_button)))

    def get_Accessibility_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.Accessibility_button)))

    def get_admin_element(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.admin_element)))

    def get_user_element(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.user_element)))

    def get_select_company(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.select_company)))

    def get_select_all_companies(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.select_all)))

        # Actions

    def input_name(self, user_name):
        self.get_name_field().send_keys(user_name)
        print("input first name")

    def input_last_name(self, user_password):
        self.get_last_name_field().send_keys(user_password)
        print("input last name")

    def click_select_role_button(self):
        self.get_select_role_button().click()
        print("click select_role_button")

    def click_select_company(self):
        self.get_select_company().click()
        print("click select company")

    def click_ACC(self):
        Acc = self.get_ACC()
        self.driver.execute_script("arguments[0].click();", Acc)
        print("Clicked Accessibility button")

    def click_super_admin(self):
        super_admin_element = self.get_super_admin_element()
        self.driver.execute_script("arguments[0].click();", super_admin_element)
        print("Clicked on Super Admin")

    def click_admin(self):
        admin_element = self.get_admin_element()
        self.driver.execute_script("arguments[0].click();", admin_element)
        print("Clicked on Admin")

    def click_user(self):
        user_element = self.get_user_element()
        self.driver.execute_script("arguments[0].click();", user_element)
        print("Clicked on User")

    def click_save_button(self):
        save_button_element = self.get_save_button()
        self.driver.execute_script("arguments[0].click();", save_button_element)
        print("Clicked Save")

    def click_edit_button(self):
        self.get_edit_button().click()
        print("CLICK edit button")

    def click_clear(self):
        self.get_clear().click()
        print("CLICK clear")

    def click_name_filter2(self):
        self.get_name_filter2().click()
        print("CLICK name FILTER2")
    def click_all_companies(self):
        self.get_select_all_companies().click()
        print("CLICK all companies")

    def click_Accessibility_button(self):
        Accessibility_button = self.get_Accessibility_button()
        self.driver.execute_script("arguments[0].click();", Accessibility_button)
        print("Clicked Accessibility button")

    def click_first_company(self):
        first_company = self.get_first_company()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("Clicked first_company")

    def click_last_company(self):
        last_company = self.get_last_company()
        self.driver.execute_script("arguments[0].click();", last_company)
        print("Clicked last company")

    def clear_input_field(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click()
        actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND)
        actions.send_keys(Keys.DELETE)
        actions.perform()

    # METHODS

    def edit_u(self):
        with allure.step("Edit User"):
            Logger.add_start_step(method='Edit User')
            self.get_current_url()
            self.click_edit_button()
            self.assert_url('https://staging.admin.vip.voyceglobal.com/pages/role-hierarchy')
            name_element = self.get_name_field()
            self.clear_input_field(name_element)
            self.assert_word(self.get_no_first_name(), "Please input first name!")
            self.input_name('AAB')
            last_name_element = self.get_last_name_field()
            self.clear_input_field(last_name_element)
            self.assert_word(self.get_no_last_name(), "Please input last name!")
            self.input_last_name("AAB")
            self.click_select_role_button()
            self.click_super_admin()
            self.click_save_button()
            self.click_save_button()
            self.assert_email_message()
            time.sleep(5)
            self.assert_word(self.get_check_role(), 'Super Admin')
            self.click_edit_button()
            self.click_select_role_button()
            self.click_admin()
            self.click_save_button()
            self.assert_word(self.get_check_role(), 'Admin')
            self.assert_email_message()
            self.click_edit_button()
            self.click_select_role_button()
            self.click_user()
            self.click_Accessibility_button()
            self.click_select_company()
            self.click_first_company()
            self.click_select_company()
            self.click_all_companies() #TODO NEW FEATURE
            self.assert_word(self.get_x2C_for_assert(), '美域翻译')
            self.click_save_button()
            self.click_edit_button()
            self.click_ACC()
            self.click_clear()
            self.assert_word(self.get_select_company(), "")
            self.click_save_button()









            # self.click_save_button()
            # self.assert_word(self.get_check_role(), "User")
            # self.assert_email_message()
            #
            # self.input_first_name("Nick")
            # self.input_last_name("Skubi")
            # self.input_email('korobka')
            # self.input_password_field("Admin123")
            # self.input_confirm_password("fefcwewdweQS%")
            # self.click_create_account_button2()
            # self.assert_word(self.get_password_dont_meet_criteria(), "Password entry does not meet criteria")
            # self.assert_word(self.get_password_dont_math(), "The two passwords that you entered do not match!")
            # with allure.step("Account_NOT_created"):
            #     Logger.add_end_step(url=self.driver.current_url, method='Account_NOT_created')
            #     self.driver.refresh()
            #     self.input_first_name("Nick")
            #     self.input_last_name("Skubi")
            #     random_string = self.generate_random_string(5)
            #     generated_email = f'korobka{random_string}.do'
            #     self.input_email(generated_email)
            #     self.input_password_field("Admin@123")
            #     self.input_confirm_password("Admin@123")
            #     self.click_create_account_button2()
            #     time.sleep(5)
            #     self.assert_url("https://staging.admin.vip.voyceglobal.com/auth/login")
            #     self.assert_word(self.get_activation_mail(),
            #                      f"We sent you an activation mail to {generated_email}@voyceglobal.com.")
            #     Logger.add_end_step(url=self.driver.current_url, method='Account_created')
            #
            #     db = self.client['auth']
            #     collection = db['User']
            #
            #     query = {"email": f"{generated_email}@voyceglobal.com"}
            #
            #     cursor = collection.find(query)
            #     email_from_db = None
            #     try:
            #         for doc in cursor:
            #             email_from_db = doc.get("email")
            #             print(doc)
            #     finally:
            #         self.client.close()

                # assert email_from_db == f"{generated_email}@voyceglobal.com"
                # print("data is correct")
                # self.driver.refresh()
