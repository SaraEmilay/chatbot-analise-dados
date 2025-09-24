from sqlalchemy import create_engine
import pandas as pd

DATABASE_URL = "postgresql://postgres:senha@localhost:5432/meu_banco"

engine = create_engine(DATABASE_URL)

def run_sql(sql: str):
    """Executa SQL e retorna um DataFrame"""
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df
