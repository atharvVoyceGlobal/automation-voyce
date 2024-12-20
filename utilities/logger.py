import datetime
import os


class Logger:
    # Относительный путь к папке logs
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Создаем директорию, если она не существует
    file_name = os.path.join(log_dir, f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.logs")

    @classmethod
    def write_log_to_file(cls, data: str):
        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_start_step(cls, method: str):
        test_name = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Start time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Start name method: {method}\n"
        data_to_add += "\n"

        cls.write_log_to_file(data_to_add)


    @classmethod
    def add_end_step(cls, url: str, method: str):
        data_to_add = f"End time: {str(datetime.datetime.now())}\n"
        data_to_add += f"End name method: {method}\n"
        data_to_add += f"URL: {url}\n"
        data_to_add += f"\n-----\n"

        cls.write_log_to_file(data_to_add)

    @classmethod
    def add_error_log(cls, method: str, error: str):
        data_to_add = f"Error in method: {method}\n"
        data_to_add += f"Error time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Error details: {error}\n"
        data_to_add += f"\n-----\n"

        cls.write_log_to_file(data_to_add)
