'''
# This need to be added beacuse you cannot import directly capm_function file here.
You can import directly when both the files are in same directory or folder.
'''
import sys
sys.path.append('D:\Data Analyst Project\CAPM Project')  

import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import pandas_datareader.data as web
import capm_function



st.set_page_config(page_title="CAPM APP",
                   page_icon="chart_with_upwards_trend",
                   layout="wide")



# taking input from the user
col1, col2=st.columns([1,1])
with col1:
    stock=st.selectbox("Choose a stock",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','GOOGL'))
with col2:
    year=st.number_input("Number of years",1,10)


# getting data for SP500
end=datetime.date.today()
start=datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)
SP500=web.DataReader(['sp500'],'fred',start,end)

# Downloading data for single stock and storing only "Close" attribute
stock_df=pd.DataFrame()
data=yf.download(stock, period=f'{year}y')
stock_df[f'{stock}']=data['Close']


stock_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)

# Merging both the data
SP500.columns=['Date','sp500']
stock_df=pd.merge(stock_df,SP500,on='Date',how='inner')
# print(stock_df)

# Calling daily_return function to calculate daily returns of the stock
stock_daily_return=capm_function.daily_return(stock_df)
# print(stock_daily_return)

beta={}
alpha={}

# Calling calculate_beta function to calculate beta and alpha values
b,a=capm_function.calculate_beta(stock_daily_return,stock)

beta[stock]=b
alpha[stock]=a


st.header(f"Beta Value = {beta[stock]}")


rf=0 # Considering risk free rate 0
rm=stock_daily_return['sp500'].mean()*252 # Average Market Return

# Calculating expected return using CAPM model
return_value=str(round(rf+(beta[stock]*(rm-rf)),2))

st.header(f"Expected Return = {return_value}%")


st.plotly_chart(capm_function.beta_chart(stock_daily_return,b,a,stock))


