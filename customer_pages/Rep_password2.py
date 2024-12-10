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
from base.base_class import Base
from database.Databricks import Databricks
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
<<<<<<< HEAD
from ev import EV

class Replace_password2(Base, Databricks, Database, EV):
=======


class Replace_password2(Base, Databricks, Database):
>>>>>>> 51a303e (Initial commit)
    url = 'https://mail.google.com/mail/u/0/#inbox'

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver

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


    def press_return_key(self):
        actions = ActionChains(self.driver)

        # Выполняем нажатие на клавишу Return
        actions.send_keys(Keys.RETURN).perform()

        print("Pressed the Return key")

    def double_press_down_arrow(self):
        # Инициализируем экземпляр ActionChains
        actions = ActionChains(self.driver)

        # Выполняем двойное нажатие на стрелку вверх
        actions.send_keys(Keys.ARROW_DOWN).perform()  # второе нажатие

        print("Pressed the Down arrow key")


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

    def Forgot_PD2(self):
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
<<<<<<< HEAD
            self.input_email(self.my_accaunt)
            self.click_submit_button()
            self.assert_word(self.get_successful_send(),
                             f"Email has been successfully sent to {self.my_accaunt}")
=======
            self.input_email("nikita.barshchuk@voyceglobal.com")
            self.click_submit_button()
            self.assert_word(self.get_successful_send(),
                             "Email has been successfully sent to nikita.barshchuk@voyceglobal.com")
>>>>>>> 51a303e (Initial commit)
            time.sleep(10)

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

<<<<<<< HEAD
            assert_equal(latest_email, self.my_accaunt, "The latest email in the database does not "
=======
            assert_equal(latest_email, "nikita.barshchuk@voyceglobal.com", "The latest email in the database does not "
>>>>>>> 51a303e (Initial commit)
                                                                           "match the expected email")
            print("data is correct")
            self.driver.get(self.url)
            time.sleep(10)
            self.double_press_down_arrow()
            time.sleep(3)
            first_mail_subject = self.driver.find_element(By.CSS_SELECTOR, "tr.zA.zE.btb")
            action = ActionChains(self.driver)
            action.move_to_element(first_mail_subject).click().perform()

            # Проверка наличия элемента после нажатия self.click_f_m()
            try:
                # Попытка получить элемент и кликнуть по нему, если он найден
                if self.get_points():
                    self.click_points()
                    time.sleep(3)
                    self.click_reset_button_center()
            except NoSuchElementException:
                # Элемент не найден, продолжаем выполнение без вызова self.click_points()
                pass
            except StaleElementReferenceException:
                # Элемент был найден, но стал устаревшим в момент взаимодействия
                try:
                    # Повторный поиск элемента и попытка клика
                    if self.get_points():
                        self.click_points()
                        time.sleep(3)
                        self.click_reset_button_center()
                except (NoSuchElementException, StaleElementReferenceException):
                    # Если элемент все еще не найден или снова стал устаревшим, пропускаем действие
                    pass
            except TimeoutException:
                # Если время ожидания истекло, и элемент так и не был найден
                self.click_reset_button_center()
                time.sleep(5)

                pass
            self.click_reset_button_center()
            window_handles = self.driver.window_handles
            if len(window_handles) > 1:
                self.driver.switch_to.window(window_handles[-1])  # Переключаемся на последнюю вкладку
                self.driver.close()  # Закрываем её
            time.sleep(3)
            window_handles = self.driver.window_handles
            self.driver.switch_to.window(window_handles[-1])
            time.sleep(10)
<<<<<<< HEAD
            self.input_password1(self.deafult_password)
            time.sleep(3)
            self.input_password2(self.deafult_password)
            self.click_reset_b()
            self.assert_word(self.get_notification(), 'Password has been successfully updated')
#
=======
            self.input_password1('Admin@123')
            time.sleep(3)
            self.input_password2('Admin@123')
            self.click_reset_b()
            self.assert_word(self.get_notification(), 'Password has been successfully updated')
>>>>>>> 51a303e (Initial commit)
