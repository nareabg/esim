import os
import numpy as np
import pandas as pd
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

class data_prep():
    
    def __init__(self,data = None):
        self.data = data

    def read_data(self, filename):
        try:
            self.data = pd.read_csv(filename)
        except FileNotFoundError:
            print(f"Error: File {filename} not found. Please try again.")
            return
        except pd.errors.EmptyDataError:
            print(f"Error: File {filename} is empty. Please try again.")
        return self.data.head()
   
    def shape(self):
        return self.data.shape, list(self.data.columns)
    
    def info(self):
        return self.data.info()
    
    def num_of_duplicate(self):
        return self.data.duplicated().sum()

    def num_of_null(self):
        return self.data.isnull().sum()

def num_of_unique_in_column(self, column):
    if column not in self.data.columns:
        print(f"Error: column '{column}' does not exist in the data. Please try again.")
        return None
    else:
        return self.data[column].nunique()
    logger.error(f"{num_of_unique_in_column.__name__}")
    
    def final_data(self):

        data = self.data.copy() 
        data = data.drop_duplicates()
        data = data.dropna()
        logger.info(f"{final_data.__name__}")
        return data


