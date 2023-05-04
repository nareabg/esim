import dash

from dash import Dash, dcc, html, Input, Output, State
app = dash.Dash(__name__, use_pages=True,suppress_callback_exceptions=True)
server=app.server

image_filename = 'logo.jpeg'
w = 'w.jpg'

app.layout= html.Div([ 
                       
    html.Div([
        html.Div([    
            html.Img(src=app.get_asset_url(image_filename), id = 'esim')
        ], id='image'),
         html.Div([   
                 html.Div([
            dcc.Link(html.Button(page['name'], className="navigation",  style={'font-size': '24px', 'font-family': 'Hanuman'}), href=page['path'])
            for page in sorted(dash.page_registry.values(), key=lambda p: p['name'], reverse=True)
        ]),
        html.Hr(),

        # content of each page
        dash.page_container   
                 ],className = 'rectangle1' )
            
        ],),  
],)

if __name__=='__main__':
	app.run_server(debug=True, port=8058)
 