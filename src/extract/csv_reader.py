import pandas as pd
from src.config import DATA_PATH

def get_data_csv():
    df = pd.read_csv(DATA_PATH)
    return df