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
from zenq.datapreparation.preparation import data_prep
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
from sqlalchemy.exc import IntegrityError
from .config import db_uri
from zenq.logger import CustomFormatter, bcolors
import logging
import os
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(funcName)s %(msg)s')
logger = logging.getLogger(os.path.basename(__file__))
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(CustomFormatter())

logger.addHandler(file_handler)
logger.addHandler(ch)
LOGS = Facts.LOGS
# Facts = Facts()
# metadata, engine = Facts.connect_to_db(db_uri)
# session = sessionmaker(bind=engine)()
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

def insert_log(filename, func_name, file_no, message):
    session = Session()
    log = LOGS(
        FILE_NAME=filename,
        FUNC_NAME=func_name,
        FILE_NO=file_no,
        MESSAGE=message,
        LOAD_TIME=datetime.now()
    )
    session.add(log)
    session.commit()
    session.close()
    
def insert_facts(filename, customer_id, gender, invoice_id, date, quantity, total_price):
    data = data_prep()
    try:
        data.read_data(filename)
    except FileNotFoundError:
        print(f"Error: File {filename} not found. Please try again.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: File {filename} is empty. Please try again.")
        return
    df = data.final_data()
    if df is None:
        print(f"Error: No data found. Please call the 'read_data' method first to load the data.")
        return
    required_columns = [customer_id, gender, invoice_id, date, quantity, total_price]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return
    print(f"Inserting facts for {customer_id} from file csv")
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
    
    insert_log(os.path.basename(__file__), 'insert_facts', 1, 'Facts have been inserted successfully.')
   
    logger.error(f"{insert_facts.__name__}")
    logger.warning(f"{insert_facts.__name__}")  
    logger.info(f"{insert_facts.__name__}")
