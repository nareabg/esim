import sqlalchemy
import pandas as pd
import IPython
from sqlalchemy.exc import IntegrityError
import ipywidgets
from sqlalchemy import Sequence, UniqueConstraint, create_engine, desc, asc
from datetime import datetime
from sqlalchemy import create_engine
from .tables import  Facts 
from sqlalchemy.orm import sessionmaker
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
from sqlalchemy.exc import IntegrityError
from .config import db_uri


engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

# def insert_facts(filename, customer_id, gender, invoice_id, date, quantity, total_price):
#     """

#     Parameters
#     ----------
#     filename :
        
#     customer_id :
        
#     gender :
        
#     invoice_id :
        
#     date :
        
#     quantity :
        
#     total_price :
        

#     Returns
#     -------

#     """
#     # Read the CSV file into a pandas DataFrame
#     df = pd.read_csv(filename)
#     print(f"Inserting facts for {customer_id} from file {filename}")
#     # Loop through the rows of the DataFrame and insert each one into the database
#     for i, row in df.iterrows():
#         fact = Facts(
#             customer_id=row[customer_id],
#             gender=row[gender],
#             invoice_id=row[invoice_id],
#             date=row[date],
#             quantity=row[quantity],
#             total_price=row[total_price]
#         )
#         try:
#             session.add(fact)
#             session.commit()
#         except IntegrityError:
#             session.rollback()
#             print(f"Skipping row with duplicate invoice_id: {row[invoice_id]}")
#             continue
#     print("Finished inserting facts")
#     session.close()

def insert_facts(filename, customer_id, gender, invoice_id, date, quantity, total_price):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: File {filename} not found. Please try again.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: File {filename} is empty. Please try again.")
        return

    # Check if all required columns are present in the DataFrame
    required_columns = [customer_id, gender, invoice_id, date, quantity, total_price]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return

    print(f"Inserting facts for {customer_id} from file {filename}")
    # Loop through the rows of the DataFrame and insert each one into the database
    for i, row in df.iterrows():
        fact = Facts(
            customer_id=row[customer_id],
            gender=row[gender],
            invoice_id=row[invoice_id],
            date=row[date],
            quantity=row[quantity],
            total_price=row[total_price]
        )
        try:
            session.add(fact)
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Skipping row with duplicate invoice_id: {row[invoice_id]}")
            continue
    print("Finished inserting facts")
    session.close()