# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib as plt

#serie historica retirada do IBGE
arquivo_IPCA = "IPCA.csv"
arquivo_Iron_Ore = "Iron_Ore.csv"
arquivo_cobre = "Cobre.csv"
arquivo_Ouro = "Ouro.csv"
arquivo_Brent = "Petroleo_Brent.csv"
arquivo_Prata = "Prata.csv"
arquivo_Dollar = "USD_BRL.csv"


#Criando dataframe do dollar
Dollar = pd.read_csv(arquivo_Dollar, delimiter = ';',decimal=',')
Dollar['Data'] =  pd.to_datetime(Dollar['Data'], format='%d.%m.%Y')
Dollar = Dollar.set_index('Data')
Dollar = Dollar['Último']
Dollar = Dollar.rename('USD x BRL')

#Criando dataframe de commodities
Ore = pd.read_csv(arquivo_Iron_Ore, delimiter = ',',decimal=',')
Ore['Data'] =  pd.to_datetime(Ore['Data'], format='%d.%m.%Y')
Ore = Ore.set_index('Data')
Ore = Ore['Último']
Ore = Ore.rename('Iron_Ore (USD)')

Ouro = pd.read_csv(arquivo_Ouro, delimiter = ';',decimal='.')
Ouro['Data'] =  pd.to_datetime(Ouro['Data'], format='%d.%m.%Y')
Ouro = Ouro.set_index('Data')
Ouro = Ouro['Último']
Ouro = Ouro.rename('Ouro (USD)')

Prata = pd.read_csv(arquivo_Prata, delimiter = ';',decimal=',')
Prata['Data'] =  pd.to_datetime(Prata['Data'], format='%d.%m.%Y')
Prata = Prata.set_index('Data')
Prata = Prata['Último']
Prata = Prata.rename('Prata (USD)')

Cobre = pd.read_csv(arquivo_cobre, delimiter = ';',decimal=',')
Cobre['Data'] =  pd.to_datetime(Cobre['Data'], format='%d.%m.%Y')
Cobre = Cobre.set_index('Data')
Cobre = Cobre['Último']
Cobre = Cobre.rename('Cobre (USD)')

Brent = pd.read_csv(arquivo_Brent, delimiter = ';',decimal=',')
Brent['Data'] =  pd.to_datetime(Brent['Data'], format='%d.%m.%Y')
Brent = Brent.set_index('Data')
Brent = Brent['Último']
Brent = Brent.rename('Brent (USD)')

Df = pd.concat([Dollar, Ore, Ouro, Prata, Cobre, Brent],axis=1)
Df = Df.fillna(method="ffill")
Df['Iron_Ore (BRL)'] = Df['USD x BRL']*Df['Iron_Ore (USD)']
Df['Ouro (BRL)'] = Df['USD x BRL']*Df['Ouro (USD)']
Df['Prata (BRL)'] = Df['USD x BRL']*Df['Prata (USD)']
Df['Cobre (BRL)'] = Df['USD x BRL']*Df['Cobre (USD)']
Df['Brent (BRL)'] = Df['USD x BRL']*Df['Brent (USD)']


#Criando dataframe para IPCA
#Criando coluna de datas
start_date = '1979-12-25'
end_date = '2021-06-25'
dates = pd.date_range(start_date, end_date, freq='M')

#lendo dados do IBGE e criando um dataframe
IPCA = pd.read_csv(arquivo_IPCA, delimiter = ',')
IPCA_t = IPCA.T
print(IPCA_t.head())
#acrescentando datas ao df do IBGE
IPCA_IBGE= pd.DataFrame({'date':dates, 'IPCA_Num_Ind':IPCA_t.iloc[1:,0], 
                         'IPCA_Var_Men':IPCA_t.iloc[1:,1],
                         'IPCA_Var_12M':IPCA_t.iloc[1:,2]})

IPCA_IBGE = IPCA_IBGE.set_index('date')
IPCA_IBGE['IPCA_Num_Ind'] = IPCA_IBGE['IPCA_Num_Ind'].astype(np.float64)
IPCA_IBGE['IPCA_Var_Men'] = IPCA_IBGE['IPCA_Var_Men'].astype(np.float64)
IPCA_IBGE['IPCA_Var_12M'] = IPCA_IBGE['IPCA_Var_12M'].astype(np.float64)

Df_Foresti = pd.concat([Df,IPCA_IBGE],axis=1)
Df_Foresti = Df_Foresti.fillna(method="ffill")

#selecionando janela de tempo 
data_inicio = '2001-12-25'
data_fim = '2021-06-25'

#greater than the start date and smaller than the end date
sub_df = IPCA_IBGE[data_inicio:data_fim]

#plot
t = list(sub_df.index.values)
data = sub_df['IPCA_Var_Men']

fig, ax1 = plt.subplots()
ax1.set_xlabel('data')
ax1.set_ylabel('IPCA_Var_Men - (%)')
ax1.plot(t,data)
plt.show()