import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime as dt
import plotly.figure_factory as ff
import plotly.express as px
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.utils import calibration_and_holdout_data
from zenq.visualizations.plot import Visuals
import dash
from dash import callback,Input, Output, State, dcc, html
dash.register_page(
    __name__,
     path='/Calculate',
    # title='Calculate',
    # name='Calculate'
)


layout =  html.Div([
    html.Div([

            dcc.Upload(id='upload_buttom',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')], id = 'csv_text')
                ),

    ], className = 'black_box33'),

    html.Div([          
        html.Div([
                    html.Div([
                    dcc.Graph(id='time-series-plot', figure=Visuals().time_series())
                    ])
        ],className = 'rect1'),
          
        html.Div([
                html.Div([
                    dcc.Graph(id='', figure=Visuals().gender_price())
                ])
            
            ], className = 'rect2') ,              
    ],  ),

    html.Div([  
                      
        html.Div([],className = 'rect3'),
          
        html.Div([], className = 'rect4') ,   
                   
    ],className = 'pordz')
    ])
