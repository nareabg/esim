from __future__ import print_function
from __future__ import division
from zenq.api.tables import Base, Facts 
from zenq.api.config import db_uri
import sqlalchemy 
from sqlalchemy.orm import load_only, relationship, joinedload, sessionmaker
from sqlalchemy import func, create_engine      
import logging
import lifetimes
from lifetimes import BetaGeoFitter, ParetoNBDFitter
from lifetimes.utils import summary_data_from_transaction_data, _check_inputs, _scale_time
from lifetimes.generate_data import pareto_nbd_model
import numpy as np
from numpy import log, exp, logaddexp, asarray, any as npany
import pandas as pd
from pandas import DataFrame
from datetime import datetime, timedelta
from scipy.special import gammaln, hyp2f1, betaln, logsumexp
from scipy.optimize import minimize
 

class Model():

    def __init__(
        self
    ):
        self.params_ = {}
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()


        
    def cltv_df(self):
        # max_date = func.max(Facts.date)
        cltv_df = self.session.query(Facts.customer_id,
                                    func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.DATE_TRUNC('day', func.max(Facts.date)) - func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.DATE_TRUNC('day', datetime.today()) - func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.count(Facts.invoice_id),
                                    func.sum(Facts.total_price)).\
                                    group_by(Facts.customer_id).\
                                    having(func.count(Facts.invoice_id) > 1).\
                                    all()
                                    
        cltv_df = pd.DataFrame(cltv_df, columns=['customer_id','min_date', 'recency', 'T', 'frequency', 'monetary'])
        one_time_buyers = round(sum(cltv_df['frequency'] == 0)/float(len(cltv_df))*(100),2)
        print('Percentage of customers that only bought onece', one_time_buyers, '%')
        cltv_df = cltv_df[cltv_df["monetary"] > 0]
        cltv_df = cltv_df[cltv_df["frequency"] > 0]
        cltv_df['T'] = cltv_df['T'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)       

        cltv_df['recency'] = cltv_df['recency'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)       
        cltv_df = cltv_df[cltv_df["recency"] > 0]
        cltv_df = cltv_df[cltv_df["T"] > 0]

        return cltv_df
        
    def rfm(self):
        cltv_df = self.cltv_df() 
        rfm = pd.DataFrame()
        rfm["recency_score"] = pd.qcut(cltv_df['recency'], 5, labels=[5, 4, 3, 2, 1])
        rfm["frequency_score"] = pd.qcut(cltv_df["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
        rfm["monetary_score"] = pd.qcut(cltv_df["monetary"], 5, labels=[1, 2, 3, 4, 5])
        rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
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
        rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
        
        return rfm
    
    def fit_paretonbd(self):
        """
        Fits Pareto/NBD model using Lifetimes library and returns the fitted model object.
        """
        cltv_df = self.cltv_df()
        print(cltv_df)
        # Check inputs for Pareto/NBD model
        frequency = cltv_df['frequency']
        recency = cltv_df['recency']
        T = cltv_df['T']
        _check_inputs(frequency, recency, T)
        # Fit Pareto/NBD model
        model = ParetoNBDFitter(penalizer_coef=0.0)
        model.fit(frequency, recency, T)
        self.params_ = pd.Series({
        'r':  model.params_['r'],
        'alpha':  model.params_['alpha'],
        's':  model.params_['s'],
        'beta':  model.params_['beta']
        })
        return model 
    
    
    def predict_paretonbd(self, num_periods=1):
        model = self.fit_paretonbd()
        cltv_df = self.cltv_df()
        frequency = cltv_df['frequency']
        recency = cltv_df['recency']
        T = cltv_df['T']
        freq = 'D' # days
        number_of_days_list = [30, 90, 180, 360]

        result_df = pd.DataFrame({'Customer': cltv_df['customer_id']})

        for days in number_of_days_list:
            cltv_df[f'expected_purchases_{days}'] = model.conditional_expected_number_of_purchases_up_to_time(
                days,
                cltv_df['frequency'].values,
                cltv_df['recency'].values,
                cltv_df['T'].values
            )
            result_df[f'Expected_Purchases_{days}'] = cltv_df[f'expected_purchases_{days}']

        return result_df

    def customer_is_alive(self):
        model = self.fit_paretonbd()
        cltv_df = self.cltv_df()
        frequency = cltv_df['frequency']
        recency = cltv_df['recency']
        T = cltv_df['T']
        cltv_df['probability_customer_alive'] = model.conditional_probability_alive(
        
        cltv_df['frequency'].values, cltv_df['recency'].values, cltv_df['T'].values)
        result_df = pd.DataFrame({
            'Customer': cltv_df['customer_id'],
            'Probability of being Alive': cltv_df['probability_customer_alive']
        })
        
        return result_df

   