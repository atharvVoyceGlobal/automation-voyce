import time
import allure
from selenium.common import TimeoutException

from utilities.logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
import string
import random
from database.Database import Database
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from ev import EV

class Add_user(Base, Database, EV):

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver

    # Locators
    first_company = '//div[@aria-selected="false" and contains(@class, "ant-select-item")]'
    account_info = '//*[@id="rc-tabs-0-tab-accountInfo"]'
    add_user_button = "//*[@id='root']/section/section/main/div/div/div/div/div/div[1]/div/div/button"
    first_name = "//*[@id='firstname']"
    last_name = "//*[@id='lastname']"
    activation_mail = "//div[@class='ant-message-notice-content']/div[@class='ant-message-custom-content ant-message-success']/span[@role='img'][@class='anticon anticon-check-circle']/following-sibling::span"
    email_field = "//*[@id='email']"
    password_field = "//*[@id='password']"
    confirm_password = "//*[@id='confirm']"
    create_account_button2 = "//*[@id='root']/div/div[3]/div/div/div/div/div/form/div/div/div[" \
                             "7]/div/div/div/div/div/button"
    password_dont_math = "//*[@id='confirm_help']/div"
    password_dont_meet_criteria = "//*[@id='password_help']/div"
    next = '//span[text()="Next"]'
    add = "//span[text()='Add']"

    error_fn = '//*[@id="firstname_help"]/div'
    error_ln = '//*[@id="lastname_help"]/div'
    error_e = '//*[@id="email_help"]/div'
    error_p = '//*[@id="password_help"]/div'
    error_cp = '//*[@id="confirm_help"]/div'
    error_r = '//*[@id="role_help"]/div'
    select_role_button = "//*[@id='rc-tabs-0-panel-accountInfo']/form/div[6]/div/div/div/div/div/div"
    user_element = '//div[contains(@class, "ant-select-item-option-content") and text()="User"]'
    check_name = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]"
    delete = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[5]/div/button[2]"
    del_ok = "//button[@type='button' and contains(@class, 'ant-btn') and contains(@class, 'ant-btn-round') and contains(@class, 'ant-btn-primary') and contains(@class, 'button-div') and .//span[text()='Ok']]"
    next_page = "//*[@id='root']/section/section/main/div/div/div/div/ul/li[3]/a"
    chp1 = "//*[text()='Select company names']"
    select_company = "//div[@class='ant-select-item-option-content' and text()='Northwestern Memorial Healthcare']"
    select_all = "//span[text()='Select All']"
    select_clients_name = '//*[@id="rc-tabs-0-panel-accessibility"]/div[2]/div/span'

    element_xpath2 = "//*[@id='root']/section/aside"
    theme_toggle_xpath = '//*[@id="header-container-id"]/div/div[3]/div/label[1]/span[2]'
    element_xpath = "//*[@id='root']/section/section/main/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[3]"
    additional_xpath = "//*[@id='root']/section/aside"
    first_client_name = '//div[contains(text(), "OPI - Delnor")]'

    # Getters
    def get_chp1(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.chp1)))

    def get_deselect_all(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-tabs-0-panel-accessibility"]/div[2]/button[1]/span[2]')))

    def get_one(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-tabs-0-panel-accessibility"]/div[2]/div/div')))
    def get_clients_name(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.select_clients_name)))
    def get_f_c_n(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.first_client_name)))

    def get_theme_toggle_xpath(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.theme_toggle_xpath)))

    def get_first_company(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.first_company)))

    def get_select_company(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.select_company)))

    def get_select_all_companies(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.select_all)))

    def get_next_page(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.next_page)))

    def get_del_ok(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.del_ok)))

    def get_delete(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.delete)))

    def get_check_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.check_name)))

    def get_user_element(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.user_element)))

    def get_select_role_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.select_role_button)))

    def get_error_fn(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_fn)))

    def get_error_ln(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_ln)))

    def get_error_e(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_e)))

    def get_error_p(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_p)))

    def get_error_cp(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_cp)))

    def get_error_r(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_r)))

    def get_account_info(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.account_info)))

    def get_add(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.add)))

    def get_add_user(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.add_user_button)))

    def get_next(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.next)))

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

        # Actions

    def click_clients_name(self):
        # Сброс фокуса с помощью JavaScript
        self.driver.execute_script("document.activeElement.blur();")
        time.sleep(1)  # Небольшая задержка для обработки события

        first_company = self.get_clients_name()
        actions = ActionChains(self.driver)
        actions.move_to_element(first_company).click().perform()
        time.sleep(5)

    def click_user(self):
        user_element = self.get_user_element()
        self.driver.execute_script("arguments[0].click();", user_element)
        print("Clicked on User")

    def click_select_role_button(self):
        self.get_select_role_button().click()
        print("click select_role_button")

    def input_first_name(self, user_name):
        self.get_first_name().send_keys(user_name)
        print("input first name")

    def input_last_name(self, user_password):
        self.get_last_name().send_keys(user_password)
        print("input last name")

    def click_f_c_n(self):
        fcn = self.get_f_c_n()
        actions = ActionChains(self.driver)
        actions.move_to_element(fcn).click().send_keys(
            'J').perform()  # Перемещение к элементу, клик и ввод 'J'
        print("click select company and entered 'J'")
        print("Clicked First client name")

    def click_f_c_n2(self):
        fcn = self.get_f_c_n()
        actions = ActionChains(self.driver)
        actions.move_to_element(fcn).click().perform()  # Перемещение к элементу, клик и ввод 'J'
        print("click select company and entered 'J'")
        print("Clicked First client name")

    def input_email(self, user_password):
        self.get_email_field().send_keys(user_password)
        print("input email")

    def input_password_field(self, user_password):
        self.get_password_field().send_keys(user_password)
        print("input password")

    def input_confirm_password(self, user_password):
        self.get_confirm_password().send_keys(user_password)
        print("input confirm password")

    def click_first_company(self):
        first_company = self.get_select_company()  # Получение элемента
        actions = ActionChains(self.driver)
        actions.move_to_element(first_company).click().perform()  # Перемещение к элементу, клик и ввод 'J'
        print("click select company and entered 'J'")

    def click_next(self):
        self.get_next().click()
        print("CLICK next")

    def click_add_user(self):
        self.get_add_user().click()
        print("CLICK add")

    def press_escape(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()
        print("Pressed Escape key")
    def click_info(self):
        self.get_account_info().click()
        print("CLICK info")

    def click_create_account_button2(self):
        self.get_create_account_button2().click()
        print("CLICK Create an Account button 2")

    def click_next_page(self):
        self.get_next_page().click()
        print("CLICK NEXT PAGE")

    def clear_input_field(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click()
        actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND)
        actions.send_keys(Keys.DELETE)
        actions.perform()

    def click_del_ok(self):
        self.get_del_ok().click()
        print("CLICK OK in Delete")

    def click_select_company(self):
        first_company = self.get_chp1()  # Получение элемента
        actions = ActionChains(self.driver)
        actions.move_to_element(first_company).click().perform()  # Перемещение к элементу и клик
        print("click select company")

    def click_all_companies(self):
        self.get_select_all_companies().click()
        print("CLICK all companies")

    def click_delete(self):
        self.get_delete().click()
        print("CLICK delete")

    def click_add(self):
        ad = self.get_add()
        action = ActionChains(self.driver)
        action.move_to_element(ad).click().perform()
        print("click Add")

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    # METHODS

    def add_user(self):
        with allure.step("Add user without data"):
            Logger.add_start_step(method='Add user without data')
            self.get_current_url()
            self.click_add_user()
            time.sleep(2)
            self.input_first_name("Nick")
            self.input_last_name("Skubi")
            self.input_email('korobka')
            self.input_password_field(self.deafult_password)
            self.input_confirm_password("fefcwewdweQS%")
            self.click_next()
            time.sleep(4)
            self.click_add()
            time.sleep(10)
            self.click_select_company()
            time.sleep(5)
            self.click_first_company()
            time.sleep(10)
            self.click_clients_name()
            time.sleep(5)

            self.click_f_c_n()
            time.sleep(2)
            self.click_add()
            self.click_info()
            name_element1 = self.get_first_name()
            time.sleep(1)
            self.clear_input_field(name_element1)
            name_element2 = self.get_last_name()
            time.sleep(1)
            self.clear_input_field(name_element2)
            name_element3 = self.get_email_field()
            time.sleep(1)
            self.clear_input_field(name_element3)
            name_element4 = self.get_password_field()
            time.sleep(1)
            self.clear_input_field(name_element4)
            name_element5 = self.get_confirm_password()
            time.sleep(1)
            self.clear_input_field(name_element5)

            self.assert_word(self.get_error_e(), "Please input your email")
            time.sleep(1)
            self.assert_word(self.get_error_p(), "Please input the password!")
            time.sleep(1)
            self.assert_word(self.get_error_r(), "Please enter role")
            time.sleep(1)
            self.assert_word(self.get_error_fn(), "Please input First name!")
            time.sleep(1)
            self.assert_word(self.get_error_ln(), "Please input last name!")
            time.sleep(1)
            self.assert_word(self.get_error_cp(), "Please confirm the password!")
            time.sleep(1)
            self.assert_url("https://staging.vip.voyceglobal.com/pages/role-hierarchy")
            self.input_first_name("Nick")
            self.input_last_name("Skubi")
            self.input_email('korobka')
            self.input_password_field(self.deafult_password)
            self.input_confirm_password("fefcwewdweQS%")
            self.click_select_role_button()
            self.click_user()
            self.assert_word(self.get_password_dont_meet_criteria(), "Password entry does not meet criteria")
            self.assert_word(self.get_password_dont_math(), "The two passwords that you entered do not match!")
            with allure.step("Add_user"):
                Logger.add_end_step(url=self.driver.current_url, method='Add_user')
                self.press_escape()
                self.click_add_user()
                self.input_first_name("aaab")
                self.input_last_name("Skubi")
                random_string = self.generate_random_string(5)
                generated_email = f'korobka{random_string}.do@voyceglobal.com'
                self.input_email(generated_email)
                self.input_password_field(self.deafult_password)
                self.input_confirm_password(self.deafult_password)
                self.click_select_role_button()
                self.click_user()
                self.click_next()
                time.sleep(2)
                self.click_select_company()
                time.sleep(2)
                self.click_first_company()
                time.sleep(2)
                self.click_all_companies()###TODO BUG
                time.sleep(5)
                self.click_add()
                self.assert_url("https://staging.vip.voyceglobal.com/pages/role-hierarchy")
                self.assert_word(self.get_activation_mail(),
                                 f"User {generated_email} has been successfully created.")  # TODO ПРОВЕРКА @*****.###
                Logger.add_end_step(url=self.driver.current_url, method='Account_created')

                database = self.client["auth-customer"]
                collection = database["User"]

                query = {"email": f"{generated_email}"}

                cursor = collection.find(query)
                email_from_db = None
                try:
                    for doc in cursor:
                        email_from_db = doc.get("email")
                        print(doc)
                except Exception as e:
                    print(f"Error: {e}")

                assert email_from_db == f"{generated_email}"
                print("data is correct")
                time.sleep(1)
                self.driver.refresh()
                time.sleep(30)
                self.assert_word(self.get_check_name(), "aaab Skubi")

        with allure.step("Delete user"):
            Logger.add_start_step(method='Delete user')
            self.click_delete()
            self.click_del_ok()
            time.sleep(1)
            self.assert_no_word(self.get_check_name(), "aaab Skubi")
            database = self.client["auth-customer"]
            collection = database["User"]

            query = {"email": f"{generated_email}", "isDeleted": True}

            cursor = collection.find(query)
            email_from_db = None
            try:
                for doc in cursor:
                    email_from_db = doc.get("email")
                    print(doc)
            finally:
                self.client.close()

            assert email_from_db == f"{generated_email}"
            print("data is correct")
            self.check_color_change(self.element_xpath, self.additional_xpath)
            self.driver.refresh()

    def check_color_change(self, element_xpath, additional_xpath):
        with allure.step("Change color"):
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
        theme_toggle_xpath = "//*[@id='header-container-id']/div/div[3]/div/label[1]/span[2]"
        theme_toggle = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, theme_toggle_xpath)))
        theme_toggle.click()
        print("Theme changed to light.")



        # with allure.step("Try to see next page"):
        #     Logger.add_start_step(method='Try to see next page')
        #     self.click_next_page()
        #     time.sleep(1)
        #     self.assert_word(self.get_check_name(), 'zzzzzzzzzzzoeyee zzzzzzzzzzz')

# TODO BUG Добвляя комании к клиентам, клиент может все равно просматривать все компани & неограниченное кол-во символов/запрещенные символы
#