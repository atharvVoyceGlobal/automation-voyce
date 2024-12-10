# import re
# import time
#
# # Инициализация переводчика
# translator = Translator()
#
# # Функция для перевода текста внутри кавычек с корректной заменой русских строк
# def translate_strings_in_quotes(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#
#     # Регулярное выражение для поиска строк внутри одинарных или двойных кавычек
#     quotes_pattern = re.compile(r'(f?["\'])(.*?)(["\'])')
#
#     new_content = []
#     for line in lines:
#         # Проверяем, является ли строка закомментированной
#         if line.strip().startswith('#'):
#             new_content.append(line)
#             continue
#
#         matches = quotes_pattern.findall(line)
#         if matches:
#             new_line = line
#             for match in matches:
#                 opening_part = match[0]  # Здесь может быть f перед строкой
#                 inside_quotes = match[1]  # Текст внутри кавычек
#                 closing_quote = match[2]  # Закрывающая кавычка
#
#                 if re.search(r'[а-яА-ЯёЁ]', inside_quotes):  # Проверяем, есть ли русские символы
#                     try:
#                         # Переводим русские части строки с задержкой между запросами
#                         translated = translator.translate(inside_quotes, src='ru', dest='en').text
#                         time.sleep(1)  # Задержка в 1 секунду между запросами
#                         # Заменяем оригинальную строку переведенной
#                         new_line = new_line.replace(f"{opening_part}{inside_quotes}{closing_quote}", f"{opening_part}{translated}{closing_quote}")
#                     except Exception as e:
#                         print(f"Error translating text: {e}")
#                         continue
#             new_content.append(new_line)
#         else:
#             new_content.append(line)
#
#     # Перезаписываем файл с корректировкой
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.writelines(new_content)
#
# # Функция для обработки всех файлов в директории
# def process_directory(directory):
#     import os
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.py'):
#                 file_path = os.path.join(root, file)
#                 translate_strings_in_quotes(file_path)
#                 print(f'File processed: {file_path}')
#
# # Указываем путь к проекту
# project_directory = '/Users/nikitabarshchuk/PycharmProjects/pythonProject3/customer_pages'
# process_directory(project_directory)
