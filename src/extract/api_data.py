import requests 
import pandas as pd
from src.config import API_URL

def fetch_users():
    response = requests.get(API_URL)
    print(f'Status code: {response.status_code}')
    data = response.json()
    return pd.DataFrame(data)
