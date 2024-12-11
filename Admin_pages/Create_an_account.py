import time
import allure
import pyautogui
from utilities.logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
import string
import random
from database.Database import Database


class Create_Account(Base, Database):

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver

    open_create_account_button = "//*[@id='root']/section/section/main/div/div/div/div/div/div[1]/div/div/button/span[2]"
    first_name = "//*[@id='firstname']"
    last_name = "//*[@id='lastname']"
    email_field = "//*[@id='email']"
    password_field = "//*[@id='password']"
    confirm_password = "//*[@id='confirm']"
    role_dropdown = '//*[@id="rc-tabs-0-panel-accountInfo"]/form/div[6]/div[1]/div/div[1]/div/div/div/span[1]'
    qa_specialist_option = "//div[contains(@class, 'ant-select-item-option-content') and text() = 'QA Specialist']"
    next_button = "//span[text()='Next']"
    add_button = "//span[text()='Add']"

    # Getters
    def get_open_create_account_button(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.open_create_account_button)))

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

    def get_role_dropdown(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.role_dropdown)))

    def get_qa_specialist_option(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.qa_specialist_option)))

    def get_next_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.next_button)))

    def get_add_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.add_button)))

    # Actions

    def click_open_create_account_button(self):
        self.get_open_create_account_button().click()
        print("CLICK open create account button")

    def input_first_name(self, user_name):
        self.get_first_name().send_keys(user_name)
        print("input first name")

    def input_last_name(self, user_lastname):
        self.get_last_name().send_keys(user_lastname)
        print("input last name")

    def input_email(self, user_email):
        self.get_email_field().send_keys(user_email)
        print("input email")

    def input_password_field(self, user_password):
        self.get_password_field().send_keys(user_password)
        print("input password")

    def input_confirm_password(self, user_password):
        self.get_confirm_password().send_keys(user_password)
        print("input confirm password")


    def click_role_dropdown(self):
        user_element = self.get_role_dropdown()
        self.driver.execute_script("arguments[0].scrollIntoView(true);", user_element)
        location = user_element.location
        size = user_element.size
        window_x = self.driver.get_window_rect()['x']
        window_y = self.driver.get_window_rect()['y']
        x = window_x + location['x'] + size['width'] / 2
        y = window_y + location['y'] + size['height'] / 2 + 180  # смещение по оси Y на 200 пикселей
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()
        print("CLICK role dropdown")

    def click_qa_specialist_option(self):
        self.get_qa_specialist_option().click()
        print("CLICK QA Specialist option")

    def click_next_button(self):
        self.get_next_button().click()
        print("CLICK Next button")

    def click_add_button(self):
        self.get_add_button().click()
        print("CLICK Add button")

    # METHODS

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def ACC(self):
        email_list = [
            'adam1.worman@voyceglobal.com', 'adriana1.quintero@voyceglobal.com', 'aldo1.lorenzo@voyceglobal.com',
            'ana1.maria.mejia@voyceglobal.com', 'aurelio1.adames@voyceglobal.com', 'autumn1.adams@voyceglobal.com',
            'axelle1.augustin@voyceglobal.com', 'byron1.miller@voyceglobal.com', 'carlos1.alvarado@voyceglobal.com',
            'carrie1.chen@voyceglobal.com', 'cecilia1.baqueiro@voyceglobal.com',
            'christian1.cantabrana@voyceglobal.com',
            'christian1.gloverwilson@voyceglobal.com', 'claudia1.altamirano@voyceglobal.com',
            'dania1.juarez@voyceglobal.com',
            'daniel1.pirestani@voyceglobal.com', 'daniela1.rodriguez@voyceglobal.com', 'debela1.chali@voyceglobal.com',
            'ehno1.paw@voyceglobal.com', 'elizabeth1.rosas@voyceglobal.com',
            'elzebir1.delcid@voyceglobal.com', 'ghada1.mohsen@voyceglobal.com', 'gloria1.alvarez@voyceglobal.com',
            'jean1.sarlat@voyceglobal.com', 'jeremy1.waiser@voyceglobal.com',
            'jessica1.pollock@voyceglobal.com', 'jonathan1.scott@voyceglobal.com', 'juan1.carrillo@voyceglobal.com',
            'kevin1.sillas@voyceglobal.com', 'laura1.keylon@voyceglobal.com', 'leidy1.ocampo@voyceglobal.com',
            'maria1.belen@voyceglobal.com', 'maria1.jalil@voyceglobal.com', 'maria1.rivera@voyceglobal.com',
            'marianne1.bustamante@voyceglobal.com', 'martin1.cedeno@voyceglobal.com', 'matthew1.dong@voyceglobal.com',
            'mauricio1.iragorri@voyceglobal.com', 'mayra1.morante@voyceglobal.com', 'mesac1.cleus@voyceglobal.com',
            'monitordisplay1.@weyimobile.com', 'naing1.ayar@voyceglobal.com', 'natalia1.schell@voyceglobal.com',
            'ning1.hu@voyceglobal.com', 'okon1.gordon@voyceglobal.com', 'olga1.bedoya@voyceglobal.com',
            'pascal1.concepcion@voyceglobal.com', 'patrick1.faroul@voyceglobal.com', 'paula1.cassiano@voyceglobal.com',
            'qa1.tester@voyceglobal.com', 'rich1.forbes@voyceglobal.com', 'ryma1.chowdhury@voyceglobal.com',
            'sahar1.eslami@voyceglobal.com', 'sheila1.lou@voyceglobal.com', 'sthefani1.rodriguez@voyceglobal.com',
            'tara1.mocco@voyceglobal.com', 'taylor1.mcdermott@voyceglobal.com', 'terry1.quintero@voyceglobal.com',
            'valentina1.ardila@voyceglobal.com', 'wli1.@weyimobile.com', 'xiang1.@weyimobile.com',
            'yesenia1.pirestani@voyceglobal.com', 'yoshelinne1.monroy@voyceglobal.com',
            'jhadir1.mendoza@voyceglobal.com',
            'engels1.chavarria@voyceglobal.com'
        ]

        for email in email_list:
            try:
                with allure.step("ACC"):
                    Logger.add_start_step(method='ACC')
                    self.get_current_url()
                    self.click_open_create_account_button()
                    self.input_first_name("Nick")
                    self.input_last_name("TEST")
                    email_prefix = email.split('@')[0]
                    self.input_email(email_prefix)
                    self.input_password_field("Admin@2")
                    self.input_confirm_password("Admin@2")
                    self.click_next_button()
                    time.sleep(3)
                    self.click_role_dropdown()
                    time.sleep(3)
                    self.click_qa_specialist_option()
                    self.click_next_button()
                    self.click_add_button()
                    Logger.add_end_step(url=self.driver.current_url, method='Account_created')

                    self.driver.refresh()
            except Exception as e:
                print(f"Error occurred for email {email}: {e}")
                self.driver.refresh()
                continue
    # Locators

    # create_account_button = "//*[@id='root']/div/div[3]/div/div/div/div/div/div[2]/div[1]/div/button"
    # first_name = "//*[@id='firstname']"
    # last_name = "//*[@id='lastname']"
    # activation_mail = "//div[contains(@class, 'ant-message-custom-content') and contains(@class, 'ant-message-success')]//span[contains(text(), 'We sent you an activation mail to')]"
    # email_field = "//*[@id='email']"
    # password_field = "//*[@id='password']"
    # confirm_password = "//*[@id='confirm']"
    # create_account_button2 = "//*[@id='root']/div/div[3]/div/div/div/div/div/form/div/div/div[7]/div/div/div/div/div/button"
    # password_dont_math = "//*[@id='confirm_help']/div"
    # password_dont_meet_criteria = "//*[@id='password_help']/div"
    #
    # # Getters
    # def get_create_account_button(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.create_account_button)))
    #
    # def get_first_name(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.first_name)))
    #
    # def get_last_name(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.last_name)))
    #
    # def get_email_field(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.email_field)))
    #
    # def get_password_field(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field)))
    #
    # def get_confirm_password(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.confirm_password)))
    #
    # def get_create_account_button2(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.create_account_button2)))
    #
    # def get_activation_mail(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.activation_mail)))
    #
    # def get_password_dont_math(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_dont_math)))
    #
    # def get_password_dont_meet_criteria(self):
    #     return WebDriverWait(self.driver, 30).until(
    #         EC.element_to_be_clickable((By.XPATH, self.password_dont_meet_criteria)))
    #
    #     # Actions
    #
    # def input_first_name(self, user_name):
    #     self.get_first_name().send_keys(user_name)
    #     print("input first name")
    #
    # def input_last_name(self, user_password):
    #     self.get_last_name().send_keys(user_password)
    #     print("input last name")
    #
    # def input_email(self, user_password):
    #     self.get_email_field().send_keys(user_password)
    #     print("input email")
    #
    # def input_password_field(self, user_password):
    #     self.get_password_field().send_keys(user_password)
    #     print("input password")
    #
    # def input_confirm_password(self, user_password):
    #     self.get_confirm_password().send_keys(user_password)
    #     print("input confirm password")
    #
    # def click_create_account(self):
    #     self.get_create_account_button().click()
    #     print("CLICK Create an Account button")
    #
    # def click_create_account_button2(self):
    #     self.get_create_account_button2().click()
    #     print("CLICK Create an Account button 2")
    #
    # # METHODS
    #
    # def generate_random_string(self, length):
    #     letters = string.ascii_lowercase
    #     return ''.join(random.choice(letters) for _ in range(length))
    #
    # def ACC(self):
    #     with allure.step("ACC"):
    #         Logger.add_start_step(method='ACC')
    #         self.get_current_url()
    #         self.click_create_account()
    #         self.assert_url("https://staging.admin.vip.voyceglobal.com/auth/signup")
    #         # self.input_first_name("Nick")
    #         # self.input_last_name("Skubi")
    #         # self.input_email('korobka')
    #         # self.input_password_field("Admin123")
    #         # self.input_confirm_password("fefcwewdweQS%")
    #         # self.click_create_account_button2()
    #         # self.assert_word(self.get_password_dont_meet_criteria(), "Password entry does not meet criteria")
    #         # self.assert_word(self.get_password_dont_math(), "The two passwords that you entered do not match!")
    #         with allure.step("Account_NOT_created"):
    #             Logger.add_end_step(url=self.driver.current_url, method='Account_NOT_created')
    #             self.driver.refresh()
    #             self.input_first_name("Nick")
    #             self.input_last_name("Skubi")
    #             random_string = self.generate_random_string(5)
    #             generated_email = f'korobka{random_string}.do'
    #             self.input_email(generated_email)
    #             self.input_password_field("Admin@123")
    #             self.input_confirm_password("Admin@123")
    #             self.click_create_account_button2()
    #             self.assert_word(self.get_activation_mail(),
    #                              f"We sent you an activation mail to {generated_email}@voyceglobal.com.")
    #             self.assert_url("https://staging.admin.vip.voyceglobal.com/auth/login")
    #             Logger.add_end_step(url=self.driver.current_url, method='Account_created')
    #
    #             db = self.client1['auth']
    #             collection1 = db['User']
    #
    #             query = {"email": f"{generated_email}@voyceglobal.com"}
    #
    #             cursor = collection1.find(query)
    #             email_from_db = None
    #             try:
    #                 for doc in cursor:
    #                     email_from_db = doc.get("email")
    #                     print(doc)
    #             finally:
    #                 self.client.close()
    #
    #             assert email_from_db == f"{generated_email}@voyceglobal.com"
    #             print("data is correct")
    #             self.driver.refresh()
