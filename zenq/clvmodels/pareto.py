# -*- coding: utf-8 -*-
"""Pareto/NBD model."""

from __future__ import print_function
from __future__ import division
import sqlalchemy       
import logging
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
from numpy import log, exp, logaddexp, asarray, any as npany
from pandas import DataFrame
from scipy.special import gammaln, hyp2f1, betaln
from scipy.special import logsumexp
from scipy.optimize import minimize
from lifetimes import ParetoNBDFitter

from lifetimes.utils import _check_inputs, _scale_time
from lifetimes.generate_data import pareto_nbd_model


class Model():

    def __init__(
        self, db_uri,
        penalizer_coef=0.0
    ):

        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        """
        Initialization, set penalizer_coef.
        """

        self.penalizer_coef = penalizer_coef
        
    def cltv_df(self):
        # max_date = func.max(Facts.date)
        cltv_df = self.session.query(Facts.customer_id,
                                    func.DATE_TRUNC('day', func.max(Facts.date)) - func.DATE_TRUNC('day', func.min(Facts.date)),
                                    func.DATE_TRUNC('day', datetime.today()) - func.DATE_TRUNC('day', func.max(Facts.date)),
                                    func.count(Facts.invoice_id),
                                    func.sum(Facts.total_price)).\
                                    group_by(Facts.customer_id).\
                                    having(func.count(Facts.invoice_id) > 1).\
                                    all()
                                    
        cltv_df = pd.DataFrame(cltv_df, columns=['customer_id','T', 'recency', 'frequency', 'monetary'])
        #ErrorHandling Raise Error
        cltv_df = cltv_df[cltv_df["monetary"] > 0]
        cltv_df = cltv_df[cltv_df["frequency"] > 0]
        cltv_df['T'] = cltv_df['T'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)       

        cltv_df['recency'] = cltv_df['recency'].astype('timedelta64[D]').astype(float).map('{:.0f}'.format).astype(int)       
        cltv_df = cltv_df[cltv_df["recency"] > 0]
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
    def fit():
        
        pass
    def output():
        pass
    def to_sql():
        
        pass

