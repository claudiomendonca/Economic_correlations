# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 18:14:02 2021
Correlação entre a wege e o dolar
@author: ClaudioMendonca

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as web
import seaborn as sns
import yfinance as yf
from scipy import stats
from alpha_vantage.timeseries import TimeSeries

alpha_vantage_key = #Criar key no site do alpha_vantage https://www.alphavantage.co/ para duvidas ver o video: https://www.youtube.com/watch?v=kB4jCoVyLRI&t=204s
ts = TimeSeries(key=alpha_vantage_key, output_format = 'pandas')
ts.get_symbol_search('IFIX')

#Importando dados do dollar e renomeando a coluna
df_dollar = web.get_data_yahoo("USDBRL=x")["Close"]
df_dollar = df_dollar.rename('Dollar')

#Importando dados do ibovespa e renomeando a coluna
df_ibov = web.get_data_yahoo("^BVSP")["Close"]
df_ibov = df_ibov.rename('IBOV')

#Importando dados da selic
df_selic = pd.read_csv("taxa_selic_BC.txt", delimiter='\t')
df_selic = df_selic.set_index("Date")
df_selic.index = df_selic.index.astype(str)
df_selic.index = pd.to_datetime(df_selic.index, errors='coerce', format="%d/%m/%Y")

#Importando dados do IFIX e renomeando a coluna
df_ifix = ts.get_daily(symbol = 'IFIX.SAO', outputsize = 'full')[0]["4. close"]
df_ifix = df_ifix.rename('IFIX')

df_ifix_selic = pd.concat([df_selic,df_ifix],axis=1)
df_ifix_selic = df_ifix_selic.fillna(method="ffill")
df_ifix_selic=df_ifix_selic.dropna()

Corr_spearman_ifix_selic = df_ifix_selic.corr(method='spearman')
Corr_pearson_ifix_selic = df_ifix_selic.corr(method='pearson')


df_all=pd.concat([df_ibov,df_dollar,df_ifix,df_selic],axis=1)
df_all = df_all.fillna(method="ffill")
df_all.dropna()

#criando database com todas ações e concatenando ao database original
ticker_text = open('tickers_reduzido.txt','r').readlines() #ticker reduzidos é um arquivo com apenas alguns tickers para teste rapido tem o arquivo completo chamado tickers
teste = ticker_text
for ticker in ticker_text:
    try:
        ticker = ticker.strip()
        df_ticker = web.get_data_yahoo(f'{ticker}.SA')["Adj Close"]
        df_ticker = df_ticker.rename(ticker)
        df_all=pd.concat([df_all,df_ticker],axis = 1) #VERIFICAR COMO ACRESCENTAR UMA COLUNA
    except:
        print('Não rodou para a ação: '+ticker)
        

df_all = df_all.fillna(method="ffill")
Corr_spearman = df_all.corr(method='spearman')
Corr_pearson = df_all.corr(method='pearson')

sns.heatmap(Corr_spearman, annot=True)



# Plot
data_inicio = '2016-12-25'
data_fim = '2021-06-25'

plot_compare(df_all,'WEGE3','Dollar',data_inicio, data_fim, False)

