import sys
import os
import time
import pytest
import subprocess
import allure
import threading
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from env import EV

def ensure_dependencies():
    """
    Проверяет и устанавливает необходимые Python-зависимости.
    """
    try:
        import pkg_resources
        required = {'selenium', 'pytest', 'allure-pytest', 'requests'}
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed
        
        if missing:
            print("Обнаружены отсутствующие зависимости:", missing)
            print("Установка недостающих зависимостей...")
            import subprocess
            subprocess.check_call(["pip", "install"] + list(missing))
            print("Зависимости успешно установлены!")
        else:
            print("Все необходимые Python-зависимости уже установлены!")

        # Проверяем наличие ffmpeg
        try:
            subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True)
            print("ffmpeg уже установлен!")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ffmpeg не найден. Устанавливаем...")
            if sys.platform == "darwin":  # MacOS
                subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
            elif sys.platform == "linux":
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'], check=True)
            print("ffmpeg успешно установлен!")
            
    except Exception as e:
        print(f"Ошибка при установке зависимостей: {e}")
        raise

def start_screen_recording(output_path, display=":99", thread_id=None):
    """
    Запускает запись экрана
    :param output_path: путь для сохранения видео
    :param display: номер дисплея для записи
    :param thread_id: идентификатор потока (если есть)
    :return: процесс записи
    """
    suffix = f"_thread_{thread_id}" if thread_id else ""
    final_output_path = f"{output_path}{suffix}.mp4"
    
    # Команда для записи экрана через ffmpeg
    command = [
        "ffmpeg",
        "-f", "x11grab",  # захват X11 дисплея
        "-video_size", "1920x1080",  # разрешение записи
        "-framerate", "30",  # частота кадров
        "-i", display,  # источник видео (дисплей)
        "-c:v", "libx264",  # кодек
        "-preset", "ultrafast",  # предустановка для быстрой записи
        "-y",  # перезаписывать файл если существует
        final_output_path
    ]
    
    print(f"Запуск записи экрана для потока {thread_id if thread_id else 'основной'}")
    print(f"Команда записи: {' '.join(command)}")
    
    process = subprocess.Popen(command)
    return process, final_output_path

def stop_screen_recording(process):
    """
    Останавливает запись экрана.
    """
    if process:
        print("\nОстанавливаем запись экрана...")
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
            print("Вывод ffmpeg:")
            print(stdout.decode() if stdout else "Нет вывода stdout")
            if stderr:
                print("Ошибки ffmpeg:")
                print(stderr.decode())
        except subprocess.TimeoutExpired:
            print("Процесс записи не завершился вовремя, принудительно завершаем...")
            process.kill()
            process.communicate()
        print("Запись экрана завершена")

@pytest.fixture(scope="function")
def screen_recorder(request):
    """
    Фикстура для записи видео теста с поддержкой нескольких потоков
    """
    # Создаем директорию если не существует
    os.makedirs("test_videos", exist_ok=True)
    
    # Генерируем базовое имя файла
    test_name = request.node.name
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    base_video_path = os.path.join("test_videos", f"{test_name}_{timestamp}")
    
    # Словарь для хранения процессов записи и путей к файлам
    recordings = {}
    
    def start_recording(thread_id=None):
        """Начинает запись для конкретного потока"""
        process, video_path = start_screen_recording(base_video_path, thread_id=thread_id)
        recordings[thread_id] = {"process": process, "path": video_path}
        return process
    
    def stop_recording(thread_id=None):
        """Останавливает запись для конкретного потока"""
        if thread_id in recordings:
            process = recordings[thread_id]["process"]
            stop_screen_recording(process)
            video_path = recordings[thread_id]["path"]
            if os.path.exists(video_path):
                print(f"Видео для потока {thread_id} записано успешно: {video_path}")
                allure.attach.file(
                    video_path,
                    name=f"{test_name}_thread_{thread_id}_recording.mp4",
                    attachment_type=allure.attachment_type.MP4
                )
            else:
                print(f"Ошибка: видео для потока {thread_id} не было создано: {video_path}")
    
    # Запускаем запись основного потока
    start_recording()
    
    # Возвращаем функции для управления записью
    yield {
        "start_recording": start_recording,
        "stop_recording": stop_recording
    }
    
    # Останавливаем все записи
    for thread_id in list(recordings.keys()):
        stop_recording(thread_id)

def download_video():
    """
    Скачивает тестовое видео для использования в тестах.
    """
    video_url = "https://drive.usercontent.google.com/u/0/uc?id=1Rv3Qitap2wANEx0I-7NLvSp1cEQlE6_K&export=download"
    video_path = os.path.join(os.getcwd(), "output.y4m")
    
    if os.path.exists(video_path):
        print("Видео файл уже существует, пропускаем скачивание.")
        return video_path
        
    print("Начинаем скачивание тестового видео...")
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0
        
        with open(video_path, 'wb') as file:
            for data in response.iter_content(block_size):
                downloaded += len(data)
                file.write(data)
                progress = int((downloaded / total_size) * 100)
                print(f"\rПрогресс скачивания: {progress}%", end='')
                
        print("\nВидео успешно скачано!")
        return video_path
    except Exception as e:
        print(f"Ошибка при скачивании видео: {e}")
        raise

def install_browser_and_driver():
    installation_path = os.path.join(os.getcwd(), "chrome_installation")
    os.makedirs(installation_path, exist_ok=True)
    try:
        print("Installing Chrome...")
        result = subprocess.run(
            ["npx", "@puppeteer/browsers", "install", "chrome@stable", "--path", installation_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print("Chrome installed successfully!")
        
        # Извлекаем версию Chrome из вывода команды
        import re
        version_match = re.search(r'chrome@(\d+\.\d+\.\d+\.\d+)', result.stdout)
        if not version_match:
            raise Exception("Could not determine Chrome version from installation output")
        chrome_version = version_match.group(1)

        # Определяем операционную систему
        import platform
        system = platform.system().lower()
        
        if system == "darwin":
            # Mac OS X path
            chrome_binary_path = os.path.join(
                installation_path, "chrome", f"mac_arm-{chrome_version}",
                "chrome-mac-arm64", "Google Chrome for Testing.app", 
                "Contents", "MacOS", "Google Chrome for Testing"
            )
        elif system == "linux":
            # Linux path
            chrome_binary_path = os.path.join(
                installation_path, "chrome", f"linux-{chrome_version}",
                "chrome-linux64", "chrome"
            )
        else:
            raise OSError(f"Unsupported operating system: {system}")

        if not os.path.exists(chrome_binary_path):
            raise FileNotFoundError(f"Chrome binary not found at {chrome_binary_path}")
        print(f"Chrome binary found at: {chrome_binary_path}")

        print("Fetching Chrome version...")
        version_output = subprocess.run([chrome_binary_path, "--version"], capture_output=True, text=True, check=True)
        chrome_version = version_output.stdout.strip().split(" ")[-1]
        print(f"Installed Chrome version: {chrome_version}")
        print(f"Installing ChromeDriver for version {chrome_version}...")
        subprocess.run(
            ["npx", "@puppeteer/browsers", "install", f"chromedriver@{chrome_version}", "--path", installation_path],
            check=True
        )
        print("ChromeDriver installed successfully!")

        if system == "darwin":
            chromedriver_path = os.path.join(
                installation_path, "chromedriver", f"mac_arm-{chrome_version}",
                "chromedriver-mac-arm64", "chromedriver"
            )
        elif system == "linux":
            chromedriver_path = os.path.join(
                installation_path, "chromedriver", f"linux-{chrome_version}",
                "chromedriver-linux64", "chromedriver"
            )

        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")
        return chrome_binary_path, chromedriver_path
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during installation: {e}")
        raise

@pytest.fixture(scope="function")
def driver():
    chrome_path, chromedriver_path = install_browser_and_driver()
    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Настройки для виртуальной камеры и live‑трансляции
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    video_path = os.path.join(os.getcwd(), "output.y4m")
    print(f"Using video file for fake camera: {video_path}")
    chrome_options.add_argument(f"--use-file-for-fake-video-capture={video_path}")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.media_stream_mic": 1
    })
    driver_service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    yield driver
    driver.quit()

@allure.feature("Video Call Testing")
@allure.story("Checking video call activation via UI with virtual camera, camera & microphone toggle")
def test_video_call_activation(driver, screen_recorder):
    """
    Тест проверяет активацию видеозвонка через пользовательский интерфейс
    с использованием виртуальной камеры и переключением камеры/микрофона.
    Каждый браузер записывается в отдельный видеофайл.
    """
    with allure.step("Начинаем тестирование видеозвонка"):
        # Скачиваем видео перед началом теста
        video_path = download_video()
        print(f"Используем видео файл: {video_path}")

        def open_agent_browser():
            # Начинаем запись для агентского браузера
            screen_recorder["start_recording"]("agent")
            
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service as ChromeService
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            chrome_path, chromedriver_path = install_browser_and_driver()
            options = Options()
            options.binary_location = chrome_path
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--use-fake-device-for-media-stream")
            options.add_argument("--use-fake-ui-for-media-stream")
            video_path = download_video()  # Используем скачанное видео
            print(f"Using video file for fake camera: {video_path}")
            options.add_argument(f"--use-file-for-fake-video-capture={video_path}")
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.media_stream_mic": 1
            })

            agent_driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=options)
            
            # Логин в агентском браузере
            agent_driver.get(EV.AGENT_URL)
            print("Agent browser opened login page")
            email_field = WebDriverWait(agent_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input28"))
            )
            email_field.clear()
            email_field.send_keys(EV.AGENT_LOGIN)
            print("Email entered")
            password_field = WebDriverWait(agent_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input36"))
            )
            password_field.clear()
            password_field.send_keys(EV.AGENT_PASSWORD)
            print("Password entered")
            sign_in_button = WebDriverWait(agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Sign in']"))
            )
            sign_in_button.click()
            print("Sign in button clicked")
            time.sleep(2)

            # Выбор статуса "Available"
            status_select = WebDriverWait(agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='status']"))
            )
            status_select.click()
            time.sleep(2)
            print("Status select opened")
            available_option = WebDriverWait(agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='status']/option[@value='Available']"))
            )
            available_option.click()
            time.sleep(1)
            
            # Клик по зелёному кружку
            green_icon = WebDriverWait(agent_driver, 30).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.flex.justify-center.items-center.rounded-full.mx-auto.ring-2.h-14.w-14.ring-green-500.group-hover\\:bg-green-200.group-focus\\:bg-green-200")
                )
            )
            ActionChains(agent_driver).move_to_element(green_icon).click().perform()
            print("Green circle element clicked!")
            

            try:
                video_count = agent_driver.execute_script("return document.querySelectorAll('video').length;")
                print("Number of <video> elements on page:", video_count)
                print(f"Found {video_count} video elements")
                return agent_driver
            except Exception as e:
                print(f"Error in open_agent_browser: {e}")
                screen_recorder["stop_recording"]("agent")
                raise

        def open_client_browser():
            # Начинаем запись для клиентского браузера
            screen_recorder["start_recording"]("client")
            
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service as ChromeService
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            chrome_path, chromedriver_path = install_browser_and_driver()
            options = Options()
            options.binary_location = chrome_path
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.media_stream_mic": 1
            })

            client_driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=options)

            # Логика для клиента
            from LOGIN import Login_page
            login_page = Login_page(client_driver)
            login_page.login_to_cloudbreak_customer()
            try:
                client_driver.execute_cdp_cmd("Browser.setPermission", {
                    "origin": "https://cloudbreak-customer-ui.qa.cloudbreak.us/home",
                    "permission": {"name": "microphone"},
                    "setting": "denied"
                })
                print("Microphone usage has been disabled for the driver.")
            except Exception as e:
                print("Error disabling microphone usage:", e)

            try:
                mic_permission = client_driver.execute_async_script("""
                    const callback = arguments[arguments.length - 1];
                    navigator.permissions.query({name: 'microphone'}).then(result => {
                        callback(result.state);
                    }).catch(err => callback("error"));
                """)
                if mic_permission == "denied":
                    print("Microphone permission is confirmed as denied.")
                else:
                    print("Microphone permission is not denied. Current state:", mic_permission)
            except Exception as e:
                print("Error checking microphone permission:", e)

            time.sleep(10)
            try:
                leave_call_button = WebDriverWait(client_driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Operator"]]'))
                )
                print("Operator button is clickable. Clicking on it...")
                ActionChains(client_driver).move_to_element(leave_call_button).click().perform()
                time.sleep(2)
            except Exception as e:
                print("Error clicking the Operator button1:", e)

            try:
                mic_permission = client_driver.execute_async_script("""
                    const callback = arguments[arguments.length - 1];
                    navigator.permissions.query({name: 'microphone'}).then(result => {
                        callback(result.state);
                    }).catch(err => callback("error"));
                """)
                if mic_permission == "denied":
                    print("Microphone permission is confirmed as denied.")
                else:
                    print("Microphone permission is not denied. Current state:", mic_permission)
            except Exception as e:
                print("Error checking microphone permission:", e)

            try:
                WebDriverWait(client_driver, 999).until(
                    EC.url_contains("https://cloudbreak-customer-ui.qa.cloudbreak.us/call-error")
                )
                print("URL успешно обновлен на https://cloudbreak-customer-ui.qa.cloudbreak.us/call-error")
            except Exception as e:
                print("Ошибка: URL не изменился на ожидаемый: https://cloudbreak-customer-ui.qa.cloudbreak.us/call-error",
                      e)

            time.sleep(20)

            try:
                return client_driver
            except Exception as e:
                print(f"Error in open_client_browser: {e}")
                screen_recorder["stop_recording"]("client")
                raise

        try:
            # Запускаем браузер агента с отдельной записью
            screen_recorder["start_recording"]("agent")
            agent_driver = open_agent_browser()
            print("Агентский браузер открыт и записывается")

            # Запускаем браузер клиента с отдельной записью
            screen_recorder["start_recording"]("client")
            client_driver = open_client_browser()
            print("Клиентский браузер открыт и записывается")

            # Продолжаем тест...
            try:
                # ... существующий код теста ...
                pass
            finally:
                # Останавливаем записи для обоих браузеров
                screen_recorder["stop_recording"]("agent")
                screen_recorder["stop_recording"]("client")
                
                # Закрываем браузеры
                if agent_driver:
                    agent_driver.quit()
                if client_driver:
                    client_driver.quit()
        except Exception as e:
            print(f"Ошибка в тесте: {e}")
            # Убеждаемся, что записи остановлены даже при ошибке
            screen_recorder["stop_recording"]("agent")
            screen_recorder["stop_recording"]("client")
            raise


        