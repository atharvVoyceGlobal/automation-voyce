import os
import shutil
import chromedriver_autoinstaller

def install_browser_and_driver():
    print("Устанавливаем ChromeDriver...")
    chromedriver_autoinstaller.install()  # Автоматическая установка ChromeDriver
    chromedriver_path = chromedriver_autoinstaller.get_chromedriver_path()
    print(f"ChromeDriver успешно установлен по пути: {chromedriver_path}")

    # Проверяем наличие Chrome или Chromium
    chrome_path = (
        shutil.which("google-chrome")
        or shutil.which("google-chrome-stable")
        or shutil.which("chromium-browser")
    )
    if not chrome_path:
        print("Доступные пути в системе:")
        print(os.environ["PATH"])
        raise FileNotFoundError("Google Chrome или Chromium не найдены. Убедитесь, что они установлены и добавлены в PATH.")

    print(f"Браузер найден по пути: {chrome_path}")

    # Проверяем версию браузера
    try:
        browser_version = os.popen(f"{chrome_path} --version").read().strip()
        print(f"Версия браузера: {browser_version}")
    except Exception as e:
        print("Ошибка при получении версии браузера:", e)
        raise

    return chrome_path, chromedriver_path

if __name__ == "__main__":
    install_browser_and_driver()
