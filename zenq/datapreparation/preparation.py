import os
import numpy as np
import pandas as pd

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

    def num_of_unique_in_column(self,column):
        return self.data[column].nunique()

    def finalizing_data(self):

        data = self.data.copy() 
        data = data.drop_duplicates()
        data = data.dropna()
        return data


