import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime as dt
import plotly.figure_factory as ff
import plotly.express as px
from sqlalchemy.orm import sessionmaker
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from sqlalchemy import Sequence, UniqueConstraint, create_engine, desc, asc
from lifetimes.utils import calibration_and_holdout_data
from zenq.visualizations.plot import Visuals
import dash
import base64
import io
from dash import callback,Input, Output, State, dcc, html
from zenq.api.endpoints import insert_facts
from zenq.api.tables import Facts
from zenq.api.config import db_uri


dash.register_page(
    __name__,
     path='/Calculate',
    # title='Calculate',
    # name='Calculate'
)
app = dash.Dash(__name__ )


engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()
 

layout =  html.Div([
    html.Div([

            dcc.Upload(id='upload_buttom',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')], id = 'csv_text')
                ),
        html.Div(id='output-data-upload'),
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

# @app.callback(Output('output-data-upload', 'children'),
#               Input('upload_buttom', 'contents'),
#               State('upload_buttom', 'filename'))
# def display_csv(contents, filename):
#     if contents is not None:
#         content_type, content_string = contents.split(',')
#         decoded = base64.b64decode(content_string)
#         try:
#             if 'csv' in filename:
#                 # Assume that the user uploaded a CSV file
#                 df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
#         except Exception as e:
#             print(e)
#             return html.Div(['There was an error processing this file.'])
        
#         columns = ['customer_id', 'gender', 'invoice_id', 'date', 'quantity', 'total_price']

#         options = [{'label': col, 'value': col} for col in df.columns]
#         dropdowns = [dcc.Dropdown(options=options, value='', placeholder=col, id=f'{col}-dropdown') for col in columns]

#         return html.Div([
#             html.H5(filename),
#             dcc.DataTable(
#                 id='datatable-upload',
#                 data=df.to_dict('records'),
#                 columns=[{'name': col, 'id': col} for col in df.columns],
#             ),
#             html.Button('Insert Data', id='insert-data-button'),
#             html.Div(dropdowns, id='columns-mapping'),
#         ])
# @app.callback(Output('columns-mapping', 'children'),
#               Output('insert-data-button', 'style'),
#               Input('insert-data-button', 'n_clicks'),
#               State('datatable-upload', 'data'),
#               State('customer_id_dropdown', 'value'),
#               State('gender_dropdown', 'value'),
#               State('invoice_id_dropdown', 'value'),
#               State('date_dropdown', 'value'),
#               State('quantity_dropdown', 'value'),
#               State('total_price_dropdown', 'value'))
# def display_columns_mapping(n_clicks, data, customer_id, gender, invoice_id, date, quantity, total_price):
#     if n_clicks is None:
#         return '', {'display': 'none'}
    
#     if customer_id == '' or gender == '' or invoice_id == '' or date == '' or quantity == '' or total_price == '':
#         print("Please select a column for each field")
#         return 'Please select a column for each field', {'display': 'block'}

#     columns = ['customer_id', 'gender', 'invoice_id', 'date', 'quantity', 'total_price']

#     options = [{'label': col, 'value': col} for col in data[0].keys()]
#     dropdowns = [dcc.Dropdown(options=options, value='', placeholder=col, id=f'{col}-dropdown') for col in columns]

#     if n_clicks is not None:
#         return html.Div([
#             html.H5('Map columns'),
#             html.Div(dropdowns),
#             html.Button('Insert Data', id='insert-data-button-2'),
#         ]), {'display': 'none'}

#     mapping = {customer_id: '', gender: '', invoice_id: '', date: '', quantity: '', total_price: ''}
#     for i, col in enumerate(columns):
#         dropdown_value = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
#         if dropdown_value == f"{col}-dropdown":
#             mapping[columns[i]] = dash.callback_context.triggered[0]['value']
#         else:
#             mapping[columns[i]] = [dropdown.value for dropdown in dropdowns][i]

#     filename = secure_filename(request.cookies.get('filename'))

#     insert_facts(filename=filename, **mapping)

#     return '', {'display': 'none'}

# import dash
# import pandas as pd
# import base64
# import io

# from dash.dependencies import Input, Output, State
# from zenq.visualizations.plot import Visuals
# from zenq.api.endpoints import insert_facts
# from zenq.api.config import db_uri

# layout = dash.html.Div([
#     html.Div([
#         html.Div([
#             dcc.Upload(
#                 id='upload_buttom',
#                 children=html.Div(['Drag and Drop or ', html.A('Select Files')], id='csv_text')
#             ),
#             dash.html.Div(id='output-data-upload'),
#         ], className='black_box33'),
#         html.Div([
#             html.Div([
#                 dcc.Graph(id='time-series-plot', figure=Visuals().time_series())
#             ])
#         ], className='rect1'),
#         html.Div([
#             html.Div([
#                 dcc.Graph(id='', figure=Visuals().gender_price())
#             ])
#         ], className='rect2'),
#     ]),
#     html.Div([
#         html.Div([], className='rect3'),
#         html.Div([], className='rect4'),
#     ], className='pordz')
# ])

# @app.callback(Output('output-data-upload', 'children'),
#               Input('upload_buttom', 'contents'),
#               State('upload_buttom', 'filename'))
# def display_csv(contents, filename):
#     if contents is not None:
#         content_type, content_string = contents.split(',')
#         decoded = base64.b64decode(content_string)
#         try:
#             if 'csv' in filename:
#                 # Assume that the user uploaded a CSV file
#                 df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
#         except Exception as e:
#             print(e)
#             return html.Div(['There was an error processing this file.'])

#         columns = ['customer_id', 'gender', 'invoice_id', 'date', 'quantity', 'total_price']

#         options = [{'label': col, 'value': col} for col in df.columns]
#         dropdowns = [dcc.Dropdown(options=options, value='', placeholder=col, id=f'{col}-dropdown') for col in columns]

#         return html.Div([
#             html.H5(filename),
#             dcc.DataTable(
#                 id='datatable-upload',
#                 data=df.to_dict('records'),
#                 columns=[{'name': col, 'id': col} for col in df.columns],
#             ),
#             html.Button('Insert Data', id='insert-data-button'),
#             html.Div(dropdowns, id='columns-mapping'),
#         ])

 