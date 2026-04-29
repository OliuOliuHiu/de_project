import pandas as pd

def transform_data(df_api,df_csv):
    df_api_users = df_api.rename(
        columns={"id": "user_id", "name": "customer_name"}
    )

    df_api_users['user_id'] = 'uc' + df_api_users['user_id'].astype(str)

    df_api_users['city'] = df_api_users.apply(
        lambda row: row['address']['city'],
        axis=1
    )

    df_api_users['company_name'] = df_api_users.apply(
        lambda row: row['company']['name'],
        axis=1
    )

    df_api_main = df_api_users[
        ['user_id', 'customer_name', 'email', 'phone', 'city', 'company_name']
    ]

    df_csv['user_id'] = 'uc' + df_csv['user_id'].astype(str)

    df_fact_sales = pd.merge(
        df_csv,
        df_api_main,
        on='user_id',
        how='left'
    )

    df_fact_sales = df_fact_sales.fillna('Unknown')

    df_fact_sales['total_amount'] = (
        df_fact_sales['quantity'] * df_fact_sales['price']
    )

    df_fact_sales['order_date'] = pd.to_datetime(
        df_fact_sales['order_date']
    )

    df_fact_sales['order_month'] = (
        df_fact_sales['order_date'].dt.strftime("%Y-%m")
    )

    columns_list = [
        'order_id',
        'user_id',
        'customer_name',
        'city',
        'product',
        'quantity',
        'total_amount',
        'order_month'
    ]

    df_fact_sales = df_fact_sales[columns_list]

    return df_fact_sales