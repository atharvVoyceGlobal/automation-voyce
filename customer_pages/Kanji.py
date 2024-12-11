import os
import time
import allure
from utilities.logger import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from base.base_class import Base
from database.Databricks import Databricks
from selenium.webdriver.chrome.options import Options


class Login_Kanji(Base, Databricks):
    url = 'https://voyce.kandji.io/signin'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        Databricks.__init__(self)

    # Locators
    login_b = '//*[@id="app"]/div/div[1]/button[1]'
    login_field = "//*[@id='identifierId']"
    next = '//*[@id="identifierNext"]/div/button/span'
    next2 = '//*[@id="passwordNext"]/div/button/span'
    password_field = "//*[@id='password']/div[1]/div/div[1]/input"
    continue_login = "//div[contains(@class, 'ccaa66e69')]/button[contains(@class, 'c6141592f')]"
    main_word = "//*[@id='header-container-id']/div/div[1]/div"
    error_email = "//*[@id='email_help']/div"
    error_password = "//*[@id='password_help']/div"
    no_valid_password = "/html/body/div[2]/div/div/div/span[2]"
    no_valid_email = "//span[text()='User not found']"
    log_out = "//*[@id='root']/section/aside/div/div[3]/div/div/span/span"
    log_out2 = "//span[@class='ant-dropdown-menu-title-content' and text()='Logout']"
    main_word2 = "//div[contains(@class, 'rc-virtual-list-holder-inner')]"
    tam = "//span[text()='Try another method']"
    rec_code = '//*[@id="with-selector-list"]/li[2]/form/button'
    code_f = '//*[@id="code"]'
    continue_rec_code = "//button[@type='submit'][@name='action'][@value='default'][contains(@class, 'c6141592f')][@data-action-button-primary='true' and text()='Continue']"
    google = "//span[text()='Continue with Google']"
    filter = '//*[@id="showFiltersTooltip"]/div'
    filter2 = '//*[@id="radix-:r5:-content-devices"]/section/section[2]/section[2]/section[1]/div[2]/section/div[1]'
    filter3 = "//*[@id='radix-:r5:-content-devices']/section/section[2]/section[2]/section[1]/div[2]/section/div[1]/section[3]/section[1]"
    filter4 = "//*[@id='radix-:r5:-content-devices']/section/section[2]/section[2]/section[1]/div[2]/section/div[2]/section[1]"
    filter5 = "//*[@id='radix-:r5:-content-devices']/section/section[2]/section[2]/section[1]/div[2]/section/div[2]/section[3]/section[5]"
    filter_field = "//*[@id='radix-:r5:-content-devices']/section/section[2]/section[2]/section[1]/div[2]/section/input"
    galka = "//i[@class='far fa-check']"
    three = "//button[@class='sc-dxgOiQ dEBpxt' and text()='300']"

    # Getters
    def get_three(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.three)))

    def get_galka(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.galka)))

    def get_filter_field(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter_field)))

    def get_filter5(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter5)))

    def get_filter4(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter4)))

    def get_filter3(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter3)))

    def get_filter2(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter2)))

    def get_filter(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.filter)))

    def get_next2(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.next2)))

    def get_next(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.next)))

    def get_google(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.google)))

    def get_continue_rec_code(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.continue_rec_code)))

    def get_code_f(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.code_f)))

    def get_rec_code(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.rec_code)))

    def get_tam(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.tam)))

    def get_login_b(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.login_b)))

    def get_main_word2(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.main_word2)))

    def get_all_clients(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.all_clients)))

    def get_log_out(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.log_out)))

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
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.continue_login)))

    def get_main_word(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.main_word)))

    def get_error_email(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_email)))

    def get_error_password(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.error_password)))

        # Actions

    def input_code(self):
        # Путь к файлу с кодом
        file_path = "/Users/nikitabarshchuk/PycharmProjects/pythonProject3/customer_pages/code"
        # Считывание кода из файла
        with open(file_path, 'r') as file:
            code = file.read().strip()  # .strip() удалит пробелы и переводы строки по краям строки
        # Вводим считанный код в поле ввода
        self.get_code_f().send_keys(code)
        print("input code")

    def input_filter_field(self, name):
        self.get_filter_field().send_keys(name)
        print("Input company NAME")

    def click_300(self):
        self.get_three().click()
        print("Click three")

    def click_filter5(self):
        self.get_filter5().click()
        print("Click Filter")

    def click_galka(self):
        self.get_galka().click()
        print("Click Galka")

    def click_filter4(self):
        self.get_filter4().click()
        print("Click Filter")

    def click_filter3(self):
        self.get_filter3().click()
        print("Click Filter")

    def click_filter2(self):
        self.get_filter2().click()
        print("Click Filter")

    def click_filter(self):
        self.get_filter().click()
        print("Click Filter")

    def click_google(self):
        self.get_google().click()
        print("Click Google")

    def click_next2(self):
        self.get_next2().click()
        print("Click next")

    def click_next(self):
        self.get_next().click()
        print("Click next")

    def click_continue_rec_code(self):
        self.get_continue_rec_code().click()
        print("Click recover code")

    def click_rec(self):
        self.get_rec_code().click()
        print("Click recover code")

    def click_tam(self):
        self.get_tam().click()
        print("Click Try another methood")

    def click_login(self):
        self.get_login_b().click()
        print("Click Log in button")

    def input_login(self, user_name):
        self.get_login_field().send_keys(user_name)
        print("input user name")

    def input_password(self, user_password):
        self.get_password_field().send_keys(user_password)
        print("input password")

    def click_button_continue(self):
        self.get_button_login().click()
        print("CLICK login button")

    def click_all_clients(self):
        self.get_all_clients().click()
        print("Click All Clients")

    def click_log_out(self):
        self.get_log_out().click()
        print("CLICK logs out")

    def click_log_out2(self):
        self.get_log_out2().click()
        print("CLICK logs out 2")

    # METHODS

    def Kanji(self):
        with allure.step("Log In Kanji"):
            Logger.add_start_step(method='VALID_authorization')
        self.driver.get(self.url)
        self.click_login()
        self.click_google()
        self.input_login("nikita.barshchuk@voyceglobal.com")
        self.click_next()
        self.input_password("Gomynkyl165432_#")
        self.click_next2()
        time.sleep(10)
        self.click_filter()
        self.click_filter2()
        self.click_filter3()
        self.click_filter4()
        self.click_filter5()
        self.input_filter_field('AscensionIndiana')
        self.click_galka()
        time.sleep(2)
        element = self.driver.find_element(By.XPATH,
                                           "//*[@id='radix-:r3:-content-devices']/section/section[2]/div[2]/div[2]/div/section/section/section/button[4]")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        time.sleep(10)
        self.get_devices_info()



        # self.assert_url('https://staging.vip.voyceglobal.com/pages')
        # self.assert_word(self.get_main_word(), 'Dashboard')
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

    def get_devices_info(self):
        with allure.step("Get Kanji devices data"):
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".react-bs-container-body table tbody"))
            )
            rows = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".react-bs-container-body .table tbody tr"))
            )

            # Путь к файлу
            file_path = os.path.join('/Users/nikitabarshchuk/PycharmProjects/pythonProject3/customer_pages/Kanji_devices')

            # Открываем файл для записи
            with open(file_path, 'w') as file:
                for row in rows:
                    try:
                        device_name = WebDriverWait(row, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(4) span"))
                        ).get_attribute('title').strip()

                        serial_number = WebDriverWait(row, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(7) span"))
                        ).get_attribute('title').strip()

                        # Формируем строку с данными
                        line = f"Device Name: {device_name}, Serial Number: {serial_number}\n"

                        # Записываем строку в файл
                        file.write(line)

                    except Exception as e:
                        print(f"Не удалось извлечь данные для строки: {row.text}. Ошибка: {e}")
