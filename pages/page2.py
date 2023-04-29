import pandas as pd
import plotly.graph_objects as go
import datetime as dt
import plotly.express as px
import dash
from dash import callback,Input, Output, State, dcc, html
 
 
 
layout =   html.Div([
    html.Div([
            html.P('UPLOAD YOUR CSV.', id = 'csv_text'), 
            html.Div([                
            ], id = 'upload_buttom'),
            dcc.Upload(id='upload_buttom',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')], id = 'csv_text')
                ),

    ], className = 'black_box3'),

    html.Div([          
        html.Div([],className = 'rect1'),          
        html.Div([], className = 'rect2') ,              
    ]),

    html.Div([                       
        html.Div([],className = 'rect3'),         
        html.Div([], className = 'rect4') ,                      
    ],className = 'pordz'),
    
    ])



