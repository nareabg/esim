import dash

from dash import Dash, dcc, html, Input, Output, State
from dash import callback,Input, Output, State, dcc, html

app = dash.Dash(__name__ )


image_filename = 'w.jpg'  
image_url = app.get_asset_url(image_filename)

nare = 'nare.jpg'  
nare = app.get_asset_url(nare)

luso = 'luso.jpg' 
luso = app.get_asset_url(luso)

armin = 'armin.jpg'  
armin = app.get_asset_url(armin)

 
dash.register_page(
    __name__,
    path='/'
)

layout =      html.Div([
    html.Div([
                html.P('UNLOCK THE POWER OF CUSTOMER LOYALTY', id = 'unlock_text'),

    ], className = 'black_box33'),

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
            html.Img(src=image_url, id = 'nkar')
        ]),
    ], id = 'box'),
    html.Div([
    html.Div([           
            html.Div([
                html.H2('OUR GIT_HUB', id = 'our_text'),],),
                    
            html.Div([
                html.H3('LINK', id = 'link'),  ], id = 'link_git')
    ], id = 'green_box') ,
    
    html.Div([
         html.H1('OUR TEAM', id = 'our_team'), 
    ],id = 'team_box'),
        
    html.Div([
        html.Div([
            
            html.Img(src=nare, id = 'nkar_nare'),
            html.H3('Nare Abgaryan', id = 'nare_name')
        ]),
        html.Div([
            html.Img(src=luso, id = 'nkar_luso'),
            html.H3('Lusine Babayan', id = 'luso_name')
        ]),
       html.Div([
            html.Img(src=armin, id = 'nkar_armin'),
            html.H3('Armine Khachatryan', id = 'armin_name')
        ]),  
        ], id = 'black_box_1')
    ], id = 'container'),
])
#   ], id='page_layout2')
    
    