# -*- coding: utf-8 -*-
"""
Created on Thu Feb 01 22:17:35 2018

@author: Plinio Bueno
"""

#%%
from __future__ import division
import pandas as pd
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft,fftfreq
import numpy as np

# =============================================================================
# =============================================================================
# Analise de ondas usando FFT.
# =============================================================================
# =============================================================================

# =============================================================================
# Criando umas ondas para o teste. 
# =============================================================================

# f = frequencia da onda
# A = Amplitude da onda
f1 = 0.3 #Hz
A1 = 3

f2 = 5
A2 = 5

f3 = 10
A3 = 1

#f4 = 30 #Nessa configuração f4 entra como uma onda energética que não está coberta pela analise. Descomentar para ver o efeito. 
#A4 = 10


# =============================================================================
# Iniciando parametros de analise de fft
# =============================================================================
# OS PARAMETROS DE FFT DEVEM SER ESCOLHIDOS COM BASE NA FREQUENCIA DE NYSQUIN
# E NO HARMONICO DE MAIOR PERIODO (MENOR FREQUENCIA) A SER OBSERVADO NO SINAL

# ti = tempo_inicial
ti = 0

#Frequencia de Nyquist = Frequencia de amostragem 
#A frequencia de Nyquist deve ser no minimo o dobro da maior frequencia presente no sinal
#
fNy = int(2*max([f1,f2,f3]) * (1.5)) #Melhor aumentar um pouco mais =D
#Repare que ao criar o gráfico, a maior frequencia presente no gráfico é justamente 10Hz
#que é a maior frequencia entre as ondas. 

#Tempo total de amostragem 
#COMO ESCOLHER O TEMPO TOTAL DE AMOSTRAGEM??? 
#A TAMANHO DA JANELA DE AMOSTRAGEM DEFINIRÁ QUAL O ARMONICO DE MENOR FREQUENCIA QUE PODERÁ SER ANALISADO.
tf = int(1/min(f1,f2,f3)) * (2) #Acho que deve ter no minimo 8* o tamanho da onda de menor frequencia.

#Definindo o numero de amostragens
n_am = tf * fNy #tempo total de amostragem x a frequencia de amostragem retorna o numero de amostras da série. 

# x representa a lista de momentos onde houve amostragem.
x = np.linspace(ti,tf,n_am)

# Criando dados para teste. Numa situação real, a variavel onda é substituida por dados reais. 
# equacao da onda = np.sin(2*np.pi*frequencia)*amplitude + deslocamento no eixo y.
onda1 = np.array([np.sin(aux*2*np.pi * f1) * A1 for aux in x])
onda2 = np.array([np.sin(aux*2*np.pi * f2) * A2 for aux in x])
onda3 = np.array([np.sin(aux*2*np.pi * f3) * A3 for aux in x])
onda4 = 0
#onda4 = np.array([np.sin(aux*2*np.pi * f4) * A4 for aux in x])
onda = onda1 + onda2 + onda3 + onda4
onda.mean()
#onda = onda - onda.mean()

plt.figure(0)
plt.plot(x[:150],onda[:150])

 
#Usando a funcao fftfreq para retirar os harmonicos da serie
# fftfreq = (n_am, d= timestep) --> Quanto maior o timestep, 
# freq = [0, 1, ...,   n/2-1,     -n/2, ..., -1] / (d*n)   if n is even 
freq = fftfreq(n_am,d = 1/fNy)
freq = np.split(freq,2)[0]


#Usando a funcao fft para descobrir o harmonico com maior energia
fy = abs(fft(onda)) #o abs retira a parte imaginaria do numero
fy = np.split(fy,2)[0]


plt.figure(1)
plt.plot(freq,fy)

#%%

from scipy.signal import butter, lfilter, freqz

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=6):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


#lowcut > 0.0001 (nao pode ser zero)
#hightcyt < fNy/2 - 0.0001  (metade do NyQuistRate)    
filtered_onda = butter_bandpass_filter(onda,0.0001,14.999,fNy,order=6)


filtered_fy = abs(fft(filtered_onda)) #o abs retira a parte imaginaria do numero
filtered_fy = np.split(filtered_fy,2)[0]



plt.figure(2)
plt.plot(freq,fy)
plt.plot(freq,filtered_fy)