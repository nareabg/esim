
import psycopg2
 
def test():
    print('ok')
    
    
def connect():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="mysecretpassword",
        database="postgres"
    )
    return conn


# add class insert,update, alter

def create_schema(conn, schema_name):
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        conn.commit()

def create_table(conn, schema_name, table_name, columns):
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({columns})")
        conn.commit()

def insert_data(conn, schema_name, table_name, values):
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO {schema_name}.{table_name} VALUES ({values})")
        conn.commit()


# add customization labels for companies