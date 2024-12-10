import time
import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from database.Databricks import Databricks
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
<<<<<<< HEAD
from ev import EV

class Edit_AAD_DELETE_user(Base, Database, Databricks, EV):
=======


class Edit_AAD_DELETE_user(Base, Database, Databricks):
>>>>>>> 51a303e (Initial commit)

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver
        Databricks.__init__(self)

    # Locators
    successful_changes = '//div[contains(@class, "ant-message-notice-content")]//span[contains(@class, "anticon-check-circle")]//following-sibling::span'
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
    ncn = "//span[text()='Please select a company.']"
    Accessibility_button = '//div[contains(@class, "ant-tabs-tab-btn") and text()="Permissions"]'
    AccountInfo = "//div[@data-node-key='accountInfo' and contains(@class, 'ant-tabs-tab-active')]//div[@role='tab']"
    cancel_button = "/html/body/div[3]/div/div[2]/div/div[2]/div[3]/button[1]"
    select_company = '//*[@id="rc-tabs-0-panel-accessibility"]/div[1]'
    select_all = "//*[@id='rc-tabs-0-panel-accessibility']/div[3]/button[1]"
    deselect = '//*[@id="rc-tabs-0-panel-accessibility"]/div[2]/button[1]/span[2]'
    clear_companies = '//*[@id="rc-tabs-0-panel-accessibility"]/div[2]/button[2]'
    clear_companies1 = '//*[@id="rc-tabs-0-panel-accessibility"]/div[3]/button[2]'
    first_company = '//div[@aria-selected="false" and contains(@class, "ant-select-item")]'
    last_company = '//div[contains(@class, "ant-select-item-option-content") and text()="美域翻译"]'
    x1C_for_assert = "//*[@id='rc-tabs-0-panel-accessibility']/div[1]/div/div/div[1]/span/span[1]"
    x2C_for_assert = '//*[@id="rc-tabs-0-panel-accessibility"]/div[1]/div/div/div[768]/span/span[1]'
    Cancel = "//span[text()='Cancel']"
    ACC = '//div[contains(@class, "ant-tabs-tab-btn") and text()="Accessibility"]'
    select_clients_name = '//*[@id="rc-tabs-0-panel-accessibility"]/div[2]/div'
    first_client_name = '//div[contains(text(), "OPI - Delnor")]'

    email_field = "//*[@id='email']"
    password_field = "//*[@id='password']"
    confirm_password = "//*[@id='confirm']"

    activation_mail = "/html/body/div[2]/div/div/div/span[2]"
    password_dont_math = "//*[@id='confirm_help']/div"
    password_dont_meet_criteria = "//*[@id='password_help']/div"

    check_name = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]/div/span/span[2]"
    fake_name = "//*[@id='firstname_help']"
    fake_name2 = "//*[@id='lastname_help']"

    # Getters
    def get_deselect(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.deselect)))
    def get_clear_companies1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.clear_companies1)))

    def get_fake_name2(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.fake_name2)))

    def get_fake_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.fake_name)))

    def get_email_value(self):
        check_email_element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//*[@id="root"]/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]'))
        )
        return check_email_element.text

    def get_check_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_name)))

    def get_last_name_value(self):
        last_name_element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.last_name_field))
        )
        return last_name_element.get_attribute("value")

    def assert_email_message(self):
        email_value = self.get_email_value()
        expected_message = self.form_message_with_email(email_value)
        self.assert_word(self.get_suc_changes(), expected_message)

    def form_message_with_email(self, email_value):
        return f"User: {email_value} has been updated."

    def get_cancel(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.Cancel)))

    def get_ncn(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.ncn)))

    def get_clients_name(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.select_clients_name)))

    def get_ACC(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.ACC)))

    def get_f_c_n(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.first_client_name)))

    def get_suc_changes(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.successful_changes)))

    def get_INFO(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.AccountInfo)))

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
        SC = self.get_select_company()
        action = ActionChains(self.driver)
        action.move_to_element(SC).click().perform()
        print("click select company")

    def click_all_companies(self):
        self.get_select_all_companies().click()
        print("CLICK all companies")

    def click_ACC(self):
        Acc = self.get_ACC()
        self.driver.execute_script("arguments[0].click();", Acc)
        print("Clicked Accessibility button")

    def click_f_c_n(self):
        fcn = self.get_f_c_n()
        self.driver.execute_script("arguments[0].click();", fcn)
        print("Clicked First client name")

    def click_clients_name(self):
        self.get_clients_name().click()

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

    def click_INFO(self):
        INFO_element = self.get_INFO()
        self.driver.execute_script("arguments[0].click();", INFO_element)
        print("CLICK INFO")

    def click_clear(self):
        self.get_clear().click()
        print("CLICK clear")

    def click_cancel(self):
        self.get_cancel().click()
        print("CLICK cancel")

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

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    # METHODS

    def edit_u(self):
        with allure.step("Edit User without companies"):
            Logger.add_start_step(method='Edit User without companies')
            self.get_current_url()
            self.click_edit_button()
            self.assert_url("https://staging.vip.voyceglobal.com/pages/role-hierarchy")
            time.sleep(3)
            name_element = self.get_name_field()
            time.sleep(3)
            self.clear_input_field(name_element)
            self.assert_word(self.get_no_first_name(), "Please input First name!")
            time.sleep(5)
            self.input_name('tttzzzzzzzzzzfrer4regfre;;;zzzzz')
            time.sleep(2)
            self.assert_word(self.get_fake_name(),
                             "First name cannot be longer than 30 characters\nOnly alphabets and hyphens are allowed")
            self.clear_input_field(name_element)
            time.sleep(5)
            self.clear_input_field(self.get_last_name_field())
            time.sleep(2)
            self.input_last_name('hhhzrrrrrrfhzz65erfrefrf;;;zzzz')
            time.sleep(2)
            self.assert_word(self.get_fake_name2(),
                             "Last name cannot be longer than 30 characters\nOnly alphabets and hyphens are allowed")
            self.clear_input_field(self.get_last_name_field())
            random_string = self.generate_random_string(5)
            generated_name = f'zzzzzzzzzzz{random_string}'
            self.input_name(generated_name)
            last_name_element = self.get_last_name_field()
            self.clear_input_field(last_name_element)
            self.assert_word(self.get_no_last_name(), "Please input last name!")
            self.clear_input_field(last_name_element)
            self.input_last_name('zzzzzzzzzzzzzzzzzzzz')
            self.assert_field_value(self.get_last_name_field(), 'zzzzzzzzzzzzzzzzzzzz')
            self.click_select_role_button()
            self.click_user()
            self.click_save_button()
            time.sleep(3)
            self.get_clear_companies1().click()
            time.sleep(2)
            self.click_save_button()
            self.assert_word(self.get_ncn(), 'Please select a company.')

        # TODO BUG НЕ Добвляя комании к клиентам, клиент может все равно просматривать все компани & неограниченное кол-во символов/запрещенные символы

        with allure.step("Edit User"):
            Logger.add_start_step(method='Edit User')
            self.click_select_company()
            self.click_first_company()
            self.click_all_companies()
            self.click_save_button()
            collection = self.client["auth-customer"]["User"]

            # Изменим запрос, чтобы проверить, что email равен 'zzz@voyceglobal.com' и assignAll равно True
            query = {"email": "zzz@voyceglobal.com", "assignAll": True, "isDeleted": False}

            # Так как нам нужен только факт наличия такой записи, изменять проекцию не требуется, если вы не хотите получить дополнительные данные
            projection = {"_id": 0, "email": 1, "assignAll": 1}

            # Сортировка по полю email в обратном порядке, как в вашем примере, но это опционально, если вы ищете конкретный email
            sort = [("email", -1)]

            # Изменение параметра limit не требуется, если мы ожидаем найти только одну запись
            cursor = collection.find(query, projection=projection, sort=sort, limit=1)
            email_from_db = None
            try:
                for doc in cursor:
                    email_from_db = doc["email"]
                    # Проверяем также, что assignAll действительно True, хотя запрос уже это учитывает
                    assert doc["assignAll"] == True, "assignAll is not True for the given email"
            except Exception as e:
                print(f"Error: {e}")
            print("correct data")
            time.sleep(3)
            self.click_edit_button()
            self.click_save_button()
            self.get_deselect().click()
            self.click_select_company()
            self.click_first_company()
            self.click_clients_name()
            self.click_f_c_n()
            self.click_clients_name()
            self.click_save_button()
            self.assert_email_message()
            self.assert_word(self.get_check_name(), f'{generated_name} zzzzzzzzzzzzzzzzzzzz')
            # TODO BUG Добвляя комании к клиентам, клиент может все равно просматривать все компани & неограниченное кол-во символов/запрещенные символ
<<<<<<< HEAD
#
=======
>>>>>>> 51a303e (Initial commit)
