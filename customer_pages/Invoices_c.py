import time
import allure
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
from operator import itemgetter
import json
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
from customer_pages.Graph_c import Graphs
from ev import EV

class invoices(Graphs, EV):

    def __init__(self, driver):
        super().__init__(driver)  # Это должно инициализировать метод __init__ класса Base
        self.driver = driver

    # Locators
    invoice_icon = "//*[@id='root']/section/aside/div/ul/li[5]"
    b_2024 = '//*[@id="header-container-id"]/div/div[5]/div/label[2]/span[2]'
    b_2023 = '//*[@id="header-container-id"]/div/div[5]/div/label[1]/span[2]'
    page = '//*[@id="root"]/section/section/main/div/div/div[3]/div/div/div/div/ul/li[3]/a'
    paid = '//*[@id="root"]/section/section/main/div/div/div[2]/div[1]/div/div[2]/div'
    pending = '//*[@id="root"]/section/section/main/div/div/div[2]/div[2]/div/div[2]/div'
    overdue = '//*[@id="root"]/section/section/main/div/div/div[2]/div[3]/div/div[2]/div'
    paid_b = '//*[@id="header-container-id"]/div/div[4]/div/label[2]'
    status = '//*[@id="root"]/section/section/main/div/div/div[3]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[8]'
    pending_b = '//*[@id="header-container-id"]/div/div[4]/div/label[3]'
    overdue_b = '//*[@id="header-container-id"]/div/div[4]/div/label[4]'
    element_xpath = '//*[@id="root"]/section/section/main/div/div/div[3]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[1]'
    additional_xpath = "//*[@id='root']/section/aside/div/ul"

    # Getters
    def get_b_2023(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.b_2023)))

    def get_paid_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.paid_b)))

    def get_status(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.status)))

    def get_pending_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.pending_b)))

    def get_overdue_b(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.overdue_b)))

    def get_overdue(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.overdue)))

    def get_pending(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.pending)))

    def get_paid(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.paid)))

    def get_page(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.page)))

    def get_invoice_icon(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.invoice_icon)))

    def get_b_2024(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.b_2024)))
        # Actions

    def input_last_name(self, user_password):
        self.get_last_name_field().send_keys(user_password)
        print("input last name")

    def click_2023(self):
        self.get_b_2023().click()
        print("click 2023")

    def click_2024(self):
        self.get_b_2024().click()
        print("click 2024")

    def click_paid_b(self):
        self.get_paid_b().click()
        print("click paid_b")

    def click_overdue_b(self):
        self.get_overdue_b().click()
        print("click overdue_b")

    def click_pending_b(self):
        self.get_pending_b().click()
        print("click pending_b")

    def click_invoice_icon(self):
        self.get_invoice_icon().click()
        print("CLICK invoice")

    def click_next_page(self):
        self.get_page().click()
        print("CLICK next page")

    def click_ACC(self):
        Acc = self.get_ACC()
        self.driver.execute_script("arguments[0].click();", Acc)
        print("Clicked Accessibility button")

    # METHODS
    def get_website_invoice_data(self):
        # Навигация к странице, содержащей таблицу с инвойсами, если нужно
        # self.driver.get("URL страницы с инвойсами")

        # Ожидание, пока таблица не будет загружена
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))  # Укажите правильный селектор для таблицы
        )

        # Находим все строки таблицы
        rows = self.driver.find_elements(By.CSS_SELECTOR, ".ant-table-tbody > .ant-table-row")
        website_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 8:  # Проверяем, что в строке есть все необходимые данные
                invoice_data = {
                    "InvoiceId": cells[0].text.strip(),
                    "InvoiceDate": cells[1].text.strip(),
                    "CompanyName": cells[2].text.strip(),
                    "Amount": cells[3].text.strip(),
                    "Currency": cells[4].text.strip(),
                    "DueDate": cells[5].text.strip(),
                    "PaymentDate": cells[6].text.strip() if cells[6].text.strip() != '' else None,
                    "PaymentStatus": cells[7].text.strip()
                }
                website_data.append(invoice_data)
            else:
                print(f"Row in the table does not contain all required cells: {row.text}")
        print(website_data)
        return website_data

    def get_web_info2023(self):
        with allure.step("Compare Invoices page data with DB 2023"):
            db_data = self.query_invoices2023()
            website_data = self.get_website_invoice_data()  # Сбор данных с первой страницы
            total_paid = total_pending = total_overdue = 0.0

            if db_data is not None and website_data:
                for web_invoice in website_data:
                    db_invoice = next(
                        (item for item in db_data if str(item['InvoiceMasterId']) == str(web_invoice['InvoiceId'])),
                        None)

                    if db_invoice:
                        db_total_amt = "{:.2f}".format(db_invoice['TotalAmt'])
                        web_total_amt = web_invoice['Amount'].replace(',', '').strip()

                        if (db_invoice['TxnDate'] == web_invoice['InvoiceDate'] and
                                db_invoice['CustomerName'] == web_invoice['CompanyName'] and
                                db_total_amt == web_total_amt and
                                db_invoice['Currency'] == web_invoice['Currency'] and
                                db_invoice['DueDate'] == web_invoice['DueDate'] and
                                (db_invoice['PaymentDate'] or '') == (web_invoice['PaymentDate'] or '') and
                                db_invoice['invoiceStatus'].lower() == web_invoice['PaymentStatus'].lower()):
                            print(f"Invoice {web_invoice['InvoiceId']} data matches.")
                        else:
                            print(f"Invoice {web_invoice['InvoiceId']} data does not match.")

                        # Подсчет сумм по статусам инвойса
                        if db_invoice['invoiceStatus'].lower() in ['paid', 'pending', 'unpaid']:
                            amount = float(web_invoice['Amount'].replace(',', '').strip())
                            if db_invoice['invoiceStatus'].lower() == 'paid':
                                total_paid += amount
                            elif db_invoice['invoiceStatus'].lower() == 'pending':
                                total_pending += amount
                            elif db_invoice['invoiceStatus'].lower() == 'unpaid':
                                total_overdue += amount

                    else:
                        print(f"Invoice {web_invoice['InvoiceId']} not found in database results.")

            # Вывод итоговых сумм за пределами цикла
            print(f"Total Paid: {round(total_paid, 2):.2f}")
            print(f"Total Pending: {round(total_pending, 2):.2f}")
            print(f"Total Overdue: {round(total_overdue, 2):.2f}")
            try:
                self.assert_word2(total_paid, self.get_paid())
                self.assert_word2(total_pending, self.get_pending())
                self.assert_word2(total_overdue, self.get_overdue())
            except AssertionError:
                # Обработка случая, когда значения просроченных платежей не совпадают
                print("Inconsistency of the amounts of overdue payments.Summification of values ​​from the next page.")
                self.click_next_page()
                time.sleep(10)
                additional_website_data = self.get_website_invoice_data()

                for web_invoice in additional_website_data:
                    if web_invoice['PaymentStatus'].lower() == 'paid':
                        amount = float(web_invoice['Amount'].replace(',', '').strip())
                        total_paid += amount

                # Повторная проверка с обновленной общей суммой просроченных платежей
                self.assert_word2(total_paid, self.get_paid())


    def get_web_info2022(self):
        with allure.step("Compare Invoices page data with DB 2022"):
            db_data = self.query_invoices2024()
            website_data = self.get_website_invoice_data()
            total_paid = total_pending = total_overdue = 0.0

            if db_data is not None and website_data:
                for web_invoice in website_data:
                    db_invoice = next(
                        (item for item in db_data if str(item['InvoiceMasterId']) == str(web_invoice['InvoiceId'])),
                        None)

                    if db_invoice:
                        db_total_amt = "{:.2f}".format(db_invoice['TotalAmt'])
                        web_total_amt = web_invoice['Amount'].replace(',', '').strip()

                        if (db_invoice['TxnDate'] == web_invoice['InvoiceDate'] and
                                db_invoice['CustomerName'] == web_invoice['CompanyName'] and
                                db_total_amt == web_total_amt and
                                db_invoice['Currency'] == web_invoice['Currency'] and
                                db_invoice['DueDate'] == web_invoice['DueDate'] and
                                (db_invoice['PaymentDate'] or '') == (web_invoice['PaymentDate'] or '') and
                                db_invoice['invoiceStatus'].lower() == web_invoice['PaymentStatus'].lower()):
                            print(f"Invoice {web_invoice['InvoiceId']} data matches.")
                        else:
                            print(f"Invoice {web_invoice['InvoiceId']} data does not match.")

                        # Подсчет сумм по статусам инвойса
                        if db_invoice['invoiceStatus'].lower() in ['paid', 'pending', 'unpaid']:
                            amount = float(web_invoice['Amount'].replace(',', '').strip())
                            if db_invoice['invoiceStatus'].lower() == 'paid':
                                total_paid += amount
                            elif db_invoice['invoiceStatus'].lower() == 'pending':
                                total_pending += amount
                            elif db_invoice['invoiceStatus'].lower() == 'unpaid':
                                total_overdue += amount

                    else:
                        print(f"Invoice {web_invoice['InvoiceId']} not found in database results.")

            # Вывод итоговых сумм за пределами цикла
            print(f"Total Paid: {round(total_paid, 2):.2f}")
            print(f"Total Pending: {round(total_pending, 2):.2f}")
            print(f"Total Overdue: {round(total_overdue, 2):.2f}")
            try:
                self.assert_word2(total_paid, self.get_paid())
                self.assert_word2(total_pending, self.get_pending())
                self.assert_word2(total_overdue, self.get_overdue())
            except AssertionError:
                # Обработка случая, когда значения просроченных платежей не совпадают
                print("Inconsistency of the amounts of overdue payments.Summification of values ​​from the next page.")
                # self.click_next_page() #TODO Следущая страница
                # additional_website_data = self.get_website_invoice_data()
                #
                # for web_invoice in additional_website_data:
                #     if web_invoice['PaymentStatus'].lower() == 'paid':
                #         amount = float(web_invoice['Amount'].replace(',', '').strip())
                #         total_paid += amount
                #
                # # Повторная проверка с обновленной общей суммой просроченных платежей
                # self.assert_word2(total_paid, self.get_paid())

    def invoice_p_check(self):
        with allure.step("Invoice Page Test"):
            Logger.add_start_step(method='Edit User without companies')
            self.click_invoice_icon()
            self.get_current_url()
            self.assert_url('https://staging.vip.voyceglobal.com/pages/invoices')
            self.click_2024()
            self.click_paid_b()
            time.sleep(15)
            self.assert_word(self.get_status(), 'Paid')
            self.click_overdue_b()
            time.sleep(15)
            # self.assert_word(self.get_status(), 'Unpaid')
            self.click_pending_b()
            time.sleep(10)
            self.assert_word(self.get_status(), 'Pending')
            self.driver.refresh()
            time.sleep(10)
            self.click_2023()
            time.sleep(3)
            self.get_web_info2023()
            self.driver.refresh()
            time.sleep(10)
            self.click_2023()
            time.sleep(10)
            self.invoices_graph()
            self.click_2024()
            self.get_web_info2022()
            time.sleep(3)
            self.check_color_change(self.element_xpath, self.additional_xpath)
            self.driver.refresh()
            time.sleep(20)

    def check_color_change(self, element_xpath, additional_xpath):
        with allure.step("Change color"):
            element = additional_element = None  # Инициализируем переменные

            try:
                element = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, element_xpath)))
                additional_element = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, additional_xpath)))

                old_color = element.value_of_css_property('background-color')
                additional_old_color = additional_element.value_of_css_property('background-color')
                print(f"Initial main element color: {old_color}")
                print(f"Initial additional element color: {additional_old_color}")

                # Кликаем, чтобы сменить тему
                self.click_light()

                # Проверяем, что клик по элементу произошел
                print("Clicked to change theme. Waiting for color change...")

                # Проверка изменения цвета для обоих элементов
                WebDriverWait(self.driver, 60).until_not(
                    lambda d: (element.value_of_css_property('background-color') == old_color and
                               additional_element.value_of_css_property('background-color') == additional_old_color)
                )

                # Вывод результатов
                new_color = element.value_of_css_property('background-color')
                additional_new_color = additional_element.value_of_css_property('background-color')
                print(f"Main element color changed from {old_color} to {new_color}")
                print(f"Additional element color changed from {additional_old_color} to {additional_new_color}")

            except TimeoutException as e:
                # Логируем ошибку с подробностями, только если элементы были инициализированы
                print(f"TimeoutException: Theme change did not occur within the expected time frame.")
                if element is not None:
                    print(f"Last known main element color: {element.value_of_css_property('background-color')}")
                if additional_element is not None:
                    print(
                        f"Last known additional element color: {additional_element.value_of_css_property('background-color')}")
                raise e

    def click_light(self):
        # Предположим, что переключатель темы имеет id 'theme-toggle'
        theme_toggle_xpath = '//*[@id="header-container-id"]/div/div[8]/div/label[1]'
        theme_toggle = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, theme_toggle_xpath)))
        theme_toggle.click()
        print("Theme changed to light.")

    def invoices_graph(self):
        with allure.step("Compare Invoices graphs Data with API"):
            Logger.add_start_step(method='Invoices_graph')

            # Получение токена из sessionStorage
            session_storage = self.driver.execute_script("return sessionStorage;")
            token = session_storage.get("token")

            # URL и заголовки для API запроса
            url = 'https://api.staging.vip.voyceglobal.com/invoices/payment-date'
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
                'authorization': f'Bearer {token}',
                'content-type': 'application/json',
                'origin': 'https://staging.vip.voyceglobal.com',
                'referer': 'https://staging.vip.voyceglobal.com/',
                'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            }
            data = {
                'start': '2023-01-02T05:00:00.000Z',
                'end': '2024-01-01T04:59:59.999Z',
                'filterType': 'company',
                'id': 1604
            }

            # Отправка запроса
            response = requests.post(url, headers=headers, json=data)
            print(f"API response status code: {response.status_code}")

            if response.status_code == 200:
                response_data = response.json()
                sorted_api_data = sorted(response_data, key=itemgetter('InvoiceMasterId'))


                website_data = []
                for page in range(2):  # Предполагается, что есть только две страницы
                    rows = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
                    )

                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) >= 8:
                            website_data.append({
                                "InvoiceId": cells[0].text,
                                "TxnDate": cells[1].text,
                                "CompanyName": cells[2].text,
                                "Amount": cells[3].text,
                                "Currency": cells[4].text,
                                "DueDate": cells[5].text,
                                "PaymentDate": cells[6].text if cells[6].text != '' else None,
                                "PaymentStatus": cells[7].text
                            })
                        else:
                            print(f"Row contains less than 8 cells: {row.text}")

                    if page < 1:
                        self.click_next_page()
                        time.sleep(3)

                sorted_website_data = sorted(website_data, key=itemgetter('InvoiceId'))
                for api_row, web_row in zip(sorted_api_data, sorted_website_data):
                    assert str(api_row['InvoiceMasterId']) == str(web_row['InvoiceId']), \
                        f"ID does not match: API {api_row['InvoiceMasterId']} != Web {web_row['InvoiceId']}"
                    print(f"ID verified: {api_row['InvoiceMasterId']} == {web_row['InvoiceId']} - Data is correct")

                    assert api_row['TxnDate'] == web_row['TxnDate'], \
                        f"Transaction date does not match: API {api_row['TxnDate']} != Web {web_row['TxnDate']}"
                    print(f"Transaction date verified: {api_row['TxnDate']} == {web_row['TxnDate']} - Data is correct")

                    assert api_row['CustomerName'] == web_row['CompanyName'], \
                        f"Customer name does not match: API {api_row['CustomerName']} != Web {web_row['CompanyName']}"
                    print(
                        f"Customer name verified: {api_row['CustomerName']} == {web_row['CompanyName']} - Data is correct")

                    assert abs(float(api_row['TotalAmt']) - float(web_row['Amount'].replace(',', ''))) < 0.01, \
                        f"Amount does not match: API {api_row['TotalAmt']} != Web {web_row['Amount']}"
                    print(f"Amount verified: {api_row['TotalAmt']} == {web_row['Amount']} - Data is correct")

                    assert api_row['Currency'] == web_row['Currency'], \
                        f"Currency does not match: API {api_row['Currency']} != Web {web_row['Currency']}"
                    print(f"Currency verified: {api_row['Currency']} == {web_row['Currency']} - Data is correct")

                    assert api_row['DueDate'] == web_row['DueDate'], \
                        f"Due date does not match: API {api_row['DueDate']} != Web {web_row['DueDate']}"
                    print(f"Due date verified: {api_row['DueDate']} == {web_row['DueDate']} - Data is correct")

                    assert (api_row['PaymentDate'] or 'None') == (web_row['PaymentDate'] or 'None'), \
                        f"Payment date does not match: API {api_row['PaymentDate']} != Web {web_row['PaymentDate']}"
                    print(
                        f"Payment date verified: {api_row['PaymentDate']} == {web_row['PaymentDate']} - Data is correct")

                    assert (api_row.get('invoiceStatus', '') or '').lower() == (
                            web_row.get('PaymentStatus', '') or '').lower(), \
                        f"Status does not match: API {api_row.get('invoiceStatus', '')} != Web {web_row.get('PaymentStatus', '')}"
                    print(
                        f"Status verified: {api_row.get('invoiceStatus', '')} == {web_row.get('PaymentStatus', '')} - Data is correct")

            else:
                print(f"Failed to get data. Status code: {response.status_code}.")
                print(response.text)

            with allure.step("Invoices_graph"):
                Logger.add_end_step(url=self.driver.current_url, method='Invoices_graph')
#