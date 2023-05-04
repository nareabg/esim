import os
import numpy as np
import pandas as pd
import logging
import os
from zenq.logger import CustomFormatter, bcolors

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(funcName)s %(msg)s')
logger = logging.getLogger(os.path.basename(__file__))
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
file_handler = logging.FileHandler('zenq/api/logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(CustomFormatter())
logger.addHandler(file_handler)
logger.addHandler(ch)

class data_prep():
    
    def __init__(self,data = None):
        self.data = data
        self.cleaned_data = None


    def read_data(self, filename):
        try:
            self.data = pd.read_csv(filename)
        except FileNotFoundError:
            logger.error(f"{self.read_data.__name__}/ File {filename} not found. Please try again.")
            return
        except pd.errors.EmptyDataError:
            logger.error(f"{self.read_data.__name__}/ File {filename} is empty. Please try again. ")
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
            logger.error(f"{self.num_of_unique_in_column.__name__}/ Column '{column}' does not exist in the data. Please try again.")
            return None
        else:
            return self.data[column].nunique()
         
    
    def final_data(self):
        
        if self.data is None:
            logger.error(f"{self.final_data.__name__}/ No data found. Please call the 'read_data' method first to load the data.")
            return None
        data = self.data.copy() 
        data = data.drop_duplicates()
        data = data.dropna()
        self.cleaned_data = data 
        return data


