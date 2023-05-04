import sqlalchemy
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
from matplotlib import rcParams
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, exc, cast, Numeric
from sqlalchemy import Sequence, UniqueConstraint, create_engine, desc, asc, text, func 
from sqlalchemy.orm import declarative_base, sessionmaker, load_only, relationship, joinedload
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.schema import CreateSchema
from zenq.api.config import db_uri
from zenq.api.tables import Base, Facts
from lifetimes import GammaGammaFitter, BetaGeoFitter
from lifetimes.plotting import plot_probability_alive_matrix, plot_frequency_recency_matrix
    

class Visuals():
    """ 
        contains six methods, each of which generates a different type of visualization of the data in a database
    """
    
    Facts = Facts()
    metadata, engine = Facts.connect_to_db(db_uri)
    session = sessionmaker(bind=engine)()

    def __init__(
        self
    ):
        self.params_ = {}

    def price_distribution(self):
        """ 
            generates a box plot showing the distribution of total prices in the database.
        """
        # Retrieving total price data from the database
        total_price = self.session.query(Facts.total_price).all()
        # Close the session to prevent any potential memory leaks.
        self.session.close()
        df = pd.DataFrame(total_price, columns=['total_price'])
        fig = px.box(df, x='total_price')
        fig.show()
        
    def time_series(self):
        """
            generates a line chart showing the daily total sales over time
        """
        # Retrieving daily sales data from the database
        daily_sales = (
            self.session.query(Facts.date, func.sum(Facts.total_price))
            .group_by(Facts.date)
            .order_by(Facts.date)  # sort by date in ascending order
            .all()
        )
        # Close the session to prevent any potential memory leaks.
        self.session.close()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[sale[0] for sale in daily_sales], y=[sale[1] for sale in daily_sales], mode='lines', line=dict(color='blue')))
        fig.update_layout(title='Daily Sales', yaxis_title='Total sales', xaxis=dict(showgrid=False, tickangle=45, tickfont=dict(size=12), tickmode='auto', title=''))
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        fig.show()


    def gender_price(self):
        """ 
            generates a box plot showing the distribution of total prices in the database by gender
        """
        # Retrieve gender and total price data from the database using SQLAlchemy.
        price_by_gender = (
            self.session.query(Facts.gender, Facts.total_price).all()
        )
        # Close the session to prevent any potential memory leaks.
        self.session.close()
        # Create a pandas dataframe from the retrieved data.
        df = pd.DataFrame(price_by_gender, columns=['gender', 'total_price'])
        fig = px.box(df, x='gender', y='total_price', title='Product price by gender')
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        fig.show()

    def rfm_treemap(self):
        """ 
            generates a treemap showing the distribution of RFM scores in the database
        """
        # Retrieve RFM score segment data from the database using SQLAlchemy and count the number of occurrences for each segment.
        rfm = self.session.query(Facts.RFMScore.segment, func.count(Facts.RFMScore.RFM_SCORE)).group_by(Facts.RFMScore.segment).all()
        # Close the session to prevent any potential memory leaks.
        self.session.close()
        df_treemap = pd.DataFrame(rfm, columns=['segment', 'RFM_SCORE'])
        fig = px.treemap(df_treemap, path=['segment'], values='RFM_SCORE')
        fig.show()
        
    def top_customers_30days(self):
        """ 
            generates a bar chart showing the top 10 customers with the highest expected number of purchases in the next 30 days
        """
        # Retrieve top customers with the highest expected number of purchases in 30 days from the database using SQLAlchemy.
        top_customers = self.session.query(Facts.Prediction.Customer, Facts.Prediction.Expected_Purchases_30)\
                      .order_by(desc(Facts.Prediction.Expected_Purchases_30))\
                      .limit(10)\
                      .all()
        # Close the session to prevent any potential memory leaks.              
        self.session.close()
                     
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
        """
            generates a bar chart showing the top 10 customers with the highest expected number of purchases in the next 90 days.
        """
        # Query the top 10 customers with the highest expected purchases in the next 90 days
        top_customers = self.session.query(Facts.Prediction.Customer, Facts.Prediction.Expected_Purchases_90)\
                      .order_by(desc(Facts.Prediction.Expected_Purchases_90))\
                      .limit(10)\
                      .all()
        # Close the session to prevent any potential memory leaks.
        self.session.close()                      
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
        """ 
            generates a bar chart showing the top 10 customers with the lowest expected number of purchases in the next 90 days.
        """
        # Query the top 10 customers with the lowest expected purchases in the next 90 days
        top_customers = self.session.query(Facts.Prediction.Customer, Facts.Prediction.Expected_Purchases_90)\
                      .order_by(asc(Facts.Prediction.Expected_Purchases_90))\
                      .limit(10)\
                      .all()
        # Close the session to prevent any potential memory leaks.
        self.session.close()            
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
        
    def customer_aliveness(self):
        """ 
            method illustrastes the probabilities of customers being alive by histogram 
        """
        # Query the probability of each customer being alive
        customer_alive_df = self.session.query(Facts.CustomerAlive.Customer, Facts.CustomerAlive.Probability_of_being_Alive).all()
        # Close the session to prevent any potential memory leaks.
        self.session.close()
        df = pd.DataFrame(customer_alive_df, columns=['Customer', 'Probability_of_being_Alive' ]) 
        fig = go.Figure(data=[go.Histogram(x=df['Probability_of_being_Alive'], nbinsx=50)])
        fig.update_layout(
            title='Distribution of Probability of Being Alive',
            xaxis_title='Probability of Being Alive',
            yaxis_title='Number of Customers'
        )
        fig.show()



