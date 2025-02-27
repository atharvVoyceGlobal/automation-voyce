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
    Весь процесс записывается на видео для последующего анализа.
    """
    with allure.step("Начинаем тестирование видеозвонка"):
        # Скачиваем видео перед началом теста
        video_path = download_video()
        print(f"Используем видео файл: {video_path}")

        # Запускаем запись для основного браузера
        main_recording = screen_recorder("main_browser", ":99")

        def open_agent_browser():
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
            
            # Запускаем запись для агентского браузера
            agent_recording = screen_recorder("agent_browser", ":99")
            
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
            except Exception as e:
                print("Error getting video elements count:", e)
            try:
                remote_video_elem = WebDriverWait(agent_driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "video.remote-videos_landscapeVideoElement__KIUeU"))
                )
                print("Video element found:", remote_video_elem)
                video_props = agent_driver.execute_script("""
                    var video = document.querySelector("video.remote-videos_landscapeVideoElement__KIUeU");
                    if (video) {
                        return {
                            paused: video.paused,
                            ended: video.ended,
                            readyState: video.readyState,
                            currentTime: video.currentTime,
                            videoWidth: video.videoWidth,
                            videoHeight: video.videoHeight
                        };
                    }
                    return null;
                """)
                print("Video element properties:", video_props)
                video_active = agent_driver.execute_script("""
                    var video = document.querySelector("video.remote-videos_landscapeVideoElement__KIUeU");
                    if (video) {
                        return !video.paused && !video.ended && video.readyState >= 2;
                    }
                    return false;
                """)
                if video_active:
                    print("✅ Video is successfully displayed on user's screen")
                else:
                    print("❌ Video is not active")
            except Exception as e:
                print(f"Error checking video recording: {e}")

            # --- Камера: Toggle camera button (выключение/включение видео) ---

            try:
                camera_button = WebDriverWait(agent_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='video-mute-btn']"))
                )
                print("Camera toggle button found. Clicking to turn off camera.")
                ActionChains(agent_driver).move_to_element(camera_button).click().perform()
                time.sleep(3)
                
                # Проверяем текст кнопки после клика: если камера выключена, кнопка должна отображать "Unpause Video"
                button_text_off = camera_button.find_element(By.XPATH, ".//span").text.strip()
                if "Unpause Video" in button_text_off:
                    print("✅ Camera is off. Button shows:", button_text_off)
                else:
                    print("❌ Camera is still on. Button shows:", button_text_off)
                
                print("Clicking camera toggle button again to turn on camera.")
                ActionChains(agent_driver).move_to_element(camera_button).click().perform()
                time.sleep(3)
                
                # Проверяем текст кнопки после повторного клика: если камера включена, кнопка должна отображать "Pause Video"
                button_text_on = camera_button.find_element(By.XPATH, ".//span").text.strip()
                if "Pause Video" in button_text_on:
                    print("✅ Camera is on. Button shows:", button_text_on)
                else:
                    print("❌ Camera is not active. Button shows:", button_text_on)
            except Exception as e:
                print("Error during camera toggle test:", e)


            # --- Микрофон: Toggle microphone button and check sound state ---
            try:
                mic_button = WebDriverWait(agent_driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='audio-mute-btn']"))
                )
                # Считываем текущее состояние кнопки микрофона
                mic_state_before = mic_button.find_element(By.XPATH, ".//span").text
                print("Current microphone state text:", mic_state_before)
                
                # Нажимаем кнопку для переключения состояния микрофона
                print("Clicking microphone toggle button to change state.")
                ActionChains(agent_driver).move_to_element(mic_button).click().perform()
                time.sleep(3)
                
                # Считываем новое состояние кнопки микрофона
                mic_state_after = mic_button.find_element(By.XPATH, ".//span").text
                print("Microphone state text after click:", mic_state_after)
                
                if mic_state_before.strip().lower() == "mute audio" and "unmute" in mic_state_after.lower():
                    print("✅ Microphone is muted.")
                elif mic_state_before.strip().lower() == "unmute audio" and "mute" in mic_state_after.lower():
                    print("✅ Microphone is unmuted.")
                else:
                    print("❌ Microphone state did not change as expected after first click.")
                
                # Нажимаем кнопку ещё раз, чтобы вернуть исходное состояние
                print("Clicking microphone toggle button again to revert state.")
                ActionChains(agent_driver).move_to_element(mic_button).click().perform()
                time.sleep(3)
                mic_state_reverted = mic_button.find_element(By.XPATH, ".//span").text
                print("Microphone state text after second click:", mic_state_reverted)
                
                if mic_state_reverted.strip().lower() == mic_state_before.strip().lower():
                    print("✅ Microphone state reverted successfully.")
                else:
                    print("❌ Microphone state did not revert as expected.")
            except Exception as e:
                print("Error during microphone toggle test:", e)



            try:
                # Находим кнопку звука по заданному XPath
                sound_button = WebDriverWait(agent_driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mute volume']"))
                )
                # Считываем исходное состояние кнопки по атрибуту class
                initial_class = sound_button.get_attribute("class")
                if "volume-control_muted__cVWPM" in initial_class:
                    print("Sound is initially OFF.")
                    initial_state = "off"
                else:
                    print("Sound is initially ON.")
                    initial_state = "on"
                
                # Нажимаем кнопку, чтобы переключить состояние звука
                print("Clicking sound toggle button to change state.")
                ActionChains(agent_driver).move_to_element(sound_button).click().perform()
                time.sleep(3)
                
                # Считываем класс кнопки после клика
                toggled_class = sound_button.get_attribute("class")
                if initial_state == "on":
                    # Если звук был включён, то теперь должен быть выключен (должен появиться класс muted)
                    if "volume-control_muted__cVWPM" in toggled_class:
                        print("✅ Sound is muted after toggle.")
                    else:
                        print("❌ Sound did not mute as expected.")
                else:
                    # Если звук был выключен, то теперь должен быть включён (класс muted отсутствует)
                    if "volume-control_muted__cVWPM" not in toggled_class:
                        print("✅ Sound is unmuted after toggle.")
                    else:
                        print("❌ Sound did not unmute as expected.")
                
                # Переключаем обратно – возвращаем исходное состояние
                print("Clicking sound toggle button again to revert state.")
                ActionChains(agent_driver).move_to_element(sound_button).click().perform()
                time.sleep(3)
                reverted_class = sound_button.get_attribute("class")
                if reverted_class.strip() == initial_class.strip():
                    print("✅ Sound state reverted successfully.")
                else:
                    print("❌ Sound state did not revert as expected.")
            except Exception as e:
                print("Error during sound toggle test:", e)

            
            try:
                print("\n=== Начинаем процесс добавления переводчика ===")
                print(f"Текущий URL агента: {agent_driver.current_url}")
                
                # Проверяем все доступные элементы на странице
                print("\nПроверяем все доступные элементы с data-testid:")
                elements_with_testid = agent_driver.find_elements(By.CSS_SELECTOR, "[data-testid]")
                for elem in elements_with_testid:
                    print(f"Найден элемент с data-testid: {elem.get_attribute('data-testid')}")
                
                # Шаг 1: Поиск кнопки "Interpreter" с расширенным поиском
                print("\nИщем кнопку Interpreter...")
                # Пробуем разные селекторы
                interpreter_buttons = agent_driver.find_elements(By.XPATH, "//button[contains(@data-testid, 'Interpreter')]")
                print(f"Найдено кнопок по частичному data-testid: {len(interpreter_buttons)}")
                
                interpreter_buttons_alt = agent_driver.find_elements(By.XPATH, "//button[contains(., 'Interpreter')]")
                print(f"Найдено кнопок по тексту: {len(interpreter_buttons_alt)}")
                

                
                # Пытаемся найти кнопку с увеличенным таймаутом
                try:
                    interpreter_button = WebDriverWait(agent_driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@data-testid='button-card-header-Interpreter']"))
                    )
                    print("✅ Кнопка Interpreter найдена")
                    print(f"Атрибуты кнопки: {interpreter_button.get_attribute('outerHTML')}")
                    
                    # Проверяем видимость и кликабельность
                    if interpreter_button.is_displayed():
                        print("Кнопка видима на странице")
                        if interpreter_button.is_enabled():
                            print("Кнопка активна")
                        else:
                            print("❌ Кнопка неактивна")
                    else:
                        print("❌ Кнопка НЕ видима на странице")
                    
                    # Пробуем разные способы клика
                    try:
                        print("Пытаемся кликнуть через стандартный клик...")
                        interpreter_button.click()
                    except Exception as click_error:
                        print(f"Стандартный клик не сработал: {click_error}")
                        try:
                            print("Пытаемся кликнуть через JavaScript...")
                            agent_driver.execute_script("arguments[0].click();", interpreter_button)
                        except Exception as js_error:
                            print(f"JavaScript клик не сработал: {js_error}")
                            print("Пытаемся кликнуть через ActionChains...")
                            ActionChains(agent_driver).move_to_element(interpreter_button).click().perform()
                    
                except Exception as e:
                    print(f"❌ Не удалось найти кнопку Interpreter после 20 секунд ожидания: {e}")
                    print("Пробуем альтернативный поиск...")
                    
                    # Пробуем найти по частичному совпадению
                    buttons = agent_driver.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        try:
                            if "interpreter" in button.text.lower():
                                print(f"Найдена кнопка с текстом: {button.text}")
                                button.click()
                                break
                        except:
                            continue
                
                print("Ждем 3 секунды после клика...")
                time.sleep(3)

                # Шаг 2: Поиск поля ввода языка
                print("\nИщем поле ввода языка...")
                input_elements = agent_driver.find_elements(By.XPATH, "(//input[@data-testid='autocomplete-input-languages'])[2]")
                print(f"Найдено полей ввода языка: {len(input_elements)}")
                
                input_element = WebDriverWait(agent_driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "(//input[@data-testid='autocomplete-input-languages'])[2]"))
                )
                print("✅ Поле ввода языка найдено")
                
                # Проверяем видимость и кликабельность
                if input_element.is_displayed():
                    print("Поле ввода видимо на странице")
                else:
                    print("❌ Поле ввода НЕ видимо на странице")
                
                print("Кликаем по полю ввода...")
                ActionChains(agent_driver).move_to_element(input_element).click().perform()
                print("Ждем 2 секунды после клика...")
                time.sleep(2)

                # Очистка поля ввода несколькими способами
                print("\nНачинаем очистку поля ввода...")
                current_value = input_element.get_attribute('value')
                print(f"Текущее значение поля: '{current_value}'")

                # Метод 1: Стандартная очистка
                input_element.clear()
                
                # Метод 2: Очистка через CTRL+A и Delete
                ActionChains(agent_driver).click(input_element)\
                    .key_down(Keys.COMMAND)\
                    .send_keys('a')\
                    .key_up(Keys.COMMAND)\
                    .send_keys(Keys.DELETE)\
                    .perform()
                
                # Метод 3: Посимвольное удаление
                current_value = input_element.get_attribute('value')
                if current_value:
                    for _ in range(len(current_value)):
                        input_element.send_keys(Keys.BACKSPACE)
                
                # Проверяем результат очистки
                final_value = input_element.get_attribute('value')
                print(f"Значение поля после очистки: '{final_value}'")
                
                if not final_value:
                    print("✅ Поле успешно очищено")
                else:
                    print(f"❌ Не удалось полностью очистить поле, осталось: '{final_value}'")

                # Шаг 3: Ввод текста
                print("\nВводим текст 'Uzbek'...")
                input_element.send_keys("Uzbek")
                print("✅ Текст введен")
                print("Ждем 2 секунды после ввода...")
                time.sleep(2)
                input_element = WebDriverWait(agent_driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Uzbek')]"))
                )
                ActionChains(agent_driver).move_to_element(input_element).click().perform()

                # Шаг 4: Поиск кнопки добавления
                print("\nИщем кнопку Add Interpreter to call...")
                add_buttons = agent_driver.find_elements(By.XPATH, "(//button[@data-testid='button-add-to-call'])[2]")
                print(f"Найдено кнопок добавления: {len(add_buttons)}")
                
                add_interpreter_button = WebDriverWait(agent_driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[@data-testid='button-add-to-call'])[2]"))
                )
                print("✅ Кнопка Add Interpreter найдена и кликабельна")
                
                # Пробуем разные способы клика
                try:
                    print("Пытаемся кликнуть через ActionChains...")
                    ActionChains(agent_driver).move_to_element(add_interpreter_button).click().perform()
                except Exception as action_error:
                    print(f"ActionChains клик не сработал: {action_error}")
                    try:
                        print("Пытаемся кликнуть через JavaScript...")
                        agent_driver.execute_script("arguments[0].click();", add_interpreter_button)
                    except Exception as js_error:
                        print(f"JavaScript клик не сработал: {js_error}")
                        print("Пытаемся кликнуть через стандартный клик...")
                        add_interpreter_button.click()
                
                print("✅ Процесс добавления переводчика завершен")
                
            except Exception as e:
                print("\n❌ Ошибка при выполнении шагов:")
                print(f"Тип ошибки: {type(e).__name__}")
                print(f"Текст ошибки: {str(e)}")
                print("\nТекущий URL:", agent_driver.current_url)
                print("\nИсточник страницы:")
                print(agent_driver.page_source[:500] + "...")




            try:
                hold_button_2 = WebDriverWait(agent_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Reconnect Call')]"))
                )
                print("Reconnect Call button is clickable. Clicking on it...")
                hold_button_2.click()
            except Exception as e:
                print("Error clicking hold button 2:", e)

            try:
                hold_button_2 = WebDriverWait(agent_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "(//*[contains(text(), 'Queue')])[3]"))
                )
                print("Queue button is clickable. Clicking on it...")
                hold_button_2.click()
            except Exception as e:
                print("Error clicking hold button 2:", e)

            
            input_elements = agent_driver.find_elements(By.XPATH, "(//input[@type='text' and @data-testid='autocomplete-input-languages'])[1]")
            print(f"Найдено полей ввода языка: {len(input_elements)}")
            
            input_element = WebDriverWait(agent_driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "(//input[@type='text' and @data-testid='autocomplete-input-languages'])[1]"))
            )
            print("✅ Поле ввода языка найдено")
            
            # Проверяем видимость и кликабельность
            if input_element.is_displayed():
                print("Поле ввода видимо на странице")
            else:
                print("❌ Поле ввода НЕ видимо на странице")
            
            print("Кликаем по полю ввода...")
            ActionChains(agent_driver).move_to_element(input_element).click().perform()
            print("Ждем 2 секунды после клика...")
            time.sleep(2)

            # Очистка поля ввода несколькими способами
            print("\nНачинаем очистку поля ввода...")
            current_value = input_element.get_attribute('value')
            print(f"Текущее значение поля: '{current_value}'")

            # Метод 1: Стандартная очистка
            input_element.clear()
            
            # Метод 2: Очистка через CTRL+A и Delete
            ActionChains(agent_driver).click(input_element)\
                .key_down(Keys.COMMAND)\
                .send_keys('a')\
                .key_up(Keys.COMMAND)\
                .send_keys(Keys.DELETE)\
                .perform()
            
            # Метод 3: Посимвольное удаление
            current_value = input_element.get_attribute('value')
            if current_value:
                for _ in range(len(current_value)):
                    input_element.send_keys(Keys.BACKSPACE)
            
            # Проверяем результат очистки
            final_value = input_element.get_attribute('value')
            print(f"Значение поля после очистки: '{final_value}'")
            
            if not final_value:
                print("✅ Поле успешно очищено")
            else:
                print(f"❌ Не удалось полностью очистить поле, осталось: '{final_value}'")

            # Шаг 3: Ввод текста
            print("\nВводим текст 'Operator'...")
            input_element.send_keys("Operator")
            print("✅ Текст введен")
            input_element = WebDriverWait(agent_driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'OPERATOR')]"))
            )
            ActionChains(agent_driver).move_to_element(input_element).click().perform()

            
            try:
                hold_button_2 = WebDriverWait(agent_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "(//*[contains(text(), 'Transfer')])[1]"))
                )
                print("Transfer button is clickable. Clicking on it...")
                hold_button_2.click()
            except Exception as e:
                print("Error clicking hold button 2:", e)



            time.sleep(30)
           

        

        def open_agent_browser_alt():
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
            print(f"Using video file for fake camera in alt agent: {video_path}")
            options.add_argument(f"--use-file-for-fake-video-capture={video_path}")
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.media_stream_mic": 1
            })

            agent_alt_driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=options)
            agent_alt_driver.get(EV.AGENT_URL)
            print("Alt Agent browser opened login page")
            email_field = WebDriverWait(agent_alt_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input28"))
            )
            email_field.clear()
            email_field.send_keys(EV.AGENT_ALT_LOGIN)
            print("Alt Agent email entered")
            password_field = WebDriverWait(agent_alt_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input36"))
            )
            password_field.clear()
            password_field.send_keys(EV.AGENT_ALT_PASSWORD)
            print("Alt Agent password entered")
            sign_in_button = WebDriverWait(agent_alt_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Sign in']"))
            )
            sign_in_button.click()
            print("Alt Agent sign in button clicked")
            time.sleep(2)

            status_select = WebDriverWait(agent_alt_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='status']"))
            )
            status_select.click()
            time.sleep(2)
            print("Status select opened")
            available_option = WebDriverWait(agent_alt_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='status']/option[@value='Available']"))
            )
            available_option.click()
            time.sleep(1)
            
            # Клик по зелёному кружку
            green_icon = WebDriverWait(agent_alt_driver, 30).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.flex.justify-center.items-center.rounded-full.mx-auto.ring-2.h-14.w-14.ring-green-500.group-hover\\:bg-green-200.group-focus\\:bg-green-200")
                )
            )
            ActionChains(agent_alt_driver).move_to_element(green_icon).click().perform()
            print("Green circle element clicked!")
            

            try:
                video_count = agent_alt_driver.execute_script("return document.querySelectorAll('video.remote-videos_landscapeVideoElement__KIUeU').length;")
                print("Number of <video> elements on page:", video_count)
            except Exception as e:
                print("Error getting video elements count:", e)
            try:
                # Получаем верхний видеоэлемент из списка
                remote_video_elem = WebDriverWait(agent_alt_driver, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "video.remote-videos_landscapeVideoElement__KIUeU"))
                )
                print("Video element found:", remote_video_elem)
                
                video_props = agent_alt_driver.execute_script("""
                    var videos = document.querySelectorAll("video.remote-videos_landscapeVideoElement__KIUeU");
                    if (!videos || videos.length === 0) {
                        return null;
                    }
                    var topVideo = videos[0];
                    for (var i = 1; i < videos.length; i++) {
                        if (videos[i].getBoundingClientRect().top < topVideo.getBoundingClientRect().top) {
                            topVideo = videos[i];
                        }
                    }
                    return {
                        paused: topVideo.paused,
                        ended: topVideo.ended,
                        readyState: topVideo.readyState,
                        currentTime: topVideo.currentTime,
                        videoWidth: topVideo.videoWidth,
                        videoHeight: topVideo.videoHeight
                    };
                """)
                print("Video element properties:", video_props)
                
                video_active = agent_alt_driver.execute_script("""
                    var videos = document.querySelectorAll("video.remote-videos_landscapeVideoElement__KIUeU");
                    if (!videos || videos.length === 0) {
                        return false;
                    }
                    var topVideo = videos[0];
                    for (var i = 1; i < videos.length; i++) {
                        if (videos[i].getBoundingClientRect().top < topVideo.getBoundingClientRect().top) {
                            topVideo = videos[i];
                        }
                    }
                    return !topVideo.paused && !topVideo.ended && topVideo.readyState >= 2;
                """)
                if video_active:
                    print("✅ Video is successfully displayed on user's screen")
                else:
                    print("❌ Video is not active")
            except Exception as e:
                print(f"Error checking video recording (agent_alt_driver): {e}")




            # --- Камера: Toggle camera button (выключение/включение видео) ---

            try:
                camera_button = WebDriverWait(agent_alt_driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='video-mute-btn']"))
                )
                print("Camera toggle button found. Clicking to turn off camera.")
                ActionChains(agent_alt_driver).move_to_element(camera_button).click().perform()
                time.sleep(3)
                
                # Проверяем текст кнопки после клика: если камера выключена, кнопка должна отображать "Unpause Video"
                button_text_off = camera_button.find_element(By.XPATH, ".//span").text.strip()
                if "Unpause Video" in button_text_off:
                    print("✅ Camera is off. Button shows:", button_text_off)
                else:
                    print("❌ Camera is still on. Button shows:", button_text_off)
                
                print("Clicking camera toggle button again to turn on camera.")
                ActionChains(agent_alt_driver).move_to_element(camera_button).click().perform()
                time.sleep(3)
                
                # Проверяем текст кнопки после повторного клика: если камера включена, кнопка должна отображать "Pause Video"
                button_text_on = camera_button.find_element(By.XPATH, ".//span").text.strip()
                if "Pause Video" in button_text_on:
                    print("✅ Camera is on. Button shows:", button_text_on)
                else:
                    print("❌ Camera is not active. Button shows:", button_text_on)
            except Exception as e:
                print("Error during camera toggle test:", e)


            # --- Микрофон: Toggle microphone button and check sound state ---
            try:
                mic_button = WebDriverWait(agent_alt_driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='audio-mute-btn']"))
                )
                # Считываем текущее состояние кнопки микрофона
                mic_state_before = mic_button.find_element(By.XPATH, ".//span").text
                print("Current microphone state text:", mic_state_before)
                
                # Нажимаем кнопку для переключения состояния микрофона
                print("Clicking microphone toggle button to change state.")
                ActionChains(agent_alt_driver).move_to_element(mic_button).click().perform()
                time.sleep(3)
                
                # Считываем новое состояние кнопки микрофона
                mic_state_after = mic_button.find_element(By.XPATH, ".//span").text
                print("Microphone state text after click:", mic_state_after)
                
                if mic_state_before.strip().lower() == "mute audio" and "unmute" in mic_state_after.lower():
                    print("✅ Microphone is muted.")
                elif mic_state_before.strip().lower() == "unmute audio" and "mute" in mic_state_after.lower():
                    print("✅ Microphone is unmuted.")
                else:
                    print("❌ Microphone state did not change as expected after first click.")
                
                # Нажимаем кнопку ещё раз, чтобы вернуть исходное состояние
                print("Clicking microphone toggle button again to revert state.")
                ActionChains(agent_alt_driver).move_to_element(mic_button).click().perform()
                time.sleep(3)
                mic_state_reverted = mic_button.find_element(By.XPATH, ".//span").text
                print("Microphone state text after second click:", mic_state_reverted)
                
                if mic_state_reverted.strip().lower() == mic_state_before.strip().lower():
                    print("✅ Microphone state reverted successfully.")
                else:
                    print("❌ Microphone state did not revert as expected.")
            except Exception as e:
                print("Error during microphone toggle test:", e)



            try:
                # Находим кнопку звука по заданному XPath
                sound_button = WebDriverWait(agent_alt_driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mute volume']"))
                )
                # Считываем исходное состояние кнопки по атрибуту class
                initial_class = sound_button.get_attribute("class")
                if "volume-control_muted__cVWPM" in initial_class:
                    print("Sound is initially OFF.")
                    initial_state = "off"
                else:
                    print("Sound is initially ON.")
                    initial_state = "on"
                
                # Нажимаем кнопку, чтобы переключить состояние звука
                print("Clicking sound toggle button to change state.")
                ActionChains(agent_alt_driver).move_to_element(sound_button).click().perform()
                time.sleep(3)
                
                # Считываем класс кнопки после клика
                toggled_class = sound_button.get_attribute("class")
                if initial_state == "on":
                    # Если звук был включён, то теперь должен быть выключен (должен появиться класс muted)
                    if "volume-control_muted__cVWPM" in toggled_class:
                        print("✅ Sound is muted after toggle.")
                    else:
                        print("❌ Sound did not mute as expected.")
                else:
                    # Если звук был выключен, то теперь должен быть включён (класс muted отсутствует)
                    if "volume-control_muted__cVWPM" not in toggled_class:
                        print("✅ Sound is unmuted after toggle.")
                    else:
                        print("❌ Sound did not unmute as expected.")
                
                # Переключаем обратно – возвращаем исходное состояние
                print("Clicking sound toggle button again to revert state.")
                ActionChains(agent_alt_driver).move_to_element(sound_button).click().perform()
                time.sleep(3)
                reverted_class = sound_button.get_attribute("class")
                if reverted_class.strip() == initial_class.strip():
                    print("✅ Sound state reverted successfully.")
                else:
                    print("❌ Sound state did not revert as expected.")
            except Exception as e:
                print("Error during sound toggle test:", e)


            try:
                Participants_button_1 = WebDriverWait(agent_alt_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[.//span[text()='Participants']])[1]"))
                )
                print("Hold button (data-testid='ea4ff00f-45a1-4c14-b2c8-c6d4be1582ac-hold') is clickable. Clicking on it...")
                Participants_button_1.click()
            except Exception as e:
                print("Error clicking hold button 1:", e)

            try:
                hold_button_1 = WebDriverWait(agent_alt_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[.//span[text()='hold']])[1]"))
                )
                print("Hold button (data-testid='ea4ff00f-45a1-4c14-b2c8-c6d4be1582ac-hold') is clickable. Clicking on it...")
                hold_button_1.click()
            except Exception as e:
                print("Error clicking hold button 1:", e)

            try:
                hold_button_2 = WebDriverWait(agent_alt_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[.//span[text()='hold']])[2]"))
                )
                print("Hold button (data-testid='0e9512e0-649c-4d92-b666-5c3d0b4e0e06-hold') is clickable. Clicking on it...")
                hold_button_2.click()
            except Exception as e:
                print("Error clicking hold button 2:", e)
            
            time.sleep(20)

            try:
                hold_button_1 = WebDriverWait(agent_alt_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[.//span[text()='resume']])[1]"))
                )
                print("Hold button (data-testid='ea4ff00f-45a1-4c14-b2c8-c6d4be1582ac-hold') is clickable. Clicking on it...")
                hold_button_1.click()
            except Exception as e:
                print("Error clicking hold button 1:", e)

            try:
                hold_button_2 = WebDriverWait(agent_alt_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[.//span[text()='resume']])[2]"))
                )
                print("Hold button (data-testid='0e9512e0-649c-4d92-b666-5c3d0b4e0e06-hold') is clickable. Clicking on it...")
                hold_button_2.click()
            except Exception as e:
                print("Error clicking hold button 2:", e)


            time.sleep(20)
            try:
                hold_button_2 = WebDriverWait(agent_alt_driver, 90).until(
                    EC.element_to_be_clickable((By.XPATH, "(//button[.//span[text()='end']])[2]"))
                )
                print("End button is clickable. Clicking on it...")
                hold_button_2.click()
            except Exception as e:
                print("Error clicking hold button 2:", e)

      

        def delayed_alt_agent():
            print("Waiting 40 seconds before starting alt agent...")
            time.sleep(20)  # Ждем 40 секунд перед запуском второго агента
            open_agent_browser_alt()
            print("Alt agent started after delay")

        def open_agent_browser_fourth():
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
            print(f"Using video file for fake camera in fourth agent: {video_path}")
            options.add_argument(f"--use-file-for-fake-video-capture={video_path}")
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.media_stream_mic": 1
            })

            fourth_agent_driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=options)
            fourth_agent_driver.get(EV.AGENT_URL)
            print("Fourth Agent browser opened login page")
            email_field = WebDriverWait(fourth_agent_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input28"))
            )
            email_field.clear()
            email_field.send_keys(EV.OPERATOR_LOGIN)
            print("Fourth Agent email entered")
            password_field = WebDriverWait(fourth_agent_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input36"))
            )
            password_field.clear()
            password_field.send_keys(EV.OPERATOR_PASSWORD)
            print("Fourth Agent password entered")
            sign_in_button = WebDriverWait(fourth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Sign in']"))
            )
            sign_in_button.click()
            print("Fourth Agent sign in button clicked")
            time.sleep(2)

            status_select = WebDriverWait(fourth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='status']"))
            )
            status_select.click()
            time.sleep(2)
            print("Status select opened")
            available_option = WebDriverWait(fourth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='status']/option[@value='Available']"))
            )
            available_option.click()
            time.sleep(1)
            
            # Клик по зелёному кружку
            green_icon = WebDriverWait(fourth_agent_driver, 999).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.flex.justify-center.items-center.rounded-full.mx-auto.ring-2.h-14.w-14.ring-green-500.group-hover\\:bg-green-200.group-focus\\:bg-green-200")
                )
            )
            ActionChains(fourth_agent_driver).move_to_element(green_icon).click().perform()
            print("Green circle element clicked in fourth agent!")

            try:
                # Count all matching video elements on the page
                video_count = fourth_agent_driver.execute_script(
                    "return document.querySelectorAll('video.remote-videos_landscapeVideoElement__KIUeU').length;"
                )
                print("Number of <video> elements on page:", video_count)
            except Exception as e:
                print("Error getting video elements count:", e)

            try:
                # Wait until at least one video element is present
                WebDriverWait(fourth_agent_driver, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "video.remote-videos_landscapeVideoElement__KIUeU"))
                )
                
                # Use JavaScript to loop through all matching videos, pick the topmost one, and return its properties
                video_props = fourth_agent_driver.execute_script("""
                    var videos = document.querySelectorAll("video.remote-videos_landscapeVideoElement__KIUeU");
                    if (!videos || videos.length === 0) {
                        return null;
                    }
                    var topVideo = videos[0];
                    var topRect = topVideo.getBoundingClientRect();
                    for (var i = 1; i < videos.length; i++) {
                        var rect = videos[i].getBoundingClientRect();
                        if (rect.top < topRect.top) {
                            topVideo = videos[i];
                            topRect = rect;
                        }
                    }
                    return {
                        paused: topVideo.paused,
                        ended: topVideo.ended,
                        readyState: topVideo.readyState,
                        currentTime: topVideo.currentTime,
                        videoWidth: topVideo.videoWidth,
                        videoHeight: topVideo.videoHeight
                    };
                """)
                print("Video element properties:", video_props)
                
                # Check if the topmost video element is active
                video_active = fourth_agent_driver.execute_script("""
                    var videos = document.querySelectorAll("video.remote-videos_landscapeVideoElement__KIUeU");
                    if (!videos || videos.length === 0) {
                        return false;
                    }
                    var topVideo = videos[0];
                    var topRect = topVideo.getBoundingClientRect();
                    for (var i = 1; i < videos.length; i++) {
                        var rect = videos[i].getBoundingClientRect();
                        if (rect.top < topRect.top) {
                            topVideo = videos[i];
                            topRect = rect;
                        }
                    }
                    return !topVideo.paused && !topVideo.ended && topVideo.readyState >= 2;
                """)
                
                if video_active:
                    print("✅ Video is successfully displayed on user's screen")
                else:
                    print("❌ Video is not active")
                    
            except Exception as e:
                print(f"Error checking video recording (agent_alt_driver): {e}")

            # --- Камера: Toggle camera button (выключение/включение видео) ---

            try:
                camera_button = WebDriverWait(fourth_agent_driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='video-mute-btn']"))
                )
                print("Camera toggle button found. Clicking to turn off camera.")
                ActionChains(fourth_agent_driver).move_to_element(camera_button).click().perform()
                time.sleep(3)
                
                # Проверяем текст кнопки после клика: если камера выключена, кнопка должна отображать "Unpause Video"
                button_text_off = camera_button.find_element(By.XPATH, ".//span").text.strip()
                if "Unpause Video" in button_text_off:
                    print("✅ Camera is off. Button shows:", button_text_off)
                else:
                    print("❌ Camera is still on. Button shows:", button_text_off)
                
                print("Clicking camera toggle button again to turn on camera.")
                ActionChains(fourth_agent_driver).move_to_element(camera_button).click().perform()
                time.sleep(3)
                
                # Проверяем текст кнопки после повторного клика: если камера включена, кнопка должна отображать "Pause Video"
                button_text_on = camera_button.find_element(By.XPATH, ".//span").text.strip()
                if "Pause Video" in button_text_on:
                    print("✅ Camera is on. Button shows:", button_text_on)
                else:
                    print("❌ Camera is not active. Button shows:", button_text_on)
            except Exception as e:
                print("Error during camera toggle test:", e)


            # --- Микрофон: Toggle microphone button and check sound state ---
            try:
                mic_button = WebDriverWait(fourth_agent_driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='audio-mute-btn']"))
                )
                # Считываем текущее состояние кнопки микрофона
                mic_state_before = mic_button.find_element(By.XPATH, ".//span").text
                print("Current microphone state text:", mic_state_before)
                
                # Нажимаем кнопку для переключения состояния микрофона
                print("Clicking microphone toggle button to change state.")
                ActionChains(fourth_agent_driver).move_to_element(mic_button).click().perform()
                time.sleep(3)
                
                # Считываем новое состояние кнопки микрофона
                mic_state_after = mic_button.find_element(By.XPATH, ".//span").text
                print("Microphone state text after click:", mic_state_after)
                
                if mic_state_before.strip().lower() == "mute audio" and "unmute" in mic_state_after.lower():
                    print("✅ Microphone is muted.")
                elif mic_state_before.strip().lower() == "unmute audio" and "mute" in mic_state_after.lower():
                    print("✅ Microphone is unmuted.")
                else:
                    print("❌ Microphone state did not change as expected after first click.")
                
                # Нажимаем кнопку ещё раз, чтобы вернуть исходное состояние
                print("Clicking microphone toggle button again to revert state.")
                ActionChains(fourth_agent_driver).move_to_element(mic_button).click().perform()
                time.sleep(3)
                mic_state_reverted = mic_button.find_element(By.XPATH, ".//span").text
                print("Microphone state text after second click:", mic_state_reverted)
                
                if mic_state_reverted.strip().lower() == mic_state_before.strip().lower():
                    print("✅ Microphone state reverted successfully.")
                else:
                    print("❌ Microphone state did not revert as expected.")
            except Exception as e:
                print("Error during microphone toggle test:", e)



            try:
                # Находим кнопку звука по заданному XPath
                sound_button = WebDriverWait(fourth_agent_driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mute volume']"))
                )
                # Считываем исходное состояние кнопки по атрибуту class
                initial_class = sound_button.get_attribute("class")
                if "volume-control_muted__cVWPM" in initial_class:
                    print("Sound is initially OFF.")
                    initial_state = "off"
                else:
                    print("Sound is initially ON.")
                    initial_state = "on"
                
                # Нажимаем кнопку, чтобы переключить состояние звука
                print("Clicking sound toggle button to change state.")
                ActionChains(fourth_agent_driver).move_to_element(sound_button).click().perform()
                time.sleep(3)
                
                # Считываем класс кнопки после клика
                toggled_class = sound_button.get_attribute("class")
                if initial_state == "on":
                    # Если звук был включён, то теперь должен быть выключен (должен появиться класс muted)
                    if "volume-control_muted__cVWPM" in toggled_class:
                        print("✅ Sound is muted after toggle.")
                    else:
                        print("❌ Sound did not mute as expected.")
                else:
                    # Если звук был выключен, то теперь должен быть включён (класс muted отсутствует)
                    if "volume-control_muted__cVWPM" not in toggled_class:
                        print("✅ Sound is unmuted after toggle.")
                    else:
                        print("❌ Sound did not unmute as expected.")
                
                # Переключаем обратно – возвращаем исходное состояние
                print("Clicking sound toggle button again to revert state.")
                ActionChains(fourth_agent_driver).move_to_element(sound_button).click().perform()
                time.sleep(5)
                reverted_class = sound_button.get_attribute("class")
                if reverted_class.strip() == initial_class.strip():
                    print("✅ Sound state reverted successfully.")
                else:
                    print("❌ Sound state did not revert as expected.")
            except Exception as e:
                print("Error during sound toggle test:", e)
            
            try:
                hold_button_2 = WebDriverWait(fourth_agent_driver, 100).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close Sheet')]"))
                )
                print("End button is clickable. Clicking on it...")
                hold_button_2.click()
            except Exception as e:
                print("Error clicking hold button 2:", e)


            time.sleep(10)

            fourth_agent_driver.quit()
            
            


        def delayed_fourth_agent():
            print("Waiting 25 seconds before starting fourth agent...") 
            time.sleep(25)  # Ждем 25 секунд перед запуском четвертого агента
            open_agent_browser_fourth()
            print("Fourth agent started after delay")

        def open_agent_browser_fifth():
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

            fifth_agent_driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=options)
            fifth_agent_driver.get(EV.AGENT_URL)
            print("Fifth Agent browser opened login page")
            email_field = WebDriverWait(fifth_agent_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input28"))
            )
            email_field.clear()
            email_field.send_keys(EV.OPERATOR_LOGIN)
            print("Fifth Agent email entered")
            password_field = WebDriverWait(fifth_agent_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input36"))
            )
            password_field.clear()
            password_field.send_keys(EV.OPERATOR_PASSWORD)
            print("Fifth Agent password entered")
            sign_in_button = WebDriverWait(fifth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Sign in']"))
            )
            sign_in_button.click()
            print("Fifth Agent sign in button clicked")
            time.sleep(2)

            status_select = WebDriverWait(fifth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='status']"))
            )
            status_select.click()
            time.sleep(2)
            print("Status select opened")
            available_option = WebDriverWait(fifth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='status']/option[@value='Available']"))
            )
            available_option.click()
            time.sleep(1)
            

            try:
                fifth_agent_driver.execute_cdp_cmd("Browser.setPermission", {
                    "origin": "https://martti-agent.qa.cloudbreak.us",
                    "permission": {"name": "camera"},
                    "setting": "denied"
                })
                print("Camera usage has been disabled for the driver.")
            except Exception as e:
                print("Error disabling camera usage:", e)

            time.sleep(10)

            # Проверяем состояние разрешения камеры через Permissions API
            try:
                camera_permission = fifth_agent_driver.execute_async_script("""
                    const callback = arguments[arguments.length - 1];
                    navigator.permissions.query({name: 'camera'}).then(result => {
                        callback(result.state);
                    }).catch(err => callback("error"));
                """)
                if camera_permission == "denied":
                    print("Camera permission is confirmed as denied.")
                    # Если разрешение отклонено, останавливаем все треки видео, чтобы поток не передавался
                    fifth_agent_driver.execute_script("""
                        var video = document.querySelector("video.remote-videos_landscapeVideoElement__KIUeU");
                        if (video && video.srcObject) {
                            video.srcObject.getTracks().forEach(track => track.stop());
                        }
                    """)
                    print("Video stream has been stopped because camera permission is denied.")
                else:
                    print("Camera permission is not denied. Current state:", camera_permission)
            except Exception as e:
                print("Error checking camera permission:", e)

            time.sleep(10)
            green_icon = WebDriverWait(fifth_agent_driver, 999).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(text(), 'ANSWER')]")
                )
            )
            ActionChains(fifth_agent_driver).move_to_element(green_icon).click().perform()
            print("Green circle element clicked in fourth agent!")

            

            try:
                error_message = WebDriverWait(fifth_agent_driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Error accessing your camera or microphone')]"))
                )
                print("Error message found:", error_message.text)
            except Exception as e:
                print("Error: The message 'Error accessing your camera or microphone' was not found within 40 seconds:", e)


            try:
                WebDriverWait(fifth_agent_driver, 30).until(EC.url_contains("https://martti-agent.qa.cloudbreak.us/"))
                print("Successfully verified that we are on https://martti-agent.qa.cloudbreak.us/")
            except Exception as e:
                print("Error: Not on the expected page https://martti-agent.qa.cloudbreak.us/:", e)

            try:
                fifth_agent_driver.execute_cdp_cmd("Browser.setPermission", {
                    "origin": "https://martti-agent.qa.cloudbreak.us",
                    "permission": {"name": "camera"},
                    "setting": "granted"
                })
                print("Camera usage has been re-enabled for the driver.")
            except Exception as e:
                print("Error re-enabling camera usage:", e)


            available_option = WebDriverWait(fifth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='status']/option[@value='Available']"))
            )
            available_option.click()


            time.sleep(60)

        def delayed_fifth_agent():
            print("Waiting 30 seconds before starting fifth agent...") 
            time.sleep(220)  # Ждем 30 секунд перед запуском пятого агента
            open_agent_browser_fifth()
            print("Fifth agent started after delay")

        def open_client_browser():
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

            # Запускаем запись для клиентского браузера
            client_recording = screen_recorder("client_browser", ":99")

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

        def delayed_client():
            print("Waiting 35 seconds before starting second client...")
            time.sleep(280)
            open_client_browser()
            print("Second client started after delay")

        # Запускаем первый поток агента
        agent_thread = threading.Thread(target=open_agent_browser)
        agent_thread.start()
        
        # Ждём, пока первый агент начнет работу
        time.sleep(14)

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


        