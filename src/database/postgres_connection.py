from sqlalchemy import create_engine
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

class PostgresConnection:
    def __init__(self):
        self.database_url = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        self.engine = create_engine(self.database_url)
        
    def get_engine(self):
        return self.engine 