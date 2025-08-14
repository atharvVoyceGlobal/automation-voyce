def ensure_dependencies():
    try:
        import pkg_resources
        required = {'selenium', 'pytest', 'allure-pytest', 'requests'}
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed
        
        if missing:
            print("Missing dependencies detected:", missing)
            print("Installing missing dependencies...")
            import subprocess
            subprocess.check_call(["pip", "install"] + list(missing))
            print("Dependencies successfully installed!")
        else:
            print("All required Python dependencies are already installed!")
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        raise


ensure_dependencies()

import time
import pytest
import subprocess
import os
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
from selenium.common.exceptions import TimeoutException
from env import EV
import re

def download_video():

    video_url = "https://drive.usercontent.google.com/u/0/uc?id=1Rv3Qitap2wANEx0I-7NLvSp1cEQlE6_K&export=download"
    video_path = os.path.join(os.getcwd(), "output.y4m")
    
    if os.path.exists(video_path):
        print("Video file already exists, skipping download.")
        return video_path
        
    print("Starting test video download...")
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
                print(f"\rDownload progress: {progress}%", end='')
                
        print("\nVideo successfully downloaded!")
        return video_path
    except Exception as e:
        print(f"Error downloading video: {e}")
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


        chrome_path_match = re.search(r'chrome@[\d\.]+ (.+?)(?:\n|$)', result.stdout)
        if not chrome_path_match:
            raise Exception("Could not find Chrome path in installation output")
        chrome_binary_path = chrome_path_match.group(1)

        if not os.path.exists(chrome_binary_path):
            raise FileNotFoundError(f"Chrome binary not found at {chrome_binary_path}")
        print(f"Chrome binary found at: {chrome_binary_path}")
        
        version_match = re.search(r'chrome@([\d\.]+)', result.stdout)
        if not version_match:
            raise Exception("Could not determine Chrome version from installation output")
        chrome_version = version_match.group(1)
        print(f"Chrome version detected: {chrome_version}")

        print(f"Installing ChromeDriver for version {chrome_version}...")
        chromedriver_result = subprocess.run(
            ["npx", "@puppeteer/browsers", "install", f"chromedriver@{chrome_version}", "--path", installation_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(chromedriver_result.stdout)
        print("ChromeDriver installed successfully!")

        chromedriver_path_match = re.search(r'chromedriver@[\d\.]+ (.+?)(?:\n|$)', chromedriver_result.stdout)
        if not chromedriver_path_match:
            raise Exception("Could not find ChromeDriver path in installation output")
        chromedriver_path = chromedriver_path_match.group(1)

        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")

        return chrome_binary_path, chromedriver_path
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during installation: {e}")
        raise

@pytest.fixture(scope="function")
def driver():
    chrome_path, chromedriver_path = install_browser_and_driver()

    y4m_path = os.path.abspath(os.path.join(os.getcwd(), "output.y4m"))

    chrome_options = Options()
    chrome_options.binary_location = chrome_path

    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument(f"--use-file-for-fake-video-capture={y4m_path}")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")

    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")

    driver = webdriver.Chrome(
        service=ChromeService(executable_path=chromedriver_path),
        options=chrome_options
    )
    yield driver
    driver.quit()

@allure.feature("Video Call Testing")
@allure.story("Checking video call activation via UI with virtual camera, camera & microphone toggle")
def test_video_call_activation(driver):
    video_path = download_video()
    print(f"Using video file: {video_path}")

    def open_agent_browser():
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        chrome_path, chromedriver_path = install_browser_and_driver()
        options = Options()
        options.binary_location = chrome_path

        video_path = download_video()
        abs_video = os.path.abspath(video_path)
        print(f"Using video file for fake camera: {abs_video}")

        options.add_argument("--use-fake-device-for-media-stream")
        options.add_argument(f"--use-file-for-fake-video-capture={abs_video}")
        options.add_argument("--use-fake-ui-for-media-stream")

        options.add_argument("--enable-logging")
        options.add_argument("--v=1")

        agent_driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=options)
        
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
        try:
            close_sheet = WebDriverWait(agent_driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close Sheet')]"))
            )

            actions = ActionChains(agent_driver)
            actions.move_to_element(close_sheet).click().perform()
            print("Close Sheet button clicked (1st time)")

            WebDriverWait(agent_driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Close Sheet')]"))
            )

            close_sheet_again = WebDriverWait(agent_driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close Sheet')]"))
            )
            actions.move_to_element(close_sheet_again).click().perform()
            print("Close Sheet button clicked (2nd time)")

        except TimeoutException:
            print("No Close Sheet button found, continuing...")

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
        
        def click_center_of_element(driver, element):
            driver.execute_script("""
                function clickCenter(element) {
                    const rect = element.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    const clickEvent = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: centerX,
                        clientY: centerY
                    });
                    element.dispatchEvent(clickEvent);
                }
                arguments[0].scrollIntoView({behavior: "instant", block: "center"});
                clickCenter(arguments[0]);
            """, element)
        
        green_icon = WebDriverWait(agent_driver, 999).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'ANSWER')]")
            )
        )
        click_center_of_element(agent_driver, green_icon)
        print("Green circle element clicked in first agent!")
        
        time.sleep(5)
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

        try:
            camera_button = WebDriverWait(agent_driver, 90).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='video-mute-btn']"))
            )
            print("Camera toggle button found. Clicking to turn off camera.")
            ActionChains(agent_driver).move_to_element(camera_button).click().perform()
            time.sleep(3)
            
            button_text_off = camera_button.find_element(By.XPATH, ".//span").text.strip()
            if "Unpause Video" in button_text_off:
                print("✅ Camera is off. Button shows:", button_text_off)
            else:
                print("❌ Camera is still on. Button shows:", button_text_off)
            
            print("Clicking camera toggle button again to turn on camera.")
            ActionChains(agent_driver).move_to_element(camera_button).click().perform()
            time.sleep(3)
            
            button_text_on = camera_button.find_element(By.XPATH, ".//span").text.strip()
            if "Pause Video" in button_text_on:
                print("✅ Camera is on. Button shows:", button_text_on)
            else:
                print("❌ Camera is not active. Button shows:", button_text_on)
        except Exception as e:
            print("Error during camera toggle test:", e)


        try:
            mic_button = WebDriverWait(agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='audio-mute-btn']"))
            )
            mic_state_before = mic_button.find_element(By.XPATH, ".//span").text
            print("Current microphone state text:", mic_state_before)
            
            print("Clicking microphone toggle button to change state.")
            ActionChains(agent_driver).move_to_element(mic_button).click().perform()
            time.sleep(3)
            
            mic_state_after = mic_button.find_element(By.XPATH, ".//span").text
            print("Microphone state text after click:", mic_state_after)
            
            if mic_state_before.strip().lower() == "mute audio" and "unmute" in mic_state_after.lower():
                print("✅ Microphone is muted.")
            elif mic_state_before.strip().lower() == "unmute audio" and "mute" in mic_state_after.lower():
                print("✅ Microphone is unmuted.")
            else:
                print("❌ Microphone state did not change as expected after first click.")
            
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
            sound_button = WebDriverWait(agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mute volume']"))
            )
            initial_class = sound_button.get_attribute("class")
            if "volume-control_muted__cVWPM" in initial_class:
                print("Sound is initially OFF.")
                initial_state = "off"
            else:
                print("Sound is initially ON.")
                initial_state = "on"
            
            print("Clicking sound toggle button to change state.")
            ActionChains(agent_driver).move_to_element(sound_button).click().perform()
            time.sleep(3)
            
            toggled_class = sound_button.get_attribute("class")
            if initial_state == "on":
                if "volume-control_muted__cVWPM" in toggled_class:
                    print("✅ Sound is muted after toggle.")
                else:
                    print("❌ Sound did not mute as expected.")
            else:
                if "volume-control_muted__cVWPM" not in toggled_class:
                    print("✅ Sound is unmuted after toggle.")
                else:
                    print("❌ Sound did not unmute as expected.")
            
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
            print("\n=== Starting interpreter addition process ===")
            print(f"Current agent URL: {agent_driver.current_url}")
            
            print("\nChecking all available elements with data-testid:")
            elements_with_testid = agent_driver.find_elements(By.CSS_SELECTOR, "[data-testid]")
            for elem in elements_with_testid:
                print(f"Found element with data-testid: {elem.get_attribute('data-testid')}")
            
            print("\nLooking for Interpreter button...")
            interpreter_buttons = agent_driver.find_elements(By.XPATH, "//button[contains(@data-testid, 'Interpreter')]")
            print(f"Found buttons by partial data-testid: {len(interpreter_buttons)}")
            
            interpreter_buttons_alt = agent_driver.find_elements(By.XPATH, "//button[contains(., 'Interpreter')]")
            print(f"Found buttons by text: {len(interpreter_buttons_alt)}")
            
            try:
                interpreter_button = WebDriverWait(agent_driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@data-testid='button-card-header-Interpreter']"))
                )
                print("✅ Interpreter button found")
                print(f"Button attributes: {interpreter_button.get_attribute('outerHTML')}")
                
                if interpreter_button.is_displayed():
                    print("Button is visible on page")
                    if interpreter_button.is_enabled():
                        print("Button is active")
                    else:
                        print("❌ Button is inactive")
                else:
                    print("❌ Button is NOT visible on page")
                
                try:
                    print("Attempting standard click...")
                    interpreter_button.click()
                except Exception as click_error:
                    print(f"Standard click failed: {click_error}")
                    try:
                        print("Attempting JavaScript click...")
                        agent_driver.execute_script("arguments[0].click();", interpreter_button)
                    except Exception as js_error:
                        print(f"JavaScript click failed: {js_error}")
                        print("Attempting ActionChains click...")
                        ActionChains(agent_driver).move_to_element(interpreter_button).click().perform()
                
            except Exception as e:
                print(f"❌ Could not find Interpreter button after 20 seconds: {e}")
                print("Trying alternative search...")
                
                buttons = agent_driver.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    try:
                        if "interpreter" in button.text.lower():
                            print(f"Found button with text: {button.text}")
                            button.click()
                            break
                    except:
                        continue
            
            print("Waiting 3 seconds after click...")
            time.sleep(3)

            print("\nLooking for language input field...")
            input_elements = agent_driver.find_elements(By.XPATH, "(//input[@data-testid='autocomplete-input-languages'])[2]")
            print(f"Found language input fields: {len(input_elements)}")
            
            input_element = WebDriverWait(agent_driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "(//input[@data-testid='autocomplete-input-languages'])[2]"))
            )
            print("✅ Language input field found")
            
            if input_element.is_displayed():
                print("Input field is visible on page")
            else:
                print("❌ Input field is NOT visible on page")
            
            print("Clicking on input field...")
            ActionChains(agent_driver).move_to_element(input_element).click().perform()
            print("Waiting 2 seconds after click...")
            time.sleep(2)

            print("\nStarting input field clearing...")
            current_value = input_element.get_attribute('value')
            print(f"Current field value: '{current_value}'")

            input_element.clear()
            
            ActionChains(agent_driver).click(input_element)\
                .key_down(Keys.COMMAND)\
                .send_keys('a')\
                .key_up(Keys.COMMAND)\
                .send_keys(Keys.DELETE)\
                .perform()
            
            current_value = input_element.get_attribute('value')
            if current_value:
                for _ in range(len(current_value)):
                    input_element.send_keys(Keys.BACKSPACE)
            
            final_value = input_element.get_attribute('value')
            print(f"Field value after clearing: '{final_value}'")
            
            if not final_value:
                print("✅ Field successfully cleared")
            else:
                print(f"❌ Could not completely clear field, remaining: '{final_value}'")

            print("\nEntering text 'Uzbek'...")
            input_element.send_keys("Uzbek")
            print("✅ Text entered")
            print("Waiting 2 seconds after input...")
            time.sleep(2)
            input_element = WebDriverWait(agent_driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Uzbek')]"))
            )
            ActionChains(agent_driver).move_to_element(input_element).click().perform()

            print("\nLooking for Add Interpreter to call button...")
            add_buttons = agent_driver.find_elements(By.XPATH, "(//button[@data-testid='button-add-to-call'])[2]")
            print(f"Found add buttons: {len(add_buttons)}")

            add_interpreter_button = WebDriverWait(agent_driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "(//button[@data-testid='button-add-to-call'])[2]"))
            )
            print("✅ Add Interpreter button found and clickable")

            def click_center_of_element(driver, element):
                driver.execute_script("""
                    function clickCenter(element) {
                        const rect = element.getBoundingClientRect();
                        const centerX = rect.left + rect.width / 2;
                        const centerY = rect.top + rect.height / 2;
                        const clickEvent = new MouseEvent('click', {
                            view: window,
                            bubbles: true,
                            cancelable: true,
                            clientX: centerX,
                            clientY: centerY
                        });
                        element.dispatchEvent(clickEvent);
                    }
                    arguments[0].scrollIntoView({behavior: "instant", block: "center"});
                    clickCenter(arguments[0]);
                """, element)

            try:
                print("Attempting to click in the center of the element...")
                click_center_of_element(agent_driver, add_interpreter_button)
            except Exception as center_error:
                print(f"Center click failed: {center_error}")
                try:
                    print("Attempting to click using ActionChains...")
                    ActionChains(agent_driver).move_to_element(add_interpreter_button).click().perform()
                except Exception as action_error:
                    print(f"ActionChains click failed: {action_error}")
                    try:
                        print("Attempting to click using JavaScript...")
                        agent_driver.execute_script("arguments[0].click();", add_interpreter_button)
                    except Exception as js_error:
                        print(f"JavaScript click failed: {js_error}")
                        print("Attempting standard click...")
                        add_interpreter_button.click()

            print("✅ Interpreter addition process completed")
            
        except Exception as e:
            print("\n❌ Error executing steps:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("\nCurrent URL:", agent_driver.current_url)
            print("\nPage source:")
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
        print(f"Found language input fields: {len(input_elements)}")
        
        input_element = WebDriverWait(agent_driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@type='text' and @data-testid='autocomplete-input-languages'])[1]"))
        )
        print("✅ Language input field found")
        
        if input_element.is_displayed():
            print("Input field is visible on page")
        else:
            print("❌ Input field is NOT visible on page")
        
        print("Clicking on input field...")
        ActionChains(agent_driver).move_to_element(input_element).click().perform()
        print("Waiting 2 seconds after click...")
        time.sleep(2)

        print("\nStarting input field clearing...")
        current_value = input_element.get_attribute('value')
        print(f"Current field value: '{current_value}'")

        input_element.clear()
        
        ActionChains(agent_driver).click(input_element)\
            .key_down(Keys.COMMAND)\
            .send_keys('a')\
            .key_up(Keys.COMMAND)\
            .send_keys(Keys.DELETE)\
            .perform()
        
        current_value = input_element.get_attribute('value')
        if current_value:
            for _ in range(len(current_value)):
                input_element.send_keys(Keys.BACKSPACE)
        
        final_value = input_element.get_attribute('value')
        print(f"Field value after clearing: '{final_value}'")
        
        if not final_value:
            print("✅ Field successfully cleared")
        else:
            print(f"❌ Could not completely clear field, remaining: '{final_value}'")

        print("\nEntering text 'Operator'...")
        input_element.send_keys("Operator")
        print("✅ Text entered")
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
        video_path = download_video()
        abs_video = os.path.abspath(video_path)
        print(f"Using video file for fake camera: {abs_video}")

        options.add_argument("--use-fake-device-for-media-stream")
        options.add_argument(f"--use-file-for-fake-video-capture={abs_video}")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--enable-logging")
        options.add_argument("--v=1")

        agent_alt_driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=options)
        agent_alt_driver.get(EV.AGENT_URL)
        print("Alt Agent browser opened login page")
        
        try:
            access_restriction_message = WebDriverWait(agent_alt_driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'You are not allowed to access this app. To request access, contact an admin.')]"))
            )
            print("Access restriction message found")
            
            back_to_signin_link = WebDriverWait(agent_alt_driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@data-se='go-back' and contains(text(), 'Back to sign in')]"))
            )
            back_to_signin_link.click()
            print("Clicked on 'Back to sign in' link")
            
            WebDriverWait(agent_alt_driver, 10).until(
                EC.presence_of_element_located((By.ID, "input28"))
            )
        except Exception as e:
            print("No access restriction found, proceeding to login")
        
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
        try:
            close_sheet = WebDriverWait(agent_alt_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close Sheet')]"))
            )
            close_sheet.click()
            print("Close Sheet button clicked")
        except TimeoutException:
            print("No Close Sheet button found, continuing...")


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
        
       
        def click_center_of_element(driver, element):
            driver.execute_script("""
                function clickCenter(element) {
                    const rect = element.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    const clickEvent = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: centerX,
                        clientY: centerY
                    });
                    element.dispatchEvent(clickEvent);
                }
                arguments[0].scrollIntoView({behavior: "instant", block: "center"});
                clickCenter(arguments[0]);
            """, element)
        
        green_icon = WebDriverWait(agent_alt_driver, 999).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'ANSWER')]")
            )
        )
        click_center_of_element(agent_alt_driver, green_icon)
        print("Green circle element clicked in second agent!")


        
        time.sleep(5)



        try:
            video_count = agent_alt_driver.execute_script("return document.querySelectorAll('video.remote-videos_landscapeVideoElement__KIUeU').length;")
            print("Number of <video> elements on page:", video_count)
        except Exception as e:
            print("Error getting video elements count:", e)
        try:
            
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





        try:
            camera_button = WebDriverWait(agent_alt_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='video-mute-btn']"))
            )
            print("Camera toggle button found. Clicking to turn off camera.")
            ActionChains(agent_alt_driver).move_to_element(camera_button).click().perform()
            time.sleep(3) 
            button_text_off = camera_button.find_element(By.XPATH, ".//span").text.strip()
            if "Unpause Video" in button_text_off:
                print("✅ Camera is off. Button shows:", button_text_off)
            else:
                print("❌ Camera is still on. Button shows:", button_text_off)     
            print("Clicking camera toggle button again to turn on camera.")
            ActionChains(agent_alt_driver).move_to_element(camera_button).click().perform()
            time.sleep(3)
            button_text_on = camera_button.find_element(By.XPATH, ".//span").text.strip()
            if "Pause Video" in button_text_on:
                print("✅ Camera is on. Button shows:", button_text_on)
            else:
                print("❌ Camera is not active. Button shows:", button_text_on)
        except Exception as e:
            print("Error during camera toggle test:", e)


       
        try:
            mic_button = WebDriverWait(agent_alt_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='audio-mute-btn']"))
            )
           
            mic_state_before = mic_button.find_element(By.XPATH, ".//span").text
            print("Current microphone state text:", mic_state_before)
            
           
            print("Clicking microphone toggle button to change state.")
            ActionChains(agent_alt_driver).move_to_element(mic_button).click().perform()
            time.sleep(3)
            
           
            mic_state_after = mic_button.find_element(By.XPATH, ".//span").text
            print("Microphone state text after click:", mic_state_after)
            
            if mic_state_before.strip().lower() == "mute audio" and "unmute" in mic_state_after.lower():
                print("✅ Microphone is muted.")
            elif mic_state_before.strip().lower() == "unmute audio" and "mute" in mic_state_after.lower():
                print("✅ Microphone is unmuted.")
            else:
                print("❌ Microphone state did not change as expected after first click.")
            
          
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
            
            sound_button = WebDriverWait(agent_alt_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mute volume']"))
            )
           
            initial_class = sound_button.get_attribute("class")
            if "volume-control_muted__cVWPM" in initial_class:
                print("Sound is initially OFF.")
                initial_state = "off"
            else:
                print("Sound is initially ON.")
                initial_state = "on"
            
            
            print("Clicking sound toggle button to change state.")
            ActionChains(agent_alt_driver).move_to_element(sound_button).click().perform()
            time.sleep(3)
            
           
            toggled_class = sound_button.get_attribute("class")
            if initial_state == "on":
               
                if "volume-control_muted__cVWPM" in toggled_class:
                    print("✅ Sound is muted after toggle.")
                else:
                    print("❌ Sound did not mute as expected.")
            else:
               
                if "volume-control_muted__cVWPM" not in toggled_class:
                    print("✅ Sound is unmuted after toggle.")
                else:
                    print("❌ Sound did not unmute as expected.")
            
            
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
            agent_alt_driver.execute_script("""
                function clickCenter(element) {
                    const rect = element.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    const clickEvent = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: centerX,
                        clientY: centerY
                    });
                    element.dispatchEvent(clickEvent);
                }
                arguments[0].scrollIntoView({behavior: "instant", block: "center"});
                clickCenter(arguments[0]);
            """, hold_button_2)
            print("Clicked in the center of the end button")
        except Exception as e:
            print("Error clicking end button:", e)

        time.sleep(300)
    

  

    def delayed_alt_agent():
        print("Waiting 40 seconds before starting alt agent...")
        time.sleep(15)  
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
        video_path = download_video()
        abs_video = os.path.abspath(video_path)
        print(f"Using video file for fake camera: {abs_video}")

        options.add_argument("--use-fake-device-for-media-stream")
        options.add_argument(f"--use-file-for-fake-video-capture={abs_video}")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--enable-logging")
        options.add_argument("--v=1")

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
        try:
            close_sheet = WebDriverWait(fourth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close Sheet')]"))
            )
            close_sheet.click()
            print("Close Sheet button clicked")
        except TimeoutException:
            print("No Close Sheet button found, continuing...")


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
        
       
        def click_center_of_element(driver, element):
            driver.execute_script("""
                function clickCenter(element) {
                    const rect = element.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    const clickEvent = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: centerX,
                        clientY: centerY
                    });
                    element.dispatchEvent(clickEvent);
                }
                arguments[0].scrollIntoView({behavior: "instant", block: "center"});
                clickCenter(arguments[0]);
            """, element)
        
        green_icon = WebDriverWait(fourth_agent_driver, 999).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'ANSWER')]")
            )
        )
        click_center_of_element(fourth_agent_driver, green_icon)
        print("Green circle element clicked in fourth agent!")

        try:
            
            video_count = fourth_agent_driver.execute_script(
                "return document.querySelectorAll('video.remote-videos_landscapeVideoElement__KIUeU').length;"
            )
            print("Number of <video> elements on page:", video_count)
        except Exception as e:
            print("Error getting video elements count:", e)
        
        time.sleep(5)

        try:
           
            WebDriverWait(fourth_agent_driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video.remote-videos_landscapeVideoElement__KIUeU"))
            )
            
           
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

       

        try:
            camera_button = WebDriverWait(fourth_agent_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='video-mute-btn']"))
            )
            print("Camera toggle button found. Clicking to turn off camera.")
            ActionChains(fourth_agent_driver).move_to_element(camera_button).click().perform()
            time.sleep(3)
            
           
            button_text_off = camera_button.find_element(By.XPATH, ".//span").text.strip()
            if "Unpause Video" in button_text_off:
                print("✅ Camera is off. Button shows:", button_text_off)
            else:
                print("❌ Camera is still on. Button shows:", button_text_off)
            
            print("Clicking camera toggle button again to turn on camera.")
            ActionChains(fourth_agent_driver).move_to_element(camera_button).click().perform()
            time.sleep(3)
            
           
            button_text_on = camera_button.find_element(By.XPATH, ".//span").text.strip()
            if "Pause Video" in button_text_on:
                print("✅ Camera is on. Button shows:", button_text_on)
            else:
                print("❌ Camera is not active. Button shows:", button_text_on)
        except Exception as e:
            print("Error during camera toggle test:", e)


       
        try:
            mic_button = WebDriverWait(fourth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='audio-mute-btn']"))
            )
           
            mic_state_before = mic_button.find_element(By.XPATH, ".//span").text
            print("Current microphone state text:", mic_state_before)
            
            
            print("Clicking microphone toggle button to change state.")
            ActionChains(fourth_agent_driver).move_to_element(mic_button).click().perform()
            time.sleep(3)
            
            
            mic_state_after = mic_button.find_element(By.XPATH, ".//span").text
            print("Microphone state text after click:", mic_state_after)
            
            if mic_state_before.strip().lower() == "mute audio" and "unmute" in mic_state_after.lower():
                print("✅ Microphone is muted.")
            elif mic_state_before.strip().lower() == "unmute audio" and "mute" in mic_state_after.lower():
                print("✅ Microphone is unmuted.")
            else:
                print("❌ Microphone state did not change as expected after first click.")
            
           
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
           
            sound_button = WebDriverWait(fourth_agent_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mute volume']"))
            )
            
            initial_class = sound_button.get_attribute("class")
            if "volume-control_muted__cVWPM" in initial_class:
                print("Sound is initially OFF.")
                initial_state = "off"
            else:
                print("Sound is initially ON.")
                initial_state = "on"
            
            
            print("Clicking sound toggle button to change state.")
            ActionChains(fourth_agent_driver).move_to_element(sound_button).click().perform()
            time.sleep(3)
            
            
            toggled_class = sound_button.get_attribute("class")
            if initial_state == "on":
                
                if "volume-control_muted__cVWPM" in toggled_class:
                    print("✅ Sound is muted after toggle.")
                else:
                    print("❌ Sound did not mute as expected.")
            else:
                
                if "volume-control_muted__cVWPM" not in toggled_class:
                    print("✅ Sound is unmuted after toggle.")
                else:
                    print("❌ Sound did not unmute as expected.")
            
            
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

        
        


    def delayed_fourth_agent():
        print("Waiting 25 seconds before starting fourth agent...") 
        time.sleep(25)  
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
        try:
            close_sheet = WebDriverWait(fifth_agent_driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close Sheet')]"))
            )
            close_sheet.click()
            print("Close Sheet button clicked")
        except TimeoutException:
            print("No Close Sheet button found, continuing...")


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

       
        try:
            camera_permission = fifth_agent_driver.execute_async_script("""
                const callback = arguments[arguments.length - 1];
                navigator.permissions.query({name: 'camera'}).then(result => {
                    callback(result.state);
                }).catch(err => callback("error"));
            """)
            if camera_permission == "denied":
                print("Camera permission is confirmed as denied.")
               
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
        def click_center_of_element1(driver, element):
            driver.execute_script("""
                function clickCenter(element) {
                    const rect = element.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    const clickEvent = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: centerX,
                        clientY: centerY
                    });
                    element.dispatchEvent(clickEvent);
                }
                arguments[0].scrollIntoView({behavior: "instant", block: "center"});
                clickCenter(arguments[0]);
            """, element)
        click_center_of_element1(fifth_agent_driver, green_icon)
        print("Green circle element clicked in fifth agent!")

        

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
        time.sleep(230) 
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

   
    agent_thread = threading.Thread(target=open_agent_browser)
    agent_thread.start()
    
    
    time.sleep(15)

   
    from LOGIN import Login_page
    login_page = Login_page(driver)
    login_page.login_to_cloudbreak_customer()

    
    agent_alt_thread = threading.Thread(target=delayed_alt_agent)
    agent_alt_thread.start()

   
    fourth_agent_thread = threading.Thread(target=delayed_fourth_agent)
    fourth_agent_thread.start()

   
    fifth_agent_thread = threading.Thread(target=delayed_fifth_agent)
    fifth_agent_thread.start()

    client_thread = threading.Thread(target=delayed_client)
    client_thread.start()
    time.sleep(5)
    
    language_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Russian')]")))
    ActionChains(driver).move_to_element(language_button).click().perform()


    time.sleep(10)
    
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
    
    
    try:
        camera_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='video-mute-btn']"))
        )
        
        camera_text_initial = camera_button.find_element(By.XPATH, ".//span").text.strip()
        print("Initial camera state:", camera_text_initial)
        
       
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
        
       
        ActionChains(driver).move_to_element(camera_button).click().perform()
        time.sleep(3)
        camera_text_revert = camera_button.find_element(By.XPATH, ".//span").text.strip()
        print("Camera state after revert:", camera_text_revert)
    except Exception as e:
        print("Error toggling camera status:", e)

   
    try:
        sound_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Mute volume']"))
        )
        sound_class_initial = sound_button.get_attribute("class")
        print("Initial sound button class:", sound_class_initial)
        
        ActionChains(driver).move_to_element(sound_button).click().perform()
        time.sleep(3)
        
        sound_class_after = sound_button.get_attribute("class")
        print("Sound button class after toggle:", sound_class_after)
        
        if ("V_OoXHutaK1ot9aXxMLh" in sound_class_initial and "V_OoXHutaK1ot9aXxMLh" not in sound_class_after) or \
        ("V_OoXHutaK1ot9aXxMLh" not in sound_class_initial and "V_OoXHutaK1ot9aXxMLh" in sound_class_after):
            print("✅ Sound toggled successfully.")
        else:
            print("❌ Sound state did not toggle as expected.")
        
        
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
        print("Leave Call button is clickable. Clicking on it...")
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
        print("URL successfully updated to https://cloudbreak-customer-ui.qa.cloudbreak.us/call-error")
    except Exception as e:
        print("Error: URL did not change to expected: https://cloudbreak-customer-ui.qa.cloudbreak.us/call-error", e)

    assert video_active, f"Failed to activate video after {max_attempts} attempts!"
    screenshot_path = f"video_test_screenshot_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)
    print(f"\nScreenshot saved: {screenshot_path}")
    allure.step("Test completed: Video activated")

   
    agent_thread.join()
    agent_alt_thread.join()
    fourth_agent_thread.join()
    fifth_agent_thread.join()
    client_thread.join()
    
    agent_thread.join()
    


    