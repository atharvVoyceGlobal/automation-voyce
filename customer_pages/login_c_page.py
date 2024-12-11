import time
import allure
from selenium.common import WebDriverException
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
from ev import EV

class Login_c_page(Base, Databricks, EV):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        Databricks.__init__(self)

    # Locators
    activity_m_b = '//*[@id="root"]/section/aside/div/ul/li[2]'
    login_field = "//*[@id='email']"
    password_field = "//*[@id='password']"
    button_login = "//*[@id='root']/div/div[3]/div/div/div/div/div/div[2]/div/form/div[3]/div/div/div/div/div/button"
    main_word = "//*[@id='header-container-id']/div/div[1]/div"
    error_email = "//*[@id='email_help']/div"
    error_password = "//*[@id='password_help']/div"
    no_valid_password = "//span[text()='Password incorrect!']"
    no_valid_email = "//span[text()='User not found!']"
    log_out = "//*[@id='root']/div/aside/div[1]/div[3]/div/button/div/div[2]/div/span"
    log_out2 = "//span[contains(@class, 'ant-typography') and contains(text(), 'Sign Out')]"
    main_word2 = "//div[contains(@class, 'rc-virtual-list-holder-inner')]"
    all_clients = "//*[@id='header-container-id']/div/div[6]/div/div/span[2]"
    company = '//*[@id="root"]/section/section/main/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[6]'

    # Getters
    def get_company(self):
        return WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, self.company)))

    def get_main_word2(self):
        return WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, self.main_word2)))

    def get_all_clients(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.all_clients)))

    def get_log_out(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.log_out)))

    def get_log_out2(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.log_out2)))

    def get_login_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.login_field)))

    def get_password_field(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.password_field)))

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
    def click_transaction_b(self):
        self.get_activity_m_b().click()
        print("CLICK Terp button")

    def input_login(self, user_name):
        self.get_login_field().send_keys(user_name)
        print("input user name")

    def input_password(self, user_password):
        self.get_password_field().send_keys(user_password)
        print("input password")

    def click_button_login(self):
        # Retrieve the element
        self.get_button_login().click()


        print("Clicked the login button at the center")

    def click_all_clients(self):
        first_company = self.get_all_clients()
        self.driver.execute_script("arguments[0].click();", first_company)
        print("Click All Clients")

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
            self.get_current_url()
            self.click_button_login()
            self.assert_word(self.get_error_email(), "Please input your email!")
            self.assert_word(self.get_error_password(), "Please input your password!")
            with allure.step("NO_DATA_authorization"):
                Logger.add_end_step(url=self.driver.current_url, method='NO_DATA_authorization')
                self.input_login(self.my_accaunt)
                self.input_password('NO_VALID')
                self.click_button_login()
                self.assert_word(self.get_no_valid_password(), "Password incorrect!")
                with allure.step("NO_VALID_PASSWORD_authorization"):
                    Logger.add_end_step(url=self.driver.current_url, method='NO_VALID_PASSWORD_authorization')
                    self.driver.refresh()
                    self.input_login("ppp")
                    self.input_password("000")
                    self.click_button_login()
                    self.assert_word(self.get_no_valid_email(), 'User not found!')
                with allure.step("NO_VALID_EMAIL_authorization"):
                    Logger.add_end_step(url=self.driver.current_url, method='NO_VALID_EMAIL_authorization')
                    self.driver.refresh()

    def authorization1(self):
        self.driver.get(self.url1)
        for email in self.emails:
            with allure.step("authorization_COOK"):
                Logger.add_start_step(method='VALID_authorization')
            try:
                time.sleep(5)
                self.input_login(email)
                self.input_password(self.deafult_password)
                self.click_button_login()
                time.sleep(3)
                self.driver.refresh()

                try:
                    # Проверка URL и слова 'Dashboard'
                    self.assert_url('https://v2.vip.voyceglobal.com/pages')
                    self.assert_word(self.get_main_word(), 'Dashboard')
                    print(email)
                    self.Log_out()
                except AssertionError as ae:
                    error_message = f"Error when checking url for {email}: {ae}"
                    Logger.add_error_log('VALID_authorization', error_message)
                    continue

            except WebDriverException as e:
                error_message = f"Authorization error for {email}: {e}"
                Logger.add_error_log('VALID_authorization', error_message)
                continue

            with allure.step("VALID_authorization"):
                Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')

    def authorization(self):
        self.driver.get(self.url)
        try:
            self.Log_out()  # Попытка выполнить выход из аккаунта
        except Exception as e:
            print(f"{e}")
        with allure.step("authorization_NM"):
            Logger.add_start_step(method='VALID_authorization')
        self.input_login(self.authorization)
        self.input_password(self.deafult_password)
        self.click_button_login()
        time.sleep(5)
        self.assert_url('https://staging.vip.voyceglobal.com/pages')
        self.assert_word(self.get_main_word(), 'Dashboard')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')
        time.sleep(3)

    def authorizationCOOK(self):
        with allure.step("authorization_COOK"):
            Logger.add_start_step(method='VALID_authorization')
        time.sleep(5)
        self.input_login(self.my_accaunt)
        self.input_password(self.deafult_password)
        self.click_button_login()
        time.sleep(10)
        self.assert_url('https://staging.vip.voyceglobal.com/pages')
        self.assert_word(self.get_main_word(), 'Dashboard')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')
        self.Log_out()

    def authorizationCOOK2(self):
        with allure.step("authorization_COOK"):
            Logger.add_start_step(method='VALID_authorization')
        time.sleep(5)
        self.input_login(self.my_accaunt)
        self.input_password(self.deafult_password)
        self.click_button_login()
        time.sleep(10)
        self.assert_url('https://staging.vip.voyceglobal.com/pages')
        self.assert_word(self.get_main_word(), 'Dashboard')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')
        self.Log_out()

    def authorization_EST(self):
        with allure.step("authorization_EST"):
            Logger.add_start_step(method='VALID_authorization')
        time.sleep(5)
        self.input_login(self.authorization_EST)
        self.input_password(self.deafult_password)
        self.click_button_login()
        time.sleep(3)
        self.assert_url('https://staging.vip.voyceglobal.com/pages')
        self.assert_word(self.get_main_word(), 'Dashboard')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')

    def authorization_check_company(self):
        with allure.step("authorization_check_company"):
            Logger.add_start_step(method='VALID_check_company')
        time.sleep(3)
        self.driver.maximize_window()
        self.input_login(self.authorization_check_company)
        self.input_password(self.deafult_password)
        self.click_button_login()
        time.sleep(5)
        self.assert_url('https://staging.vip.voyceglobal.com/pages')
        self.click_transaction_b()
        self.assert_word(self.get_company(), 'OPI - Delnor')

        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')

    def authorization_new_york(self):
        self.driver.get(self.url1)
        try:
            self.Log_out()  # Попытка выполнить выход из аккаунта
        except Exception as e:
            print(f"{e}")

        with allure.step("authorization_indiana"):
            Logger.add_start_step(method='VALID_check_company_indiana')
        time.sleep(10)
        self.input_login(self.authorization_new_york33)
        self.input_password(self.deafult_password)
        self.click_button_login()
        time.sleep(5)
        self.assert_url('https://staging.vip.voyceglobal.com/users/customer')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')

    def authorization_Yale(self):
        self.driver.get(self.url)
        try:
            self.Log_out()  # Попытка выполнить выход из аккаунта
        except Exception as e:
            print(f"{e}")
        with allure.step("authorization_Yale"):
            Logger.add_start_step(method='VALID_authorization')
        self.input_login(self.authorization_Yale)
        self.input_password(self.deafult_password)
        self.click_button_login()
        time.sleep(5)
        self.assert_url('https://staging.vip.voyceglobal.com/pages')
        self.assert_word(self.get_main_word(), 'Dashboard')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')
        time.sleep(3)

    def authorization_for_widjets(self):
        with allure.step("authorization"):
            Logger.add_start_step(method='VALID_check_company_indiana')
        time.sleep(10)
        self.input_login(self.authorization_for_widjets)
        self.input_password(self.deafult_password)
        self.click_button_login()
        time.sleep(5)
        self.assert_url('https://staging.vip.voyceglobal.com/pages')
        with allure.step("VALID_authorization"):
            Logger.add_end_step(url=self.driver.current_url, method='VALID_authorization')

        # query = "select child.Id as Id, child.RequestId as ReferenceTransactionId, q2.IOSSerialNumber AS IOSSerialNumber, ceil(child.ServiceSeconds/60) as ServiceMinutes, master.RequestTime as RequestTime, date_format(master.RequestTime, 'HH:mm:ss') as ExtractedTime, timezone.TimeZoneId as Timezone, master.ClientUserName AS UserName, child.ProviderFirstName AS InterpreterFirstName, master.RowDate AS Date, child.WaitSeconds AS WaitingSeconds, master.RequestCompanyId AS CompanyId, master.ClientName AS ClientName, child.ProviderId AS InterpreterId, lang.EnglishName AS TargetLanguage, IF(child.RoutedToBackup, 'Yes', 'No') AS RouteToBackup, child.ServiceStartTime AS ServiceStartTime, IF(master.IsVideo, 'Video', 'Audio') AS VideoOption, CASE WHEN master.CallerId = '9999999999' THEN 'Application' ELSE master.CallerId END AS CallerId, child.CancelTime AS ServiceCancelTime, eval.Answer AS CallQualityRatingStar, companyProduct.Name AS RequestProductName, CASE WHEN req.RequestStatusCodeId = 1 THEN 'New' WHEN req.RequestStatusCodeId = 2 THEN 'In Service' ELSE CASE WHEN master.ServiceItemStatusCodeId = 3 THEN 'Pending' ELSE CASE WHEN child.ServiceSeconds > 0 THEN 'Serviced' ELSE 'Cancelled' END END END AS Status FROM voyce.serviceitemmaster AS master INNER JOIN voyce.serviceitemdetail AS child ON master.id = child.ServiceItemMasterId INNER JOIN voyce.request AS req ON child.RequestId = req.Id INNER JOIN voyce.billcompanyproduct AS companyProduct ON companyProduct.Id = master.RequestBillCompanyProductId INNER JOIN voyce.language AS lang ON lang.Id = child.TargetLanguageId LEFT JOIN voyce.requesteval AS eval ON eval.RequestId = child.RequestId AND eval.EvalQuestionId = 1 LEFT JOIN voyce.companytimezone AS timezone ON master.RequestCompanyId = timezone.CompanyId LEFT JOIN hive_metastore.voyce.requestpersonsession AS q1 ON q1.RequestId = master.RequestId LEFT JOIN (SELECT DISTINCT PersonSessionId, FIRST_VALUE(PropertyValue) OVER (PARTITION BY PersonSessionId) AS IOSSerialNumber FROM hive_metastore.voyce.PersonSessionProperty WHERE PropertyName = 'SerialNumber' AND PropertyType = 'SerialNumber') AS q2 ON q2.PersonSessionId = q1.PersonSessionId WHERE master.RowDate > CURRENT_DATE() - INTERVAL 1 DAY AND master.RequestCompanyId = 1090 AND lang.EnglishName NOT IN ('Spanish', 'American Sign Language (ASL)') AND master.IsVideo = true ORDER BY master.RequestTime DESC;"
        # try:
        #     with self.client0.cursor() as cursor:
        #         cursor.execute(query)
        #         result = cursor.fetchall()
        #         for row in result:
        #             print(row)
        # except Exception as e:
        #     print("An error occurred while executing the Databricks query:", e)

    def Log_out(self):
        with allure.step("log_out"):
            Logger.add_start_step(method='log_out')
        self.click_log_out()
        time.sleep(2)
        self.click_log_out2()
#