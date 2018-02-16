# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:11:26 2018

@author: Plinio Bueno
"""

from __future__ import division
import pandas as pd
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft,fftfreq
import numpy as np
import sys



f1 = 1/np.random.rand()
#f1 = 1/10
A1 = 0.5

f2 = 1/np.random.rand()
A2 = .6

f3 = 1/np.random.rand()
A3 = .3

f4 = 1/np.random.rand()
A4 = .4

ti = 0


f = [f1,f2,f3,f4]

f = np.random.rayleigh(.1,50)
A = np.random.rayleigh(.4,50) 


#f = [f1,f1,f1,f1]
#A = [A1,A2,A3,A4]
#f = [f1]


#n_am = 1024 #numero total de amostras

#Determinar frequencia de Nysquin que é em função da maior frequencia a ser analisada
#Escolher uma fNy incorreta ( fNy < f_alta_energética*2) pode rebater a energia de alta frequencia em frequencias mais baixas. 
#fNy também determina a frequencia maxima que aparecerá no espectro (assim como fi define a minima e intervalo entre elas)
fNy = round(2*max(f) * (2.5),2) #Nysquin rate / frequencia de amostragem. 

#Determinar a frequencia fundamental (fi) do sinal. É a menor frequencia que poderá ser analisada no sinal
#A frequencia fundamental = 1/min(f) / 2 | metade do comprimento de onda do sinal com maior comprimento.

tf_min = 1/min(f) # Tempo minimo necessário para que a série seja coletada
                  # Não deve ser multiplicado por nada!!!

#Numero minimo de amostras para pegar a onda de menor frequencia na janela.
n_amin = tf_min * fNy 

#Passando numero de amostras para base 2^n (1024). Numero recomendado minimo de amostras
for aux in xrange(20):
    if 2**aux < n_amin:
        pass
    else:
        n_am = 2**aux *(4)
        break
    pass

#Tempo recomendado para realizar as amostras:
tf = n_am * 1/fNy #Não deve ser multiplicado por nada!!!

#frequencia fundamental (menor frequencia que aparecerá no espectro.)
#pode ser usada ao invés do fftfreq para criar o eixo de frequencias do fft. 
#fi é o intervalo entre frequencias.
fi = 1/tf 

#Serie com os momentos de coleta
t_series = np.linspace(ti,tf,n_am,endpoint=False) 


onda1 = np.array([np.sin(aux*2*np.pi * f1 + np.pi) * A1 for aux in t_series])
onda2 = np.array([np.sin(aux*2*np.pi * f2 + np.pi/2) * A2 for aux in t_series])
onda3 = np.array([np.sin(aux*2*np.pi * f3 + np.pi/4) * A3 for aux in t_series])
onda4 = np.array([np.sin(aux*2*np.pi * f4) * A4 for aux in t_series])
onda = onda1 + onda2 + onda3 + onda4
#onda = onda - onda.mean()

onda = 0
for ix,ax in enumerate(A):
    onda += np.array([np.sin(aux*2*np.pi * f[ix]) * A[ix] for aux in t_series])




plt.figure()
plt.plot(t_series,onda)


#aplicando hanning window para suavisar o sinal
hanning_onda = onda * np.hanning(len(t_series))
plt.plot(t_series,hanning_onda)


# =============================================================================
#%% Analisando onda
# =============================================================================
print('analisando onda')
from scipy.signal import hanning
from scipy.interpolate import CubicSpline
from scipy.integrate import quad, quadrature
from scipy.signal import welch

df = pd.DataFrame()
df['P'] = onda
df['t_series'] = t_series

#df.P = df.P - df.P.mean()

#aplicando hanning window
df['filtered_P']  = df.P  * hanning(len(df.P))

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

#Criando série filtrada
#df['filtered_P'] = butter_bandpass_filter(df.P,f1,f3 - 0.01,fNy,order=6)

print('welch')
dx,dy = welch(df.P,fs = fNy,scaling = 'density')
dffw = pd.DataFrame(data=dict(dx=dx,dy=dy))

# =============================================================================
#%%Plotando FFT e Welch
# =============================================================================
plt.figure()
plt.title('Signal Power Density Welch')
plt.plot(dffw.dx,dffw.dy,ls='--',label="Welch densidade")

Wpower = CubicSpline(dffw.dx,dffw.dy) #Criando uma funcao para calculo de área do spectro
temp = np.arange(dffw.dx.iloc[0],dffw.dx.iloc[-1],0.001)
plt.plot(temp,Wpower(temp),'-',label='Welch CubicSpline')
plt.legend()

# =============================================================================
# Descobrindo os picos do espectro
# =============================================================================

def nextpeak(data):
    d = pd.DataFrame(data=data)
    for ix in range(len(d)):
        if ix == 0: #Primeiro item, nao faz nada
            pass
        elif d.iloc[ix].values < d.iloc[ix - 1].values: #Verifica se está descendo ainda
            pass
        elif d.iloc[ix].values > d.iloc[ix - 1].values: #Achou o Vale apenas descida! Acha prox max
            return int(d.iloc[ix:].idxmax().values) #Procura pela posicao (iloc), MAS RETORNA O INDICE
                                                    #então pode ser usado para achar o valor no 
                                                    #dataframe original =D
        else:
            return 'erro'


def allpeaks(frequencia,energia):
    
    d = pd.DataFrame(data=dict(frequencia=frequencia,energia=energia))
    d['sentido'] = 0
    for ix in range(len(d)):
        if ix == 0: #Primeiro item, nao faz nada
            pass
        elif d.loc[ix,'energia'] > d.loc[ix - 1,'energia']: #Ascendente
            d.loc[ix,'sentido'] = +1
        elif d.loc[ix,'energia'] < d.loc[ix - 1,'energia']: #Descendente
            d.loc[ix,'sentido'] = -1
        else:
            return 'erro'        
        pass
    
    d['shift'] = d.loc[1:,'sentido'].append(pd.Series(),ignore_index=True) #Adiciona uma coluna shift com 1 shift pra cima
    d = d.loc[np.logical_not(d['sentido'] == d['shift'])] #logica not. sentido == 1 é pico, sentido == -1 é vale.
    d = d[1:len(d)-1]#tira a primeira e ultima linha 
    d = d.drop(columns = 'shift') #tira a coluna shift
    picos = d.loc[d['sentido'] == 1]
    picos = picos.sort_values(by=['energia'],ascending = False) 
    vales = d.loc[d['sentido'] == -1]
    vales = vales.sort_values(by=['energia'],ascending = False)        
    return d,picos.frequencia.values,picos.energia.values

print('determinando picos')    
temp = np.arange(0,dffw.dx.iloc[-1],0.001)
dtemp2 = pd.DataFrame()
dtemp2['frequencia'] = temp
dtemp2['energia'] = Wpower(temp)
    
pica,x_peaks,y_peaks = allpeaks(dtemp2.frequencia,dtemp2.energia)      
Delta_f = fi/2 #É o delta de cada frequencia. 
   
#%%
# =============================================================================
# Calculando e armazendo os valores associados aos picos encontrados.
# =============================================================================    
print('iniciando calculo da area teste')
H3 = [] #armazenará o valor calculado de Altura significativa Hs
Tp = []

#print(quadrature(Wpower,x_peaks[0] - Delta_f,x_peaks[0] + Delta_f))

print('iniciando calculo da area') 
for ix,aux in enumerate(x_peaks):
    if len(H3) == 0: #Caso nao haja nenhum valor ainda / primeiro pico
        H3.append(abs(quadrature(Wpower,aux - Delta_f,aux + Delta_f)[0])**0.5 * 4) 
        #plt.plot([aux - Delta_f for _ in xrange(int(y_peaks[ix]))],xrange(int(y_peaks[ix])),'--')       
        #plt.plot([aux + Delta_f for _ in xrange(int(y_peaks[ix]))],xrange(int(y_peaks[ix])),'--')       
        Tp.append(1/aux)
    elif Wpower(aux) > Wpower(x_peaks[0])*0.4: #so adiciona um segundo pico se ele tiver pelo menos 70% da energia do primeiro
        H3.append(abs(quadrature(Wpower,aux - Delta_f,aux + Delta_f)[0])**0.5 * 4) 
        #plt.plot([aux - Delta_f for _ in xrange(int(y_peaks[ix]))],xrange(int(y_peaks[ix])),'--')       
        #plt.plot([aux + Delta_f for _ in xrange(int(y_peaks[ix]))],xrange(int(y_peaks[ix])),'--')               
        Tp.append(1/aux)
    else:
        break    

print('calculo da area finalizado')

resultWelch = pd.DataFrame(data = dict(H3=H3,Tp=Tp))

print('H3',H3)
print('Tp',Tp)



