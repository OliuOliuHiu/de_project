import pandas as pd
from src.extract import fetch_users, get_data_csv


df_api = fetch_users()
print(df_api.head(5))