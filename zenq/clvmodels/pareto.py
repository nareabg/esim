from __future__ import print_function
from __future__ import division

import sqlalchemy 
import logging
import os
import lifetimes
import pandas as pd
import numpy as np
from sqlalchemy.orm import load_only, relationship, joinedload, sessionmaker
from sqlalchemy import func, create_engine      
from lifetimes import BetaGeoFitter, ParetoNBDFitter
from lifetimes.utils import summary_data_from_transaction_data, _check_inputs, _scale_time
from lifetimes.generate_data import pareto_nbd_model
from numpy import log, exp, logaddexp, asarray, any as npany
from pandas import DataFrame
from datetime import datetime, timedelta
from scipy.special import gammaln, hyp2f1, betaln, logsumexp
from scipy.optimize import minimize
from zenq.api.tables import Base, Facts 
from zenq.api.config import db_uri
from zenq.logger import CustomFormatter, bcolors


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

# Define the Model class
class Model():
    """ 
        contains methods to compute customer lifetime value metrics, RFM score, and the Pareto/NBD model parameters
    """
    
    # Set up the Facts table, metadata, engine, and session
    Facts = Facts()
    metadata, engine = Facts.connect_to_db(db_uri)
    session = sessionmaker(bind=engine)()
    params_ = {}

    def cltv_df(self):
        """
            method queries a database to get customer transaction data and computes customer lifetime value metrics
        """
        # Query the database to get customer transaction data and compute customer lifetime value metrics
        cltv_df = self.session.query(Facts.customer_id,
                                    func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.DATE_TRUNC('day', func.max(Facts.date)) - func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.DATE_TRUNC('day', datetime.today()) - func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.count(Facts.invoice_id),
                                    func.sum(Facts.total_price)).\
                                    group_by(Facts.customer_id).\
                                    having(func.count(Facts.invoice_id) > 1).\
                                    all()
        # Create a Pandas dataframe from the query results and clean the data                            
        cltv = pd.DataFrame(cltv_df, columns=['customer_id','min_date', 'recency', 'T', 'frequency', 'monetary'])
        # one_time_buyers = round(sum(cltv_df['frequency'] == 0)/float(len(cltv_df))*(100),2)
        cltv = cltv[cltv["monetary"] > 0]
        cltv = cltv[cltv["frequency"] > 0]
        cltv['T'] = cltv['T'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)       
        cltv['recency'] = cltv['recency'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)       
        cltv = cltv[cltv["recency"] > 0]
        cltv = cltv[cltv["T"] > 0]
        
        # Write the cleaned data to a SQL table called CLTV
        cltv.to_sql('CLTV', self.engine, if_exists='replace', index=False, schema='result')
        logger.info(f"{self.cltv_df.__name__}/ {len(cltv)} rows written to CLTV table")
        return cltv
        
    def rfm_score(self):
        """ 
            generates RFM_SCORES based on recency, frequency, monetary
        """
        # calculate the customer lifetime value using the method cltv_df() and assign it to the variable cltv_df
        cltv_df = self.cltv_df() 
        
        # Create an empty DataFrame called rfm
        rfm = pd.DataFrame()
        rfm['customer_id'] = cltv_df['customer_id']
        rfm["recency_score"] = pd.qcut(cltv_df['recency'], 5, labels=[5, 4, 3, 2, 1])
        rfm["frequency_score"] = pd.qcut(cltv_df["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
        rfm["monetary_score"] = pd.qcut(cltv_df["monetary"], 5, labels=[1, 2, 3, 4, 5])
        
        # Concatenate recency_score and frequency_score columns to create RFM_SCORE
        rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
        
        # Create a dictionary to map RFM_SCORE to customer segments
        seg_map = {
            r'[1-2][1-2]': 'HIBERNATING',
            r'[1-2][3-4]': 'AT RISK',
            r'[1-2]5': 'CANT LOSE',
            r'3[1-2]': 'ABOUT TO SLEEP',
            r'33': 'NEED ATTENTION',
            r'[3-4][4-5]': 'LOYAL CUSTOMER',
            r'41': 'PROMISING',
            r'51': 'NEW CUSTOMERS',
            r'[4-5][2-3]': 'POTENTIAL LOYALIST',
            r'5[4-5]': 'CHAMPIONS'
        }
        
        # Map RFM_SCORE to customer segments using the seg_map dictionary
        rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
        
        # Write rfm DataFrame to SQL database table called RFMScore using the engine attribute
        rfm.to_sql('RFMScore', self.engine, if_exists='replace', index=False, schema='result')
        
        # Log the number of rows written to the RFMScore table using logger object
        logger.info(f"{self.rfm_score.__name__}/ {len(rfm)} rows written to RFMScore table")
        return rfm
    
    def fit_paretonbd(self):
        """ 
            method instantiates the Pareto/NBD model with a penalizer coefficient of 0.0 and fits the model
        """
        cltv_df = self.cltv_df()
        _check_inputs(cltv_df['frequency'], cltv_df['recency'], cltv_df['T'])
        # instantiate the Pareto/NBD model
        model = ParetoNBDFitter(penalizer_coef=0.0)
        # fit the model
        model.fit(cltv_df['frequency'], cltv_df['recency'], cltv_df['T'])
        logger.info(f"{self.model_params.__name__}/ Model initiation done.")
        return model 
    
    def model_params(self):
        """ 
            stores the model parameters lambda, alpha, and beta values to the dictionary 
        """
        
        # fit the Pareto/NBD model
        model = self.fit_paretonbd()
        
        # create a pandas series to store the fitted model's parameters
        params_ = pd.Series({
        'r':  model.params_['r'],
        'alpha':  model.params_['alpha'],
        's':  model.params_['s'],
        'beta':  model.params_['beta']
        })
        
        # create a pandas dataframe to store the model parameters
        params = pd.DataFrame({
        'r': [params_['r']],
        'alpha': [params_['alpha']],
        's': [params_['s']],
        'beta': [params_['beta']]
        })
        
        # store the parameters in a database
        params.to_sql('ParetoParameters', self.engine, if_exists='replace', index=False, schema='result')
        logger.info(f"{self.model_params.__name__} / Model parameters inserted to table ParetoParameters")
        return params
        
    
    def predict_paretonbd(self):
        """ 
            method predicts the expected number of purchases for each customer for different time periods
        """
        model = self.fit_paretonbd()
        cltv_df = self.cltv_df()
        # list of number of days for which we want to predict expected purchases
        number_of_days_list = [30, 90, 180, 360]
        predict_paretonbd_d = pd.DataFrame({'Customer': cltv_df['customer_id']})
        for days in number_of_days_list:
            # calculate the expected purchases up to a specific number of days
            cltv_df[f'expected_purchases_{days}'] = model.conditional_expected_number_of_purchases_up_to_time(
                days,
                cltv_df['frequency'].values,
                cltv_df['recency'].values,
                cltv_df['T'].values
            )
            # add the predicted values to the dataframe
            predict_paretonbd_d[f'Expected_Purchases_{days}'] = cltv_df[f'expected_purchases_{days}']
            # write the predicted values to a database table
            predict_paretonbd_d.to_sql('Prediction', self.engine, if_exists='replace', index=False, schema='result')
        logger.info(f"{self.predict_paretonbd.__name__} / {len(predict_paretonbd_d)} rows written to Prediction table")
        return predict_paretonbd_d

 
    def customer_is_alive(self):
        """
            method calculates the probability of each customer being alive 
        """
        model = self.fit_paretonbd()
        cltv_df = self.cltv_df()
        # calculate the probability that the customer is still alive
        cltv_df['probability_customer_alive'] = model.conditional_probability_alive(        
        cltv_df['frequency'].values, cltv_df['recency'].values, cltv_df['T'].values)
        # create a dataframe to hold the probability values
        customer_alive = pd.DataFrame({
            'Customer': cltv_df['customer_id'],
            'Probability_of_being_Alive': cltv_df['probability_customer_alive']
        })        
        # write the probability values to a database table
        customer_alive.to_sql('CustomerAlive', self.engine, if_exists='replace', index=False, schema='result')
        logger.info(f"{self.customer_is_alive.__name__}/ {len(customer_alive)} rows written to CustomerAlive table")
        return customer_alive

 