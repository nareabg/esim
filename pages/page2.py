# import pandas as pd
# import plotly.graph_objects as go

# import datetime as dt
# import plotly.express as px

# import dash

# from dash import callback,Input, Output, State, dcc, html

# data = pd.read_excel("Dataset.xlsx")
# data.dropna(inplace=True)
# data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
# today_date = dt.datetime(2011, 12, 11)
# data["TotalPrice"] = data["Price"] * data["Quantity"]
# rfm = data.groupby("Customer ID").agg({"InvoiceDate": lambda InvıiceDate: (today_date- InvıiceDate.max()).days,
#                                        "Invoice": lambda Invoice: Invoice.nunique(),
#                                        "TotalPrice": lambda TotalPrice: TotalPrice.sum()})
# rfm.columns = ["recency","frequency","monetary"]
# #excluding below zero monetary values
# rfm = rfm[rfm["monetary"] > 0]
# rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
# rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
# rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])
# rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
# seg_map = {
#     r'[1-2][1-2]': 'HIBERNATING',
#     r'[1-2][3-4]': 'AT RISK',
#     r'[1-2]5': 'CANT LOSE',
#     r'3[1-2]': 'ABOUT TO SLEEP',
#     r'33': 'NEED ATTENTION',
#     r'[3-4][4-5]': 'LOYAL CUSTOMER',
#     r'41': 'PROMISING',
#     r'51': 'NEW CUSTOMERS',
#     r'[4-5][2-3]': 'POTENTIAL LOYALIST',
#     r'5[4-5]': 'CHAMPIONS'
# }
# rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
# rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])
# sgm= rfm["segment"].value_counts()
# c = sgm.index.tolist()
# d = sgm.tolist()
# color_series = ['#5b9aa0','#667292','#8d9db6','#daebe8','#d6d4e0',
#  '#e4d1d1','#b0aac0','#f9d5e5','#b9b0b0','#622569']

# fig_pie = go.Figure(data=[go.Pie(labels=c, values=d, pull=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])])
# fig_pie.update_layout({
# 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
# 'paper_bgcolor': 'rgba(1, 0, 0, 0)',
# })

# df_treemap = rfm.groupby('segment').agg('count').reset_index()
# fig_treemap = px.treemap(df_treemap, path=['segment'], values='RFM_SCORE')
# fig_treemap.update_layout({
# 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
# 'paper_bgcolor': 'rgba(1, 0, 0, 0)',
# })

# dash.register_page(
#     __name__,
#     path='/page2',
#     title='CLV',
#     name='CLV',

# )

# image1 = 'a.png'
# image2 = 'p.png'
# layout = html.Div([
#     html.Div([dcc.Graph(figure=fig_pie),],  id="data-description-container03"),
#     html.Div([dcc.Graph(figure=fig_treemap),],  id="data-description-container04"),
#     html.Div([ html.Img(src=dash.get_asset_url(image1), id = 'img_1')],  id="data-description-container05"),
#     html.Div([html.Img(src=dash.get_asset_url(image2), id = 'img_2')],  id="data-description-container06"),
#     html.Div([ html.H1('Date', id = 'data-description-text7'),
#              ],  id="data-description-container09"),
#     html.Div([ html.H1('Country', id = 'data-description-text8'),
#              ],  id="data-description-container10"),

# ], className='twelve columns')

