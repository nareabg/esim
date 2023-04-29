
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

app.layout= html.Div([ 
                       
    html.Div([
        html.Div([    
            html.Img(src=app.get_asset_url(image_filename), id = 'esim')
        ], id=''),
            
        html.Div([
            html.Button(
                dcc.Link('Home', href='/page1', id = 'home_text'), id='home_button', 
            ), html.Hr(),
        ]),
            
        html.Div([
            html.Button(
                dcc.Link('Details', href='/page2', id = 'detail_text'), id='detail_button', 
            ), html.Hr(),
        ]),
            
        html.Div([
            html.Button(
                dcc.Link('Calculate', href='/page3', id = 'calculate_text'), id='calculate_button', 
             ), html.Hr(),
        ]),            
    ], className='rectangle1'),
  #page1

    # html.Div([
    #             html.P('UNLOCK THE POWER OF CUSTOMER LOYALTY', id = 'unlock_text'),

    # ], className = 'black_box3'),

    # html.Div([
    #     html.Div([
    #         html.H1('What is zenq?', id = 'zenq_text'),
    #     ], id = 'zenq'),
    #     html.Div([
    #         html.H4('The aim of the ZENQ package is to create a tool for marketing analysts and data scientists. It is linked to a database, which makes our product accessible for a wider range of users that have shallow coding knowledge. The package works on data related to customers; the users are able to insert the data into the database and run codes from the ZENQ package. It allows users to analyze customers’ behaviors by their interaction with the business. The main purpose of the package is CLV and RFM computations along with the predictions. It has a Machine Learning part that will assume if the customer will ‘die’ or still be alive after some period of time. ZENQ is using BG/NBD and GammaGamma models for making assumptions on business. It has a range of visualizations that makes it easy to understand the statistics and make business decisions based on them.', id = 'long_text'),
    #         ]),    
    #     html.Div([ ], id='purple'),    
    #     html.Div([ ], id = 'green'),   
    
    #     html.Div([
    #         html.Img(src=app.get_asset_url(w), id = 'nkar')
    #     ]),
    # ]),

    # html.Div([           
    #         html.Div([
    #             html.H2('OUR GIT_HUB', id = 'our_text'),],),
                    
    #         html.Div([
    #             html.H3('LINK', id = 'link'),  ], id = 'link_git')
    # ], id = 'green_box') ,
    
    # html.Div([
    #      html.H1('OUR TEAM', id = 'our_team'), 
    # ],id = 'team_box'),
        
    # html.Div([
    #     html.Div([
    #         html.Img(src=app.get_asset_url(nare), id = 'nkar_nare'),
    #         html.H3('Nare Abgaryan', id = 'nare_name')
    #     ]),
    #     html.Div([
    #         html.Img(src=app.get_asset_url(lusine), id = 'nkar_luso'),
    #         html.H3('Lusine Babayan', id = 'luso_name')
    #     ]),
    #    html.Div([
    #         html.Img(src=app.get_asset_url(armine), id = 'nkar_armin'),
    #         html.H3('Armine Khachatryan', id = 'armin_name')
    #     ]),  
    #     ], id = 'black_box_1')


#page2

#    html.Div([
#                 html.P('EXPLORE OUR PACKAGE.', id = 'explore_text'),

#     ], className = 'black_box3'),

#     html.Div([
          
#         html.Div([
#             html.H1('What is CLV in general?', id = 'clv_text'),
#             html.H4('The Customer Lifetime Value (CLV) is a measure that is used to track the relationship between the customer and the business at a particular time. It is a vital metric to understand the lifetime of the customers, that is, understand and predict how much time a person will stay as a customer in a business. It also helps to explore the factors that keep customers, moreover helps to enlarge the number of customers by acquiring new techniques. CLV model helps to understand whether it is more beneficial to focus on keeping the existing customers than on increasing the number of new customers. The value supports understanding whether a business should invest money in gaining new customers; if so, how much money should be invested? Overall, the CLV model helps to make decisions regarding business, customers, and money. ', id = 'long_text_1'),
#         ],id = 'rect1'),
          
#         html.Div([
            
#             html.H1('What is RFM?', id = 'rfm'),
#             html.H4('RFM stands for Recency, Frequency, and Monetary Value, which is a method used by marketers to analyze customer behavior and segment customers based on their purchasing habits.Recency refers to how recently a customer has made a purchase, Frequency refers to how often they make purchases, and Monetary Value refers to how much money they have spent on their purchases. By analyzing these three factors, marketers can identify which customers are most valuable and target them with tailored marketing campaigns to encourage them to make repeat purchases.',id='rfm_text')
            
#         ], id = 'rect2') ,              
#     ]),



#page3


#    html.Div([
#             #  html.P('UPLOAD YOUR CSV.', id = 'csv_text'),
 
#             # html.Div([
                 
#             # ], id = 'upload_buttom'),
#             dcc.Upload(id='upload_buttom',
#                 children=html.Div(['Drag and Drop or ', html.A('Select Files')], id = 'csv_text')
#                 ),

#     ], className = 'black_box3'),

#     html.Div([          
#         html.Div([],className = 'rect1'),
          
#         html.Div([], className = 'rect2') ,              
#     ]),

#     html.Div([  
                      
#         html.Div([],className = 'rect3'),
          
#         html.Div([], className = 'rect4') ,   
                   
#     ],className = 'pordz'),








], id = 'layout1')


if __name__=='__main__':
	app.run_server(debug=True, port=8058)
 