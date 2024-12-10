import pytest


@pytest.fixture(scope='function')
def set_up():
    print("start test")
    yield
    print("finish test")


@pytest.fixture(scope='module')
def set_group():
    print("Entry")
    yield
    print("Exit")

# def set_up():
#     print("start test")
#     driver = webdriver.Chrome(executable_path='\\Users\\hallway\\PycharmProjects\\resource\\chromedriver')
#     url = 'https://www.saucedemo.com/'
#     self.driver.get(self.url)
#     yield
#     driver.quit()
#     print("finish test")
