from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from env import EV

class Login_page:
    def __init__(self, driver):
        self.driver = driver

    def login_to_cloudbreak_customer(self):
        # Переходим на страницу авторизации
        self.driver.get(EV.CUSTOMER_URL)
        
        # Ждем появления поля для логина
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login-username-input"))
        )
        
        # Вводим логин
        username_input.clear()
        username_input.send_keys(EV.CUSTOMER_LOGIN)
        
        # Ждем и кликаем по кнопке входа
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div[1]/div[2]/div[2]/div/div/div[1]/div/button'))
        )
        
        # Используем ActionChains для клика
        try:
            ActionChains(self.driver).move_to_element(login_button).click().perform()
        except:
            # Если ActionChains не сработал, используем JavaScript
            self.driver.execute_script("arguments[0].click();", login_button)