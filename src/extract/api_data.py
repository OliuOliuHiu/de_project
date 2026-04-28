import requests 
import pandas as pd
from src.config import API_URL

def fetch_users():
    response = requests.get(API_URL)

    data = response.json()

    return pd.DataFrame(data)
