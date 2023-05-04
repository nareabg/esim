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
import os
from flask import Flask


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
# app = dash.Dash(__name__ )
 
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()
 
UPLOAD_DIRECTORY = os.path.join(os.getcwd(), 'tmp')

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
server = Flask(__name__)
app = dash.Dash(server=server)
@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory.

    Parameters
    ----------
    path :
        

    Returns
    -------

    """
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

layout =  html.Div([
    html.Div([
        html.Div([
            dcc.Upload(id='upload_buttom',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')], id = 'csv_text'),
                ),        
            html.H2("File List"),
        html.Ul(id="file-list"),]),
        html.Div([    
            dcc.Input(
                id='input1',
                type='text',
                placeholder='csv name(globbing.csv)',
            ),
            dcc.Input(
                id='input1',
                type='text',
                placeholder='customer_id',
            ),
            
            # Second input field
            dcc.Input(
                id='input2',
                type='text',
                placeholder='gender',
            ),
            
            # Third input field
            dcc.Input(
                id='input3',
                type='text',
                placeholder='invoice_id',
            ),
            
            # Fourth input field
            dcc.Input(
                id='input4',
                type='text',
                placeholder='date',
            ),
            
            # Fifth input field
            dcc.Input(
                id='input5',
                type='text',
                placeholder='quantity',
            ),
            
            # Sixth input field
            dcc.Input(
                id='input6',
                type='text',
                placeholder='total_price',
            ),],id = 'column_inputs'), 
         
            html.Div(
            html.Button('Submit', id='submit_button',  n_clicks=0),
            style={'textAlign': 'center' }  # Center the button
        ), 
         
        html.Div(id='output_div')
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

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash.

    Parameters
    ----------
    name :
        
    content :
        

    Returns
    -------

    """
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app.

    Parameters
    ----------
    filename :
        

    Returns
    -------

    """
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    [Input("upload_buttom", "filename"), Input("upload_buttom", "contents")])
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list.

    Parameters
    ----------
    uploaded_filenames :
        
    uploaded_file_contents :
        

    Returns
    -------

    """

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

if __name__ == "__main__":
    app.run_server(debug=True, port=8058)
    