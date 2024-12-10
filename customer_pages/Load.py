import time
import pytest
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import threading
from selenium.common.exceptions import TimeoutException
<<<<<<< HEAD
from ev import EV


=======

users = [
    {'Email': 'adam1.worman@voyceglobal.com'},
    {'Email': 'adriana1.quintero@voyceglobal.com'},
    {'Email': 'aldo1.lorenzo@voyceglobal.com'},
    {'Email': 'ana1.maria.mejia@voyceglobal.com'},
    {'Email': 'aurelio1.adames@voyceglobal.com'},
    {'Email': 'autumn1.adams@voyceglobal.com'},
    {'Email': 'axelle1.augustin@voyceglobal.com'},
    {'Email': 'byron1.miller@voyceglobal.com'},
    {'Email': 'carlos1.alvarado@voyceglobal.com'},
    {'Email': 'carrie1.chen@voyceglobal.com'},
    {'Email': 'cecilia1.baqueiro@voyceglobal.com'},
    {'Email': 'christian1.cantabrana@voyceglobal.com'},
    {'Email': 'juan.carrillo@voyceglobal.com'},
    {'Email': 'claudia1.altamirano@voyceglobal.com'},
    {'Email': 'dania1.juarez@voyceglobal.com'},
    {'Email': 'daniel1.pirestani@voyceglobal.com'},
    {'Email': 'daniela1.rodriguez@voyceglobal.com'},
    {'Email': 'debela1.chali@voyceglobal.com'},
    {'Email': 'ehno1.paw@voyceglobal.com'},
    {'Email': 'elizabeth1.rosas@voyceglobal.com'},
    {'Email': 'elzebir1.delcid@voyceglobal.com'},
    {'Email': 'ghada1.mohsen@voyceglobal.com'},
    {'Email': 'gloria1.alvarez@voyceglobal.com'},
    {'Email': 'jean1.sarlat@voyceglobal.com'},
    {'Email': 'jeremy1.waiser@voyceglobal.com'},
    {'Email': 'jessica1.pollock@voyceglobal.com'},
    {'Email': 'jonathan1.scott@voyceglobal.com'},
    {'Email': 'juan1.carrillo@voyceglobal.com'},
    {'Email': 'adam.worman@voyceglobal.com'},
    {'Email': 'adriana.quintero@voyceglobal.com'},
    {'Email': 'aldo.lorenzo@voyceglobal.com'},
    {'Email': 'ana.maria.mejia@voyceglobal.com'},
    {'Email': 'aurelio.adames@voyceglobal.com'},
    {'Email': 'autumn.adams@voyceglobal.com'},
    {'Email': 'axelle.augustin@voyceglobal.com'},
    {'Email': 'byron.miller@voyceglobal.com'},
    {'Email': 'carlos.alvarado@voyceglobal.com'},
    {'Email': 'carrie.chen@voyceglobal.com'},
    {'Email': 'cecilia.baqueiro@voyceglobal.com'},
    {'Email': 'christian.cantabrana@voyceglobal.com'},
    {'Email': 'maria1.rivera@voyceglobal.com'},
    {'Email': 'claudia.altamirano@voyceglobal.com'},
    {'Email': 'dania.juarez@voyceglobal.com'},
    {'Email': 'daniel.pirestani@voyceglobal.com'},
    {'Email': 'daniela.rodriguez@voyceglobal.com'},
    {'Email': 'debela.chali@voyceglobal.com'},
    {'Email': 'ehno.paw@voyceglobal.com'},
    {'Email': 'kevin.sillas@voyceglobal.com'},
    {'Email': 'martin1.cedeno@voyceglobal.com'},
    {'Email': 'matthew1.dong@voyceglobal.com'},
    {'Email': 'mauricio1.iragorri@voyceglobal.com'},
    {'Email': 'mayra1.morante@voyceglobal.com'},
    {'Email': 'mesac1.cleus@voyceglobal.com'},
    {'Email': 'monitordisplay1.@weyimobile.com'},
    {'Email': 'naing1.ayar@voyceglobal.com'},
    {'Email': 'natalia1.schell@voyceglobal.com'},
    {'Email': 'ning1.hu@voyceglobal.com'},
    {'Email': 'okon1.gordon@voyceglobal.com'},
    {'Email': 'olga1.bedoya@voyceglobal.com'},
    {'Email': 'pascal1.concepcion@voyceglobal.com'},
    {'Email': 'patrick1.faroul@voyceglobal.com'},
    {'Email': 'paula1.cassiano@voyceglobal.com'},
    {'Email': 'christian1.gloverwilson@voyceglobal.com'},
    {'Email': 'kevin1.sillas@voyceglobal.com'},
    {'Email': 'laura1.keylon@voyceglobal.com'},
    {'Email': 'leidy1.ocampo@voyceglobal.com'},
    {'Email': 'maria1.belen@voyceglobal.com'},
    {'Email': 'maria1.jalil@voyceglobal.com'},
    {'Email': 'marianne1.bustamante@voyceglobal.com'}
]
>>>>>>> 51a303e (Initial commit)

response_times = []

def assert_url(driver, expected_url, timeout=30):
    """Проверка текущего URL с ожиданием."""
    try:
        WebDriverWait(driver, timeout).until(lambda driver: driver.current_url == expected_url)
        print("URL is correct:", driver.current_url)
    except TimeoutException:
        get_url = driver.current_url
        assert False, f"Expected URL '{expected_url}', but got '{get_url}'"

def assert_is_number(driver, xpath):
    """Проверка, что текст элемента является числом и больше нуля."""
    element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    text = element.text.replace(',', '')  # Удаляем запятые перед проверкой
    assert text.isdigit() and int(text) > 0, f"Expected a number greater than zero, but got '{text}'"
    print("The text is a number greater than zero:", text)

def click_elements_in_table(driver, index):
    """Click on a specific element in a table based on the given index."""
    xpath = f'//*[@id="All-terp-table"]/div/div/table/tbody/tr[{index}]/td[1]/button'
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        print(f"Clicked on element {index}")

        # Check for the target element
        target_xpath = '//*[@id="button-join"]'
        try:
            target_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, target_xpath)))
            print("Target element detected, stopping.")
            return  # Exit the function as the target element is found
        except TimeoutException:
            print("Target element not found, continuing.")
            return

    except TimeoutException:
        print(f"Failed to click on element {index}")

def run_authorization(driver_path, url, email, password, index, visible=False):
    chrome_options = Options()
    chrome_options.binary_location = '/Users/nikitabarshchuk/chrome/mac_arm-126.0.6478.63/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
    if not visible:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2
    })

    service = ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "email"))).send_keys(email)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)



        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Sign In"]]'))
        ).click()
        time.sleep(10)

        start_time = time.time()
        start_time_str = time.strftime("%H:%M:%S", time.localtime(start_time))
        print(f"Login action started at {start_time_str} for user {index}")
        try:
            force_login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//*[@id='root']/section/section/main/div/div/div/div/div[2]/div/div[2]/div[1]/div"))
            )
            force_login_btn.click()
            print(f"Clicked on 'Force Login' for user {index}")
        except TimeoutException:
            print(f"No 'Force Login' button to click for user {index}")

        click_elements_in_table(driver, index)

        # Measure the end time
        end_time = time.time()
        end_time_str = time.strftime("%H:%M:%S", time.localtime(end_time))
        print(f"Action ended at {end_time_str} for user {index}")

        response_time = end_time - start_time
        print(f"Response time for action: {response_time} for user {index}")

        # Append the response time to the list with user email and time strings
        response_times.append(
            {'email': email, 'response_time': response_time, 'start_time': start_time_str, 'end_time': end_time_str, 'index': index})

        time.sleep(400)

    finally:
        driver.quit()

def test_parallel_authorizations():
    """Запуск многопоточной авторизации."""
    url = 'https://staging.admin.vip.voyceglobal.com/auth/login'
    password = 'Admin@2'
<<<<<<< HEAD
    driver_path = '/chromedriver'
    users = EV.users
=======
    driver_path = '/Users/nikitabarshchuk/PycharmProjects/pythonProject3/chromedriver'
>>>>>>> 51a303e (Initial commit)

    threads = []
    for i, user in enumerate(users):
        email = user['Email']
        index = i + 1  # Уникальный индекс для каждого пользователя
        thread = threading.Thread(target=run_authorization,
                                  args=(
                                  driver_path, url, email, password, index, False))  # Использование headless режима
        threads.append(thread)
        thread.start()
        time.sleep(3)

    for thread in threads:
        thread.join()

    # Plot the response times after all threads are finished
    plot_response_times(response_times)

    # Print detailed report
    print_detailed_report(response_times)

def plot_response_times(response_times):
    """Функция для построения графика времени отклика."""
    emails = [entry['email'] for entry in response_times]
    times = [entry['response_time'] for entry in response_times]

    plt.figure(figsize=(15, 7))
    plt.plot(emails, times, marker='o')
    plt.xlabel('User Email')
    plt.ylabel('Response Time (seconds)')
    plt.title('Response Times for Users')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('response_times.png')
    plt.show()

def print_detailed_report(response_times):
    """Функция для вывода подробного отчета."""
    for entry in response_times:
        print(f"User {entry['index']}:")
        print(f"  Email: {entry['email']}")
        print(f"  Start Time: {entry['start_time']}")
        print(f"  End Time: {entry['end_time']}")
        print(f"  Response Time: {entry['response_time']} seconds")
        print("")

if __name__ == "__main__":
    test_parallel_authorizations()
