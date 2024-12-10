import os
from pymongo import MongoClient
from ev import EV

def get_connection1():      #Admin
    global client1
    os.environ['SSL_CERT_FILE'] = EV.SSL
    try:
        # Подключение к MongoDB
        client1 = MongoClient(EV.mongo_client)

        # Проверка подключения к базе данных MongoDB
        if client1.server_info():
            print("MongoDB database connection successfully established.")
            return client1
        else:
            print("Failed to connect to MongoDB database.")
    except Exception as e:
        print("An error occurred while connecting to the database:", e)
    return client1


def get_connection():      #Покупатель
    global client
    os.environ['SSL_CERT_FILE'] = EV.SSL
    try:
        # Подключение к MongoDB
        client = MongoClient(EV.mongo_client1)


        # Проверка подключения к базе данных MongoDB
        if client.server_info():
            print("MongoDB database connection successfully established.")
            return client
        else:
            print("Failed to connect to MongoDB database.")
    except Exception as e:
        print("An error occurred while connecting to the database:", e)
    return client


def assert_equal(a, b, message):
    if a != b:
        raise AssertionError(f"Assert failed: {message}")


class Database:
    def __init__(self):
        self.client = get_connection()
        self.client1 = get_connection1()

    """Assert database data"""
