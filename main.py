from src.extract import fetch_users, get_data_csv
from src.transform import transform_data
from src.load import incremental_load


def main():
    df_user = fetch_users()
    df_sale = get_data_csv()

    df_transform = transform_data(df_user,df_sale)

    incremental_load(df_transform,'sales_data','sales')
    

if __name__ == "__main__":
    main()