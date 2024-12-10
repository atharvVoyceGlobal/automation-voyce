import time
import allure
import uuid
import requests
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ev import EV
import json
import subprocess
import os
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import logging


class Login_page_martii(EV):
    url_m = 'https://cloudbreak-admin-ui.dev.cloudbreak.us/okta-login'

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def install_browser_and_driver():
        installation_path = os.path.join(os.getcwd(), "chrome_installation")
        os.makedirs(installation_path, exist_ok=True)

        try:
            print("Installing Chrome...")
            subprocess.run(
                [
                    "npx", "@puppeteer/browsers", "install", "chrome@stable",
                    "--path", installation_path
                ],
                check=True
            )
            print("Chrome installed successfully!")

            #
            chrome_binary_path = os.path.join(
                installation_path,
                "chrome",
                "mac_arm-131.0.6778.85",
                "chrome-mac-arm64",
                "Google Chrome for Testing.app",
                "Contents",
                "MacOS",
                "Google Chrome for Testing"
            )

            if not os.path.exists(chrome_binary_path):
                raise FileNotFoundError(f"Chrome binary not found at {chrome_binary_path}")

            #
            print("Fetching Chrome version...")
            version_output = subprocess.run(
                [chrome_binary_path, "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            chrome_version = version_output.stdout.strip().split(" ")[-1]  #
            print(f"Installed Chrome version: {chrome_version}")

            #
            print(f"Installing ChromeDriver for version {chrome_version}...")
            subprocess.run(
                [
                    "npx", "@puppeteer/browsers", "install", f"chromedriver@{chrome_version}",
                    "--path", installation_path
                ],
                check=True
            )
            print("ChromeDriver installed successfully!")

            #
            chromedriver_path = os.path.join(
                installation_path,
                "chromedriver",
                f"mac_arm-{chrome_version}",
                "chromedriver-mac-arm64",
                "chromedriver"
            )

            if not os.path.exists(chromedriver_path):
                raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")

            print(f"Chrome binary: {chrome_binary_path}")
            print(f"ChromeDriver binary: {chromedriver_path}")

            return chrome_binary_path, chromedriver_path
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during installation: {e}")
            raise

    @staticmethod
    def driver():
        #
        chrome_path, chromedriver_path = Login_page_martii.install_browser_and_driver()

        #
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.binary_location = chrome_path

        driver_service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)

        return driver

    ACCESS_CODE_ID1 = "aAAO30000008M4zOAE"
    PARTNER_ID2 = "aAHD300000002jsOAA"
    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
    PARTNER_ID = "aAHD30000004IGhOAM"
    DEPARTMENT_ID = "aAMD3000000APICOA4"
    login_field = "//*[@id='input28']"
    password_field = "//*[@id='input36']"
    button_login = "//*[@id='form20']/div[2]/input"
    main_word = "//*[@id='header-container-id']/div/div[1]/div"
    error_email = "//*[@id='email_help']/div"
    error_password = "//*[@id='password_help']/div"
    no_valid_password = "/html/body/div[2]/div/div/div/span[2]"
    no_valid_email = "/html/body/div[2]/div/div/div/span[2]"
    log_out = "//*[@id='root']/section/aside/div/div[3]/div/div/span/span"
    log_out2 = "//li[contains(@class, 'ant-dropdown-menu-item') and contains(@class, 'ant-dropdown-menu-item-danger') and .//span[contains(@class, 'ant-dropdown-menu-title-content') and text()='Logout']]"
    PARTNER_ID1 = "aAHO3000000Ni1xOAC"
    SITE_ID = "aAHO3000000Ni8POAS"

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
        print("Input user name")

    def input_password(self, user_password):
        self.get_password_field().send_keys(user_password)
        print("Input password")

    def click_button_login(self):
        self.get_button_login().click()
        print("Clicked login button")

    def check_response(self, response):
        assert 200 <= response.status_code < 300, f"HTTP error {response.status_code}: {response.text}"
        return response.json()

    def authorization(self):
        self.driver.get(self.url_m)
        self.input_login(self.my_accaunt_m)
        self.input_password(self.my_password)
        self.click_button_login()
        time.sleep(20)
        token_data = self.driver.execute_script("return window.localStorage.getItem('okta-token-storage');")

        if token_data:
            token_json = json.loads(token_data)

            token = token_json.get("accessToken", {}).get("accessToken")

            if token:

                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }

                def get_json_or_html(response):
                    try:
                        return response.json()
                    except requests.exceptions.JSONDecodeError:
                        print("Response content is not valid JSON:", response.text)
                        return None

                def test_get_partners_list():
                    url = f"{self.BASE_URL}/v1/partners"
                    response = requests.get(url, headers=headers)
                    assert response.status_code == 200, f"Failed GET partners list: {response.status_code}"
                    json_response = get_json_or_html(response)

                    assert json_response and "results" in json_response, "Key 'results' not found in response"
                    assert isinstance(json_response["results"], list), "'results' is not a list"

                    assert len(json_response["results"]) > 0, "Partners list is empty"

                    print("GET partners list test passed")

                def test_get_department():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}/departments/{self.DEPARTMENT_ID}"
                    response = requests.get(url, headers=headers)
                    assert response.status_code == 200, f"Failed GET department: {response.status_code}"
                    json_response = get_json_or_html(response)
                    assert json_response and "id" in json_response, "ID not in response"
                    print("GET department test passed")

                def test_update_department():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}/departments/{self.DEPARTMENT_ID}"
                    data = {"name": "Updated Department Name"}
                    response = requests.put(url, headers=headers, json=data)
                    assert response.status_code == 200, f"Failed PUT department: {response.status_code}"
                    json_response = get_json_or_html(response)
                    assert json_response and json_response["name"] == data["name"], "Name update failed"
                    print("PUT department test passed")

                def test_create_department():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}/departments"
                    data = {
                        "partnerId": self.PARTNER_ID,
                        "name": "New Department",
                        "description": "Description of new department"
                    }
                    response = requests.post(url, headers=headers, json=data)

                    #
                    print("Response status code:", response.status_code)

                    #
                    assert response.status_code == 201, f"Failed POST department: {response.status_code}, Response: {response.text}"

                    #
                    json_response = get_json_or_html(response)
                    assert json_response and "id" in json_response, "New department creation failed"
                    print("POST department test passed")

                def test_create_access_code():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}/departments/{self.DEPARTMENT_ID}/accesscode"
                    response = requests.post(url, headers=headers)

                    #
                    print("Response status code:", response.status_code)

                    assert response.status_code == 201, f"Failed POST access code: {response.status_code}, Response: {response.text}"

                    #
                    json_response = get_json_or_html(response)
                    assert json_response and "accessCode" in json_response, "Access code creation failed"
                    print("Access code created successfully")

                def test_update_department_languages():
                    #
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}/departments/{self.DEPARTMENT_ID}/languages"

                    #
                    data = [
                        "aAX2i0000008PQWGA2",  #
                        "aAX2i0000008PQXGA2",  #
                        "aAX2i0000008PQYGA2"  #
                    ]

                    #
                    print("Request URL:", url)
                    print("Request data:", data)

                    #
                    response = requests.put(url, headers=headers, json=data)

                    #
                    print("Response status code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed PUT department languages: {response.status_code}, Response: {response.text}"

                    #
                    json_response = response.json()

                    #
                    assert "languages" in json_response, "Languages update failed or missing in response"

                    #
                    updated_languages = json_response["languages"]
                    print("Department languages updated successfully:", updated_languages)

                def test_create_secret():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}/departments/{self.DEPARTMENT_ID}/secret"
                    response = requests.post(url, headers=headers)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 201, f"Failed POST secret: {response.status_code}, Response: {response.text}"

                    #
                    if response.headers.get("Content-Type") == "application/json":
                        #
                        json_response = get_json_or_html(response)
                        assert json_response and "secret" in json_response, "Expected 'secret' key not found in JSON response"
                        print("Secret created successfully (JSON):", json_response["secret"])
                    else:
                        #
                        secret_key = response.text.strip()
                        print("Secret created successfully (Text):", secret_key)
                        assert len(secret_key) > 0, "Secret is empty"

                def test_get_secret():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}/departments/{self.DEPARTMENT_ID}/secret"
                    response = requests.get(url, headers=headers)
                    assert response.status_code == 200, f"Failed GET secret: {response.status_code}"
                    content_type = response.headers.get('Content-Type', '')

                    if 'text/plain' in content_type or 'text/html' in content_type:
                        #
                        secret = response.text
                        assert secret, "Secret retrieval failed"
                        print(f"Retrieved secret: {secret}")
                    elif 'application/json' in content_type:
                        json_response = get_json_or_html(response)
                        assert json_response and "secret" in json_response, "Secret retrieval failed"
                        print(f"Retrieved JSON secret: {json_response['secret']}")
                    else:
                        assert False, f"Unexpected Content-Type: {content_type}"

                def test_get_departments_list():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}/departments"
                    response = requests.get(url, headers=headers)
                    print("Response status code:", response.status_code)

                    assert response.status_code == 200, f"Failed GET departments list: {response.status_code}"
                    json_response = get_json_or_html(response)
                    assert json_response and "results" in json_response, "Key 'results' not found in response"
                    assert isinstance(json_response["results"], list), "'results' is not a list"

                    assert len(json_response["results"]) > 0, "Departments list is empty"
                    print("First department in the results")

                    print("GET departments list test passed")

                def test_get_languages():
                    #
                    url = f"{self.BASE_URL}/v1/languages"

                    #
                    print("Request URL:", url)

                    #
                    response = requests.get(url, headers=headers)

                    #
                    print("Response status code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed GET languages: {response.status_code}, Response: {response.text}"

                    #
                    json_response = response.json()

                    #
                    assert isinstance(json_response, list), "Languages response is not a list"

                    #
                    if json_response:
                        first_language = json_response[0]
                        assert "id" in first_language, "Language entry missing 'id'"
                        assert "name" in first_language, "Language entry missing 'name'"
                        assert "languageCode" in first_language, "Language entry missing 'languageCode'"

                    print("GET languages test passed")

                def test_create_partner():
                    url = f"{self.BASE_URL}/v1/partners"
                    data = {
                        "isTelemed": False,
                        "name": "CL-4592",
                        "clientName": "Epic Test",
                        "physicalLocationCity": "Somewhere",
                        "physicalAddressState": "AL",
                        "physicalAddressZip": "11122",
                        "contactName": "Agon",
                        "contactEmail": "will.sadler@uphealthinc.com",
                        "contactPhoneNumber": "+18005551212",
                        "callCenterPlatform": "MARTTI_NEXT",
                        "status": "Active",
                        "unimplemented": False
                    }

                    #
                    print("Request URL:", url)
                    #
                    response = requests.post(url, headers=headers, json=data)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 201, f"Failed to create partner: {response.status_code}, Response: {response.text}"

                    #
                    json_response = response.json()
                    assert "id" in json_response, "Response missing 'id' field"
                    assert "name" in json_response, "Response missing 'name' field"  #
                    assert json_response["clientName"] == data["clientName"], "Client name mismatch"
                    print("Partner created successfully")

                def test_update_partner():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}"
                    data = {
                        "isTelemed": False,
                        "id": self.PARTNER_ID,
                        "name": "CL-4589",
                        "createdDate": "2023-08-24T17:01:52.000+0000",
                        "createdById": "0052i000002EzFvAAK",
                        "lastModifiedDate": "2024-03-20T16:38:57.000+0000",
                        "lastModifiedById": "0052i000002EzFvAAK",
                        "accountId": None,
                        "microCallCenterRouterWorkspaceId": None,
                        "microCallCenter": False,
                        "phoneNumber": None,
                        "primaryContact": None,
                        "status": "Active",
                        "clientName": "Zoom Marketplace Tester",
                        "physicalAddressLine1": None,
                        "physicalAddressLine2": None,
                        "physicalLocationCity": "Columbus",
                        "physicalAddressState": "OH",
                        "physicalAddressZip": "49543",
                        "callCenterPlatform": "MARTTI_NEXT",
                        "accessCodeValidationRequired": False,
                        "billingEntity": None,
                        "parentAccount": None,
                        "contactName": None,
                        "contactEmail": None,
                        "contactPhoneNumber": "+19012345671",
                        "unimplemented": False
                    }

                    print("Request URL:", url)

                    #
                    response = requests.put(url, headers=headers, json=data)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to update partner: {response.status_code}, Response: {response.text}"
                    json_response = response.json()

                    #
                    assert json_response["id"] == self.PARTNER_ID, "Partner ID mismatch"
                    assert json_response["name"] == data["name"], "Partner name mismatch"
                    assert json_response["clientName"] == data["clientName"], "Client name mismatch"
                    assert json_response["physicalLocationCity"] == data["physicalLocationCity"], "City mismatch"
                    assert json_response["physicalAddressState"] == data["physicalAddressState"], "State mismatch"
                    assert json_response["status"] == data["status"], "Status mismatch"

                    print("Partner successfully updated")

                def test_delete_partner():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID}"

                    #
                    response = requests.delete(url, headers=headers)

                    #
                    print("DELETE Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to delete partner: {response.status_code}, Response: {response.text}"

                    #
                    get_response = requests.get(url, headers=headers)
                    print("GET after DELETE - Status Code:", get_response.status_code)

                    #
                    if get_response.status_code == 200:
                        json_response = get_response.json()
                        assert json_response.get(
                            "status") == "Inactive", "Partner not marked as inactive after deletion."
                        print(f"Partner {self.PARTNER_ID} successfully marked as inactive.")
                    else:
                        assert get_response.status_code == 404, "Deleted partner still exists."
                        print(f"Partner {self.PARTNER_ID} successfully deleted.")

                def test_get_partner_providers():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID1}/providers"

                    #
                    print("Request URL:", url)

                    #
                    response = requests.get(url, headers=headers)

                    #
                    print("GET Providers Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to get partner's providers: {response.status_code}, Response: {response.text}"

                    #
                    json_response = response.json()
                    assert isinstance(json_response, dict), "Response is not a valid JSON object."
                    assert "results" in json_response, "'results' key is missing in the response."
                    assert isinstance(json_response["results"], list), "'results' is not a list."

                    #
                    assert len(json_response["results"]) > 0, "No providers found for the partner."

                    print(
                        f"Successfully retrieved {len(json_response['results'])} providers for partner {self.PARTNER_ID}.")

                def test_get_partner_sites():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID1}/sites"

                    #
                    print("Request URL:", url)

                    #
                    response = requests.get(url, headers=headers)

                    #
                    print("GET Sites Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to get partner's sites: {response.status_code}, Response: {response.text}"

                    #
                    json_response = response.json()
                    assert isinstance(json_response, dict), "Response is not a valid JSON object."
                    assert "results" in json_response, "'results' key is missing in the response."
                    assert isinstance(json_response["results"], list), "'results' is not a list."

                    #
                    sites = json_response["results"]
                    assert len(sites) > 0, "No sites found for the partner."

                    #
                    print(f"Successfully retrieved {len(sites)} sites for partner {self.PARTNER_ID1}.")

                def test_get_partner_site():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID1}/sites/{self.SITE_ID}"

                    #
                    print("Request URL:", url)

                    #
                    response = requests.get(url, headers=headers)

                    #
                    print("GET Site Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to get partner's site: {response.status_code}, Response: {response.text}"

                    #
                    json_response = response.json()
                    assert json_response["id"] == self.SITE_ID, f"Unexpected site ID: {json_response['id']}"

                    print(f"Successfully retrieved site {self.SITE_ID} for partner {self.PARTNER_ID1}.")

                def test_get_site_providers():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID1}/sites/{self.SITE_ID}/providers"

                    #
                    print("Request URL:", url)

                    #
                    response = requests.get(url, headers=headers)

                    #
                    print("GET Site Providers Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to get site's providers: {response.status_code}, Response: {response.text}"

                    #
                    json_response = response.json()
                    assert isinstance(json_response, dict), "Response is not a valid JSON object."
                    assert "results" in json_response, "'results' key is missing in the response."
                    assert isinstance(json_response["results"], list), "'results' is not a list."

                    #
                    providers = json_response["results"]
                    assert len(providers) > 0, "No providers found for the site."

                    #
                    print(f"Successfully retrieved {len(providers)} providers for site {self.SITE_ID}.")

                def test_get_partner_access_codes():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID1}/access-codes"

                    print("Request URL:", url)

                    response = requests.get(url, headers=headers)

                    print("GET Access Codes Response Status Code:", response.status_code)

                    assert response.status_code == 200, f"Failed to get partner's access codes: {response.status_code}, Response: {response.text}"

                    json_response = response.json()

                    assert isinstance(json_response, dict), "Response is not a valid JSON object"
                    assert "results" in json_response, "'results' key not found in the response"
                    assert isinstance(json_response["results"], list), "'results' is not a list"

                    access_codes = json_response["results"]

                def check_partner_account():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID1}"
                    response = requests.get(url, headers=headers)

                    print("GET Partner Response Status Code:", response.status_code)

                    assert response.status_code == 200, f"Failed to retrieve partner details: {response.status_code}, {response.text}"
                    json_response = response.json()

                    account_id = json_response.get("accountId")
                    client_name = json_response.get("clientName")

                    #
                    if not account_id:
                        print("Warning: Account ID is missing in the partner details.")
                    else:
                        print(f"Account ID for partner: {account_id}")

                    if not client_name:
                        print("Warning: Client Name is missing in the partner details.")
                    else:
                        print(f"Client Name for partner: {client_name}")

                    return account_id, client_name

                def test_update_partner1():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID2}"
                    data = {
                        "isTelemed": False,
                        "id": self.PARTNER_ID2,
                        "name": "CL-4589",
                        "createdDate": "2023-08-24T17:01:52.000+0000",
                        "createdById": "0052i000002EzFvAAK",
                        "lastModifiedDate": "2024-03-20T16:38:57.000+0000",
                        "lastModifiedById": "0052i000002EzFvAAK",
                        "accountId": "001D300000lYhYDIA0",  #
                        "microCallCenterRouterWorkspaceId": None,
                        "microCallCenter": False,
                        "phoneNumber": None,
                        "primaryContact": None,
                        "status": "Active",
                        "clientName": "Zoom Marketplace Tester",
                        "physicalAddressLine1": None,
                        "physicalAddressLine2": None,
                        "physicalLocationCity": "Columbus",
                        "physicalAddressState": "OH",
                        "physicalAddressZip": "49543",
                        "callCenterPlatform": "MARTTI_NEXT",
                        "accessCodeValidationRequired": False,
                        "billingEntity": None,
                        "parentAccount": None,
                        "contactName": None,
                        "contactEmail": None,
                        "contactPhoneNumber": "+19012345671",
                        "unimplemented": False
                    }

                    print("Request URL:", url)

                    response = requests.put(url, headers=headers, json=data)

                    print("Response Status Code:", response.status_code)

                    assert response.status_code == 200, f"Failed to update partner: {response.status_code}, Response: {response.text}"
                    json_response = response.json()

                    assert "accountId" in json_response, "Account ID is missing in the updated partner response"
                    print(f"Partner updated successfully with accountId: {json_response['accountId']}")

                def test_create_and_delete_partner_access_code():
                    account_id, client_name = check_partner_account()
                    if not account_id or not client_name:
                        print("Account ID or Client Name is missing. Attempting to update partner...")
                        test_update_partner1()
                        account_id, client_name = check_partner_account()
                        assert account_id, "Account ID is still missing after partner update. Cannot proceed."

                    create_url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID1}/access-codes"
                    data = {
                        "type": "CLIENT",
                        "status": "Active",
                        "partnerId": self.PARTNER_ID1
                    }

                    print("Request URL for Access Code Creation:", create_url)

                    create_response = requests.post(create_url, headers=headers, json=data)
                    print("POST Access Code Response Status Code:", create_response.status_code)
                    assert create_response.status_code == 201, f"Failed to create access code: {create_response.status_code}, Response: {create_response.text}"

                    json_response = create_response.json()
                    access_code_id = json_response["id"]
                    print(f"Access code created successfully with ID: {access_code_id}")

                    delete_url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID1}/access-codes/{access_code_id}"
                    print("Request URL for Access Code Deletion:", delete_url)
                    delete_response = requests.delete(delete_url, headers=headers)

                    print("DELETE Access Code Response Status Code:", delete_response.status_code)
                    assert delete_response.status_code == 200, f"Failed to delete access code: {delete_response.status_code}, Response: {delete_response.text}"
                    print("Access code deleted successfully.")

                def test_update_partner_access_code():
                    url = f"{self.BASE_URL}/v1/partners/{self.PARTNER_ID2}/access-codes/aAAO30000008QADOA2"

                    #
                    data = {
                        "results": [
                            {
                                "id": self.ACCESS_CODE_ID1,
                                "name": "Updated Access Code Name",
                                "client": self.PARTNER_ID2,
                                "partnerId": self.PARTNER_ID2,
                                "code": str("84889831"),  #
                                "department": "aAMO3000000UnePOAS",
                                "martti": "aAZO30000000pIfOAI",
                                "status": "ACTIVE",
                                "type": "MARTTI",
                                "showCallerFirstName": False,
                                "showCallerLastName": False,
                                "showPatientDOB": True,
                                "showPatientFirstName": True,
                                "showPatientLastName": True,
                                "showPatientMRN": True,
                                "showProviderFirstName": True,
                                "showProviderLastName": True,
                                "showMemberIDNumber": False,
                                "showNYUAccessCode": False,
                                "showSentaraAccessCode": False,
                                "showVisitID": False,
                                "showLocation": False,
                                "showBCHOaklandHospitalConfirmation": False,
                                "skipAudioCallAccessCodeValidation": False,
                                "phoneNumberAccessCode": False
                            }
                        ],
                        "page": 1,
                        "total": 1,
                        "limit": 20
                    }

                    #
                    print("Sending PUT request to update access code...")
                    print("Request URL:", url)

                    #
                    response = requests.put(url, headers=headers, json=data)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to update access code: {response.status_code}, Response: {response.text}"

                    #
                    response_data = response.json()
                    assert response_data["id"] == self.ACCESS_CODE_ID1, "Access code ID mismatch."
                    assert response_data["code"] == "87654321", "Access code value was not updated."

                    print("Test passed. Access code updated successfully.")

                def test_get_partner_queues():
                    """Test to get a list of an MCC partner's queues."""

                    #
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    PARTNER_ID = "aAHO3000000LtmHOAS"
                    PARAMS = {
                        "page": 1,
                        "limit": 20,
                        "withInhouse": "false",
                        "orderBy": "name",
                        "orderType": "asc"
                    }

                    #
                    url = f"{BASE_URL}/v1/partners/{PARTNER_ID}/queues"

                    #
                    print("Sending GET request to fetch partner queues...")
                    print("Request URL:", url)

                    print("Request Params:", json.dumps(PARAMS, indent=2))

                    response = requests.get(url, headers=headers, params=PARAMS)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to fetch queues: {response.status_code}, Response: {response.text}"

                    response_data = response.json()

                    #
                    assert "page" in response_data, "Missing 'page' in response"
                    assert "limit" in response_data, "Missing 'limit' in response"
                    assert "total" in response_data, "Missing 'total' in response"
                    assert "results" in response_data, "Missing 'results' in response"

                    #
                    for queue in response_data["results"]:
                        assert "id" in queue, "Missing 'id' in queue"
                        assert "name" in queue, "Missing 'name' in queue"
                        assert "partnerId" in queue, "Missing 'partnerId' in queue"
                        assert queue["partnerId"] == PARTNER_ID, f"Unexpected partnerId: {queue['partnerId']}"

                    print("Test passed. Queues fetched successfully.")

                def test_create_and_delete_language():
                    """Test to create a new language and then delete it."""

                    #
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    CREATE_ENDPOINT = "/v1/languages"

                    #
                    payload = {
                        "name": "Test Language two",
                        "translationName": "Test lang",
                        "direction": "LTR"
                    }

                    #
                    print("Sending POST request to create a language...")
                    create_url = BASE_URL + CREATE_ENDPOINT
                    print("Request URL:", create_url)

                    response = requests.post(create_url, headers=headers, json=payload)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code in [200,
                                                    201], f"Failed to create language: {response.status_code}, Response: {response.text}"

                    #
                    response_data = response.json()
                    language_id = response_data["id"]
                    print("Language created successfully with ID:", language_id)

                    #
                    print("Sending DELETE request to delete the language...")
                    delete_url = f"{BASE_URL}/v1/languages/{language_id}"
                    print("Request URL:", delete_url)

                    delete_response = requests.delete(delete_url, headers=headers)

                    #
                    print("Response Status Code:", delete_response.status_code)

                    #
                    assert delete_response.status_code == 200, f"Failed to delete language: {delete_response.status_code}, Response: {delete_response.text}"

                    print("Test passed. Language created and deleted successfully.")

                def test_update_language():
                    """Test to update an existing language."""

                    #
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    LANGUAGE_ID = "aAXO30000009gMbOAI"  #
                    UPDATE_ENDPOINT = f"/v1/languages/{LANGUAGE_ID}"
                    url = BASE_URL + UPDATE_ENDPOINT

                    payload = {
                        "name": "Updated Test Language",
                        "translationName": "Updated Test Lang",
                        "direction": "LTR"
                    }

                    #
                    print("Sending PUT request to update a language...")
                    print("Request URL:", url)

                    response = requests.put(url, headers=headers, json=payload)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to update language: {response.status_code}, Response: {response.text}"

                    #
                    response_data = response.json()
                    assert response_data["name"] == payload["name"], "Name mismatch in the response."
                    assert response_data["translationName"] == payload[
                        "translationName"], "Translation name mismatch in the response."
                    assert response_data["direction"] == payload["direction"], "Direction mismatch in the response."

                    print("Test passed. Language updated successfully.")

                def test_get_language():
                    """Test to retrieve information about a specific language."""

                    #
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    LANGUAGE_ID = "aAXO30000009gMbOAI"  #
                    GET_ENDPOINT = f"/v1/languages/{LANGUAGE_ID}"
                    url = BASE_URL + GET_ENDPOINT

                    print("Sending GET request to retrieve language details...")
                    print("Request URL:", url)

                    response = requests.get(url, headers=headers)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to retrieve language: {response.status_code}, Response: {response.text}"

                    #
                    response_data = response.json()
                    assert response_data["id"] == LANGUAGE_ID, "Language ID mismatch in the response."
                    assert "name" in response_data, "Response missing 'name' field."
                    assert "translationName" in response_data, "Response missing 'translationName' field."
                    assert "direction" in response_data, "Response missing 'direction' field."

                    print("Test passed. Language details retrieved successfully.")

                def test_get_paginated_languages():
                    """Test to retrieve a paginated list of languages."""

                    #
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    GET_ENDPOINT = "/v2/languages"
                    url = BASE_URL + GET_ENDPOINT

                    #
                    params = {
                        "page": 1,  #
                        "limit": 20,  #
                        "orderBy": "name",  #
                        "orderType": "asc",  #
                        "search": ""  #
                    }

                    #
                    print("Sending GET request to retrieve paginated list of languages...")
                    print("Request URL:", url)

                    print("Request Params:", json.dumps(params, indent=2))

                    response = requests.get(url, headers=headers, params=params)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to retrieve languages: {response.status_code}, Response: {response.text}"

                    #
                    response_data = response.json()
                    assert "results" in response_data, "Response missing 'results' field."
                    assert "page" in response_data, "Response missing 'page' field."
                    assert "limit" in response_data, "Response missing 'limit' field."
                    assert "total" in response_data, "Response missing 'total' field."

                    #
                    if response_data["results"]:
                        first_result = response_data["results"][0]
                        assert "id" in first_result, "Result missing 'id' field."
                        assert "name" in first_result, "Result missing 'name' field."
                        assert "translationName" in first_result, "Result missing 'translationName' field."

                    print("Test passed. Paginated list of languages retrieved successfully.")

                def test_get_status():
                    """Test to check the health status of the service."""

                    #
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    STATUS_ENDPOINT = "/status"
                    url = BASE_URL + STATUS_ENDPOINT

                    #
                    print("Sending GET request to check service health status...")
                    print("Request URL:", url)

                    response = requests.get(url, headers=headers)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code in [200,
                                                    503], f"Unexpected response code: {response.status_code}, Response: {response.text}"

                    #
                    response_data = response.json()

                    #
                    assert "status" in response_data, "Response missing 'status' field."
                    assert "info" in response_data, "Response missing 'info' field."
                    assert "details" in response_data, "Response missing 'details' field."

                    if response.status_code == 200:
                        #
                        assert response_data["status"] == "ok", f"Unexpected status value: {response_data['status']}"
                        print("Service health check passed. Status is 'ok'.")
                    elif response.status_code == 503:
                        #
                        assert response_data["status"] == "error", f"Unexpected status value: {response_data['status']}"
                        print("Service health check failed. Status is 'error'.")

                    #
                    details = response_data["details"]
                    if "database" in details:
                        print(f"Database status: {details['database']['status']}")
                    elif "tcp" in details:
                        print(f"TCP status: {details['tcp']['status']}")
                    else:
                        assert False, "Neither 'database' nor 'tcp' status found in details."

                def test_get_list_of_queues():
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    QUEUES_ENDPOINT = "/v1/queues"
                    url = BASE_URL + QUEUES_ENDPOINT

                    #
                    params = {
                        "page": 1,
                        "limit": 20,
                        "orderBy": "name",  #
                        "orderType": "desc",  #
                        "search": ""  #
                    }

                    #
                    print("Sending GET request to fetch list of queues...")
                    print("Request URL:", url)

                    print("Request Params:", json.dumps(params, indent=2))

                    response = requests.get(url, headers=headers, params=params)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    assert response.status_code == 200, f"Failed to fetch list of queues: {response.status_code}, Response: {response.text}"

                    #
                    response_data = response.json()

                    #
                    assert "results" in response_data, "Response missing 'results' field."
                    assert "page" in response_data, "Response missing 'page' field."
                    assert "limit" in response_data, "Response missing 'limit' field."
                    assert "total" in response_data, "Response missing 'total' field."

                    #
                    if response_data["results"]:
                        queue = response_data["results"][0]  #
                        timeout_queue_id = queue["id"]
                        partner_id = queue.get("partnerId", "default-partner-id")
                        language_id = queue.get("languageId", "default-language-id")
                    else:
                        raise ValueError("No queues found to use for creating a new queue.")

                    print("Extracted IDs from GET response:")
                    print(f"timeout_queue_id: {timeout_queue_id}")
                    print(f"partner_id: {partner_id}")
                    print(f"language_id: {language_id}")

                    print("Test passed. List of queues fetched successfully.")

                    #
                    payload = {
                        "name": "Test Queue",
                        "type": "LANGUAGE",
                        "service": "OPERATOR",
                        "description": "Queue for testing purposes",
                        "timeoutInSeconds": 30,
                        "languageId": language_id,
                        "channel": "VIDEO",
                        "timeoutQueueId": timeout_queue_id,
                        "timeoutPhoneNumber": "1234567890",
                        "partnerId": "aAH2i000000CezPGAS",
                        "microCallCenter": True,
                        "user": "AGENT"
                    }

                    print("Sending POST request to create a queue...")
                    print("Request URL:", url)

                    post_response = requests.post(url, headers=headers, json=payload)

                    #
                    print("POST Response Status Code:", post_response.status_code)

                    #
                    assert post_response.status_code == 200, f"Failed to create queue: {post_response.status_code}, Response: {post_response.text}"

                    #
                    post_response_data = post_response.json()
                    assert "id" in post_response_data, "POST response missing 'id' field."
                    assert post_response_data["name"] == payload["name"], "Queue name does not match the payload."

                    print(f"POST test passed. Queue created successfully with ID: {post_response_data['id']}.")

                def test_get_providers():
                    """Test to get a list of providers."""

                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    PROVIDERS_ENDPOINT = "/v1/providers"
                    url = BASE_URL + PROVIDERS_ENDPOINT

                    params = {
                        "page": 1,
                        "limit": 20,
                        "withSites": False,
                        "withSpecialization": False
                    }

                    print("Sending GET request to fetch list of providers...")
                    print("Request URL:", url)
                    print("Request Params:", json.dumps(params, indent=2))

                    response = requests.get(url, headers=headers, params=params)

                    print("Response Status Code:", response.status_code)

                    assert response.status_code == 200, f"Failed to fetch providers: {response.status_code}, Response: {response.text}"

                    response_data = response.json()
                    assert "results" in response_data, "Response is missing 'results' field."
                    assert isinstance(response_data["results"], list), "'results' should be a list."
                    print(f"Fetched {len(response_data['results'])} providers successfully.")

                    if len(response_data["results"]) > 0:
                        sample_provider = response_data["results"][0]
                        assert "id" in sample_provider, "Provider is missing 'id' field."
                        assert "name" in sample_provider, "Provider is missing 'name' field."
                        assert "status" in sample_provider, "Provider is missing 'status' field."
                        print("Sample provider fields validated successfully.")

                    print("Test passed. Providers fetched successfully.")

                def fetch_create_and_delete_provider():
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    PARTNERS_ENDPOINT = "/v1/partners"
                    PROVIDERS_ENDPOINT = "/v1/providers"

                    fetch_url = BASE_URL + PARTNERS_ENDPOINT
                    print("Fetching partners...")
                    response = requests.get(fetch_url, headers=headers)
                    print("Partners Response Status Code:", response.status_code)

                    assert response.status_code == 200, "Failed to fetch partners."
                    partners = response.json().get("results", [])
                    if not partners:
                        raise Exception("No partners found in the system.")

                    valid_partner_id = partners[0]["id"]

                    create_url = BASE_URL + PROVIDERS_ENDPOINT
                    unique_email = f"test.provider.{uuid.uuid4().hex[:8]}@example.com"

                    payload = {
                        "firstname": "Test",
                        "lastname": "Provider",
                        "initials": "TP",
                        "email": unique_email,
                        "contactNumber": "1234567890",
                        "status": "Active",
                        "partnerId": valid_partner_id,
                        "specializationIds": []
                    }

                    print("Creating a new provider...")
                    print("Request URL:", create_url)

                    create_response = requests.post(create_url, headers=headers, json=payload)
                    print("Create Response Status Code:", create_response.status_code)
                    print("Create Response Body")

                    assert create_response.status_code == 201, f"Failed to create provider: {create_response.status_code}"
                    created_provider = create_response.json()
                    created_provider_id = created_provider["id"]

                    print(f"Provider created successfully with ID: {created_provider_id}")

                    delete_url = f"{BASE_URL}{PROVIDERS_ENDPOINT}/{created_provider_id}"
                    print(f"Deleting provider with ID: {created_provider_id}...")
                    delete_response = requests.delete(delete_url, headers=headers)
                    print("Delete Response Status Code:", delete_response.status_code)
                    print("Delete Response Body:", delete_response.text)

                    assert delete_response.status_code == 200, f"Failed to delete provider: {delete_response.status_code}"

                    print(f"Provider with ID: {created_provider_id} deleted successfully.")

                def fetch_provider(provider_id="aCM2i000000BiNxGAK", with_sites=False, with_specialization=False):

                    endpoint = f"/v1/providers/{provider_id}"
                    url = self.BASE_URL + endpoint
                    params = {
                        "withSites": with_sites,
                        "withSpecialization": with_specialization
                    }

                    print(f"Fetching provider with ID: {provider_id}...")
                    response = requests.get(url, headers=headers, params=params)

                    #
                    print("Response Status Code:", response.status_code)

                    #
                    if response.status_code == 200:
                        provider_data = response.json()
                        print("Provider fetched successfully!")
                        return provider_data
                    elif response.status_code == 404:
                        raise Exception(f"Provider with ID {provider_id} not found.")
                    else:
                        raise Exception(f"Failed to fetch provider: {response.status_code}, {response.text}")

                try:
                    provider_data = fetch_provider()
                except Exception as e:
                    print("Done")

                def update_provider(provider_id="aCM2i000000BiNxGAK"):
                    """Update an existing provider."""
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    PROVIDERS_ENDPOINT = f"/v1/providers/{provider_id}"

                    update_payload = {
                        "firstname": "UpdatedFirstName",
                        "lastname": "UpdatedLastName",
                        "initials": "UF",
                        "contactNumber": "9876543210",
                        "status": "Active",
                        "specializationIds": [],
                        "partnerId": "aAHD3000000GmiDOAS"
                    }

                    update_url = BASE_URL + PROVIDERS_ENDPOINT

                    print(f"Updating provider with ID: {provider_id}...")
                    print("Request URL:", update_url)

                    response = requests.put(update_url, headers=headers, json=update_payload)
                    print("Update Response Status Code:", response.status_code)

                    assert response.status_code == 200, f"Failed to update provider: {response.status_code}"

                    updated_provider = response.json()
                    print("Provider updated successfully")

                def add_martti_to_provider():
                    provider_id = "aCM2i000000BiNxGAK"
                    partner_id = "aAHD3000000GmiDOAS"
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    MARTTIS_ENDPOINT = f"/v1/providers/{provider_id}/marttis"

                    add_martti_url = f"{BASE_URL}{MARTTIS_ENDPOINT}?partnerId={partner_id}"

                    print(f"Adding Martti to provider with ID: {provider_id}...")
                    print("Request URL:", add_martti_url)

                    response = requests.post(add_martti_url, headers=headers)
                    print("Response Status Code:", response.status_code)

                    #
                    if response.status_code == 201:
                        print("Martti added successfully:")
                    else:
                        print(f"Failed to add Martti: {response.status_code} - {response.text}")

                def bulk_update_provider_specializations():
                    provider_id = "aCM2i000000BiO1GAK"
                    specialization_ids = ["spec1", "spec2", "spec3"]
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    SPECIALIZATIONS_ENDPOINT = f"/v1/providers/{provider_id}/specializations"

                    payload = {
                        "specializationIds": specialization_ids
                    }

                    update_specializations_url = BASE_URL + SPECIALIZATIONS_ENDPOINT

                    print(f"Updating specializations for provider with ID: {provider_id}...")
                    print("Request URL:", update_specializations_url)

                    response = requests.put(update_specializations_url, headers=headers, json=payload)

                    print("Response Status Code:", response.status_code)
                    if response.status_code != 200:
                        raise AssertionError(
                            f"Failed to update specializations: {response.status_code} - {response.text}"
                        )

                    print("Specializations updated successfully:", json.dumps(response.json(), indent=2))

                def reset_provider_password():
                    provider_id = "aCM2i000000BiNxGAK"
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    RESET_PASSWORD_ENDPOINT = f"/v1/providers/{provider_id}/reset-password"

                    reset_password_url = BASE_URL + RESET_PASSWORD_ENDPOINT

                    print(f"Resetting password for provider with ID: {provider_id}...")
                    print("Request URL:", reset_password_url)

                    response = requests.post(reset_password_url, headers=headers)
                    print("Response Status Code:", response.status_code)

                    # Явная проверка успешного результата
                    assert response.status_code == 204, (
                        f"Password reset failed for provider {provider_id}. "
                        f"Status code: {response.status_code}, Response: {response.text}"
                    )

                    print(f"Password reset successful for provider {provider_id}.")

                def change_provider_password():
                    provider_id = "aCM2i000000BiNxGAK"
                    new_password = "NewSecurePassword123!"
                    url = f"{self.BASE_URL}/v1/providers/{provider_id}/change-password"
                    payload = {"password": new_password}

                    response = requests.post(url, headers=headers, json=payload)
                    assert response.status_code == 204, f"Failed to change provider password: {response.status_code}, {response.text}"
                    print(f"Password changed successfully for provider {provider_id}.")

                def get_specializations():
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    SPECIALIZATIONS_ENDPOINT = "/v1/specializations"

                    specializations_url = BASE_URL + SPECIALIZATIONS_ENDPOINT

                    print("Fetching specializations...")
                    print("Request URL:", specializations_url)

                    response = requests.get(specializations_url, headers=headers)
                    print("Response Status Code:", response.status_code)

                    if response.status_code == 200:
                        specializations = response.json()
                        print("Fetched Specializations:")
                        print(f"Total Specializations Fetched: {len(specializations)}")
                        return specializations
                    elif response.status_code == 401:
                        print("Unauthorized: Check your authorization token.")
                    else:
                        print(f"Unexpected error: {response.status_code} - {response.text}")

                    return None

                def get_skills():
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    SKILLS_ENDPOINT = "/v1/skills"

                    skills_url = BASE_URL + SKILLS_ENDPOINT

                    print("Fetching skills...")
                    print("Request URL:", skills_url)

                    response = requests.get(skills_url, headers=headers)
                    print("Response Status Code:", response.status_code)

                    if response.status_code == 200:
                        skills = response.json()
                        print("Fetched Skills:")
                        for skill in skills:
                            print(f"ID: {skill['id']}, Name: {skill['name']}")
                        print(f"Total Skills Fetched: {len(skills)}")
                        return skills
                    elif response.status_code == 401:
                        print("Unauthorized: Check your authorization token.")
                    else:
                        print(f"Unexpected error: {response.status_code} - {response.text}")

                    return None

                def create_skill():
                    url = "https://cloudbreak-admin-api.dev.cloudbreak.us/v1/skills"

                    skill_data = {
                        "microCallCenter": True,
                        "partnerId": "examplePartnerId",
                        "skillType": "LANGUAGE",
                        "channel": "AUDIO",
                        "name": "Test Skill",
                        "description": "This is a test skill created via automation",
                        "timeoutInSec": 30,
                        "timeoutSkillId": "timeoutSkillIdExample",
                        "timeoutPhoneNumber": "1234567890",
                        "countryCode": "US",
                        "languageId": "en",
                        "service": "ASL_OPERATOR"
                    }

                    response = requests.post(url, headers=headers, json=skill_data)

                    # Assert for success
                    assert response.status_code == 200, (
                        f"Failed to create skill: Status Code {response.status_code}, Response: {response.text}"
                    )

                    response_data = response.json()

                    # Assert that the skill name matches the input
                    assert response_data.get("name") == skill_data["name"], (
                        f"Skill name does not match: Expected {skill_data['name']}, Got {response_data.get('name')}"
                    )

                    print("Skill created successfully!", response_data)

                def update_skill():
                    skill_id = "aCM2i000000BiNxGAK"
                    url = f"https://cloudbreak-admin-api.dev.cloudbreak.us/v1/skills/{skill_id}"  #

                    skill_data = {
                        "microCallCenter": True,
                        "partnerId": "updatedPartnerId",
                        "skillType": "LANGUAGE",
                        "channel": "AUDIO",
                        "name": "Updated Skill Name",
                        "description": "This skill has been updated via automation",
                        "timeoutInSec": 60,
                        "timeoutSkillId": "updatedTimeoutSkillId",
                        "timeoutPhoneNumber": "0987654321",
                        "countryCode": "US",
                        "languageId": "en",
                        "service": "ASL_OPERATOR"
                    }

                    response = requests.put(url, headers=headers, json=skill_data)

                    # Assert for success
                    assert response.status_code == 200, (
                        f"Failed to update skill: Status Code {response.status_code}, Response: {response.text}"
                    )

                    response_data = response.json()

                    # Assert that the skill description matches the input
                    assert response_data.get("description") == skill_data["description"], (
                        f"Skill description does not match: Expected {skill_data['description']}, Got {response_data.get('description')}"
                    )

                    print("Skill updated successfully!", response_data)

                def test_get_admins():
                    base_url = "https://cloudbreak-admin-api.dev.cloudbreak.us/v1/admins"

                    params_success = {
                        "page": 1,
                        "limit": 20,
                        "orderBy": "lastName",
                        "orderType": "desc"
                    }
                    response = requests.get(base_url, headers=headers, params=params_success)
                    if response.status_code == 200:
                        data = response.json()
                        print("SUCCESS: Admins fetched successfully.")
                        print(f"Total admins: {data['total']}")
                    else:
                        print(
                            f"ERROR: Failed to fetch admins. Status code: {response.status_code}, Details: {response.text}")

                    #
                    response = requests.get(base_url, headers=headers)
                    if response.status_code == 401:
                        print("SUCCESS: Unauthorized access test passed. Status code 401 returned.")

                    params_filter = {
                        "page": 1,
                        "limit": 5,
                        "roles": ["CLOUDBREAK_ADMIN", "PARTNER_ADMIN"]
                    }
                    response = requests.get(base_url, headers=headers, params=params_filter)
                    if response.status_code == 200:
                        data = response.json()
                        roles_valid = all(
                            admin["role"] in ["CLOUDBREAK_ADMIN", "PARTNER_ADMIN"] for admin in data.get("results", [])
                        )
                        if roles_valid:
                            print("SUCCESS: Role filtering test passed.")
                            print(f"Filtered admins: {len(data.get('results', []))}")
                        else:
                            print("ERROR: Some admins do not match the filtered roles.")
                    else:
                        print(
                            f"ERROR: Role filtering test failed. Status code: {response.status_code}, Details: {response.text}")

                def manage_admins():
                    admin_data = {
                        "oktaLogin": "newadmin@example.com",
                        "firstName": "New",
                        "lastName": "Admin",
                        "email": "newadmin@example.com",
                        "mobilePhone": "123-456-7890",
                        "role": "PARTNER_ADMIN",
                        "partnerIds": ["aAH2i000000CezPGAS"]
                    }

                    #
                    post_url = f"{self.BASE_URL}/v1/admins"
                    print("Creating a new admin...")
                    post_response = requests.post(post_url, headers=headers, json=admin_data)

                    if post_response.status_code in (200, 201):
                        created_admin = post_response.json()
                        admin_id = created_admin.get("oktaId")
                        print("Admin created successfully:")
                    else:
                        print(f"Error creating admin: {post_response.status_code}, {post_response.text}")
                        return

                    #
                    delete_url = f"{self.BASE_URL}/v1/admins/{admin_id}"
                    print(f"Deactivating admin with ID: {admin_id}...")
                    delete_response = requests.delete(delete_url, headers=headers)

                    if delete_response.status_code == 200:
                        print(f"Admin with ID {admin_id} deactivated successfully.")
                    else:
                        print(f"Error deactivating admin: {delete_response.status_code}, {delete_response.text}")

                def update_admin():
                    url = f"{self.BASE_URL}/v1/admins/00u1dmyuvfWBY6THk1d7"
                    updated_data = {
                        "firstName": "UpdatedFirstName",
                        "lastName": "UpdatedLastName",
                        "email": "cypressuser@cloudbreak.us",
                        "mobilePhone": None,
                        "role": "CLOUDBREAK_ADMIN",
                        "partnerIds": ["aAH2i000000CezPGAS"]
                    }

                    response = requests.put(url, headers=headers, json=updated_data)
                    assert response.status_code == 200, f"Failed to update admin: {response.status_code}, {response.text}"

                    updated_admin = response.json()
                    assert updated_admin["email"] == updated_data["email"], "Admin email not updated correctly."
                    print("Admin updated successfully:", updated_admin)

                def get_admin_profile():
                    okta_id = "00u1dmyuvfWBY6THk1d7"
                    url = f"{self.BASE_URL}/v1/admins/{okta_id}/profile"
                    print(f"Fetching profile for admin with ID: {okta_id}...")
                    response = requests.get(url, headers=headers)

                    if response.status_code == 200:
                        admin_profile = response.json()
                        print("Admin profile fetched successfully:")
                        return admin_profile
                    elif response.status_code == 404:
                        print(f"Admin with ID {okta_id} not found.")
                    elif response.status_code == 401:
                        print("Unauthorized request. Check your access token.")
                    else:
                        print(f"Error fetching admin profile: {response.status_code}, {response.text}")

                def fetch_agents(page=1, limit=20, search=None, order_by="lastName", order_type="desc", roles=None,
                                 statuses=None, partner_id=None, vendor_id=None):
                    url = f"{self.BASE_URL}/v1/agents"
                    params = {
                        "page": page,
                        "limit": limit,
                        "search": search,
                        "orderBy": order_by,
                        "orderType": order_type,
                        "partnerId": partner_id,
                        "vendorId": vendor_id,
                    }

                    if roles:
                        params["roles"] = roles
                    if statuses:
                        params["statuses"] = statuses

                    response = requests.get(url, headers=headers, params=params)
                    assert response.status_code == 200, f"Failed to fetch agents: {response.status_code}, {response.text}"

                    agents = response.json()
                    assert "results" in agents, "Key 'results' not found in response."
                    assert isinstance(agents["results"], list), "Agents 'results' is not a list."
                    print("Agents fetched successfully.")
                    return agents

                def create_agent(page=1, limit=1, search=None, order_by="lastName", order_type="desc", partner_id=None):
                    # Fetch existing agents
                    agents = fetch_agents(
                        page=page,
                        limit=limit,
                        search=search,
                        order_by=order_by,
                        order_type=order_type,
                        partner_id=partner_id
                    )

                    # Assert at least one agent exists
                    assert agents and "results" in agents and len(
                        agents["results"]) > 0, "No agents found to copy data from."

                    source_agent = agents["results"][0]
                    print("Source agent data:", source_agent)

                    # Generate unique details for new agent
                    unique_suffix = uuid.uuid4().hex[:8]
                    unique_email = f"test.{unique_suffix}@example.com"
                    unique_interpreter_number = f"A-{unique_suffix}"

                    new_agent_payload = {
                        "firstName": f"{source_agent['firstName']}_new_{unique_suffix}",
                        "lastName": f"{source_agent['lastName']}_new_{unique_suffix}",
                        "email": unique_email,
                        "birthDate": source_agent.get("birthDate", "1990-01-01"),
                        "partnerId": source_agent.get("partnerId", partner_id),
                        "microCallCenter": source_agent.get("microCallCenter", True),
                        "isAudioOnly": source_agent.get("isAudioOnly", False),
                        "gender": source_agent.get("gender", "M"),
                        "phoneNumber": source_agent.get("phoneNumber", "1234567890"),
                        "allowQueueActivation": source_agent.get("allowQueueActivation", True),
                        "isOktaUser": source_agent.get("isOktaUser", True),
                        "role": source_agent.get("role", "SUPERVISOR"),
                        "interpreterLanguageIds": [str(lang) for lang in source_agent.get("interpreterLanguages", [])],
                        "interpreterNumber": unique_interpreter_number,
                        "vendorId": source_agent.get("vendorId"),
                    }

                    print("New agent payload:", new_agent_payload)

                    # Create new agent
                    url = f"{self.BASE_URL}/v1/agents"
                    response = requests.post(url, headers=headers, json=new_agent_payload)

                    # Assert successful agent creation
                    assert response.status_code == 201, f"Failed to create agent: {response.status_code}, {response.text}"

                    created_agent = response.json()
                    print("New agent created successfully:", created_agent)

                    # Update the created agent
                    agent_id = created_agent["id"]
                    updated_data = {
                        "firstName": f"{created_agent['firstName']}_updated",
                        "lastName": f"{created_agent['lastName']}_updated",
                        "email": f"updated_{created_agent['email']}",
                        "birthDate": created_agent.get("birthDate", "1984-05-29"),
                        "phoneNumber": "9876543210",
                        "role": "SUPERVISOR",
                        "gender": "F",
                        "allowQueueActivation": created_agent.get("allowQueueActivation", True),
                        "isAudioOnly": created_agent.get("isAudioOnly", False),
                        "status": "Active",
                        "interpreterLanguageIds": [str(lang) for lang in created_agent.get("interpreterLanguages", [])],
                    }

                    update_url = f"{self.BASE_URL}/v1/agents/{agent_id}"
                    print(f"Updating agent with ID: {agent_id}...")
                    print("Update payload:", updated_data)

                    update_response = requests.put(update_url, headers=headers, json=updated_data)

                    # Assert successful agent update
                    assert update_response.status_code == 200, f"Failed to update agent: {update_response.status_code}, {update_response.text}"

                    updated_agent = update_response.json()
                    print("Agent updated successfully:", updated_agent)

                    return updated_agent

                def test_get_agent_by_id():
                    #
                    agent_id = "aAUO3000000TbPBOA0"  #
                    url = f"{self.BASE_URL}/v1/agents/{agent_id}"

                    print(f"Testing GET {url}")

                    #
                    params = {
                        "withLanguages": "false"  #
                    }

                    #
                    response = requests.get(url, headers=headers, params=params)

                    #
                    if response.status_code == 200:
                        data = response.json()
                        print("Test passed: Agent fetched successfully.")

                        #
                        assert "id" in data, "Agent ID is missing in the response."
                        assert data["id"] == agent_id, f"Expected agent ID {agent_id}, got {data['id']}."
                        assert "firstName" in data, "Agent firstName is missing in the response."
                        assert "lastName" in data, "Agent lastName is missing in the response."
                        assert "status" in data and data["status"] == "Active", "Agent status is not Active."
                    else:
                        print(f"Test failed: Unexpected response status {response.status_code}")

                        #
                        if response.status_code == 400:
                            print("Error 400: Bad request - Check the query parameters or request format.")
                        elif response.status_code == 401:
                            print("Error 401: Unauthorized - Check your API token.")
                        elif response.status_code == 404:
                            print(f"Error 404: Agent with ID {agent_id} not found.")
                        else:
                            print(f"Unexpected error: {response.status_code}, {response.text}")

                def test_get_agent_queues():
                    agent_id = "aAUO3000000TbPBOA0"
                    url = f"{self.BASE_URL}/v1/agents/{agent_id}/queues"

                    print(f"Testing GET {url}")

                    #
                    response = requests.get(url, headers=headers)

                    #
                    if response.status_code == 200:
                        data = response.json()
                        print("Test passed: Queues fetched successfully.")
                        #
                        assert "activeQueues" in data, "Missing 'activeQueues' in response"
                        assert "availableQueues" in data, "Missing 'availableQueues' in response"

                        #
                        active_queues = data["activeQueues"]
                        if active_queues:
                            print(f"Active queues found: {len(active_queues)}")
                            for queue in active_queues:
                                assert "id" in queue, "Missing 'id' in activeQueue"
                                assert "name" in queue, "Missing 'name' in activeQueue"
                                assert "channel" in queue, "Missing 'channel' in activeQueue"
                            print("Active queues data is valid.")
                        else:
                            print("No active queues found for the agent.")

                        #
                        available_queues = data["availableQueues"]
                        if available_queues:
                            print(f"Available queues found: {len(available_queues)}")
                            for queue in available_queues:
                                assert "id" in queue, "Missing 'id' in availableQueue"
                                assert "name" in queue, "Missing 'name' in availableQueue"
                                assert "channel" in queue, "Missing 'channel' in availableQueue"
                            print("Available queues data is valid.")
                        else:
                            print("No available queues found for the agent.")

                    else:
                        #
                        print(f"Test failed: Unexpected status code {response.status_code}")

                        #
                        if response.status_code == 400:
                            print("Error 400: Bad Request - Проверьте параметры запроса.")
                        elif response.status_code == 401:
                            print("Error 401: Unauthorized - Проверьте токен доступа.")
                        elif response.status_code == 404:
                            print(f"Error 404: Agent with ID {agent_id} not found.")
                        else:
                            print(f"Unexpected error: {response.status_code}, {response.text}")

                def test_update_agent_active_queues():
                    agent_id = "aAUO3000000TbPBOA0"
                    active_queues = ["aAi2i000000ChBhCAK"]  #
                    url = f"{self.BASE_URL}/v1/agents/{agent_id}/active-queues"
                    payload = {
                        "activeQueues": active_queues
                    }

                    response = requests.put(url, headers=headers, json=payload)

                    print(f"Response Status Code: {response.status_code}")

                    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

                    #
                    response_data = response.json()
                    assert "activeQueues" in response_data, "Response does not contain 'activeQueues'"
                    updated_queues = response_data["activeQueues"]
                    assert len(updated_queues) == len(active_queues), "Mismatch in the number of updated queues"

                    for queue_id in active_queues:
                        assert any(queue["id"] == queue_id for queue in
                                   updated_queues), f"Queue ID {queue_id} not found in response"

                    print(f"Test passed for agent_id: {agent_id} with active_queues: {active_queues}")

                def test_reset_agent_password():
                    agent_id = "aAUO3000000TbPBOA0"
                    url = f"{self.BASE_URL}/v1/agents/{agent_id}/reset-password"

                    response = requests.post(url, headers=headers)  #

                    #
                    print(f"Response Status Code: {response.status_code}")

                    #
                    assert response.status_code == 204, f"Expected 204, got {response.status_code}"

                    print(f"Password reset successfully for agent ID: {agent_id}")

                def reset_agent_presence():
                    agent_id = "aAUO3000000TbPBOA0"
                    url = f"{self.BASE_URL}/v1/agents/{agent_id}/reset-presence"

                    response = requests.put(url, headers=headers)
                    assert response.status_code == 204, f"Failed to reset agent presence: {response.status_code}, {response.text}"
                    print(f"Agent presence reset successfully for agent ID: {agent_id}")

                def change_agent_password():
                    agent_id = "aAUO3000000TbPBOA0"
                    url = f"{self.BASE_URL}/v1/agents/{agent_id}/change-password"
                    payload = {"password": "NewSecurePassword123!"}

                    response = requests.post(url, headers=headers, json=payload)
                    assert response.status_code == 204, f"Failed to change password: {response.status_code}, {response.text}"
                    print(f"Password changed successfully for agent ID: {agent_id}")

                def get_scripts():
                    url = f"{self.BASE_URL}/v1/scripts"

                    response = requests.get(url, headers=headers)
                    assert response.status_code == 200, f"Failed to fetch scripts: {response.status_code}, {response.text}"

                    scripts = response.json()
                    assert isinstance(scripts, list), "Scripts response is not a list."
                    assert len(scripts) > 0, "Scripts list is empty."
                    print("Scripts retrieved successfully.")
                    return scripts

                def handle_scripts():
                    #
                    SCRIPT_ID = "72bd0fdd-2355-4e41-976c-1528d99d5cea"
                    SCRIPT_PG_ID = "aCM2i000000BiNxGAK"
                    NEW_ORDER = 2  #
                    SCRIPT_TYPE = "Technical Issues"  #
                    SCRIPT_TEXT = "Sample text for the script."  #

                    try:
                        #
                        fetch_url = f"{self.BASE_URL}/v1/scripts/{SCRIPT_ID}"
                        params = {"scriptPgId": SCRIPT_PG_ID}
                        fetch_response = requests.get(fetch_url, headers=headers, params=params)

                        if fetch_response.status_code == 200:
                            script_data = fetch_response.json()
                            print(f"Script fetched successfully")
                        else:
                            print(f"Failed to fetch script. Status code: {fetch_response.status_code}")
                            print(fetch_response.json())

                        #
                        create_url = f"{self.BASE_URL}/v1/scripts"
                        create_payload = {
                            "type": SCRIPT_TYPE,
                            "text": SCRIPT_TEXT,
                            "order": NEW_ORDER
                        }
                        create_response = requests.post(create_url, headers=headers, json=create_payload)

                        if create_response.status_code == 201:
                            print(f"Script created successfully")
                        else:
                            print(f"Failed to create script. Status code: {create_response.status_code}")
                            print(create_response.json())

                        #
                        update_url = f"{self.BASE_URL}/v1/scripts"
                        update_payload = {
                            "updates": [
                                {
                                    "id": SCRIPT_ID,
                                    "order": NEW_ORDER
                                }
                            ]
                        }

                        update_response = requests.put(update_url, headers=headers, json=update_payload)

                        if update_response.status_code == 200:
                            print(f"Script order updated successfully")
                        else:
                            print(f"Failed to update script order. Status code: {update_response.status_code}")
                            print(update_response.json())

                    except Exception as e:
                        print(f"An error occurred: {e}")

                def test_update_script():
                    BASE_URL = "https://your-api-url.com"
                    SCRIPT_PG_ID = "aCM2i000000BiNxGAK"
                    UPDATED_TYPE = "Updated Type"
                    UPDATED_TEXT = "Updated text for the script."

                    url = f"{BASE_URL}/v1/scripts/{SCRIPT_PG_ID}"
                    payload = {"type": UPDATED_TYPE, "text": UPDATED_TEXT}

                    print("Updating script...")
                    response = requests.put(url, headers=headers, json=payload)

                    assert response.status_code == 200, f"Failed to update script: {response.status_code}, {response.text}"

                    try:
                        response_data = response.json()
                        assert response_data["type"] == UPDATED_TYPE, "Script type was not updated correctly."
                        assert response_data["text"] == UPDATED_TEXT, "Script text was not updated correctly."
                        print("Script updated successfully:", response_data)
                    except ValueError:
                        assert False, "Response is not in JSON format."

                def test_delete_script():
                    pgId = "aCM2i000000BiNxGAK"
                    url = f"https://your-api-url.com/v1/scripts/{pgId}"

                    response = requests.delete(url, headers=headers, allow_redirects=False)

                    assert response.status_code == 200, f"Failed to delete script: {response.status_code}, {response.text}"

                    try:
                        response_data = response.json()
                        assert "success" in response_data, "Response JSON does not indicate success."
                        print("Script deleted successfully:", response_data)
                    except ValueError:
                        assert False, "Response is not in JSON format."


                def test_create_queue():
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    CREATE_QUEUE_ENDPOINT = "/v1/queues"
                    url = BASE_URL + CREATE_QUEUE_ENDPOINT

                    language_id = "aAX2i0000008POWGA2"
                    timeout_queue_id = "aAi2i000000ChBhCAK"
                    partner_id = "aAH2i000000CezPGAS"

                    payload = {
                        "name": "Test Queue",
                        "type": "LANGUAGE",
                        "service": "OPERATOR",
                        "description": "Queue for testing purposes",
                        "timeoutInSeconds": 30,
                        "languageId": language_id,
                        "channel": "VIDEO",
                        "timeoutQueueId": timeout_queue_id,
                        "timeoutPhoneNumber": "1234567890",
                        "partnerId": partner_id,
                        "microCallCenter": True,
                        "user": "AGENT"
                    }

                    print("Sending POST request to create a queue...")
                    print("Request URL:", url)

                    response = requests.post(url, headers=headers, json=payload)

                    print("Response Status Code:", response.status_code)

                    assert response.status_code == 200, f"Failed to create queue: {response.status_code}, Response: {response.text}"

                    response_data = response.json()

                    assert "id" in response_data, "Response missing 'id' field."
                    assert response_data["name"] == payload["name"], "Queue name does not match the payload."

                    print(f"POST test passed. Queue created successfully with ID: {response_data['id']}.")

                def test_get_queue():
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    QUEUE_ENDPOINT = "/v1/queues"
                    queue_id = "aAi2i000000Ch9zCAC"
                    url = f"{BASE_URL}{QUEUE_ENDPOINT}/{queue_id}"

                    print("Sending GET request to fetch queue details...")
                    print("Request URL:", url)

                    response = requests.get(url, headers=headers)

                    print("Response Status Code:", response.status_code)

                    assert response.status_code == 200, f"Failed to fetch queue details: {response.status_code}, Response: {response.text}"

                    response_data = response.json()

                    assert "id" in response_data, "Response missing 'id' field."
                    assert "name" in response_data, "Response missing 'name' field."
                    assert "createdDate" in response_data, "Response missing 'createdDate' field."
                    assert "lastModifiedDate" in response_data, "Response missing 'lastModifiedDate' field."
                    assert "type" in response_data, "Response missing 'type' field."
                    assert "channel" in response_data, "Response missing 'channel' field."

                    assert response_data[
                               "id"] == queue_id, f"Queue ID mismatch: expected {queue_id}, got {response_data['id']}"
                    assert response_data["channel"] in ["VIDEO", "AUDIO"], "Unexpected channel value."

                    print("Test passed. Queue details fetched successfully.")

                def test_update_queue():
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    QUEUE_ENDPOINT = "/v1/queues"
                    queue_id = "aAi2i000000Ch9zCAC"
                    url = f"{BASE_URL}{QUEUE_ENDPOINT}/{queue_id}"

                    payload = {
                        "name": "Updated Queue Name",
                        "type": "LANGUAGE",
                        "service": None,
                        "description": "Staff serving Zophei interpretation",
                        "timeoutInSeconds": 120,
                        "languageId": "aAX2i0000008PSAGA2",
                        "channel": "VIDEO",
                        "timeoutQueueId": "aAi2i000000ChBhCAK",
                        "timeoutPhoneNumber": None,
                        "partnerId": None,
                        "microCallCenter": False
                    }

                    print("Sending PUT request to update queue...")
                    print("Request URL:", url)

                    response = requests.put(url, headers=headers, json=payload)

                    print("Response Status Code:", response.status_code)

                    assert response.status_code == 200, f"Failed to update queue: {response.status_code}, Response: {response.text}"

                    response_data = response.json()

                    assert response_data["name"] == payload["name"], "Queue name not updated correctly."
                    assert response_data["description"] == payload[
                        "description"], "Queue description not updated correctly."
                    assert response_data["timeoutInSec"] == payload[
                        "timeoutInSeconds"], "Timeout not updated correctly."

                    print("Test passed. Queue updated successfully.")

                def test_delete_queue():
                    BASE_URL = "https://cloudbreak-admin-api.dev.cloudbreak.us"
                    QUEUE_ENDPOINT = "/v1/queues"
                    queue_id = "aAi2i000000ChB2CAK"
                    url = f"{BASE_URL}{QUEUE_ENDPOINT}/{queue_id}"

                    print("Sending DELETE request to delete queue...")
                    print("Request URL:", url)

                    response = requests.delete(url, headers=headers)

                    print("Response Status Code:", response.status_code)

                    assert response.status_code == 200, f"Failed to delete queue: {response.status_code}, Response: {response.text}"

                    print("Test passed. Queue deleted successfully.")

                methods = [
                    test_get_list_of_queues, ###TODO
                    test_get_list_of_queues, ###TODO
                    test_delete_queue, ###TODO
                    test_create_queue, ###TODO
                    test_update_partner_access_code, ###TODO
                    test_get_site_providers, ###TODO
                    test_update_department_languages, ###TODO
                    bulk_update_provider_specializations, ### Todo
                    reset_provider_password, ### Todo
                    create_skill, ### Todo
                    update_skill, ### Todo
                    create_agent, ### Todo
                    test_get_languages,
                    test_get_partners_list,
                    test_get_department,
                    test_update_department,
                    test_create_department,
                    test_create_access_code,
                    test_create_partner,
                    test_create_secret,
                    test_get_secret,
                    test_get_departments_list,
                    test_update_partner,
                    test_delete_partner,
                    test_get_partner_providers,
                    test_get_partner_sites,
                    test_get_partner_site,
                    test_create_and_delete_partner_access_code,
                    test_get_partner_access_codes,
                    test_get_partner_queues,
                    test_create_and_delete_language,
                    test_update_language,
                    test_get_language,
                    test_get_paginated_languages,
                    test_get_status,
                    test_get_queue,
                    test_update_queue,
                    test_get_providers,
                    fetch_create_and_delete_provider,
                    fetch_provider,
                    update_provider,
                    add_martti_to_provider,
                    change_provider_password,
                    get_specializations,
                    get_skills,
                    test_get_admins,
                    manage_admins,
                    update_admin,
                    get_admin_profile,
                    fetch_agents,
                    test_get_agent_by_id,
                    test_get_agent_queues,
                    test_update_agent_active_queues,
                    test_reset_agent_password,
                    reset_agent_presence,
                    change_agent_password,
                    get_scripts,
                    handle_scripts,
                    test_update_script,
                    test_delete_script,
                ]

                # Закомментированные методы
                skipped_methods = [

                ]

                print("\n--- Running Tests ---")
                results = []  # Для хранения результатов выполнения

                # Выполнение методов
                for method in methods + skipped_methods:
                    if not callable(method):  # Пропуск неактивных методов (из закомментированных)
                        continue

                    try:
                        print(f"Running {method.__name__}...")
                        method()  # Запуск метода
                        results.append((method.__name__, "PASSED"))
                    except AssertionError as e:
                        # Обработка ошибок с провалившимся assert
                        print(f"Test {method.__name__} FAILED: {str(e)}")
                        results.append((method.__name__, f"FAILED: {str(e)}"))
                    except Exception as e:
                        # Обработка любых других ошибок
                        print(f"Test {method.__name__} ERRORED: {str(e)}")
                        results.append((method.__name__, f"ERRORED: {str(e)}"))

                # Итоговые результаты
                print("\n--- Test Results ---")
                for name, status in results:
                    print(f"{name}: {status}")

                # Вывод списка пропущенных методов
                if skipped_methods:
                    print("\n--- Skipped Tests ---")
                    for method in skipped_methods:
                        print(f"{method.__name__} (TODO or inactive)")

                return token
            else:
                print("Token found, but 'idToken' key is missing.")
        else:
            print("Token could not be found in local storage.")
        return None


if __name__ == "__main__":
    driver_instance = Login_page_martii.driver()
    login_page = Login_page_martii(driver_instance)

    token = login_page.authorization()

    driver_instance.quit()
