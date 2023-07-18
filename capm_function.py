import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

# Function to plot inetrative plotly chart
def interactive_plot(df):
    fig=px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[i], name=i)
    fig.update_layout(width=450, margin=dict(l=20, r=20, t=20, b=20),
                       legend=dict(orientation='h', yanchor='bottom',
                                   y=1.02, xanchor='right', x=1))
    return fig

# function to normalize the prices based on the initial price
def normalize(df_org):
    df=df_org.copy()
    for i in df.columns[1:]:
        df[i]=df[i]/df[i][0]
    return df

# function to calculate daily returns
def daily_return(df):
    df_DR=df.copy()
    for i in df.columns[1:]:
        for j in range(1,len(df)):
            df_DR[i][j]=((df[i][j]-df[i][j-1])/df[i][j-1])*100
        df_DR[i][0]=0
    return df_DR

# funtion to calculate beta
def calculate_beta(stocks_daily_return,stock):
    b,a= np.polyfit(stocks_daily_return['sp500'],stocks_daily_return[stock],1)
    return b,a


def beta_chart(stock_daily_return,b,a,stock):
    fig=px.scatter(stock_daily_return, stock_daily_return['sp500'],stock_daily_return[stock],title=stock)
    fig.add_scatter(x=stock_daily_return['sp500'], y=b * stock_daily_return['sp500'] + a, line=dict(color="red"))
    fig.update_layout(width=800, margin=dict(l=20, r=20, t=20, b=20),
                       legend=dict(orientation='h', yanchor='bottom',
                                   y=1.02, xanchor='right', x=1))
    return fig