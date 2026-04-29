from src.database import PostgresConnection
import pandas as pd

db = PostgresConnection()

engine = db.get_engine()

def get_max_order_id():
    query = """
    select max(order_id) from sales.sales_data
    """
    result = pd.read_sql(
        query,
        engine
    )
    return result.iloc[0,0]

def incremental_load(df,table_name,schema):
    max_id = get_max_order_id()
    if max_id is None:
        max_id = 0
    new_df = df[df['order_id'] > max_id]
    if new_df.empty:
        print('No new rows')
    else:
        new_df.to_sql(
            name=table_name,
            con=engine,
            schema=schema,
            if_exists='append',
            index=False
        )
    print(f'Loaded {len(new_df)} rows')