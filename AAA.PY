
import dash
from dash import Dash, dcc, html, Input, Output, State
app = dash.Dash(__name__, use_pages=True,suppress_callback_exceptions=True)
server=app.server

#image
image_filename = 'logo.jpeg'
w = 'w.jpg'
nare = 'nare.jpg'
lusine = 'luso.jpg'
armine = 'armin.jpg'

app.layout=html.Div([ 
                       
    html.Div([
        # html.Div([    
        #     html.Img(src=app.get_asset_url(image_filename), id = 'esim')
        # ], id=''),
            
        # html.Div([
        #     html.Button(
        #         dcc.Link('Home', href='/page1', id = 'home_text'), id='home_button', 
        #     ), html.Hr(),
        # ]),
            
        # html.Div([
        #     html.Button(
        #         dcc.Link('Details', href='/page2', id = 'detail_text'), id='detail_button', 
        #     ), html.Hr(),
        # ]),
            
        # html.Div([
        #     html.Button(
        #         dcc.Link('Calculate', href='/page3', id = 'calculate_text'), id='calculate_button', 
        #      ), html.Hr(),
        # ]),            
    ], className='rectangle1'),
  

# html.Div([
    html.Div([
        # html.H1('UNLOCK THE POWER OF CUSTOMER LOYALTY', id = 'unlock_text'),
    ], id = 'black_box'),

    html.Div([
        html.Div([
            html.H1('What is zenq?', id = 'zenq_text'),
        ], id = 'zenq'),
        html.Div([
            html.H4('The aim of the ZENQ package is to create a tool for marketing analysts and data scientists. It is linked to a database, which makes our product accessible for a wider range of users that have shallow coding knowledge. The package works on data related to customers; the users are able to insert the data into the database and run codes from the ZENQ package. It allows users to analyze customers’ behaviors by their interaction with the business. The main purpose of the package is CLV and RFM computations along with the predictions. It has a Machine Learning part that will assume if the customer will ‘die’ or still be alive after some period of time. ZENQ is using BG/NBD and GammaGamma models for making assumptions on business. It has a range of visualizations that makes it easy to understand the statistics and make business decisions based on them.', id = 'long_text'),
            ]),    
        html.Div([ ], id='purple'),    
        html.Div([ ], id = 'green'),   
    
        html.Div([
            html.Img(src=app.get_asset_url(w), id = 'nkar')
        ]),
    ]),

html.Div([
    html.Div([           
            # html.Div([
            #     html.H1('OUR GIT_HUB', id = 'our_text'),],),
                    
            # html.Div([
            #     html.H3('LINK', id = 'link'),  ], id = 'link_git')
    ], id = 'green_box') ,
    
    html.Div([
        html.H1('OUR TEAM', id = 'our_team'), 
    ],id = 'team_box'),
        
        html.Div([
        #     html.Div([
        #         html.Img(src=app.get_asset_url(nare), id = 'nkar_nare')
        #     ]),
        #     html.Div([
        #         html.Img(src=app.get_asset_url(lusine), id = 'nkar_luso')
        #     ]),
        #    html.Div([
        #         html.Img(src=app.get_asset_url(armine), id = 'nkar_armin')
        #     ]),
    ], id = 'black_box_1')
],)

# ], id='page_layout2')
], id = 'layout1')


if __name__=='__main__':
	app.run_server(debug=True, port=8058)
 