from __future__ import print_function
from __future__ import division
from zenq.api.tables import Base, Facts 
from zenq.api.config import db_uri
import sqlalchemy 
from zenq.logger import CustomFormatter, bcolors
from sqlalchemy.orm import load_only, relationship, joinedload, sessionmaker
from sqlalchemy import func, create_engine      
import logging
import os
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

class Model():
    
    Facts = Facts()
    metadata, engine = Facts.connect_to_db(db_uri)
    session = sessionmaker(bind=engine)()
    params_ = {}

    def cltv_df(self):
        cltv_df = self.session.query(Facts.customer_id,
                                    func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.DATE_TRUNC('day', func.max(Facts.date)) - func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.DATE_TRUNC('day', datetime.today()) - func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.count(Facts.invoice_id),
                                    func.sum(Facts.total_price)).\
                                    group_by(Facts.customer_id).\
                                    having(func.count(Facts.invoice_id) > 1).\
                                    all()
                                    
        cltv = pd.DataFrame(cltv_df, columns=['customer_id','min_date', 'recency', 'T', 'frequency', 'monetary'])
        # one_time_buyers = round(sum(cltv_df['frequency'] == 0)/float(len(cltv_df))*(100),2)
        cltv = cltv[cltv["monetary"] > 0]
        cltv = cltv[cltv["frequency"] > 0]
        cltv['T'] = cltv['T'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)       

        cltv['recency'] = cltv['recency'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)       
        cltv = cltv[cltv["recency"] > 0]
        cltv = cltv[cltv["T"] > 0]
        cltv.to_sql('CLTV', self.engine, if_exists='replace', index=False, schema='result')
        logger.info(f"{self.cltv_df.__name__}, {len(cltv)} rows written to CLTV table")
        insert_log(os.path.basename(__file__), cltv_df.__name__, f"{len(cltv)} rows written to CLTV table")

        return cltv
        
    def rfm_score(self):
        cltv_df = self.cltv_df() 
        rfm = pd.DataFrame()
        rfm['customer_id'] = cltv_df['customer_id']
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
        rfm.to_sql('RFMScore', self.engine, if_exists='replace', index=False, schema='result')
        logger.info(f"{self.rfm_score.__name__}")
        insert_log(os.path.basename(__file__), rfm_score.__name__, f"{len(rfm)} rows written to RFMScore table")

        return rfm
    
    def fit_paretonbd(self):
        cltv_df = self.cltv_df()
        _check_inputs(cltv_df['frequency'], cltv_df['recency'], cltv_df['T'])
        model = ParetoNBDFitter(penalizer_coef=0.0)
        model.fit(cltv_df['frequency'], cltv_df['recency'], cltv_df['T'])
        insert_log(os.path.basename(__file__), fit_paretonbd.__name__, "Model created successfully")
        logger.info(f"{self.model_params.__name__}")
        return model 
    
    def model_params(self):
        
        model = self.fit_paretonbd()
        params_ = pd.Series({
        'r':  model.params_['r'],
        'alpha':  model.params_['alpha'],
        's':  model.params_['s'],
        'beta':  model.params_['beta']
        })
        params = pd.DataFrame({
        'r': [params_['r']],
        'alpha': [params_['alpha']],
        's': [params_['s']],
        'beta': [params_['beta']]
        })
        params.to_sql('ParetoParameters', self.engine, if_exists='replace', index=False, schema='result')
        logger.info(f"{self.model_params.__name__}")
        logger.error(f"{self.model_params.__name__}")

        return params
        
    
    def predict_paretonbd(self):
        model = self.fit_paretonbd()
        cltv_df = self.cltv_df()
        number_of_days_list = [30, 90, 180, 360]
        predict_paretonbd_d = pd.DataFrame({'Customer': cltv_df['customer_id']})
        for days in number_of_days_list:
            cltv_df[f'expected_purchases_{days}'] = model.conditional_expected_number_of_purchases_up_to_time(
                days,
                cltv_df['frequency'].values,
                cltv_df['recency'].values,
                cltv_df['T'].values
            )
            predict_paretonbd_d[f'Expected_Purchases_{days}'] = cltv_df[f'expected_purchases_{days}']
            predict_paretonbd_d.to_sql('Prediction', self.engine, if_exists='replace', index=False, schema='result')
        logger.info(f"{self.predict_paretonbd.__name__}")
        return predict_paretonbd_d

 
    def customer_is_alive(self):
        model = self.fit_paretonbd()
        cltv_df = self.cltv_df()
        cltv_df['probability_customer_alive'] = model.conditional_probability_alive(        
        cltv_df['frequency'].values, cltv_df['recency'].values, cltv_df['T'].values)
        customer_alive = pd.DataFrame({
            'Customer': cltv_df['customer_id'],
            'Probability_of_being_Alive': cltv_df['probability_customer_alive']
        })        
        customer_alive.to_sql('CustomerAlive', self.engine, if_exists='replace', index=False, schema='result')
        logger.info(f"{self.customer_is_alive.__name__}")

        return customer_alive

 