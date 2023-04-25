# import pandas as pd
# import plotly.graph_objects as go
# import numpy as np
# import datetime as dt
# import plotly.figure_factory as ff
# import plotly.express as px
# from lifetimes import BetaGeoFitter
# from lifetimes import GammaGammaFitter
# from lifetimes.utils import calibration_and_holdout_data


# import dash

# from dash import callback,Input, Output, State, dcc, html

# #
# data = pd.read_excel("Dataset.xlsx")
# #
# fd = data.drop_duplicates()
# fd = fd [['Customer ID','Description','InvoiceDate','Invoice','Quantity','Price', 'Country']]
# fd = fd[(fd['Quantity']>0)]
# fd['TotalPurchase'] = fd['Quantity'] * fd['Price']
# #
# data.dropna(inplace=True)
# data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
# today_date = dt.datetime(2011, 12, 11)
# data["TotalPrice"] = data["Price"] * data["Quantity"]
# cltv_df = data.groupby('Customer ID').agg({'InvoiceDate': [lambda date: (date.max() - date.min()).days,
#                                                            lambda date: (today_date - date.min()).days],
#                                            'Invoice':      lambda num: num.nunique(),
#                                            'TotalPrice':   lambda TotalPrice: TotalPrice.sum()})
# cltv_df.columns = cltv_df.columns.droplevel(0)
# cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']
# cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]
# cltv_df = cltv_df[cltv_df["monetary"] > 0]
# cltv_df["recency"] = cltv_df["recency"] / 7
# cltv_df["T"] = cltv_df["T"] / 7
# cltv_df = cltv_df[(cltv_df['frequency'] > 1)]
# #
# bgf = BetaGeoFitter(penalizer_coef=0.0)
# bgf.fit(cltv_df['frequency'],
#         cltv_df['recency'],
#         cltv_df['T'])
# #
# summary_cal_holdout = calibration_and_holdout_data(fd, 'Customer ID', 'InvoiceDate',
#                                         calibration_period_end='2010-11-09',
#                                         observation_period_end='2011-01-01' )  
# #
# cltv_df["expected_purc_1_week"] = bgf.predict(1,cltv_df['frequency'],cltv_df['recency'],cltv_df['T'])
# cltv_df["expected_purc_1_month"] = bgf.predict(4,cltv_df['frequency'],cltv_df['recency'],cltv_df['T'])
# #
# ggf = GammaGammaFitter(penalizer_coef=0.1)
# ggf.fit(cltv_df['frequency'], cltv_df['monetary'])
# summary_cal_holdout = calibration_and_holdout_data(fd, 'Customer ID', 'InvoiceDate',
#                                         calibration_period_end='2010-11-09',
#                                       observation_period_end='2011-01-01',
#                                                    monetary_value_col = 'TotalPurchase') 
# summary_cal_holdout
# summary_cal_holdout = summary_cal_holdout[(summary_cal_holdout['monetary_value_cal']>0)]

    
# ggf.fit(summary_cal_holdout['frequency_cal'],
#         summary_cal_holdout['monetary_value_cal'])
# summary_cal_holdout['monetary_pred'] = ggf.conditional_expected_average_profit(summary_cal_holdout['frequency_holdout'],
#                                          summary_cal_holdout['monetary_value_holdout'])


# fig_0 = px.scatter(summary_cal_holdout, x="monetary_value_holdout", y="monetary_pred", width=400, labels={
#                      "monetary_value_holdout": "Actual",
#                      "monetary_pred": "Predicted"
#                  },
#                 title="GG model prediction")
# fig_0.update_layout({
# 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
# 'paper_bgcolor': 'rgba(1, 0, 0, 0)',
# })
# # 
# bgf = BetaGeoFitter(penalizer_coef=0.0)
# bgf.fit(summary_cal_holdout['frequency_cal'], summary_cal_holdout['recency_cal'], summary_cal_holdout['T_cal'])
# summary_cal_holdout['predicted_bgf'] = bgf.predict(30,  
#                         summary_cal_holdout['frequency_cal'], 
#                         summary_cal_holdout['recency_cal'], 
#                         summary_cal_holdout['T_cal'])
# fig_5 = px.scatter(summary_cal_holdout, x="frequency_holdout", y="predicted_bgf", width=400, labels={
#                      "frequency_holdout": "Actual",
#                      "predicted_bgf": "Predicted"
#                  },
#                 title="Beta Geo Fitter model prediction")
# fig_5.update_layout({
# 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
# 'paper_bgcolor': 'rgba(1, 0, 0, 0)',
# })
# # 
# cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],cltv_df['monetary'])
# x = cltv_df['expected_average_profit'].values.tolist()
# hist_data = [x]
# group_labels = ['expected_average_profit'] # name of the dataset

# fig_histogram = ff.create_distplot(hist_data, group_labels)
# fig_histogram.update_layout({
# 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
# 'paper_bgcolor': 'rgba(1, 0, 0, 0)',
# })
# # 
# cltv_12 = ggf.customer_lifetime_value(bgf,
#                                    cltv_df['frequency'],
#                                    cltv_df['recency'],
#                                    cltv_df['T'],
#                                    cltv_df['monetary'],
#                                    time=12, 
#                                    freq="W",  
#                                    discount_rate=0.01)
# cltv_12 = cltv_12.reset_index()
# cltv_12 = cltv_df.merge(cltv_12, on="Customer ID", how="left")
# cltv_12.sort_values(by="clv", ascending=False).head(5)
# # 
# x = cltv_12['clv'].values.tolist()
# cumsum = np.cumsum(x)
# trace = go.Scatter(x=[i for i in range(len(cumsum))], y=10*cumsum/np.linalg.norm(cumsum),
#                      marker=dict(color='rgb(150, 25, 120)'))
# layout = go.Layout(
#     title="CDF of 12 month clv predictions"
# )
# fig_density = go.Figure(data=go.Data([trace]), layout=layout)
# fig_density.update_layout({
# 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
# 'paper_bgcolor': 'rgba(1, 0, 0, 0)',
# })

# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# # 
# dash.register_page(
#     __name__,
#     path='/page3',
#     title='Model Visuals',
#     name='Model Visuals'
# )

# layout = html.Div([
#     html.Div([dcc.Graph(figure=fig_0),],  id="data-description-container03"),
#     html.Div([dcc.Graph(figure=fig_5),],  id="data-description-container04"),
#     html.Div([dcc.Graph(figure=fig_histogram),],  id="data-description-container05"),
#     html.Div([dcc.Graph(figure=fig_density),],  id="data-description-container06"),
#     html.Div([ html.H1('Date', id = 'data-description-text7'),
#              ],  id="data-description-container09"),
#     html.Div([ html.H1('Country', id = 'data-description-text8'),
#              ],  id="data-description-container10"),
    
# ], className='twelve columns')

