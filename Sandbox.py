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
from plot_comparativo import plot_compare
import requests

alpha_vantage_key = 'XMZZGD9RSMNPOYIJ'#Criar key no site do alpha_vantage https://www.alphavantage.co/ para duvidas ver o video: https://www.youtube.com/watch?v=kB4jCoVyLRI&t=204s
ts = TimeSeries(key=alpha_vantage_key, output_format = 'pandas')
ts.get_symbol_search('petr4')

url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=PETR4.SAO&apikey=XMZZGD9RSMNPOYIJ'
r = requests.get(url)
data = r.json()

print(data)


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=PETR4.SAO&apikey=XMZZGD9RSMNPOYIJ'
r = requests.get(url)
data = r.json()

print(data)

#Importando dados da petr4 e renomeando a coluna
df_PETR4 = ts.get_daily(symbol = 'PETR4.SAO', outputsize = 'full')[0]["4. close"]
df_PETR4 = df_PETR4.rename('PETR4')
df_PETR4 = df_PETR4.fillna(method="ffill")

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
Df_Foresti = pd.concat([Df_Foresti,df_PETR4], axis=1)
Df_Foresti = Df_Foresti.fillna(method="ffill")

data_inicio = '2016-01-04'
data_fim = '2021-06-25'
normalized = True
col1 = 'PETR4'
col2 = 'Brent (BRL)'
col3 = 'Brent (USD)'

plot_compare(Df_Foresti,'PETR4','Brent (BRL)',data_inicio, data_fim, False)

data_frame = Df_Foresti

data_frame = data_frame[data_inicio:data_fim]
t = list(data_frame.index.values)

if normalized == False:    
    data1 = data_frame[col1]
    data2 = data_frame[col2]

else:
    data1 = data_frame[col1]/data_frame[col1][0]
    data2 = data_frame[col2]/data_frame[col2][0]
      
plt.plot()

color = 'tab:red'
plt.plot(t, data1, color=color, label='PETR4')
color = 'tab:blue'
plt.plot(t, data2, color=color, label = 'Brent (BRL)')
plt.legend()
plt.show()


color = 'tab:red'
ax1.set_xlabel('data')
ax1.set_ylabel(col1, color=color)
ax1.plot(t, data1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel(col2, color=color)  # we already handled the x-label with ax1
ax2.plot(t, data2, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
