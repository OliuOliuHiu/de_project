from sqlalchemy import text
from src.database import PostgresConnection
import uuid
import pandas as pd
from datetime import datetime
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

def get_incremental_rows(df):
    max_id = get_max_order_id()
    if max_id is None:
        max_id = 0
    new_df = df[df['order_id'] > max_id]
    return new_df

def validate_staging(staging_table_name,schema):

    query = f"""
    SELECT order_id, COUNT(*)

    FROM {schema}.{staging_table_name}

    GROUP BY order_id

    HAVING COUNT(*) > 1
    """

    duplicate_df = pd.read_sql(
        query,
        engine
    )

    if not duplicate_df.empty:

        raise Exception(
            "Duplicate order_id found in staging"
        )

def merge_to_final(table_name,schema_sales,schema_staging):

    query = f"""
    INSERT INTO {schema_sales}.{table_name}

    SELECT *
    FROM {schema_staging}.{table_name}
    """

    with engine.begin() as conn:

        conn.execute(
            text(query)
        )

    print("Merge completed")


def insert_metadata(batch_id,row_count,status,schema,table_name):
    query = text(f"""
    INSERT INTO {schema}.{table_name} (

        batch_id,
        load_time,
        row_count,
        status

    )

    VALUES (

        :batch_id,
        :load_time,
        :row_count,
        :status
    )
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "batch_id": batch_id,
                "load_time": datetime.now(),
                "row_count": row_count,
                "status": status
            }
        )

def load_to_staging(df,staging_table_name,schema):
    df.to_sql(
        name=staging_table_name,
        con=engine,
        schema=schema,
        if_exists='replace',
        index=False,
        method='multi',
        chunksize=1000
    )
    print(f"Loaded {len(df)} rows into staging")

def incremental_load(df,schema_table,schema_staging,table_name):
    batch_id = str(uuid.uuid4())
    print(f"Batch ID: {batch_id}")
    new_df = get_incremental_rows(df)
    rows_count = len(new_df)
    try:
        if new_df.empty:
            print("No new data to load")
            insert_metadata(batch_id,rows_count,"No new data",schema_staging,"pipeline_metadata")
            return
        load_to_staging(new_df,table_name,schema_staging)
        validate_staging(table_name,schema_staging)
        merge_to_final(table_name,schema_table,schema_staging)
        insert_metadata(batch_id,rows_count,'Success',schema_staging,"pipeline_metadata")
    except Exception as e:
        insert_metadata(batch_id,0,'Fail',schema_staging,"pipeline_metadata")
        print(
            f"Pipeline failed: {e}"
        )


