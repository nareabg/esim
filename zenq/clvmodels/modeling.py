#class BGnbd:
#   def bg(self):
#       print('b') 
        
import logging
from sqlalchemy.orm import load_only
from lifetimes import BetaGeoFitter
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from .models import Base, Location, Customer, Facts, CustomerFact, Prediction

class Model:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def count_coding(self):
        df_data_group = self.session.query(Customer.customer_id,
                                            func.max(Facts.date) - func.min(Facts.date),
                                            func.count(Facts.id),
                                            func.sum(Facts.quantity),
                                            func.sum(Facts.total_price)).\
                                            join(Customer.facts).\
                                            group_by(Customer.customer_id).all()

        df_data_group = pd.DataFrame(df_data_group, columns=['customer_id', 'date', 'invoice_id', 'quantity', 'price'])
        df_data_group['avg_order_value'] = df_data_group['price'] / df_data_group['invoice_id']
        purchase_frequency = sum(df_data_group['invoice_id']) / df_data_group.shape[0]
        repeat_rate = df_data_group[df_data_group.invoice_id > 1].shape[0] / df_data_group.shape[0]
        churn_rate = 1 - repeat_rate
        df_data_group['CLV'] = (df_data_group['avg_order_value'] * purchase_frequency) / churn_rate

        return df_data_group

    def count_cltv(self, days=30):
        today_date = datetime.today()
        past_date = today_date - timedelta(days=days)
        past_date_str = past_date.strftime('%Y-%m-%d %H:%M:%S')
        cltv_data = self.session.query(Customer.customer_id,
                                       func.sum(Facts.total_price)).\
                                       join(Customer.facts).\
                                       filter(Facts.date >= past_date_str).\
                                       group_by(Customer.customer_id).\
                                       options(joinedload(Customer.facts)).all()
        cltv_data = pd.DataFrame(cltv_data, columns=['customer_id', 'total_price'])
        df_data_group = self.count_coding()
        cltv_data = pd.merge(cltv_data, df_data_group[['customer_id', 'CLV']], on='customer_id', how='left')
        cltv_data['purchase_frequency'] = cltv_data['customer_id'].map(df_data_group.set_index('customer_id')['invoice_id'])
        cltv_data['repeat_rate'] = cltv_data['customer_id'].map(df_data_group.set_index('customer_id')['repeat_rate'])
        cltv_data['churn_rate'] = 1 - cltv_data['repeat_rate']
        cltv_data['cltv_predicted'] = (cltv_data['total_price'] / cltv_data['purchase_frequency']) * cltv_data['CLV'] * cltv_data['churn_rate']
        return cltv_data
