# my_db_module.py
from sqlalchemy import create_engine
import pandas as pd

# Create a database engine.
# Adjust the connection string as needed.
engine = create_engine("postgresql://anubhab@localhost:5432/text_to_sql_gen")

def execute_query(query: str):
    try:
        result = pd.read_sql(query, engine)
        return result
    except Exception as e:
        return f"Query execution error: {e}"
