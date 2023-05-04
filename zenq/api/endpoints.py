import sqlalchemy
import pandas as pd
import IPython
import re
from sqlalchemy.exc import IntegrityError
import ipywidgets
from sqlalchemy import Sequence, UniqueConstraint, create_engine, desc, asc
from datetime import datetime
from sqlalchemy import func
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
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s/ %(funcName)s/ %(msg)s/')

logger = logging.getLogger(os.path.basename(__file__))
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
file_handler = logging.FileHandler('zenq/api/logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(CustomFormatter())

logger.addHandler(file_handler)
logger.addHandler(ch)
LOGS = Facts.LOGS
# create a formatter object with the desired format
# Facts = Facts()
# metadata, engine = Facts.connect_to_db(db_uri)
# session = sessionmaker(bind=engine)()
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()


def insert_logs_to_db(log_file_path='zenq/api/logs.log'):
    with open(log_file_path, 'r') as f:
        log_contents = f.read()
    log_contents = re.sub(r'\x1b\[\d+;\d+m', '', log_contents)
    log_lines = [line.split('\x1b[0m')[0] for line in log_contents.split('\n')]
    log_lines = [line for line in log_lines if line.strip()]
    print(type(log_lines))
    for line in log_lines:
        my_string = line
        timestamp = my_string.split('/')[1].strip()
        # print(f"timestamp {timestamp}")        
        filename = my_string.split('/')[2].strip()
        # print(f"filename {filename}")         
        error_level = my_string.split('/')[3].strip()
        # print(f"error_level {error_level}")
        function_name = my_string.split('/')[4].strip()
        # print(f"function_name {function_name}")
        my_message = my_string.split('/')[5].strip()
        # print(f"my_message {my_message}")
        line_number = my_string.split('/')[7].strip().rstrip('/')
        # print(f"line_number {line_number}")
        load_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S,%f')
        log_obj = LOGS(level=error_level, file_name=filename, func_name=function_name, message=my_message, line_number=int(line_number), load_time=load_time)
        session.add(log_obj)
    session.commit()
    session.close()

def update_log(log_file_path='zenq/api/logs.log'):
    # Get the max timestamp from the LOGS table
    max_time = session.query(func.max(LOGS.load_time)).scalar()
    if not max_time:
        max_time = datetime.min

    with open(log_file_path, 'r') as f:
        log_contents = f.read()
    log_contents = re.sub(r'\x1b\[\d+;\d+m', '', log_contents)
    log_lines = [line.split('\x1b[0m')[0] for line in log_contents.split('\n')]
    log_lines = [line for line in log_lines if line.strip()]

    for line in log_lines:
        my_string = line
        timestamp = my_string.split('/')[1].strip()
        load_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S,%f')
        if load_time > max_time:
            filename = my_string.split('/')[2].strip()
            error_level = my_string.split('/')[3].strip()
            function_name = my_string.split('/')[4].strip()
            my_message = my_string.split('/')[5].strip()
            line_number = my_string.split('/')[7].strip().rstrip('/')
            log_obj = LOGS(level=error_level, file_name=filename, func_name=function_name, message=my_message, line_number=int(line_number), load_time=load_time)
            session.add(log_obj)
    session.commit()
    session.close()

        
def insert_facts(filename, customer_id, gender, invoice_id, date, quantity, total_price):
    data = data_prep()
    try:
        data.read_data(filename)
    except FileNotFoundError:
        # print(f"Error: File {filename} not found. Please try again.")
        logger.error(f"{insert_facts.__name__}/ {filename} not found. Please try again.") 

        return
    except pd.errors.EmptyDataError:
        logger.error(f"{insert_facts.__name__}/ {filename} is empty. Please try again") 
        return
    df = data.final_data()
    if df is None:
        logger.error(f"{insert_facts.__name__}/ No data found. Please call the 'read_data' method first to load the data.") 
        return
    required_columns = [customer_id, gender, invoice_id, date, quantity, total_price]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        logger.warning(f"{insert_facts.__name__}/ Missing columns: {missing_columns}.") 
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
            logger.warning(f"{insert_facts.__name__}/ Skipping row with duplicate invoice_id: {row[invoice_id]}.")           
            continue
    return "Finished inserting facts"
    session.commit()           
    session.close()
    
    # insert_log(os.path.basename(__file__), 'insert_facts', 1, 'Facts have been inserted successfully.')
   
    # logger.error(f"{insert_facts.__name__} / ERROR FOR INSERTING FACTS MESSAGE")
    # logger.warning(f"{insert_facts.__name__} / WARNING MESSAGE")  
    # logger.info(f"{insert_facts.__name__} / INFO MESSAGE")
