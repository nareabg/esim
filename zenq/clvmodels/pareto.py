# -*- coding: utf-8 -*-
"""Pareto/NBD model."""

from __future__ import print_function
from __future__ import division
import sqlalchemy       
import logging
import lifetimes
from sqlalchemy.orm import load_only, relationship
from lifetimes import BetaGeoFitter
import pandas as pd
from sqlalchemy import func
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload, sessionmaker
from zenq.api.tables import Base, Facts 
import pandas as pd
import numpy as np
# -*- coding: utf-8 -*-
"""Pareto/NBD model."""


from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from numpy import log, exp, logaddexp, asarray, any as npany
from pandas import DataFrame
from scipy.special import gammaln, hyp2f1, betaln, logsumexp
from scipy.optimize import minimize
from lifetimes import BetaGeoFitter, ParetoNBDFitter
from lifetimes.utils import _check_inputs, _scale_time
from lifetimes.generate_data import pareto_nbd_model

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import load_only, relationship, joinedload
from zenq.api.tables import Base, Facts 
from zenq.api.config import db_uri
from numpy import log, exp, logaddexp, asarray, any as npany
from pandas import DataFrame
from scipy.special import gammaln, hyp2f1, betaln
from scipy.special import logsumexp
from scipy.optimize import minimize
from lifetimes import ParetoNBDFitter

from lifetimes.utils import _check_inputs, _scale_time
from lifetimes.generate_data import pareto_nbd_model
from zenq.api.config import db_uri

class Model():

    def __init__(
        self
    ):
        self.params_ = {}
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        """
        Initialization, set penalizer_coef.
        """

        
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
                                    
        # cltv_df = pd.DataFrame(cltv_df, columns=['customer_id','min_date','recency', 'T', 'frequency', 'monetary'])
        # # cltv_df['monetary'] = cltv_df['monetary'].astype(int)
        # cltv_df['T'] = cltv_df['T'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)              
        # cltv_df['recency'] = cltv_df['recency'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)       
        # one_time_buyers = round(sum(cltv_df['frequency'] == 0)/float(len(cltv_df))*(100),2)
        # print('Percentage of customers that only bought onece', one_time_buyers, '%')
        # #ErrorHandling Raise Error
        # cltv_df = cltv_df[cltv_df["monetary"] > 0]
        # cltv_df = cltv_df[cltv_df["frequency"] > 0]
        # cltv_df = cltv_df[cltv_df["recency"] > 0]
        # cltv_df = cltv_df[cltv_df["T"] > 0]
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
        monetary_value = cltv_df['monetary']
        _check_inputs(frequency, recency, T, monetary_value)
        # Fit Pareto/NBD model
        model = ParetoNBDFitter(penalizer_coef=0.0)
        model.fit(frequency, recency, T, monetary_value)
        self.params_ = pd.Series({
        'r':  model.params_['r'],
        'alpha':  model.params_['alpha'],
        's':  model.params_['s'],
        'beta':  model.params_['beta']
        })
        return model, self.params_
    def predict_paretonbd(self, num_periods=1):
        """
        Predicts the expected number of repeat purchases and the expected average value of those purchases
        for the next `num_periods` periods using the fitted Pareto/NBD model.
        """
        model = self.fit_paretonbd()
        cltv_df = self.cltv_df()
        frequency = cltv_df['frequency']
        recency = cltv_df['recency']
        T = cltv_df['T']
        conditional_expected_number_of_purchases_up_to_time
        conditional_probability_alive
        predicted_values = model.predict(num_periods, frequency, recency, T)
        expected_num_purchases = predicted_values.iloc[-1]['predicted_purchases']
        expected_avg_value = predicted_values.iloc[-1]['predicted_average_profit']
        return expected_num_purchases, expected_avg_value

        