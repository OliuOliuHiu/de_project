import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("USER_API_URL")

DATA_PATH = './data/orders.csv'
