import yfinance as yf
import streamlit as st
import pandas as pd 


st.write(''' #Simple Stock Price App
         Shown are the stock 'closing price' and 'volume' of Google!''')


tickerSymbol = "AAPL"

tickerData = yf.Ticker(tickerSymbol)

ticketDf = tickerData.history(period ='id', start='2010-5-31', end='2020-5-31')

st.write('''## Closing Price''')

st.line_chart(ticketDf.Close)

st.write('''## Volume Price''')
st.line_chart(ticketDf.Volume)