import datetime
import streamlit as st
import pandas as pd
import pandas_datareader.data as web

import yfinance as yf

import capm_function

st.set_page_config(page_title="CAPM Return",
                   page_icon="chart_with_upwards_trend",
                   layout="wide")


st.title("Capital Asset Pricing Model")

# taking input from the user
col1, col2=st.columns([1,1])
with col1:
    stocks_list=st.multiselect("Choose a stocks",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','GOOGL'),('TSLA','AAPL','AMZN','GOOGL'))
with col2:
    year=st.number_input("Number of years",1,10)


# getting data for SP500
end=datetime.date.today()
start=datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)
SP500=web.DataReader(['sp500'],'fred',start,end)
# print(SP500.head())

# Downloading data for all selected stocks and storing only "Close" attribute
stocks_df=pd.DataFrame()
for stock in stocks_list:
    data=yf.download(stock, period=f'{year}y')
    stocks_df[f'{stock}']=data['Close']

# print(stocks_df.head())

stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)
# print(SP500.dtypes)
# print(stocks_df.dtypes)

SP500.columns=['Date','sp500']
stocks_df=pd.merge(stocks_df,SP500,on='Date',how='inner')

# print(stocks_df.head())

# Displaying the Data
col1,col2=st.columns([1,1])
with col1:
    st.markdown("### Dataframe Head")
    st.dataframe(stocks_df.head(), use_container_width=True)
with col2:
    st.markdown("### Dataframe Tail")
    st.dataframe(stocks_df.tail(), use_container_width=True)



col1, col2=st.columns([1,1])
with col1:
    st.markdown('### Price of all the stocks')
    st.plotly_chart(capm_function.interactive_plot(stocks_df))
with col2:
    st.markdown('### Price of all the stocks(After Normalizing)')
    st.plotly_chart(capm_function.interactive_plot(capm_function.normalize(stocks_df)))

# Calling daily_return function to calculate daily returns of the stock
stocks_daily_return=capm_function.daily_return(stocks_df)
# print(stocks_daily_return.head())


beta={}
alpha={}

# Calling calculate_beta function to calculate beta and alpha values
for i in stocks_daily_return.columns:
    if i!='Date' and i!='sp500':
        b,a=capm_function.calculate_beta(stocks_daily_return,i)

        beta[i]=b
        alpha[i]=a

# print(beta,alpha)


# Displaying Beta values
beta_df=pd.DataFrame(columns=['Stock','Beta Value'])
beta_df['Stock']=beta.keys()
beta_df['Beta Value']=[str(round(i,2)) for i in beta.values()]

col1, col2=st.columns([1,1])
with col1:
    st.markdown('### Calculated Beta Value')
    st.dataframe(beta_df, use_container_width=True)



rf=0 # Considering risk free rate 0
rm=stocks_daily_return['sp500'].mean()*252 # Average Market Return

# Calculating expected return using CAPM model
return_df=pd.DataFrame()
return_value=[]
for stock, value in beta.items():
    return_value.append(str(round(rf+(value*(rm-rf)),2)))

return_df['Stock']=stocks_list

return_df['Return Value']=return_value
with col2:
    st.markdown('### Calculated return using CAPM')
    st.dataframe(return_df, use_container_width=True)





