import psycopg2
from pgvector.psycopg2 import register_vector
import os
import dotenv

load_dotenv()

sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")



def get_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="lolo_memory",
        user=sql_user,
        password=sql_password,
        port="5432"
    )
    register_vector(conn)
    return conn
