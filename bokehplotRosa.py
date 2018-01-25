# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 15:51:22 2017

@author: Plinio Bueno Andrade Silva
"""
 
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import LinearAxis, Range1d,HoverTool, Arrow, OpenHead, NormalHead, VeeHead,BoxAnnotation,LabelSet,Label
from bokeh.embed import components 

from datetime import datetime
from datetime import timedelta
#from datetime import tzinfo
import numpy as np

from math import isnan
import os
import time
import zipfile
import copy
import sys
import json
from scipy import interpolate
import pandas as pd

f = open('bokehplotRosa.txt','w')
f.write(datetime.today().strftime('%d %H:%M:%S '))
f.close()


rm = 1 #raio da figura
figsize = 250
hS = figsize/20  # headsize
lS = figsize/65.5  # linesize  
tS = '%.0fpx'%float(figsize/25)
Hs0 = 0.4 #min Hs estimado
Hs1 = 1.8 #max Hs estimado
VC0 = 0.01 #min velocidade de corrente estimado
VC1 = 0.2 #max velocidade de corrente estimado


#%%

path = os.path.abspath(__file__)

dirr = os.path.dirname(path)



try:
    with open(os.path.join(dirr,'dados.txt_json.txt')) as f:
        temp = f.read()
        temp = temp.strip('_marcadordivisao')
        dB10 = json.loads(temp)
        f.close()
except Exception as e:
    print (str(e))
    pass

        
try:    
    with open(os.path.join(dirr,'dados.txt_json.txt')) as f:
        temp = f.read()
        temp = temp.strip('_marcadordivisao')
        dB4 = json.loads(temp)
        f.close()
except Exception as e:
    print(str(e))
    pass

d = pd.DataFrame([dB4,dB10],index=['bb4','bb10'])
d = d.loc[:,['dataF','corRVelNow','corRDirNow','HsNow','TpNow','DpNow','Tensao','Pitch','Roll','Pressao']]
temp = d.columns.values.astype(dtype='string').tolist()
temp[0] = u'Data'
temp[1] = u'C.Mag (m/s)'
temp[2] = u'C.Dir (°)'
temp[3] = u'Hs(m)'
temp[4] = u'Tp(s)'
temp[5] = u'Dp(°)'
temp[6] = u'Tensão'
temp[9] = u'Pressão'
d.columns = temp

TabelaResumo = d.to_html(classes="table table-striped table-condensed table-bordered")
#temp = d.to_html(classes="table table-striped table-condensed table-bordered")
#TabelaResumo = json.dumps(temp.encode('utf-8'))

#f = open('teste.html','w')
#f.write(temp.encode('utf-8'))
#f.close()


#%%

def rosa(titulo,nomeArquivo,figsize):
    TTOOLS = ['save']
              
    output_file(os.path.basename(__file__)+nomeArquivo)
    tS = figsize/35
#    
    pp = figure(width=figsize,height=int(figsize+(figsize*0.22)),
                x_range = (-rm-rm*0.2 ,rm+rm*0.2),
                y_range = (-rm-rm*0.2 ,rm+rm*0.2),
                toolbar_location="above",
                toolbar_sticky=False,
                tools=TTOOLS,
                title=titulo,
                background_fill_alpha=0.9,
                border_fill_alpha=0.9)
    
    ### Fabricando a rosa dos ventos
    def poi(h,al,n):
        y1 = np.sin(np.deg2rad(al)) * h * n
        x1 = np.cos(np.deg2rad(al)) * h 
        y2 = np.sin(np.deg2rad(al+90)) * h/8 * n
        x2 = np.cos(np.deg2rad(al+90)) * h/8  
        y3 = 0
        x3 = 0
        return[[x1,x2,x3],[y1,y2,y3]]
    
    #Criando as coordenadas dos triangulos que farão a rosa dos ventos
    anglesp = np.arange(0,360,90) #angulos do N,S,L,E
    angless = np.arange(45,405,90) #angulos do NE,NO,SE,SO
    x = [] #guarda as coordenadas x de todos os pontos do triangulo.
    y = []
    px = [] #guarda as coordenadas x somente do ponto mais distante. 
    py = []
    for aux in anglesp:
        x0,y0 = poi(rm,aux,1)
        x1,y1 = poi(rm,aux,-1)
        x.append(x0)
        x.append(x1)
        y.append(y0)
        y.append(y1)
        px.append(x0[0])
        py.append(y0[0])
        
    for aux in angless:    
        x0,y0 = poi(rm*0.75,aux,1)
        x1,y1 = poi(rm*0.75,aux,-1)
        x.append(x0)
        x.append(x1)
        y.append(y0)
        y.append(y1)
        px.append(x0[0])
        py.append(y0[0])
        pass
    
#    alpha1 = [1,0.8,1,0.8,1,0.8,1,0.8]
#    alpha1 = [0.6,0.4,0.6,0.4,0.6,0.4,0.6,0.4]
#    alpha1 = [0.2,0.1,0.2,0.1,0.2,0.1,0.2,0.1]
#    alpha2 = [0.2,0.1,0.2,0.1,0.2,0.1,0.2,0.1]
    alpha1 = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    alpha2 = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    
    
    
    alpha = alpha1+alpha2
    
    pp.patches(x, y, alpha=alpha, line_width=1,) #plota os triangulos da rosa dos ventos.
#    color='blue'
    ###Colocando os labels na rosa dos ventos
    names=['L', 'N', 'O', 'S','NE','NO','SO','SE']
#    offsetx = [5, -5, -15, -5, 0, -15, -17 , 0]
#    offsety = [-10, 0,-10, -17, 0, 0, -17,-15]
    
    offsetx = [4, -3, -9, -3, 0, -14, -15 , 1]
    offsety = [-5, 0,-5, -12, 0, 3, -12,-11]
    
    for aux in xrange(len(px)):
        label = Label(
                    x = px[aux], 
                    y = py[aux], 
                    text = names[aux],
                    render_mode = 'canvas',
                    x_offset = offsetx[aux],
                    y_offset = offsety[aux],
                    text_font_size = '%.0fpt'%tS
                    
                    )
        pp.add_layout(label)
    
    
    #criando ciculos perimetrais
    pr = np.arange(0,rm,0.2*rm)
    for aux in pr:
        pp.arc (0, 0, radius = aux, start_angle = 0, end_angle = 6.28, color = 'black',alpha = 0.1,line_dash = 'dotted')
        pass
    pp.arc (0, 0, radius = rm, start_angle = 0, end_angle = 6.28, color = 'black',alpha = 0.3,line_dash = 'solid')
    
    #criando radiais
    angulos = []
    p0 = []
    for aux in np.linspace(0,360,16,endpoint=False):
        p0.append(0)    
        angulos.append(aux)
        pass
    pp.ray(p0,p0,length = rm, angle=angulos,angle_units="deg",color="black",line_width=1,alpha = 0.2,line_dash = 'dotted')
    
    
    #criando label das perimetrais
#    px = [np.cos(np.deg2rad(20))*aux for aux in pr]
#    py = [np.sin(np.deg2rad(20))*aux for aux in pr]
#    names = ['%0.2f'%(aux*1) for aux in pr]
#    offsetx = [0,0,0,0,0]
#    offsety = [0,0,0,0,0]
#    for aux in xrange(len(px)):
#        label = Label(
#                    x = px[aux], 
#                    y = py[aux], 
#                    text = names[aux],
#                    render_mode = 'canvas',
#                    text_font_size = '8pt',
#                    x_offset = offsetx[aux],
#                    y_offset = offsety[aux])
#        pp.add_layout(label)
#        pass
    return pp



#==============================================================================
#==============================================================================
#==============================================================================
# # # 
#==============================================================================
#==============================================================================
#==============================================================================


#Funcao escala normaliza os valores de Hs e VelCor para escala de 0 a 1.
#NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
def escala(value,maxx,minn):
    return (((value - minn) * (rm - 0)) / (maxx - minn)) + 0

#escala(dB4['HsNow'],maxSerieHs,minSerieHs)
#escala(dB4['corRVelNow'],maxSerieCorVel,minSerieCorVel)

#dataS = pd.Series(dB4)
#temp2 = pd.read_json(temp,typ='series')



#==============================================================================
# A partir daqui entra com os dados corrente B4. 
#==============================================================================

### Criando label da caixa.    
#text = [u'Dir. Cor. B4: %s°'%dB4['corRDirNow'],u'Vel. Cor. B4: %s m/s'%(dB4['corRVelNow']*1)]
#pos = 10
#for aux in text:
#    citation = Label(x=10, y = pos, x_units='screen', y_units='screen',
#                     text=aux, render_mode='css',
#                     border_line_color='black', border_line_alpha=1.0,
#                     background_fill_color='white', background_fill_alpha=1.0)    
#    
#    ppB4.add_layout(citation)   
#    pos += 21
#    pass    
    
    
    
#Criando seta que aponta a direção. 

### ppB4 = rosa
ppB4 = rosa(u'Onda e Corrente bb4','bokeh_rosa_onda_corrente_B4.html',figsize)

dB4['corRVelNow'] = float(dB4['corRVelNow'])
dB4['corRDirNow'] = float(dB4['corRDirNow'])

x_end = np.cos(np.deg2rad((dB4['corRDirNow']) * -1 + 90)) * escala(dB4['corRVelNow'],VC1,VC0)
y_end = np.sin(np.deg2rad((dB4['corRDirNow']) * -1 + 90)) * escala(dB4['corRVelNow'],VC1,VC0)
x_start = 0
y_start = 0

ppB4.add_layout(Arrow(end=VeeHead(size=hS,fill_color='DarkMagenta',line_color="DarkMagenta",fill_alpha=0.7), 
                   line_color="DarkMagenta",
                   line_cap="round",
                   line_width=lS,
                   line_alpha = 0.7,
                   x_start=x_start,
                   y_start=y_start,
                   x_end=x_end,
                   y_end=y_end,
                   ))

ppB4.circle(10,10,size=1,color='DarkMagenta',legend='Corr.')

#==============================================================================
# A partir daqui entra com os dados onda B4
#==============================================================================
#Criando seta que aponta a direção. <------------------------------ Dados Aqui!
x_start = np.cos(np.deg2rad(dB4['DpNow'] * -1 + 90)) * escala(dB4['HsNow'],Hs1,Hs0)
y_start = np.sin(np.deg2rad(dB4['DpNow'] * -1 + 90)) * escala(dB4['HsNow'],Hs1,Hs0)
x_end = 0
y_end = 0

ppB4.add_layout(Arrow(end=VeeHead(size=hS,fill_color="DarkBlue",line_color="DarkBlue",fill_alpha=0.7), 
                   line_color="DarkBlue",
                   line_cap="round",
                   line_width= lS,
                   line_alpha = 0.7,
                   x_start=x_start,
                   y_start=y_start,
                   x_end=x_end,
                   y_end=y_end,
                   ))

ppB4.circle(10,10,size=1,color='DarkBlue',legend='Onda')
### Criando label da caixa. <-------------------------------------- Dados Aqui!
#text = [u'Direção: %3.0f°'%dB4['DpNow'],u'Periodo: %2.0f s'%(dB4['TpNow']),u'Altura: %2.2f m'%(dB4['HsNow'])]
#
#pos = 10
#for aux in text:
#    citation = Label(x=10, y = pos, x_units='screen', y_units='screen',
#                     text=aux, render_mode='css',
#                     border_line_color='black', border_line_alpha=1.0,
#                     background_fill_color='white', background_fill_alpha=1.0)    
#    
#    ppB4.add_layout(citation)   
#    pos += 21
#    pass


ppB4.circle(10,10,size=1,color='DarkMagenta',legend='Corr.')
ppB4.legend.label_text_font_size = tS
ppB4.legend.background_fill_alpha = 0
ppB4.legend.location =(-12,-12)

ppB4.grid.grid_line_alpha = 0 #tira o grid lines
ppB4.yaxis.bounds = (0,0) #tira os labels do eixo y
ppB4.xaxis.bounds = (0,0) #tira os labels do eixo x
ppB4.background_fill_color = 'gray'
ppB4.background_fill_alpha = 0.05


RosaB4, divB4 = components(ppB4)

show(ppB4)

#%%

#==============================================================================
# A partir daqui entra com os dados corrente B10. 
#==============================================================================

### ppB10 = rosa
ppB10 = rosa(u'Onda e Corrente bb10',u't10,bokeh_rosa_onda_corrente_B10.html',figsize)


    
dB10['corRDirNow'] = float(dB10['corRDirNow'])  
dB10['corRVelNow'] = float(dB10['corRVelNow'])  

#Criando seta que aponta a direção. 
x_end = np.cos(np.deg2rad((dB10['corRDirNow']) * -1 + 90)) * escala(dB10['corRVelNow'],VC1,VC0)
y_end = np.sin(np.deg2rad((dB10['corRDirNow']) * -1 + 90)) * escala(dB10['corRVelNow'],VC1,VC0)
x_start = 0
y_start = 0

ppB10.add_layout(Arrow(end=VeeHead(size=hS,fill_color='DarkMagenta',line_color="DarkMagenta",fill_alpha=0.7), 
                   line_color="DarkMagenta",
                   line_cap="round",
                   line_width=lS,
                   line_alpha = 0.7,
                   x_start=x_start,
                   y_start=y_start,
                   x_end=x_end,
                   y_end=y_end,
                   ))



#==============================================================================
# A partir daqui entra com os dados onda B10
#==============================================================================
#Criando seta que aponta a direção. <------------------------------ Dados Aqui!
x_start = np.cos(np.deg2rad(dB10['DpNow'] * -1 + 90)) * escala(dB10['HsNow'],Hs1,Hs0)
y_start = np.sin(np.deg2rad(dB10['DpNow'] * -1 + 90)) * escala(dB10['HsNow'],Hs1,Hs0)
x_end = 0
y_end = 0

ppB10.add_layout(Arrow(end=VeeHead(size=hS,fill_color="DarkBlue",line_color="DarkBlue",fill_alpha=0.7), 
                   line_color="DarkBlue",
                   line_cap="round",
                   line_width=lS,
                   line_alpha = 0.7,
                   x_start=x_start,
                   y_start=y_start,
                   x_end=x_end,
                   y_end=y_end,
                   ))

ppB10.circle(10,10,size=1,color='DarkBlue',legend='Onda')



ppB10.circle(10,10,size=1,color='DarkMagenta',legend='Corr.')
ppB10.legend.label_text_font_size = tS
ppB10.legend.background_fill_alpha = 0
ppB10.legend.location =(-12,-12)

ppB10.grid.grid_line_alpha = 0 #tira o grid lines
ppB10.yaxis.bounds = (0,0) #tira os labels do eixo y
ppB10.xaxis.bounds = (0,0) #tira os labels do eixo x
ppB10.background_fill_color = 'gray'
ppB10.background_fill_alpha = 0.05


[aux for aux in dir(ppB10) if aux.find('ground')>0]

RosaB10, divB10 = components(ppB10)


xdic = {}
xdic.update(
        dict(RosaB4 = divB4 + RosaB4,
             RosaB10 = divB10 + RosaB10,
             TabelaResumo = TabelaResumo)
            )
        
temp = json.dumps(xdic,allow_nan = True)

#path = os.path.relpath(__file__)
#dirr = os.path.dirname(path)
f = open(os.path.join(dirr,'boiasTabelaResumoRosa.json'),'w')
f.write(temp)
f.close()

f = open('bokehplotRosa.txt','a')
f.write(datetime.today().strftime('%d %H:%M:%S'))
f.close()

#print('ok')

show(ppB10)
