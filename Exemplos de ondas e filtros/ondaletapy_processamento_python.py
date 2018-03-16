# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 13:54:30 2018

@author: pliniobas
"""

from scipy.signal import butter, lfilter, freqz
from scipy.fftpack import fft,fftfreq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftfreq
from scipy.signal import butter, lfilter, freqz, hanning

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

#Lendo a serie de pressao
df = pd.read_csv('P.txt',header=None)
df.columns=['P']
df = df*10 #transforma a pressão em metros (dbar)

#retirando a média da série
df.P = df.P - df.P.mean()

#aplicando hanning window
df.P = df.P * hanning(len(df.P))

#Criando série filtrada
df['filtered_P'] = butter_bandpass_filter(df.P,1.0/15,1.0/5,1,order=6)

#Aplicando hanning Window na série filtrada
df.filtered_P = df.filtered_P * hanning(len(df.P))

#frequencia de amostragem do sinal = fNy
fNy = 1

plt.figure()
plt.plot(df.filtered_P)

from scipy.signal import periodogram
from scipy.interpolate import CubicSpline
from scipy.integrate import quad

x,y = periodogram(df.filtered_P)
dff = pd.DataFrame(data=dict(x=x,y=y))
Ppower = CubicSpline(x,y)
plt.figure()
plt.plot(x,Ppower(x))
H3 = (quad(Ppower,x[0],x[-1])[0]**0.5) * 4
Tp = 1/dff.loc[dff.y.idxmax(),'x']


#%%














fft_a = np.split(abs(fft(a)),2)[0]
fft_ax = np.split(fftfreq(len(a)),2)[0]
#%%
#plt.figure(-1)
#plt.plot(a)
#plt.plot(fft_ax,fft_a)
#arredondando o valor da série para apenas 3 casas. É necessário? MUDA O VALOR DO TP quando as há dois picos de frequencias muito próximos
#df.P = np.round(df.P,3) 

#Criando série filtrada
df['filtered_P'] = butter_bandpass_filter(df.P,1.0/15,1.0/5,1,order=5)

#FFT da série bruta
fy = np.split(abs(fft(df['P'])),2)[0]

#FFT da série filtrada
filtered_fy = np.split(abs(fft(df['filtered_P'])),2)[0]

#Obtendo as frequencias da série de FFT
fx = np.split(fftfreq(512,d=1),2)[0]

#Plotando as duas sériesd de FFT 
plt.figure(0)
plt.plot(fx,fy)
plt.plot(fx,filtered_fy)

#Jogando as séries em um novo dataframe para facilitar a descoberta dos maiores picos
dft = pd.DataFrame(data = dict(fx=fx,fy=fy,filtered_fy=filtered_fy))

#periodo associado ao pico de energia 1
tp1 = 1/dft.loc[dft.filtered_fy.idxmax(),'fx']
fq1 = dft.loc[dft.filtered_fy.idxmax(),'fx']
#energia no pico 1
en1 = dft.loc[dft.filtered_fy.idxmax(),'filtered_fy']

temp = dft.drop(dft.filtered_fy.idxmax())
tp2 = 1/temp.loc[temp.filtered_fy.idxmax(),'fx']
fq2 = temp.loc[temp.filtered_fy.idxmax(),'fx']

#energia no pico 2
en2 = dft.loc[dft.filtered_fy.idxmax(),'filtered_fy']


#%%







# =============================================================================
#ECAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#%%Tentando descobrir a altura da onda pela Energia dela. 
#Considerando que a energia da onda é a area = base x altura.

from scipy.integrate import quad,simps,cumtrapz      

#Distribuindo a energia em uma onda senoidal de amplitude constante. 
onda_x = lambda x,f : np.sin(x*2*np.pi*f) #*A so que A passa dividindo....
#A integral da eq. da onda dá sua energia multiplicada pela Amplitude. 

#tp1 = usando metade do periodo (tp1/2) para calcular o metade do valor da energia, 
#para não se cancelarem por causa do lobulo negativo da onda. 
temp = en1 / (256/tp1) #256/tp1 é o numero de meias ondas dentro da serie. A energia total da série dividida entre ondas iguais que preencheriam a série toda
A1 = temp / quad(onda_x,0,tp1/2,args = (fq1,))[0] #acha a amplitude de 1 onda. tp1/2 é para a parte negativa da onda não cancelar a positiva.
h1_mean = A1*2
print('Tp1= %.3f Hmean= %.3f'%(tp1,h1_mean))

temp = en2 / (256/tp2) 
A2 = temp / quad(onda_x,0,tp2/2,args = (fq2))[0]
h2_mean = A2*2
print('Tp1= %.3f Hmean= %.3f'%(tp2,h2_mean))


# =============================================================================
#%% Devaneios para  calculo.
#
# =============================================================================
filtered_tp1 = butter_bandpass_filter(df.P,fq1-0.01,fq1+0.01,1,order=5)
max(filtered_tp1) - min(filtered_tp1) 

filtered_tp2 = butter_bandpass_filter(df.P,fq2-0.01,fq2+0.01,1,order=5)
max(filtered_tp2) - min(filtered_tp2) 

#max(df.P) - min(df.P)

plt.figure(1)
plt.plot(filtered_tp1)


#%%

from scipy.interpolate import interp1d,CubicSpline

#temp = [aux if aux > 0 else aux for aux in filtered_tp1]
onda = CubicSpline(df.index,temp)
plt.plot(np.linspace(0,512,1024,endpoint=False),onda(np.linspace(0,512,1024,endpoint=False)))
#quad(onda,0,512)
#zzz =  np.split(abs(fft(filtered_tp1)),2)[0]

