import time
import allure
import pyautogui
from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from utilities.logger import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from base.base_class import Base
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from database.Databricks import Databricks
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
<<<<<<< HEAD
from ev import EV

class Replace_password(Base, Databricks, EV):
=======


class Replace_password(Base, Databricks):
>>>>>>> 51a303e (Initial commit)
    url = 'https://mail.google.com/mail/u/0/#inbox'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        Databricks.__init__(self)

    # Locators
    activity_m_b = '//*[@id="root"]/section/aside/div/ul/li[2]'
    login_field = "//*[@id='identifierId']"
    password_field = "//*[@id='password']/div[1]/div/div[1]/input"
    password_field1 = "//input[@placeholder='Password']"
    password_field2 = "//*[@id='confirmPassword']"
    button_login = "//*[@id='root']/div/div[3]/div/div/div/div/div/div[2]/div/form/div[3]/div/div/div/div/div/button"
    main_word = "//*[@id='header-container-id']/div/div[1]/div"
    error_email = "//*[@id='email_help']/div"
    error_password = "//*[@id='password_help']/div"
    no_valid_password = "/html/body/div[2]/div/div/div/span[2]"
    no_valid_email = "//span[text()='User not found']"
    log_out = "//span[contains(@class, 'ant-avatar') and contains(@class, 'ant-avatar-lg') and contains(@class, 'ant-avatar-circle') and contains(@class, 'ant-avatar-icon')]/span[@role='img' and @aria-label='user']"
    log_out2 = "//span[@class='ant-dropdown-menu-title-content' and text()='Logout']"
    main_word2 = "//div[contains(@class, 'rc-virtual-list-holder-inner')]"
    all_clients = "//*[@id='header-container-id']/div/div[6]/div/div/span[2]"
    company = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[6]'
    next = '//*[@id="identifierNext"]/div/button/span'
    next2 = '//*[@id="passwordNext"]/div/button/span'
    f_m = '//*[@id=":1i"]/td[4]'
    reset_button2 = "//button[@type='submit'][contains(@class, 'ant-btn')][contains(@class, 'ant-btn-primary')]/span[text()='Reset Password']"
    reset_button = "//a[contains(text(), 'Reset Password')]"
    points = '//div[@data-tooltip="Show trimmed content"]'
    notification = "//span[text()='Password has been successfully updated']"

    # Getters

    def get_notification(self):
        return WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, self.notification)))

    def get_points(self):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.points)))

    def get_reset_button(self):
        return WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, self.reset_button)))

    def get_reset_button2(self):
        return WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, self.reset_button2)))

    def get_f_m(self):
        return WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, self.f_m)))

    def get_company(self):
        return WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, self.company)))

    def get_main_word2(self):
        return WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, self.main_word2)))

    def get_all_clients(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.all_clients)))

    def get_log_out(self):
        return WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.log_out)))

    def get_next(self):
        return WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.next)))

    def get_next2(self):
        return WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.next2)))

    def get_log_out2(self):
        return WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.log_out2)))

    def get_login_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.login_field)))

    def get_password_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field)))

    def get_password_field1(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field1)))

    def get_password_field2(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field2)))

    def get_no_valid_password(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.no_valid_password)))

    def get_no_valid_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.no_valid_email)))

    def get_activity_m_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.activity_m_b)))

    def get_button_login(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.button_login)))

    def get_main_word(self):
        return WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.main_word)))

    def get_error_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_email)))

    def get_error_password(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_password)))

        # Actions

    def click_points(self):
        action = ActionChains(self.driver)
        action.move_to_element(self.get_points()).click().perform()
        print("CLICK points")

    def click_transaction_b(self):
        self.get_activity_m_b().click()
        print("CLICK Terp button")

    def input_login(self, user_name):
        self.get_login_field().send_keys(user_name)
        print("input user name")

    def input_password(self, user_password):
        self.get_password_field().send_keys(user_password)
        print("input password")

    def input_password1(self, user_password):
        self.get_password_field1().send_keys(user_password)
        print("input password")

    def input_password2(self, user_password):
        self.get_password_field2().send_keys(user_password)
        print("input password")

    def click_next(self):
        self.get_next().click()
        print("CLICK next")

    def click_reset_b(self):
        self.get_reset_button2().click()
        print("CLICK reset_button")

    def click_f_m(self):
        first_company = self.get_f_m()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK f_m")

    def click_next2(self):
        self.get_next2().click()
        print("CLICK next2")

    def click_button_login(self):
        self.get_button_login().click()
        print("CLICK login button")

    def click_all_clients(self):
        first_company = self.get_all_clients()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("Click All Clients")

    def click_log_out(self):
        first_company = self.get_log_out()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK logs out")

    def click_log_out2(self):
        first_company = self.get_log_out2()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("CLICK logs out 2")

    def click_reset_button_center(self):
        # Получаем элемент
        reset_button = self.get_reset_button()

        # Рассчитываем смещение для нажатия на центр элемента
        button_width = reset_button.size['width']
        button_height = reset_button.size['height']

        # Смещение относительно верхнего левого угла элемента для клика в центр
        offset_x = button_width / 4   # Для центра изменено с /4 на /2
        offset_y = button_height / 4   # Для центра изменено с /4 на /2

        # Прокрутка страницы к элементу
        self.driver.execute_script("arguments[0].scrollIntoView(true);", reset_button)

        # Выполняем нажатие на центр элемента
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(reset_button, offset_x, offset_y).click().perform()


        # METHODS

    def Check_gmail(self):
        self.driver.get(self.url)
<<<<<<< HEAD
        self.input_login(self.my_accaunt)
        self.click_next()
        time.sleep(3)
        self.input_password(self.my_password)
=======
        self.input_login("nikita.barshchuk@voyceglobal.com")
        self.click_next()
        time.sleep(3)
        self.input_password("Gomynkyl165432_#")
>>>>>>> 51a303e (Initial commit)
        time.sleep(3)
        self.click_next2()
        time.sleep(20)  # Замените time.sleep на явные ожидания, если возможно
        self.double_press_down_arrow()
        time.sleep(3)
        first_mail_subject = self.driver.find_element(By.CSS_SELECTOR, "tr.zA.zE.btb")
        action = ActionChains(self.driver)
        action.move_to_element(first_mail_subject).click().perform()
        print(self.driver.window_handles)

        # Проверка наличия элемента после нажатия self.click_f_m()
        try:
            if self.get_points():
                self.click_points()
                time.sleep(3)
                self.click_reset_button_center()
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            try:
                if self.get_points():
                    self.click_points()
                    time.sleep(3)
                    self.click_reset_button_center()
            except (NoSuchElementException, StaleElementReferenceException):
                pass
        except TimeoutException:
            self.click_reset_button_center()
            print(self.driver.window_handles)
            time.sleep(5)
            pass
        self.click_reset_button_center()
        print(self.driver.window_handles)
        time.sleep(20)

        window_handles = self.driver.window_handles
        if len(window_handles) > 1:
            self.driver.switch_to.window(window_handles[-1])  # Переключаемся на последнюю вкладку
            time.sleep(3)
            window_handles = self.driver.window_handles
            self.driver.switch_to.window(window_handles[-1])
            print(self.driver.window_handles)

        # Проверка наличия элементов перед вводом пароля
        password_field1 = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.password_field1)))
        password_field2 = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.password_field2)))

        # Ввод пароля
<<<<<<< HEAD
        password_field1.send_keys(self.new_password)
        time.sleep(3)
        password_field2.send_keys(self.new_password)
=======
        password_field1.send_keys('Admin@1234')
        time.sleep(3)
        password_field2.send_keys('Admin@1234')
>>>>>>> 51a303e (Initial commit)
        self.click_reset_b()
        self.assert_word(self.get_notification(), 'Password has been successfully updated')
        self.driver.refresh()

    def press_return_key(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем нажатие на клавишу Return
        actions.send_keys(Keys.RETURN).perform()

        print("Pressed the Return key")

    def double_press_down_arrow(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем двойное нажатие на стрелку вверх
        actions.send_keys(Keys.ARROW_DOWN).perform()  # второе нажатие

<<<<<<< HEAD
        print("Pressed the Down arrow key")
#
=======
        print("Pressed the Down arrow key")
>>>>>>> 51a303e (Initial commit)
