import time
import allure
import threading
from utilities.logger import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base


class Login_page(Base):
    url = 'https://staging.admin.vip.voyceglobal.com/auth/login'
    url1 = 'https://admin.vip.voyceglobal.com/auth/login'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators

    login_field = "//*[@id='email']"
    password_field = "//*[@id='password']"
    button_login = "//*[@id='root']/div/div[3]/div/div/div/div/div/div[2]/div[4]/form/div[3]/div/div/div/div/div/button"
    main_word = "//*[@id='header-container-id']/div/div[1]/div"
    error_email = "//*[@id='email_help']/div"
    error_password = "//*[@id='password_help']/div"
    no_valid_password = "/html/body/div[2]/div/div/div/span[2]"
    no_valid_email = "/html/body/div[2]/div/div/div/span[2]"
    log_out = "//*[@id='root']/section/aside/div/div[3]/div/div/span/span"
    log_out2 = "//li[contains(@class, 'ant-dropdown-menu-item') and contains(@class, 'ant-dropdown-menu-item-danger') and .//span[contains(@class, 'ant-dropdown-menu-title-content') and text()='Logout']]"

    # Getters
    def get_log_out(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.log_out)))

    def get_log_out2(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.log_out2)))

    def get_login_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.login_field)))

    def get_password_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field)))

    def get_no_valid_password(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.no_valid_password)))

    def get_no_valid_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.no_valid_email)))

    def get_button_login(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.button_login)))

    def get_main_word(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.main_word)))

    def get_error_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_email)))

    def get_error_password(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_password)))

        # Actions

    def input_login(self, user_name):
        self.get_login_field().send_keys(user_name)
        print("input user name")

    def input_password(self, user_password):
        self.get_password_field().send_keys(user_password)
        print("input password")

    def click_button_login(self):
        self.get_button_login().click()
        print("CLICK login button")

    def click_log_out(self):
        self.get_log_out().click()
        print("CLICK logs out")

    def click_log_out2(self):
        self.get_log_out2().click()
        print("CLICK logs out 2")

    # METHODS

    def NVP_authorization(self):
        with allure.step("authorization"):
            Logger.add_start_step(method='authorization')
            self.driver.get(self.url)
            self.get_current_url()
            self.click_button_login()
            self.assert_word(self.get_error_email(), "'email' is required")
            self.assert_word(self.get_error_password(), "Please input your password!")
            with allure.step("NO_DATA_authorization"):
                Logger.add_end_step(url=self.driver.current_url, method='NO_DATA_authorization')
                self.input_login('nikita.barshchuk')
                self.input_password('NO_VALID')
                self.click_button_login()
                self.assert_word(self.get_no_valid_password(), "password is not valid")
                with allure.step("NO_VALID_PASSWORD_authorization"):
                    Logger.add_end_step(url=self.driver.current_url, method='NO_VALID_PASSWORD_authorization')
                    self.driver.refresh()
                    self.input_login("ppp")
                    self.input_password("000")
                    self.click_button_login()
                    self.assert_word(self.get_no_valid_email(), "user not found")
                with allure.step("NO_VALID_EMAIL_authorization"):
                    Logger.add_end_step(url=self.driver.current_url, method='NO_VALID_EMAIL_authorization')
                    self.driver.refresh()

    def authorization(self):
        self.driver.get(self.url)
        self.input_login("nikita.barshchuk")
        self.input_password("Admin@123")
        self.click_button_login()
        time.sleep(30)
        self.assert_url('https://staging.admin.vip.voyceglobal.com/pages')
        self.assert_word(self.get_main_word(), 'Dashboard')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')

    def authorization_individual(self):
        local_driver_service = ChromeService(
            executable_path='/Users/nikitabarshchuk/PycharmProjects/pythonProject3/chromedriver')
        local_driver = webdriver.Chrome(service=local_driver_service)
        try:
            local_driver.get(self.url)
            WebDriverWait(local_driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.login_field))).send_keys(
                "nikita.barshchuk")
            WebDriverWait(local_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.password_field))).send_keys("Admin@123")
            WebDriverWait(local_driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.button_login))).click()

            # Здесь используем WebDriverWait для проверки успешной загрузки страницы
            WebDriverWait(local_driver, 30).until(
                lambda driver: driver.current_url == 'https://staging.admin.vip.voyceglobal.com/pages'
            )
            assert WebDriverWait(local_driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.main_word))).text == 'Dashboard'
        finally:
            local_driver.quit()

    def authorization20(self):
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=self.authorization_individual)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

###TODO nikita.barshchuk PASSQORD: Gomynkyl165432_#
    def authorization_QA_HUD(self):
        self.driver.get(self.url)
        self.input_login("nikita.qa")
        self.input_password("Admin@123")
        self.click_button_login()
        time.sleep(30)
        self.assert_word(self.get_main_word(), 'Dashboard')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')


    def authorization_PROD(self):
        self.driver.get('https://admin.vip.voyceglobal.com/auth/login')
        self.input_login("nikita.barshchuk")
        self.input_password("Gomynkyl165432_#")
        self.click_button_login()
        time.sleep(5)
        self.assert_url('https://admin.vip.voyceglobal.com/pages')
        self.assert_word(self.get_main_word(), 'Dashboard')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')

    def Log_out(self):
        self.click_log_out()
        self.click_log_out2()


    def log_in_Wei_Portal(self):
        self.driver.get('https://voyceglobal.com/manager/Main/VoyceCSRCompanys.aspx?LoginSessionId=442291&LoginProcessorId=968232&VoyceToken=55F5F1878BFA4CBBAB3273FF49FB0C49&v=202404101611494813&NavMenu=NavMenu_ProfileGeneral&func=')
        self.input_login("nikita.barshchuk@voyceglobal.com")
        self.input_password("cC086B58")
        self.click_button_login()
        time.sleep(5)
        self.assert_url('https://admin.vip.voyceglobal.com/pages')
        self.assert_word(self.get_main_word(), 'Dashboard')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')

# def test_VIP():
#     driver = webdriver.Chrome(
#         service=ChromeService(executable_path='\\Users\\nikitabarshchuk\\PycharmProjects\\resource\\chromedriver'))
#     el = Login_page(driver)
#     el.NVP_authorization()
#
#
# test_VIP()

# with allure.step("authorization-no-valid"):
#     Logger.add_end_step(url=self.driver.current_url, method='no valid authorization')
#     self.input_user_name('standard_user')
#     self.click_button_login()
#     self.assert_word(self.get_main_word(), "Products")
#     Logger.add_end_step(url=self.driver.current_url, method='authorization')

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
