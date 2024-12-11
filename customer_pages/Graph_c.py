import time
from datetime import datetime, timedelta
from utilities.logger import Logger
import allure
import pyodbc
import logging
import requests
import os
from operator import itemgetter
import json
import requests
import logging
import json
from selenium.common.exceptions import StaleElementReferenceException
import ssl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from database.Database import Database
from database.Databricks import Databricks
from base.base_class import Base
from ev import EV

class Graphs(Base, Database, Databricks, EV):

    def __init__(self, driver):
        super().__init__(driver)
        Database.__init__(self)
        self.driver = driver
        Databricks.__init__(self)

    def execute_comparison(self):
        with allure.step("Compare DB data with web data"):
            # Fetch data from SQL query
            sql_data = self.query_get_devices_Indiana()
            if not sql_data:
                print("No data retrieved from SQL query.")
                return

            # Get data from file to compare with the web page
            web_data_matched_count = self.compare_devices_with_web(
                '/Users/nikitabarshchuk/PycharmProjects/pythonProject3/customer_pages/Kanji_devices')

            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
            )

            matched_count = 0  # Counter for matching SQL and web data
            mismatched_data = []  # List to store mismatched data

            # Compare SQL data with web page data
            for sql_row in sql_data:
                matched = False
                for row in self.driver.find_elements(By.CSS_SELECTOR, "table > tbody > tr"):
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) < 6:
                        logging.warning(f"Row in the table does not contain enough cells. Row content: {row.text}")
                        continue

                    serial_number_web = cells[1].text
                    service_minutes_web = cells[3].text
                    number_of_services_web = cells[5].text

                    if (sql_row['IOSSerialNumber'] == serial_number_web and
                            str(sql_row['ServiceMinutes']) == service_minutes_web and
                            str(sql_row['NumberOfServices']) == number_of_services_web):
                        matched_count += 1
                        matched = True
                        break  # If match found, break inner loop

                if not matched:
                    mismatched_data.append({
                        "SQL": {
                            "SerialNumber": sql_row['IOSSerialNumber'],
                            "ServiceMinutes": sql_row['ServiceMinutes'],
                            "NumberOfServices": sql_row['NumberOfServices']
                        },
                        "Web": {
                            "SerialNumber": serial_number_web if len(cells) > 1 else "N/A",
                            "ServiceMinutes": service_minutes_web if len(cells) > 3 else "N/A",
                            "NumberOfServices": number_of_services_web if len(cells) > 5 else "N/A"
                        }
                    })

            # Print matching information
            print(f"Total devices from SQL query: {len(sql_data)}")
            print(f"Total matched devices from web: {web_data_matched_count}")
            print(f"Total matched devices between SQL and Web data: {matched_count}")

            if web_data_matched_count == len(sql_data):
                print("All devices from SQL query matched with devices from the web page.")
            else:
                print("There is a mismatch in the number of devices between SQL query and web page.")
                print("Mismatched Data:")
                for mismatch in mismatched_data:
                    print(f"SQL Data: {mismatch['SQL']}")
                    print(f"Web Data: {mismatch['Web']}")

    @allure.step("Comparing device data")
    def compare_devices_data1(self):
        with allure.step("Compare Graphs data with API"):
            print("Starting API data comparison...")

            token = self.get_token_from_session_storage()
            if not token:
                print("No token found in session storage. Cannot proceed with the API call.")
                return

            print(f"Using token: {token}")
            with allure.step("Fetching data from API"):
                url = 'https://api.staging.vip.voyceglobal.com/get-all-devices'
                headers = {
                    'authority': 'api.staging.vip.voyceglobal.com',
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
                    'authorization': f'Bearer {token}',
                    'content-type': 'application/json',
                    'origin': 'https://staging.vip.voyceglobal.com',
                    'referer': 'https://staging.vip.voyceglobal.com/',
                    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                current_utc_date = datetime.utcnow()
                start_date = (current_utc_date - timedelta(hours=5)).strftime('%Y-%m-%dT05:00:00.000Z')
                end_date = (current_utc_date - timedelta(hours=5) + timedelta(days=1)).strftime(
                    '%Y-%m-%dT04:59:59.999Z')

                data = {
                    'RequestCompanyId': 1598,
                    'filterType': 'company',
                    'id': 1598
                }
                params = {
                    'start': start_date,
                    'end': end_date,
                }

                response = requests.post(url, headers=headers, json=data, params=params)
                print(f"Raw API Response: {response.text}")
                if response.status_code != 200:
                    print(
                        f"Failed to get data from API. Status code: {response.status_code}. Response: {response.text}")
                    return

                api_data = response.json()

                print("API data retrieved successfully.")
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0"))
                )

                rows = self.driver.find_elements(By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0")
                print(f"Number of rows retrieved from web: {len(rows)}")
                discrepancies = []  # List to store discrepancies

                for client_site in api_data:
                    for device in client_site['SerialNumbers']:
                        serial_number_api = device['IOSSerialNumber']
                        num_transactions_api = device['TotalTransactions']
                        service_minutes_api = device['ServiceMinutes']
                        found_match = False

                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if len(cells) >= 4:
                                serial_number_web = cells[0].text
                                service_minutes_web = cells[1].text
                                num_transactions_web = cells[3].text

                                if serial_number_api == serial_number_web:
                                    print(f"Comparing device: {serial_number_api}")
                                    print(f"API - Transactions: {num_transactions_api}, Minutes: {service_minutes_api}")
                                    print(f"WEB - Transactions: {num_transactions_web}, Minutes: {service_minutes_web}")

                                    if str(num_transactions_api) != num_transactions_web:
                                        discrepancies.append(
                                            f"Number of transactions does not match for {serial_number_api}: API {num_transactions_api} != Web {num_transactions_web}")
                                    if str(service_minutes_api) != service_minutes_web:
                                        discrepancies.append(
                                            f"Service minutes do not match for {serial_number_api}: API {service_minutes_api} != Web {service_minutes_web}")
                                    else:
                                        print(f"Data for {serial_number_api} is correct.")
                                        found_match = True
                                        break

                        if not found_match:
                            discrepancies.append(f"{serial_number_api} does not have matching data on the web page")

                # Output all found discrepancies
                if discrepancies:
                    for discrepancy in discrepancies:
                        print(discrepancy)
                else:
                    print("All data matched.")

    @allure.step("Comparing device data for Yale")
    def compare_devices_data_Yale(self):
        with allure.step("Compare Graphs data with API"):
            print("Starting API data comparison...")

            token = self.get_token_from_session_storage()
            if not token:
                print("No token found in session storage. Cannot proceed with the API call.")
                return

            print(f"Using token: {token}")
            with allure.step("Fetching data from API"):
                url = 'https://api.staging.vip.voyceglobal.com/get-all-devices'
                headers = {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
                    'authorization': f'Bearer {token}',
                    'content-type': 'application/json',
                    'origin': 'https://staging.vip.voyceglobal.com',
                    'referer': 'https://staging.vip.voyceglobal.com/',
                    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                }
                current_utc_date = datetime.utcnow()
                start_date = (current_utc_date - timedelta(hours=4)).strftime('%Y-%m-%dT04:00:00.000Z')
                end_date = (current_utc_date - timedelta(hours=4) + timedelta(days=1)).strftime(
                    '%Y-%m-%dT03:59:59.999Z')

                data = {
                    'filterType': 'company',
                    'id': 1899
                }
                params = {
                    'start': start_date,
                    'end': end_date,
                }

                response = requests.post(url, headers=headers, json=data, params=params)
                # print(f"Raw API Response: {response.text}")
                if response.status_code != 200:
                    print(
                        f"Failed to get data from API. Status code: {response.status_code}. Response: {response.text}")
                    return

                api_data = response.json()
                print("API data retrieved successfully. Data:")
                for site in api_data:
                    print(site)

            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0"))
            )

            rows = self.driver.find_elements(By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0")
            print(f"Number of rows retrieved from web: {len(rows)}")
            discrepancies = []  # List to store discrepancies

            for site in api_data:
                site_name = site['Site']
                site_service_minutes = site['ServiceMinutes']
                site_total_calls = site['TotalCalls']

                found_site = False
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 4:
                        site_name_web = cells[1].text
                        service_minutes_web = cells[2].text
                        total_calls_web = cells[3].text



                        if site_name == site_name_web:
                            found_site = True
                            if str(site_service_minutes) != service_minutes_web:
                                discrepancies.append(
                                    f"Service minutes do not match for {site_name}: API {site_service_minutes} != Web {service_minutes_web}")
                            if str(site_total_calls) != total_calls_web:
                                discrepancies.append(
                                    f"Total calls do not match for {site_name}: API {site_total_calls} != Web {total_calls_web}")
                            else:
                                print(f"Data for {site_name} is correct.")
                            break

                if not found_site:
                    discrepancies.append(f"{site_name} does not have matching data on the web page")

                for department in site.get('Departments', []):
                    for device in department.get('Devices', []):
                        serial_number_api = device['IOSSerialNumber']
                        num_transactions_api = device['TotalCalls']
                        service_minutes_api = device['ServiceMinutes']
                        found_device = False

                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if len(cells) >= 6:
                                serial_number_web = cells[2].text
                                service_minutes_web = cells[3].text
                                num_transactions_web = cells[5].text


                                if serial_number_api == serial_number_web:
                                    found_device = True
                                    if str(num_transactions_api) != num_transactions_web:
                                        discrepancies.append(
                                            f"Number of transactions does not match for {serial_number_api}: API {num_transactions_api} != Web {num_transactions_web}")
                                    if str(service_minutes_api) != service_minutes_web:
                                        discrepancies.append(
                                            f"Service minutes do not match for {serial_number_api}: API {service_minutes_api} != Web {service_minutes_web}")
                                    else:
                                        print(f"Data for {serial_number_api} is correct.")
                                    break

                        if not found_device:
                            discrepancies.append(f"{serial_number_api} does not have matching data on the web page")

            # Output all found discrepancies
            if discrepancies:
                for discrepancy in discrepancies:
                    print(discrepancy)
            else:
                print("All data matched.")

    def get_token_from_session_storage(self):
        # Получение токена из sessionStorage через Selenium
        session_storage = self.driver.execute_script("return JSON.stringify(sessionStorage);")
        session_storage_data = json.loads(session_storage)
        return session_storage_data.get("token")

    def read_device_info(self, file_path):
        # Чтение данных об устройствах из файла
        devices = []
        with open(file_path, 'r') as file:
            for line in file:
                if "Device Name:" in line and "Serial Number:" in line:
                    parts = line.split(',')
                    device_name_part = parts[0].strip()
                    serial_number_part = parts[1].strip()

                    device_name = device_name_part.split(':')[1].strip()
                    serial_number = serial_number_part.split(':')[1].strip()

                    devices.append({"DeviceName": device_name, "SerialNumber": serial_number})
        return devices

    def compare_devices_with_web(self, file_path):
        with allure.step("Compare Kanji Devices with Devices from Web-site"):
            # Reading device information from file
            file_devices = self.read_device_info(file_path)

            # Navigating to device usage page
            with allure.step("Navigating to device usage page"):
                rows = WebDriverWait(self.driver, 120).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr")),
                    message="Failed to locate table rows within the given time."
                )

            # Comparing file data with web data
            matched_count = 0  # Counter for matched devices
            with allure.step("Comparing File data with Web data"):
                for file_device in file_devices:
                    device_name_file = file_device['DeviceName']
                    serial_number_file = file_device['SerialNumber']

                    for attempt in range(3):  # Retry mechanism to handle stale elements
                        try:
                            for row in rows:
                                cells = row.find_elements(By.TAG_NAME, "td")

                                if len(cells) < 2:
                                    logging.warning(
                                        f"Row in the table does not contain enough cells. Row content: {row.text}")
                                    continue

                                device_name_web = cells[0].text  # Index 0 for device name
                                serial_number_web = cells[1].text  # Index 1 for serial number

                                if device_name_file.lower() == device_name_web.lower() and serial_number_file.lower() == serial_number_web.lower():
                                    print(
                                        f"Matched - Device Name: {device_name_web}, Serial Number: {serial_number_web}")
                                    matched_count += 1  # Increase counter for matched devices
                                    break  # If match found, break inner loop
                            break  # Exit retry loop if successful
                        except StaleElementReferenceException:
                            logging.warning(f"Stale element reference exception encountered. Retry {attempt + 1}/3.")
                            time.sleep(1)
                            rows = WebDriverWait(self.driver, 120).until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr")),
                                message="Failed to locate table rows within the given time."
                            )

            # Print total matched devices count
            print(f"Total matched devices: {matched_count}")
            return matched_count

    def compare_devices(self, file_path):
        with allure.step("Compare Devices from Kanji with API data"):
            # Получение токена
            token = self.get_token_from_session_storage()

            if not token:
                logging.error("No token found in session storage. Cannot proceed with the API call.")
                return

            logging.info(f"Using token: {token}")

            # Задание параметров для API запроса
            url = 'https://vdmsapi.voyceglobal.com/device-informations'
            headers = {
                'authority': 'vdmsapi.voyceglobal.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
                'authorization': f'Bearer {token}',
                'content-type': 'application/json',
                'origin': 'https://staging.vip.voyceglobal.com',
                'referer': 'https://staging.vip.voyceglobal.com/',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
            data = {
                'blueprintName': 'AscensionIndiana',
                'filterType': 'company',
                'id': 1604
            }

            # Отправка запроса на API
            try:
                response = requests.post(url, headers=headers, json=data, verify=False)
                if response.status_code == 200:
                    api_data = response.json()
                    file_devices = self.read_device_info(file_path)

                    # Сравнение данных из файла и API
                    for api_device in api_data:
                        for file_device in file_devices:
                            if api_device['deviceName'] == file_device['DeviceName'] and api_device['serialNumber'] == \
                                    file_device['SerialNumber']:
                                print(
                                    f"Data is correct - Device Name: {api_device['deviceName']}, Serial Number: {api_device['serialNumber']}")
                                logging.info(
                                    f"Match found: {api_device['deviceName']} with Serial Number: {api_device['serialNumber']}")
                                break  # Прерывание внутреннего цикла, если соответствие найдено

                else:
                    logging.error(f"Failed to fetch data: {response.status_code} - {response.text}")
            except Exception as e:
                logging.error(f"Exception occurred: {e}")

    def get_blueprint_names(self):
        token = self.get_token_from_session_storage()

        if not token:
            raise Exception("Failed to get a token from SessionStorage")
        url = 'https://vdmsapi.voyceglobal.com/device-informations'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'authorization': f'Bearer {token}',
            'content-type': 'application/json',
            'origin': 'https://staging.admin.vip.voyceglobal.com',
            'referer': 'https://staging.admin.vip.voyceglobal.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        data = {
            'filterType': 'admin'
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Data obtaining error.Status Code: {Response.status_code}.")

        blueprint_names = set()
        for device_info in response.json():
            if 'blueprintName' in device_info:
                blueprint_names.add(device_info['blueprintName'])
        print(blueprint_names)
        return list(blueprint_names)
    def languages_by_hour(self):
        token = self.get_token_from_session_storage()

        if not token:
            raise Exception("Failed to get a token from SessionStorage")

        url = 'https://api.staging.vip.voyceglobal.com/agg-by-client/language/hour'
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

        current_utc_date = datetime.utcnow()
        data = {
            'start': current_utc_date.strftime('%Y-%m-%dT05:00:00.000Z'),
            'end': (current_utc_date + timedelta(days=1)).strftime('%Y-%m-%dT04:59:59.999Z'),
            'filterType': 'company',
            'id': 1355  # Идентификатор компании обновлен в соответствии с вашим запросом
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Data obtaining error.Status Code: {Response.status_code}.")
        return response.json()

    def get_blueprint_name(self, blueprint_name, company_id):
        token = self.get_token_from_session_storage()
        url = 'https://vdmsapi.voyceglobal.com/device-informations'
        headers = {
            'authority': 'vdmsapi.voyceglobal.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'authorization': f'Bearer {token}',
            'content-type': 'application/json',
            'origin': 'https://admin.vip.voyceglobal.com',
            'referer': 'https://admin.vip.voyceglobal.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        data = {
            "blueprintName": blueprint_name,
            "filterType": "company",
            "id": company_id  # Вместо фиксированного id можно использовать переменную, если он также динамичен
        }

        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        response_blueprint_name = response_json.get('blueprintName')
        print(response_blueprint_name)
        return response_blueprint_name
    def top_languages_api(self):
        token = self.get_token_from_session_storage()

        if not token:
            raise Exception("Failed to get a token from SessionStorage")

        url = 'https://api.staging.vip.voyceglobal.com/agg-by-client/hour/language'
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

        current_utc_date = datetime.utcnow()
        data = {
            'start': current_utc_date.strftime('%Y-%m-%dT05:00:00.000Z'),
            'end': (current_utc_date + timedelta(days=1)).strftime('%Y-%m-%dT04:59:59.999Z'),
            'languageType': '-1',
            'filterType': 'company',
            'id': 1533
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Data obtaining error.Status Code: {Response.status_code}.")

        return response.json()






    def language_report_test_today(self):
        with allure.step("Language report compare Today's Data"):
            Logger.add_start_step(method='Language_Report_Test')

            session_storage = self.driver.execute_script("return JSON.stringify(sessionStorage);")
            session_storage_data = json.loads(session_storage)
            token = session_storage_data.get("token")

            if not token:
                raise Exception("Failed to retrieve token from sessionStorage")


            url = 'https://api.staging.vip.voyceglobal.com/agg-by-client/language/detail/total'
            headers = {
                'accept': 'application/json, text/plain, */*',
                'authorization': f'Bearer {token}',
                'content-type': 'application/json',
            }
            current_utc_date = datetime.utcnow()
            start_date = (current_utc_date - timedelta(hours=5)).strftime('%Y-%m-%dT05:00:00.000Z')
            end_date = (current_utc_date - timedelta(hours=5) + timedelta(days=1)).strftime('%Y-%m-%dT04:59:59.999Z')

            data = {
                'start': start_date,
                'end': end_date,
                'languageType': '-1',
                'filterType': 'company',
                'id': 1604
            }

            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                raise Exception(f"Failed to get data. Status code: {response.status_code}.")

            api_data = response.json()
            sorted_api_data = sorted(api_data, key=itemgetter('TargetLanguage'))

            Logger.add_end_step(url=url, method='Language_Report_Test')
            return sorted_api_data

    def fetch_website_data1(self):
        rows = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
        )

        website_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 6:
                website_data.append({
                    "LanguageName": cells[0].text,
                    "TotalCalls": cells[1].text.replace(',', ''),
                    "TotalMinutes": cells[2].text.replace(',', ''),
                    "CallsbyAudio": cells[3].text.replace(',', ''),
                    "CallsbyVideo": cells[4].text.replace(',', ''),
                    # Продолжение извлечения данных для остальных столбцов, если необходимо
                })
            else:
                print(f"Not enough cells in the row to extract data: {row.text}")
        return website_data

    def fetch_website_data12(self):
        rows = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
        )

        website_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 7:
                website_data.append({
                    "LanguageName": cells[0].text,
                    "TotalCalls": cells[1].text.replace(',', ''),
                    "TotalMinutes": cells[2].text.replace(',', ''),
                    "CallsbyAudio": cells[3].text.replace(',', ''),
                    "CallsbyVideo": cells[4].text.replace(',', ''),
                    "MinutesbyAudio": cells[5].text.replace(',', ''),
                    "MinutesbyVideo": cells[6].text.replace(',', ''),
                    # Продолжение извлечения данных для остальных столбцов, если необходимо
                })
            else:
                print(f"Not enough cells in the row to extract data: {row.text}")
        return website_data

    def fetch_website_data(self):
        rows = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
        )

        website_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 5:
                website_data.append({
                    "LanguageName": cells[0].text,
                    "TotalCalls": cells[1].text.replace(',', ''),
                    "TotalMinutes": cells[2].text.replace(',', ''),
                    "ServicedAudioCalls": cells[3].text.replace(',', ''),
                    "ServicedVideoCalls": cells[4].text.replace(',', ''),
                    # Продолжение извлечения данных для остальных столбцов, если необходимо
                })
            else:
                print(f"Not enough cells in the row to extract data: {row.text}")
        return website_data

    def compare_lang_rep(self, sorted_api_data):
        with allure.step("Compare API data and Web Data"):
            Logger.add_start_step(method='Compare API and Web Data')

            rows = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
            )

            website_data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 5:
                    website_data.append({
                        "LanguageName": cells[0].text,
                        "TotalCalls": cells[1].text.replace(',', ''),
                        "TotalMinutes": cells[2].text.replace(',', ''),
                        "ServicedAudioCalls": cells[3].text.replace(',', ''),
                        "ServicedVideoCalls": cells[4].text.replace(',', ''),
                        # Продолжение извлечения данных для остальных столбцов, если необходимо
                    })
                else:
                    print(f"Not enough cells in the row to extract data: {row.text}")

            print(f"API Languages Count: {len(sorted_api_data)}")
            print(f"Web Languages Count: {len(website_data)}")

            sorted_website_data = sorted(website_data, key=lambda x: x['LanguageName'].lower())
            for api_row in sorted_api_data:
                web_row = next((item for item in sorted_website_data if
                                item['LanguageName'].lower() == api_row['TargetLanguage'].lower()), None)

                if not web_row:
                    print(f"Language {api_row['TargetLanguage']} found in API but not on the web.")
                    continue

                # Проверка TotalCalls
                assert str(api_row['TotalCalls']) == web_row['TotalCalls'], \
                    f"Total calls do not match: API {api_row['TotalCalls']} != Web {web_row['TotalCalls']}"
                print(
                    f"Total calls verified: API {api_row['TotalCalls']} == Web {web_row['TotalCalls']} - Data is correct")

                # Проверка ServiceMinutes
                web_service_minutes = web_row['TotalMinutes']
                api_service_minutes = api_row.get('ServiceMinutes', 0)  # Используем 0 по умолчанию, если значение None

                # Преобразование None в '0' для корректного сравнения
                api_service_minutes = '0' if api_service_minutes is None else str(api_service_minutes)
                web_service_minutes = '0' if web_service_minutes == '' else web_service_minutes

                assert api_service_minutes == web_service_minutes, \
                    f"Service minutes do not match: API {api_service_minutes} != Web {web_service_minutes}"
                print(
                    f"Service minutes verified: API {api_service_minutes} == Web {web_service_minutes} - Data is correct")

                # Проверка ServicedAudioCalls

                # Проверка ServicedAudioCalls
                assert str(api_row['CountSuccessAudioCalls']) == web_row['ServicedAudioCalls'], \
                    f"Serviced audio calls do not match: API {api_row['CountSuccessAudioCalls']} != Web {web_row['ServicedAudioCalls']}"
                print(
                    f"Serviced audio calls verified: API {api_row['CountSuccessAudioCalls']} == Web {web_row['ServicedAudioCalls']} - Data is correct")

                # Проверка ServicedVideoCalls
                assert str(api_row['CountSuccessVideoCalls']) == web_row['ServicedVideoCalls'], \
                    f"Serviced video calls do not match: API {api_row['CountSuccessVideoCalls']} != Web {web_row['ServicedVideoCalls']}"
                print(
                    f"Serviced video calls verified: API {api_row['CountSuccessVideoCalls']} == Web {web_row['ServicedVideoCalls']} - Data is correct")

            Logger.add_end_step(url=self.driver.current_url, method='Compare API and Web Data')
#
    def compare_avsv_rep(self, sorted_api_data):
        with allure.step("Compare API data with Graphs data"):
            Logger.add_start_step(method='Compare API and Web Data')

            rows = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
            )

            website_data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 7:
                    minutes_by_video_text = cells[6].text.replace('minutes', '').replace(',', '').strip()
                    website_data.append({
                        "LanguageName": cells[0].text,
                        "TotalCalls": cells[1].text.replace(',', ''),
                        "TotalMinutes": cells[2].text.replace(',', ''),
                        "ServicedAudioCalls": cells[3].text.replace(',', ''),
                        "ServicedVideoCalls": cells[4].text.replace(',', ''),
                        "MinutesbyVideo": minutes_by_video_text,
                    })
                else:
                    print(f"Not enough cells in the row to extract data: {row.text}")

            print(f"API Languages Count: {len(sorted_api_data)}")
            print(f"Web Languages Count: {len(website_data)}")

            sorted_website_data = sorted(website_data, key=lambda x: x['LanguageName'].lower())
            for api_row in sorted_api_data:
                web_row = next((item for item in sorted_website_data if
                                item['LanguageName'].lower() == api_row['TargetLanguage'].lower()), None)

                if not web_row:
                    print(f"Language {api_row['TargetLanguage']} found in API but not on the web.")
                    continue

                # Сравнение TotalCalls
                assert str(api_row['TotalCalls']) == web_row[
                    'TotalCalls'], f"Total calls do not match: API {api_row['TotalCalls']} != Web {web_row['TotalCalls']}"
                print(
                    f"Total calls verified: API {api_row['TotalCalls']} == Web {web_row['TotalCalls']} - Data is correct")

                # Сравнение ServiceMinutes
                web_service_minutes = web_row['TotalMinutes']
                api_service_minutes = api_row.get('ServiceMinutes', 0)
                api_service_minutes = '0' if api_service_minutes is None else str(api_service_minutes)
                web_service_minutes = '0' if web_service_minutes == '' else web_service_minutes

                assert api_service_minutes == web_service_minutes, f"Service minutes do not match: API {api_service_minutes} != Web {web_service_minutes}"
                print(
                    f"Service minutes verified: API {api_service_minutes} == Web {web_service_minutes} - Data is correct")

                # Сравнение ServicedAudioCalls
                assert str(api_row['CountSuccessAudioCalls']) == web_row[
                    'ServicedAudioCalls'], f"Serviced audio calls do not match: API {api_row['CountSuccessAudioCalls']} != Web {web_row['ServicedAudioCalls']}"
                print(
                    f"Serviced audio calls verified: API {api_row['CountSuccessAudioCalls']} == Web {web_row['ServicedAudioCalls']} - Data is correct")

                # Сравнение ServicedVideoCalls
                assert str(api_row['CountSuccessVideoCalls']) == web_row[
                    'ServicedVideoCalls'], f"Serviced video calls do not match: API {api_row['CountSuccessVideoCalls']} != Web {web_row['ServicedVideoCalls']}"
                print(
                    f"Serviced video calls verified: API {api_row['CountSuccessVideoCalls']} == Web {web_row['ServicedVideoCalls']} - Data is correct")

                # Сравнение CountVideoMinute
                api_count_video_minute = '0' if api_row.get('CountVideoMinute') is None else str(
                    api_row.get('CountVideoMinute'))
                web_minutes_by_video = '0' if web_row.get('MinutesbyVideo') == '' else web_row.get(
                    'MinutesbyVideo').strip()

                assert api_count_video_minute == web_minutes_by_video, f"Video minutes do not match: API {api_count_video_minute} != Web {web_minutes_by_video}"
                print(
                    f"Video minutes verified: API {api_count_video_minute} == Web {web_minutes_by_video} - Data is correct")

        Logger.add_end_step(url=self.driver.current_url, method='Compare API and Web Data')

    def compare_devices_data_with_sql(self):
        with allure.step("Compare Graphs data with SQL Data"):
            print("Starting SQL data comparison...")

            sql_data = self.query_get_devices_Yale()
            if not sql_data:
                print("No data returned from SQL query.")
                return

            print("SQL data retrieved successfully.")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0"))
            )

            rows = self.driver.find_elements(By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0")
            print(f"Number of rows retrieved from web: {len(rows)}")
            discrepancies = []  # List to store discrepancies

            for device in sql_data:
                serial_number_sql = device.IOSSerialNumber
                num_transactions_sql = device.TotalTransactions
                service_minutes_sql = device.ServiceMinutes
                found_match = False  # Set the flag to False before starting the search

                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 4:
                        serial_number_web = cells[0].text
                        service_minutes_web = cells[1].text
                        num_transactions_web = cells[3].text

                        if serial_number_sql == serial_number_web:
                            print(f"Comparing device: {serial_number_sql}")
                            print(f"SQL - Transactions: {num_transactions_sql}, Minutes: {service_minutes_sql}")
                            print(f"WEB - Transactions: {num_transactions_web}, Minutes: {service_minutes_web}")

                            if str(num_transactions_sql) != num_transactions_web:
                                discrepancies.append(
                                    f"Number of transactions does not match for {serial_number_sql}: SQL {num_transactions_sql} != Web {num_transactions_web}")
                            if str(service_minutes_sql) != service_minutes_web:
                                discrepancies.append(
                                    f"Service minutes do not match for {serial_number_sql}: SQL {service_minutes_sql} != Web {service_minutes_web}")
                            else:
                                print(f"Data for {serial_number_sql} is correct.")
                                found_match = True  # Match found, set the flag to True
                                break  # Break the current loop as the match is found
                    else:
                        print(f"Row does not contain enough cells: {len(cells)} found")

                if not found_match:  # Check if a match was found
                    discrepancies.append(
                        f"Serial number {serial_number_sql} from SQL does not match any on the web page.")

            # Output all found discrepancies
            if discrepancies:
                for discrepancy in discrepancies:
                    print(discrepancy)
            else:
                print("All data matched.")



    def compare_devices_data_with_sql_NM(self):
        with allure.step("Compare Graphs data with SQL Data"):
            print("Starting SQL data comparison...")

            sql_data = self.query_get_devices_NM()
            if not sql_data:
                print("No data returned from SQL query.")
                return

            print("SQL data retrieved successfully.")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0"))
            )

            rows = self.driver.find_elements(By.CSS_SELECTOR, ".ant-table-tbody > tr.ant-table-row-level-0")
            print(f"Number of rows retrieved from web: {len(rows)}")
            discrepancies = []  # List to store discrepancies

            for device in sql_data:
                serial_number_sql = device.IOSSerialNumber
                num_transactions_sql = device.TotalTransactions
                service_minutes_sql = device.ServiceMinutes
                found_match = False  # Set the flag to False before starting the search

                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 4:
                        serial_number_web = cells[0].text
                        service_minutes_web = cells[1].text
                        num_transactions_web = cells[3].text

                        if serial_number_sql == serial_number_web:
                            print(f"Comparing device: {serial_number_sql}")
                            print(f"SQL - Transactions: {num_transactions_sql}, Minutes: {service_minutes_sql}")
                            print(f"WEB - Transactions: {num_transactions_web}, Minutes: {service_minutes_web}")

                            if str(num_transactions_sql) != num_transactions_web:
                                discrepancies.append(
                                    f"Number of transactions does not match for {serial_number_sql}: SQL {num_transactions_sql} != Web {num_transactions_web}")
                            if str(service_minutes_sql) != service_minutes_web:
                                discrepancies.append(
                                    f"Service minutes do not match for {serial_number_sql}: SQL {service_minutes_sql} != Web {service_minutes_web}")
                            else:
                                print(f"Data for {serial_number_sql} is correct.")
                                found_match = True  # Match found, set the flag to True
                                break  # Break the current loop as the match is found
                    else:
                        print(f"Row does not contain enough cells: {len(cells)} found")

                if not found_match:  # Check if a match was found
                    discrepancies.append(
                        f"Serial number {serial_number_sql} from SQL does not match any on the web page.")

            # Output all found discrepancies
            if discrepancies:
                for discrepancy in discrepancies:
                    print(discrepancy)
            else:
                print("All data matched.")

    # url = 'https://api.staging.vip.voyceglobal.com/agg-by-client/hour/hourly/language/'
    # headers = {
    #     'authority': 'api.staging.vip.voyceglobal.com',
    #     'accept': 'application/json, text/plain, */*',
    #     'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    #     'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiTmlraXRhIEJCQiIsImlkIjoiNjRmYjY1NjI5MzZlZGYwMDQ4OGE1NzY5IiwiZW1haWwiOiJnbWFpbEB2b3ljZWdsb2JhbC5jb20iLCJwZXJtaXNzaW9ucyI6eyJpZCI6IjY0ZmI2NTYyOTM2ZWRmMDA0ODhhNTc2OSIsIm5hbWUiOiJOaWtpdGEgQkJCIiwiZW1haWwiOiJnbWFpbEB2b3ljZWdsb2JhbC5jb20iLCJwYXNzd29yZCI6IiQyYSQxMCRCbXR4cE5MNjVIdDFGdXBkNHl5TWEuaGVzUFAxVHp0ejRJT0JnL21kYVltcE5hL21aN05XcSIsImNvbW1lbnQiOiJDcmVhdGUgdXNpbmcgVklQIEFkbWluIHBvcnRhbCIsImRlc2lnbmF0aW9uIjoicG9ydGFsLXNpZ25pbiIsImNyZWF0ZWRBdCI6IjIwMjMtMDktMDVUMDM6NDA6NDQuMDE0WiIsInVwZGF0ZWRBdCI6IjIwMjMtMTAtMjdUMTM6NDM6NTUuMzc1WiIsImlzRGVsZXRlZCI6ZmFsc2UsImlzQXBwcm92ZWQiOnRydWUsInJvbGUiOiJBZG1pbiIsImNvbXBhbnkiOjE1OTh9LCJpYXQiOjE3MDAwNzc1MTksImV4cCI6MTcwMDEwMjcxOX0.SOqRPugFJOtFYjswCIIB_IDB96Zw_Ua1vKzFUcPGvzI',
    #     'content-type': 'application/json',
    #     'origin': 'https://staging.vip.voyceglobal.com',
    #     'referer': 'https://staging.vip.voyceglobal.com/',
    #     'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"macOS"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-site',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    # }
    #
    # data = {
    #     'start': '2023-11-15T05:00:00.000Z',
    #     'end': '2023-11-16T04:59:59.999Z',
    #     'languageType': '-1',
    #     'filterType': 'company',
    #     'id': 1598
    # }
    #
    # response = requests.post(url, headers=headers, json=data)
    # print(response.text)

    def compare_data(self):
        with allure.step("Compare data from DB with Web data"):
            languages = self.query_lang_rep()  # Получение списка языков
            website_data = self.fetch_website_data()
            all_discrepancies = []  # Список для хранения всех найденных несоответствий

            for lang in languages:
                language_name = lang[0]
                db_data = self.query_language_stats(language_name)
                if db_data:
                    for row in db_data:
                        discrepancies = []

                        # Инициализация списка расхождений перед проверкой условий
                        if language_name == "Arabic":
                            web_rows = [item for item in website_data if "Arabic" in item["LanguageName"]]
                        elif language_name == "French":
                            web_rows = [item for item in website_data if "French" in item["LanguageName"]]
                        elif language_name == "Portuguese":
                            web_rows = [item for item in website_data if "Portuguese" in item["LanguageName"]]
                        else:
                            web_rows = [item for item in website_data if item["LanguageName"] == language_name]

                        if web_rows:
                            print(f"Comparing data for language: {language_name}")

                            # Инициализация и вычисление общих значений для веб-данных
                            total_calls_web = sum(int(item["TotalCalls"]) for item in web_rows)
                            total_minutes_web = sum(int(item["TotalMinutes"]) for item in web_rows)
                            serviced_audio_calls_web = sum(int(item["ServicedAudioCalls"]) for item in web_rows)
                            serviced_video_calls_web = sum(int(item["ServicedVideoCalls"]) for item in web_rows)

                            # Обработка случая с None
                            db_total_calls = 0 if row.TotalCalls is None else row.TotalCalls
                            db_total_minutes = 0 if row.ServiceMinutes is None else row.ServiceMinutes
                            db_serviced_audio_calls = 0 if row.CountSuccessAudioCalls is None else row.CountSuccessAudioCalls
                            db_serviced_video_calls = 0 if row.CountSuccessVideoCalls is None else row.CountSuccessVideoCalls

                            # Сравнение значений
                            if str(db_total_calls) != str(total_calls_web):
                                discrepancies.append(f"Total Calls: DB({db_total_calls}) != Web({total_calls_web})")
                            if str(db_total_minutes) != str(total_minutes_web):
                                discrepancies.append(
                                    f"Total Minutes: DB({db_total_minutes}) != Web({total_minutes_web})")
                            if str(db_serviced_audio_calls) != str(serviced_audio_calls_web):
                                discrepancies.append(
                                    f"Serviced Audio Calls: DB({db_serviced_audio_calls}) != Web({serviced_audio_calls_web})")
                            if str(db_serviced_video_calls) != str(serviced_video_calls_web):
                                discrepancies.append(
                                    f"Serviced Video Calls: DB({db_serviced_video_calls}) != Web({serviced_video_calls_web})")

                            # Добавляем несоответствия в общий список, если они есть
                            if discrepancies:
                                discrepancy_message = f"Discrepancies for {language_name}:\n" + "\n".join(discrepancies)
                                all_discrepancies.append(discrepancy_message)

                        else:
                            print(f"No web data found for language: {language_name}")
                else:
                    print(f"No database data found for language: {language_name}")

            # Проверяем, есть ли общие несоответствия
            if all_discrepancies:
                all_discrepancies_message = "\n\n".join(all_discrepancies)
                print(f"Discrepancies found:\n{all_discrepancies_message}")
            else:
                print("No discrepancies found across all languages.")

    def compare_data1(self):
        languages = self.query_lang_rep()  # Получение списка языков
        website_data = self.fetch_website_data()
        all_discrepancies = []  # Инициализация списка для всех расхождений

        for lang in languages:
            language_name = lang[0]
            db_data = self.query_language_stats_CHH(language_name)
            if db_data:
                for row in db_data:
                    discrepancies = []
                    if language_name == "Arabic":
                        web_rows = [item for item in website_data if "Arabic" in item["LanguageName"]]
                    elif language_name == "French":
                        web_rows = [item for item in website_data if "French" in item["LanguageName"]]
                    elif language_name == "Portuguese":
                        web_rows = [item for item in website_data if "Portuguese" in item["LanguageName"]]
                    else:
                        web_rows = [item for item in website_data if item["LanguageName"] == language_name]

                    if web_rows:
                        print(f"Comparing data for language: {language_name}")

                        # Инициализация и вычисление общих значений для веб-данных
                        total_calls_web = sum(int(item["TotalCalls"]) for item in web_rows)
                        total_minutes_web = sum(int(item["TotalMinutes"]) for item in web_rows)
                        serviced_audio_calls_web = sum(int(item["ServicedAudioCalls"]) for item in web_rows)
                        serviced_video_calls_web = sum(int(item["ServicedVideoCalls"]) for item in web_rows)

                        # Обработка случая с None
                        db_total_calls = 0 if row.TotalCalls is None else row.TotalCalls
                        db_total_minutes = 0 if row.ServiceMinutes is None else row.ServiceMinutes
                        db_serviced_audio_calls = 0 if row.CountSuccessAudioCalls is None else row.CountSuccessAudioCalls
                        db_serviced_video_calls = 0 if row.CountSuccessVideoCalls is None else row.CountSuccessVideoCalls

                        # Сравнение значений
                        if str(db_total_calls) != str(total_calls_web):
                            discrepancies.append(f"Total Calls: DB({db_total_calls}) != Web({total_calls_web})")
                        if str(db_total_minutes) != str(total_minutes_web):
                            discrepancies.append(f"Total Minutes: DB({db_total_minutes}) != Web({total_minutes_web})")
                        if str(db_serviced_audio_calls) != str(serviced_audio_calls_web):
                            discrepancies.append(
                                f"Serviced Audio Calls: DB({db_serviced_audio_calls}) != Web({serviced_audio_calls_web})")
                        if str(db_serviced_video_calls) != str(serviced_video_calls_web):
                            discrepancies.append(
                                f"Serviced Video Calls: DB({db_serviced_video_calls}) != Web({serviced_video_calls_web})")

                        # Остальная часть кода
                        if discrepancies:
                            discrepancy_messages = "\n".join(discrepancies)
                            all_discrepancies.append(f"Discrepancies for {language_name}:\n{discrepancy_messages}")
                        else:
                            print("No discrepancies found for this language.")
                else:
                    print(f"No database data found for language: {language_name}")

                        # После проверки всех языков, если были обнаружены расхождения, выводим их
            if all_discrepancies:
                discrepancies_report = "\n\n".join(all_discrepancies)
                print(f"Discrepancies found:\n{discrepancies_report}")
            else:
                print("No discrepancies found in all languages.")

    def compare_data1234(self):
        with allure.step("Compare data for the specific Client"):
            languages = self.query_lang_rep()  # Получение списка языков
            website_data = self.fetch_website_data1()
            all_discrepancies = []  # Список для сбора всех расхождений

            for lang in languages:
                language_name = lang[0]
                db_data = self.query_language_stats_CHH(language_name)
                if db_data:
                    for row in db_data:
                        discrepancies = []
                        if language_name == "Arabic":
                            web_rows = [item for item in website_data if "Arabic" in item["LanguageName"]]
                        elif language_name == "French":
                            web_rows = [item for item in website_data if "French" in item["LanguageName"]]
                        elif language_name == "Portuguese":
                            web_rows = [item for item in website_data if "Portuguese" in item["LanguageName"]]
                        else:
                            web_rows = [item for item in website_data if item["LanguageName"] == language_name]

                        if web_rows:
                            print(f"Comparing data for language: {language_name}")

                            total_calls_web = sum(int(item["TotalCalls"] or 0) for item in web_rows)
                            total_minutes_web = sum(int(item["TotalMinutes"] or 0) for item in web_rows)
                            serviced_audio_calls_web = sum(int(item["CallsbyAudio"] or 0) for item in web_rows)
                            serviced_video_calls_web = sum(int(item["CallsbyVideo"] or 0) for item in web_rows)

                            db_total_calls = 0 if row.TotalCalls is None else row.TotalCalls
                            db_total_minutes = 0 if row.ServiceMinutes is None else row.ServiceMinutes
                            db_serviced_audio_calls = 0 if row.CountSuccessAudioCalls is None else row.CountSuccessAudioCalls
                            db_serviced_video_calls = 0 if row.CountSuccessVideoCalls is None else row.CountSuccessVideoCalls

                            if str(db_total_calls) != str(total_calls_web):
                                discrepancies.append(f"Total Calls: DB({db_total_calls}) != Web({total_calls_web})")
                            if str(db_total_minutes) != str(total_minutes_web):
                                discrepancies.append(
                                    f"Total Minutes: DB({db_total_minutes}) != Web({total_minutes_web})")
                            if str(db_serviced_audio_calls) != str(serviced_audio_calls_web):
                                discrepancies.append(
                                    f"Serviced Audio Calls: DB({db_serviced_audio_calls}) != Web({serviced_audio_calls_web})")
                            if str(db_serviced_video_calls) != str(serviced_video_calls_web):
                                discrepancies.append(
                                    f"Serviced Video Calls: DB({db_serviced_video_calls}) != Web({serviced_video_calls_web})")

                            if discrepancies:
                                discrepancy_messages = "\n".join(discrepancies)
                                all_discrepancies.append(f"Discrepancies for {language_name}:\n{discrepancy_messages}")
                            else:
                                print("No discrepancies found for this language.")
                    else:
                        print(f"No database data found for language: {language_name}")

            if all_discrepancies:
                discrepancies_report = "\n\n".join(all_discrepancies)
                print(f"Discrepancies found:\n{discrepancies_report}")
            else:
                print("No discrepancies found in all languages.")


    @allure.step("Comparing device data")
    def compare_devices_data(self):
        with allure.step("Compare Graphs data with API"):
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

            token = self.get_token_from_session_storage()
            if not token:
                logging.error("No token found in session storage. Cannot proceed with the API call.")
                return

            logging.info(f"Using token: {token}")
            with allure.step("Fetching data from API"):
                url = 'https://api.staging.vip.voyceglobal.com/get-all-devices'
                headers = {
                    'authority': 'api.staging.vip.voyceglobal.com',
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
                    'authorization': f'Bearer {token}',
                    'content-type': 'application/json',
                    'origin': 'https://staging.vip.voyceglobal.com',
                    'referer': 'https://staging.vip.voyceglobal.com/',
                    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                current_utc_date = datetime.utcnow()
                start_date = (current_utc_date - timedelta(hours=5)).strftime('%Y-%m-%dT05:00:00.000Z')
                end_date = (current_utc_date - timedelta(hours=5) + timedelta(days=1)).strftime(
                    '%Y-%m-%dT04:59:59.999Z')

                data = {
                    'RequestCompanyId': 1604,
                    'filterType': 'company',
                    'id': 1604
                }
                params = {
                    'start': start_date,
                    'end': end_date,
                }

                response = requests.post(url, headers=headers, json=data, params=params)
                if response.status_code != 200:
                    logging.error(
                        f"Failed to get data from API. Status code: {response.status_code}. Response: {response.text}")
                    return

                api_data = response.json()

            with allure.step("Get web site data"):
                self.driver.get("https://staging.vip.voyceglobal.com/pages/reports/device-usage")
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table > tbody > tr"))
                )

            with allure.step("Comparing API data with Web data"):
                rows = self.driver.find_elements(By.CSS_SELECTOR, "table > tbody > tr.ant-table-row")
                for device in api_data:
                    serial_number_api = device['IOSSerialNumber']
                    num_services_api = device['NumberOfServices']
                    service_minutes_api = device['ServiceMinutes']

                    device_found = False
                    for row in rows:
                        cells = row.find_elements(By.CSS_SELECTOR, "td.ant-table-cell")
                        if len(cells) >= 6:  # Проверка наличия достаточного количества ячеек
                            serial_number_web = cells[1].text
                            num_services_web = cells[5].text
                            service_minutes_web = cells[3].text

                            if serial_number_api == serial_number_web:
                                device_found = True
                                try:
                                    assert str(num_services_api) == num_services_web, \
                                        f"Number of services does not match: API {num_services_api} != Web {num_services_web}"
                                    assert str(service_minutes_api) == service_minutes_web, \
                                        f"Service minutes does not match: API {service_minutes_api} != Web {service_minutes_web}"
                                    logging.info(f"Data for {serial_number_api} is correct.")
                                    allure.attach(f"Data for {serial_number_api} is correct.",
                                                  name="Correct data match")
                                except AssertionError as e:
                                    logging.error(str(e))
                                    allure.attach(str(e), name="Data mismatch")
                                break
                        else:
                            logging.warning(f"Row in the table does not contain enough cells: {len(cells)}")

                    if not device_found:
                        logging.warning(f"Device with serial number {serial_number_api} not found on the web page.")
                        allure.attach(f"Device with serial number {serial_number_api} not found on the web page.",
                                      name="Missing device")
