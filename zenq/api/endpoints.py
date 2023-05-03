import sqlalchemy
import pandas as pd
import IPython
import re
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
    



def insert_logs_to_db(log_file_path='zenq/api/logs.log'):
    # Open the log file and read all its contents
    with open(log_file_path, 'r') as f:
        log_contents = f.read()

    # Remove escape characters and color codes from the log lines
    log_contents = re.sub(r'\x1b\[\d+;\d+m', '', log_contents)

    # Split the contents into individual lines
    log_lines = [line.split('\x1b[0m')[0] for line in log_contents.split('\n')]
    log_lines = [line for line in log_lines if line.strip()]
    print(type(log_lines))
    # Define a regular expression to extract the required information from each line
    # log_regex = re.compile(r"/(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}),\d{3}\s/\s(.+?)\s/\s(.+?)\s/\s(.+?)\s/\s(.+?)/(\d+)/")
    # log_pattern = re.compile(log_regex)

    # Loop through each line, extract the required information, and add it to the database
    for line in log_lines:
        my_string = line
        # Extract timestamp
        timestamp = my_string.split('/')[1].strip()
        print(f"timestamp {timestamp}")
         
        # Extract filename
        filename = my_string.split('/')[2].strip()
        print(f"filename {filename}")
         
        # Extract error level
        error_level = my_string.split('/')[3].strip()
        print(f"error_level {error_level}")
         
        # Extract function name
        function_name = my_string.split('/')[4].strip()
        print(f"function_name {function_name}")
        
        # Extract message
        my_message = my_string.split('/')[5].strip()
        print(f"my_message {my_message}")
        
        # Extract line number
        line_number = my_string.split('/')[7].strip().rstrip('/')
        print(f"line_number {line_number}")
       
        load_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S,%f')
        log_obj = LOGS(level=error_level, file_name=filename, func_name=function_name, message=my_message, line_number=int(line_number), load_time=load_time)
        session.add(log_obj)
    # # for line in log_lines:
    #     match = log_pattern.match(line)
    #     if match:
    #         load_time_str, file_name, level, func_name, message, line_number = match.groups()
    #         load_time = datetime.strptime(load_time_str, '%Y-%m-%d %H:%M:%S')
    #         log_obj = LOGS(level=level, file_name=file_name, func_name=func_name, message=message, line_number=int(line_number), load_time=load_time)
    #         session.add(log_obj)
    # Commit the changes and close the session
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
    
    # insert_log(os.path.basename(__file__), 'insert_facts', 1, 'Facts have been inserted successfully.')
   
    logger.error(f"{insert_facts.__name__} / ERROR FOR INSERTING FACTS MESSAGE")
    logger.warning(f"{insert_facts.__name__} / WARNING MESSAGE")  
    logger.info(f"{insert_facts.__name__} / INFO MESSAGE")
