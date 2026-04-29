import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("USER_API_URL")

DATA_PATH = './data/orders.csv'

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")