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

def start_screen_recording(output_path, display=None):
    """
    Запускает запись экрана с помощью ffmpeg
    """
    if sys.platform == "darwin":  # MacOS
        cmd = [
            "ffmpeg", "-f", "avfoundation",
            "-i", "1:none",  # захват экрана без звука
            "-vcodec", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",  # для совместимости с большинством плееров
            "-y",  # перезаписывать файл если существует
            f"{output_path}.mp4"
        ]
    else:  # Linux
        display = display or os.getenv("DISPLAY", ":0.0")
        cmd = [
            "ffmpeg", "-f", "x11grab",
            "-video_size", "1920x1080",
            "-i", display,
            "-vcodec", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            "-y",
            f"{output_path}.mp4"
        ]
    
    print(f"Запуск записи экрана для {display}. Команда: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def stop_screen_recording(process, browser_name="unknown"):
    """
    Останавливает запись экрана.
    """
    if process:
        print(f"\nОстанавливаем запись экрана для {browser_name}...")
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
            print(f"Вывод ffmpeg для {browser_name}:")
            print(stdout.decode() if stdout else "Нет вывода stdout")
            if stderr:
                print(f"Ошибки ffmpeg для {browser_name}:")
                print(stderr.decode())
        except subprocess.TimeoutExpired:
            print(f"Процесс записи для {browser_name} не завершился вовремя, принудительно завершаем...")
            process.kill()
            process.communicate()
        print(f"Запись экрана для {browser_name} завершена")

@pytest.fixture(scope="function")
def screen_recorder(request):
    """
    Фикстура для записи видео теста
    """
    # Создаем директорию если не существует
    os.makedirs("test_videos", exist_ok=True)
    
    # Словарь для хранения процессов записи для каждого браузера
    recording_processes = {}
    
    def start_recording_for_browser(browser_name, display=None):
        # Генерируем имя файла на основе имени теста и браузера
        test_name = request.node.name
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        video_path = os.path.join("test_videos", f"{test_name}_{browser_name}_{timestamp}")
        
        # Запускаем запись
        process = start_screen_recording(video_path, display)
        recording_processes[browser_name] = {
            "process": process,
            "path": video_path
        }
        return process
    
    # Предоставляем функцию для запуска записи
    yield start_recording_for_browser
    
    # Останавливаем все записи
    for browser_name, info in recording_processes.items():
        stop_screen_recording(info["process"], browser_name)
        
        # Проверяем, что файл создан и прикрепляем к отчету
        video_file = f"{info['path']}.mp4"
        if os.path.exists(video_file):
            print(f"Видео для {browser_name} записано успешно: {video_file}")
            allure.attach.file(
                video_file,
                name=f"{browser_name}_recording.mp4",
                attachment_type=allure.attachment_type.MP4
            )
        else:
            print(f"Ошибка: видео для {browser_name} не было создано: {video_file}")

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
    """
    with allure.step("Начинаем тестирование видеозвонка"):
        # Глобальные переменные для синхронизации
        global agent_ready, client_ready
        agent_ready = threading.Event()
        client_ready = threading.Event()

        # Словарь для хранения дисплеев для каждого потока
        displays = {
            'main': ':99',
            'agent': ':98',
            'agent_alt': ':97',
            'agent_fourth': ':96',
            'agent_fifth': ':95'
        }

        def open_agent_browser():
            try:
                os.environ['DISPLAY'] = displays['agent']
                print(f"Агент использует дисплей {displays['agent']}")
                
                chrome_path, chromedriver_path = install_browser_and_driver()
                options = Options()
                options.binary_location = chrome_path
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--use-fake-device-for-media-stream")
                options.add_argument("--use-fake-ui-for-media-stream")
                video_path = download_video()
                print(f"Using video file for fake camera: {video_path}")
                options.add_argument(f"--use-file-for-fake-video-capture={video_path}")
                
                agent_driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=options)
                agent_recording = screen_recorder("agent_browser", displays['agent'])
                
                # ... остальной код для агента ...
                
                agent_ready.set()  # Сигнализируем о готовности агента
            except Exception as e:
                print(f"Ошибка в потоке агента: {e}")
                raise
            finally:
                agent_driver.quit()

        def open_client_browser():
            try:
                # Ждем готовности агента
                if not agent_ready.wait(timeout=30):
                    raise TimeoutError("Агент не подготовился за отведенное время")
                
                os.environ['DISPLAY'] = displays['main']
                print(f"Клиент использует дисплей {displays['main']}")
                
                chrome_path, chromedriver_path = install_browser_and_driver()
                options = Options()
                options.binary_location = chrome_path
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--use-fake-device-for-media-stream")
                options.add_argument("--use-fake-ui-for-media-stream")
                video_path = download_video()
                print(f"Using video file for fake camera: {video_path}")
                options.add_argument(f"--use-file-for-fake-video-capture={video_path}")
                
                client_driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=options)
                client_recording = screen_recorder("client_browser", displays['main'])
                
                # ... остальной код для клиента ...
                
                client_ready.set()  # Сигнализируем о готовности клиента
            except Exception as e:
                print(f"Ошибка в потоке клиента: {e}")
                raise
            finally:
                client_driver.quit()

        # Запускаем потоки с разными дисплеями
        agent_thread = threading.Thread(target=open_agent_browser)
        agent_thread.start()
        print("Агентский поток запущен")

        client_thread = threading.Thread(target=open_client_browser)
        client_thread.start()
        print("Клиентский поток запущен")

        # Ждем завершения всех потоков
        agent_thread.join(timeout=300)  # 5 минут максимум
        client_thread.join(timeout=300)

        if agent_thread.is_alive() or client_thread.is_alive():
            raise TimeoutError("Тест не завершился за отведенное время")

        print("Все потоки завершили работу")

        # Основная логика для клиента
        from LOGIN import Login_page
        login_page = Login_page(driver)
        login_page.login_to_cloudbreak_customer()

        # Запускаем второй поток с задержкой
        agent_alt_thread = threading.Thread(target=delayed_alt_agent)
        agent_alt_thread.start()

        # Запускаем четвертый поток с задержкой
        fourth_agent_thread = threading.Thread(target=delayed_fourth_agent)
        fourth_agent_thread.start()

        # Запускаем пятый поток с задержкой
        fifth_agent_thread = threading.Thread(target=delayed_fifth_agent)
        fifth_agent_thread.start()

        client_thread = threading.Thread(target=delayed_client)
        client_thread.start()
        
        language_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'language-tile') and contains(@class, 'frequent-language-tile-orange-background')]//span[text()='Pусский']")
            )
        )
        driver.execute_script("arguments[0].click();", language_button)
        time.sleep(5)
        
        max_attempts = 5
        attempt = 0
        video_active = False
        while attempt < max_attempts and not video_active:
            attempt += 1
            print(f"\nAttempt {attempt} of {max_attempts}")
            try:
                user_id_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'HS2uzLU4rZSTbb8ktGRx')]//span[contains(text(), '8944PA00006')]")
                    )
                )
                print(f"User ID found: {user_id_element.text}")
                video_active = driver.execute_script("""
                    const video = document.querySelector('video');
                    if (!video) {
                        console.log('Video element not found');
                        return false;
                    }
                    console.log('Video state:', {
                        paused: video.paused,
                        ended: video.ended,
                        readyState: video.readyState,
                        currentTime: video.currentTime,
                        videoWidth: video.videoWidth,
                        videoHeight: video.videoHeight
                    });
                    return !video.paused && !video.ended && video.readyState >= 2;
                """)
                if video_active:
                    print("✅ Video successfully activated!")
                    break
                else:
                    print("❌ Video not active, waiting...")
                    time.sleep(5)
            except Exception as e:
                print(f"Error during check: {str(e)}")
                time.sleep(5)

        time.sleep(5)
        


    # --- Переключение камеры ---
        try:
            camera_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='video-mute-btn']"))
            )
            # Получаем начальное состояние
            camera_text_initial = camera_button.find_element(By.XPATH, ".//span").text.strip()
            print("Initial camera state:", camera_text_initial)
            
            # Кликаем, чтобы переключить состояние камеры
            ActionChains(driver).move_to_element(camera_button).click().perform()
            time.sleep(3)
            
            camera_text_after = camera_button.find_element(By.XPATH, ".//span").text.strip()
            print("Camera state after toggle:", camera_text_after)
            
            if camera_text_initial == "Pause Video" and camera_text_after == "Unpause Video":
                print("✅ Camera successfully toggled to disabled.")
            elif camera_text_initial == "Unpause Video" and camera_text_after == "Pause Video":
                print("✅ Camera successfully toggled to enabled.")
            else:
                print("❌ Camera state did not toggle as expected.")
            
            # Опционально: возвращаем исходное состояние
            ActionChains(driver).move_to_element(camera_button).click().perform()
            time.sleep(3)
            camera_text_revert = camera_button.find_element(By.XPATH, ".//span").text.strip()
            print("Camera state after revert:", camera_text_revert)
        except Exception as e:
            print("Error toggling camera status:", e)


        # --- Переключение звука ---
        try:
            sound_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Mute volume']"))
            )
            sound_class_initial = sound_button.get_attribute("class")
            print("Initial sound button class:", sound_class_initial)
            
            # Кликаем, чтобы переключить состояние звука
            ActionChains(driver).move_to_element(sound_button).click().perform()
            time.sleep(3)
            
            sound_class_after = sound_button.get_attribute("class")
            print("Sound button class after toggle:", sound_class_after)
            
            # Считаем, что если класс содержит "V_OoXHutaK1ot9aXxMLh", звук выключен
            if ("V_OoXHutaK1ot9aXxMLh" in sound_class_initial and "V_OoXHutaK1ot9aXxMLh" not in sound_class_after) or \
            ("V_OoXHutaK1ot9aXxMLh" not in sound_class_initial and "V_OoXHutaK1ot9aXxMLh" in sound_class_after):
                print("✅ Sound toggled successfully.")
            else:
                print("❌ Sound state did not toggle as expected.")
            
            # Опционально: возвращаем исходное состояние
            ActionChains(driver).move_to_element(sound_button).click().perform()
            time.sleep(3)
            sound_class_revert = sound_button.get_attribute("class")
            print("Sound button class after revert:", sound_class_revert)
        except Exception as e:
            print("Error toggling sound status:", e)

        


        time.sleep(200)
        try:
            leave_call_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "_LKm8iHTwJx1Jox10NmL") and @data-testid="testid-call-end-btn"]'))
            )
            print("1Leave Call button is clickable. Clicking on it...")
            ActionChains(driver).move_to_element(leave_call_button).click().perform()
            time.sleep(2)
        except Exception as e:
            print("Error clicking the Leave Call button1:", e)

        try:
            leave_call_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Skip']"))
            )
            print("Operator button is clickable. Clicking on it...")
            ActionChains(driver).move_to_element(leave_call_button).click().perform()
            time.sleep(2)
        except Exception as e:
            print("Error Skip button:", e)

        time.sleep(60)



        try:
            driver.execute_cdp_cmd("Browser.setPermission", {
                "origin": "https://martti-agent.qa.cloudbreak.us",
                "permission": {"name": "microphone"},
                "setting": "denied"
            })
            print("Microphone usage has been disabled for the driver.")
        except Exception as e:
            print("Error disabling microphone usage:", e)


        try:
            leave_call_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Operator"]]'))
            )
            print("Operator button is clickable. Clicking on it...")
            ActionChains(driver).move_to_element(leave_call_button).click().perform()
            time.sleep(2)
        except Exception as e:
            print("Error clicking the Operator button1:", e)

        try:
            WebDriverWait(driver, 900).until(
                EC.url_contains("https://cloudbreak-customer-ui.qa.cloudbreak.us/call-error")
            )
            print("URL успешно обновлен на https://cloudbreak-customer-ui.qa.cloudbreak.us/call-error")
        except Exception as e:
            print("Ошибка: URL не изменился на ожидаемый: https://cloudbreak-customer-ui.qa.cloudbreak.us/call-error", e)



        assert video_active, f"Failed to activate video after {max_attempts} attempts!"
        screenshot_path = f"video_test_screenshot_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        print(f"\nScreenshot saved: {screenshot_path}")
        allure.step("Test completed: Video activated")

        # В конце теста ждем завершения всех потоков
        agent_thread.join()
        agent_alt_thread.join()
        fourth_agent_thread.join()
        fifth_agent_thread.join()
        client_thread.join()
        
        agent_thread.join()


        