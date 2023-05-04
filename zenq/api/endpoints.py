import pandas as pd
import IPython
import re
import logging
import os
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Sequence, UniqueConstraint, create_engine, desc, asc, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from zenq.logger import CustomFormatter, bcolors 
from zenq.datapreparation.preparation import data_prep
from .tables import  Facts 
from .config import db_uri

# Set up logging 
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

# Define the LOGS table and create the database session
LOGS = Facts.LOGS
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()


def insert_logs_to_db(log_file_path='zenq/api/logs.log'):
    """

    Parameters
    ----------
    log_file_path :
         (Default value = 'zenq/api/logs.log')

    Returns
    -------
    inserts data into database LOGS table
    """
    with open(log_file_path, 'r') as f:
        log_contents = f.read()
        
    # Remove escape sequences from the log file    
    log_contents = re.sub(r'\x1b\[\d+;\d+m', '', log_contents)
    
    # Split the log file into lines and remove empty lines
    log_lines = [line.split('\x1b[0m')[0] for line in log_contents.split('\n')]
    log_lines = [line for line in log_lines if line.strip()]
    
    # Parse the log data and insert it into the database
    for line in log_lines:
        my_string = line
        timestamp = my_string.split('/')[1].strip()     
        filename = my_string.split('/')[2].strip()   
        error_level = my_string.split('/')[3].strip()
        function_name = my_string.split('/')[4].strip()
        my_message = my_string.split('/')[5].strip()
        line_number = my_string.split('/')[7].strip().rstrip('/')
        load_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S,%f')
        log_obj = LOGS(level=error_level, file_name=filename, func_name=function_name, message=my_message, line_number=int(line_number), load_time=load_time)
        session.add(log_obj)
        
    # Commit the changes and close the session    
    session.commit()
    session.close()

def update_log(log_file_path='zenq/api/logs.log'):
    """

    Parameters
    ----------
    log_file_path :
         (Default value = 'zenq/api/logs.log')

    Returns
    -------
    inserts into LOGS table data that are bigger than the mac date in the database
    """
    
    # Get the max timestamp from the LOGS table
    max_time = session.query(func.max(LOGS.load_time)).scalar()
    if not max_time:
        max_time = datetime.min

    # Read the log file and remove escape sequences
    with open(log_file_path, 'r') as f:
        log_contents = f.read()
    log_contents = re.sub(r'\x1b\[\d+;\d+m', '', log_contents)
    
    # Split the log file into lines and remove empty lines
    log_lines = [line.split('\x1b[0m')[0] for line in log_contents.split('\n')]
    log_lines = [line for line in log_lines if line.strip()]

    # Parse the log data and insert it into the database
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
            
    # Commit the changes and close the session         
    session.commit()
    session.close()

        
def insert_facts(filename, customer_id, gender, invoice_id, date, quantity, total_price):
    """

    Parameters
    ----------
    filename : the name of the file (ex. globbing.csv)
        
    customer_id : customer id column mapping
        
    gender : gender column mapping
        
    invoice_id : transaction id column mapping
        
    date : date column mapping
        
    quantity : quantity/weight column mapping
        
    total_price : price column mapping
        

    Returns
    -------
    inserts data into FACTS table of database
    """
    
    # create an instance of the data_prep class
    data = data_prep()
    
    try:
        # read the CSV file using the read_data method from the data_prep class
        data.read_data(filename)
    except FileNotFoundError:
        # log an error if the file is not found
        logger.error(f"{insert_facts.__name__}/ {filename} not found. Please try again.") 

        return
    except pd.errors.EmptyDataError:
        # log an error if the file is empty
        logger.error(f"{insert_facts.__name__}/ {filename} is empty. Please try again") 
        return
    
    # get the final data in the required format for inserting into the database
    df = data.final_data()
    if df is None:
        # log an error if no data is found
        logger.error(f"{insert_facts.__name__}/ No data found. Please call the 'read_data' method first to load the data.") 
        return
    # check if all the required columns are present in the data
    required_columns = [customer_id, gender, invoice_id, date, quantity, total_price]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        # log a warning if any required column is missing
        logger.warning(f"{insert_facts.__name__}/ Missing columns: {missing_columns}.") 
        return
    # iterate over the rows in the data and insert facts into the database
    print(f"Inserting facts for {customer_id} from file csv")
    for i, row in df.iterrows():
        # create a new instance of the Facts class for each row in the data
        fact = Facts(
            customer_id=row[customer_id],
            gender=row[gender],
            invoice_id=row[invoice_id],
            date=row[date],
            quantity=row[quantity],
            total_price=row[total_price]
        )
        try:
            # add the fact to the session and commit the changes to the database
            session.add(fact)
            session.commit()
        except IntegrityError:
            # if the invoice_id already exists in the database, log a warning and skip the row
            session.rollback()
            logger.warning(f"{insert_facts.__name__}/ Skipping row with duplicate invoice_id: {row[invoice_id]}.")           
            continue
        
    logger.info(f"{insert_facts.__name__}/ Finished inserting facts.")           
    return "Finished inserting facts"

    # commit and close the session after all the facts have been inserted
    session.commit()           
    session.close()
     