import datetime
import os

class Base:
    def __init__(self, driver):
        self.driver = driver

    """"method get current url"""

    def get_current_url(self):
        get_url = self.driver.current_url
        print("current url " + get_url)

    """method assert words"""

    def assert_word2(self, word, result):
        # Если 'result' является WebElement, извлекаем его текст
        if hasattr(result, 'text'):
            value_result = result.text
        else:
            value_result = str(result)

        value_word = str(word)

        # Удаление нечисловых символов (например, валюты и запятых)
        value_result = ''.join(filter(lambda x: x.isdigit() or x == '.', value_result))
        value_word = ''.join(filter(lambda x: x.isdigit() or x == '.', value_word))

        # Проверка на пустую строку и задание значения по умолчанию
        value_word_float = float(value_word) if value_word else 0.0
        value_result_float = float(value_result) if value_result else 0.0

        # Преобразование чисел с плавающей точкой в целые числа для сравнения
        value_word_int = int(value_word_float)
        value_result_int = int(value_result_float)

        print(f" Actual '{value_word_int}', Expected '{value_result_int}'")

        assert value_word_int == value_result_int, f"Ожидалось '{value_result_int}', получено '{value_word_int}'"
    def assert_field_value(self, field, expected_value):
        actual_value = field.get_attribute("value")
        print(f"Actual value: '{actual_value}', Expected value: '{expected_value}'")
        assert actual_value == expected_value, f"Expected value '{expected_value}' but got '{actual_value}'"
        print("Value matches as expected")

    def assert_word(self, word, result):
        if hasattr(word, 'text'):
            value_word = word.text
        else:
            value_word = word

        print(f"Actual text: '{value_word}', Expected text: '{result}'")
        assert value_word == result, f"Expected '{result}', Result '{value_word}'"
        print("good word")

    def assert_no_word(self, word, unwanted_result):
        value_word = word.text
        assert unwanted_result not in value_word
        print("good, the word is absent")

    """method screen shot"""

    def screenshot(self):
        # Ensure the 'screen' directory exists
        screen_dir = "screen"
        if not os.path.exists(screen_dir):
            os.makedirs(screen_dir)
    
        # Generate a timestamped filename for the screenshot
        now_date = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")
        photo = f"photo_{now_date}.png"
        file_path = os.path.join(screen_dir, photo)
    
        # Save the screenshot
        self.driver.save_screenshot(file_path)
        print(f"[INFO] Screenshot saved: {file_path}")

    """method assert url"""

    def assert_url(self, result):
        get_url = self.driver.current_url
        assert get_url == result
        print("value url")

    """method assert location"""

    def assert_location(self, element, x, y):
        location = element.location
        assert location['x'] == x
        assert location['y'] == y
        print("Location is good")
        print(f'x: {location["x"]}')
        print(f'y: {location["y"]}')

        """method assert background color"""

    def assert_background_color(self, element, expected_color):
        background_color = element.value_of_css_property('background-color')
        assert background_color == expected_color


