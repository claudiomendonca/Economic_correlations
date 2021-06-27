# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 14:21:29 2021
Função para plotar duas series temporais 
Não finalizado
@author: ClaudioMendonca
"""

import matplotlib

def plot_compare(data_frame,col1,col2):
        
    t = list(data_frame.index.values)
    data1 = data_frame[col1]
    data2 = data_frame[col2]
    
    fig, ax1 = plt.subplots()
    
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
