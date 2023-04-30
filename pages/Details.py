import pandas as pd
import plotly.graph_objects as go
import datetime as dt
import plotly.express as px
import dash
from dash import callback,Input, Output, State, dcc, html
 
dash.register_page(
    __name__,
    path='/Details',
    title='Details',
    name='Details'
)

 
layout =    html.Div([
   html.Div([
                html.P('EXPLORE OUR PACKAGE.', id = 'explore_text'),

    ], className = 'black_box3'),

    html.Div([
          
        html.Div([
            html.H1('What is CLV in general?', id = 'clv_text'),
            html.H4('The Customer Lifetime Value (CLV) is a measure that is used to track the relationship between the customer and the business at a particular time. It is a vital metric to understand the lifetime of the customers, that is, understand and predict how much time a person will stay as a customer in a business. It also helps to explore the factors that keep customers, moreover helps to enlarge the number of customers by acquiring new techniques. CLV model helps to understand whether it is more beneficial to focus on keeping the existing customers than on increasing the number of new customers. The value supports understanding whether a business should invest money in gaining new customers; if so, how much money should be invested? Overall, the CLV model helps to make decisions regarding business, customers, and money. ', id = 'long_text_1'),
        ],className = 'rect1'),
          
        html.Div([
            
            html.H1('What is RFM?', id = 'rfm'),
            html.H4('RFM stands for Recency, Frequency, and Monetary Value, which is a method used by marketers to analyze customer behavior and segment customers based on their purchasing habits.Recency refers to how recently a customer has made a purchase, Frequency refers to how often they make purchases, and Monetary Value refers to how much money they have spent on their purchases. By analyzing these three factors, marketers can identify which customers are most valuable and target them with tailored marketing campaigns to encourage them to make repeat purchases.',id='rfm_text')
            
        ], className = 'rect2') ,              
    ]),
        html.Div([  
                      
        html.Div([],className = 'rect3'),
          
        html.Div([], className = 'rect4') ,   
                   
    ],className = 'pordz')
    ])



