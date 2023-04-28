#from zenq.utils import connect
# from zenq.utils import test
import sqlalchemy
from sqlalchemy import cast, Numeric

from sqlalchemy import exc
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy import Sequence, UniqueConstraint 
from sqlalchemy import create_engine, desc, asc
import matplotlib.pyplot as plt

from sqlalchemy import text
from sqlalchemy.orm import relationship
from zenq.api.config import db_uri
from sqlalchemy import func, create_engine      
from zenq.api.tables import Base, Facts
from sqlalchemy.orm import load_only, relationship, joinedload, sessionmaker
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from lifetimes import GammaGammaFitter
from lifetimes import BetaGeoFitter
import datetime as dt
from lifetimes.plotting import plot_probability_alive_matrix
from lifetimes.plotting import plot_frequency_recency_matrix
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
 

class Visuals():

    def __init__(
        self
    ):
        self.params_ = {}
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        
 
    # def total_sales_by_location(self):
    #     result = self.session.query(Facts.location_name, sqlalchemy.func.sum(Facts.total_price)).\
    #                 group_by(Facts.location_name).all()
    #     x = [i[0] for i in result]
    #     y = [i[1] for i in result]
    #     plt.bar(x, y)
    #     plt.xlabel("Location Name")
    #     plt.ylabel("Total Sales")
    #     plt.show()

        
    def price_distribution(self):
        total_price = self.session.query(Facts.total_price).all()
        df = pd.DataFrame(total_price, columns=['total_price'])
        fig = px.box(df, x='total_price')
        fig.show()
        
    def time_series(self):
        daily_sales = (
            self.session.query(Facts.date, func.sum(Facts.total_price))
            .group_by(Facts.date)
            .order_by(Facts.date)  # sort by date in ascending order
            .all()
        )
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[sale[0] for sale in daily_sales], y=[sale[1] for sale in daily_sales], mode='lines'))
        fig.update_layout(title='Daily Sales', xaxis_title='Date', yaxis_title='Total sales')
        fig.show()
        


    def gender_price(self):
        price_by_gender = (
            self.session.query(Facts.gender, Facts.total_price).all()
        )
        df = pd.DataFrame(price_by_gender, columns=['gender', 'total_price'])
        fig = px.box(df, x='gender', y='total_price', title='Product price by gender')
        fig.show()

    def rfm_treemap(self):
        rfm = self.session.query(Facts.RFMScore.segment, func.count(Facts.RFMScore.RFM_SCORE)).group_by(Facts.RFMScore.segment).all()
        df_treemap = pd.DataFrame(rfm, columns=['segment', 'RFM_SCORE'])
        fig = px.treemap(df_treemap, path=['segment'], values='RFM_SCORE')
        fig.show()
        
        
    def top_customers_30days(self):
        top_customers = self.session.query(Facts.Prediction.Customer, Facts.Prediction.Expected_Purchases_30)\
                      .order_by(desc(Facts.Prediction.Expected_Purchases_30))\
                      .limit(10)\
                      .all()
        fig = go.Figure(data=[go.Bar(
        x=[customer.Customer for customer in top_customers],
        y=[customer.Expected_Purchases_30 for customer in top_customers],
        text=[f"Expected Purchases in 30 Days: {customer.Expected_Purchases_30:.2f}" for customer in top_customers],
        textposition='auto'
                    )])
        fig.update_layout(
        title="Top Customers with the Highest Expected Number of Purchases in 30 Days",
        xaxis_title="Customer",
        yaxis_title="Expected Number of Purchases"
        )

        fig.show()
        
            
    def top_customers_90days(self):
        top_customers = self.session.query(Facts.Prediction.Customer, Facts.Prediction.Expected_Purchases_90)\
                      .order_by(desc(Facts.Prediction.Expected_Purchases_90))\
                      .limit(10)\
                      .all()
        fig = go.Figure(data=[go.Bar(
        x=[customer.Customer for customer in top_customers],
        y=[customer.Expected_Purchases_90 for customer in top_customers],
        text=[f"Expected Purchases in 90 Days: {customer.Expected_Purchases_90:.2f}" for customer in top_customers],
        textposition='auto'
                    )])
        fig.update_layout(
        title="Top Customers with the Highest Expected Number of Purchases in 90 Days",
        xaxis_title="Customer",
        yaxis_title="Expected Number of Purchases"
        )

        fig.show()
        
    def lowest_customers_90days(self):
        top_customers = self.session.query(Facts.Prediction.Customer, Facts.Prediction.Expected_Purchases_90)\
                      .order_by(asc(Facts.Prediction.Expected_Purchases_90))\
                      .limit(10)\
                      .all()
        fig = go.Figure(data=[go.Bar(
        x=[customer.Customer for customer in top_customers],
        y=[customer.Expected_Purchases_90 for customer in top_customers],
        text=[f"Expected Purchases in 90 Days: {customer.Expected_Purchases_90:.2f}" for customer in top_customers],
        textposition='auto'
                    )])
        fig.update_layout(
        title="Top Customers with the Lowest Expected Number of Purchases in 90 Days",
        xaxis_title="Customer",
        yaxis_title="Expected Number of Purchases"
        )

        fig.show()
        
    # def customer_aliveness(self):
    #     customer_alive_df = self.session.query(Facts.CustomerAlive.Customer, Facts.CustomerAlive.Probability_of_being_Alive).all()
    #     df = pd.DataFrame(customer_alive_df, columns=['Customer', 'Probability_of_being_Alive' ])
    #     plt.hist(df['Probability_of_being_Alive'], bins=50)
    #     plt.title('Distribution of Probability of Being Alive')
    #     plt.xlabel('Probability of Being Alive')
    #     plt.ylabel('Number of Customers')
    #     plt.show()
    def customer_aliveness(self):
        customer_alive_df = self.session.query(Facts.CustomerAlive.Customer, Facts.CustomerAlive.Probability_of_being_Alive).all()
        df = pd.DataFrame(customer_alive_df, columns=['Customer', 'Probability_of_being_Alive' ])
        
        # set custom color scheme
        color = '#4F1BBD'
        plt.rcParams['text.color'] = '#000000'
        plt.rcParams['axes.labelcolor'] = '#000000'
        plt.rcParams['xtick.color'] = '#000000'
        plt.rcParams['ytick.color'] = '#000000'
        plt.rcParams['grid.color'] = '#d4d4d4'
        
        # create histogram plot
        plt.figure(figsize=(8, 6))
        plt.hist(df['Probability_of_being_Alive'], bins=50, color=color, edgecolor='#ffffff')
        
        # set title and labels
        plt.title('Distribution of Probability of Being Alive', fontsize=16)
        plt.xlabel('Probability of Being Alive', fontsize=14)
        plt.ylabel('Number of Customers', fontsize=14)
        
        # add gridlines
        plt.grid(True)
        
        # show plot
        plt.show()


