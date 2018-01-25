#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 16:44:30 2016

@author: Plinio Bueno Andrade Silva
"""

"""
Para char o arquivo via linha de comando, sempre chame da seguinte forma:
    python bokehplot.py "NomeArquivoDados.txt" Data1 Data2
    
    
    Se chamar direto:
        bokeplot.py ... ele não irá conseguir ler os argumentos 2 e 3 das datas.

"""


#import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import LinearAxis, Range1d,HoverTool, Arrow, OpenHead, NormalHead, VeeHead,BoxAnnotation,LabelSet,Label
from bokeh.embed import components 

from datetime import datetime
from datetime import timedelta
#from datetime import tzinfo
import numpy as np

from math import isnan
import os
import subprocess
import time
import zipfile
import copy
import sys
import json
from scipy import interpolate
import pandas as pd

FILE = __file__

#Horario analizado 14:20 (horario de verao)
print time.clock();
try:
    f = open('bokehplot.txt','w')
    f.write(datetime.today().strftime('%d %H:%M:%S '))
    f.close()
except:
    pass

xdic = {}
dTX = pd.DataFrame(index=[u'Hs(m)',u'Tp(s)',u'Dp(°)',u'CorVel(m/s)',u'CorDir(°)'],columns=['Atual','Max','Min','Med','Std'])

#==============================================================================
#%% Acerto de variaveis.              
#==============================================================================

#ajusde te horario de Verao: 0 para nao / 1 para sim.
Verao = 0              

#horaCompensa pode ser usado para ajustar o horario impresso pelo datalogger no arquivo.
#horaCompensa = timedelta(hours= Verao) 

horaVerao = timedelta(hours=Verao)   

                                         
#bokehTime modifica o horario no grafico bokeh
bokehTime = -3 # 

#datarange basico 
datarange = 30
#==============================================================================
# entrando com o intervalo de tempo. Se nao houver argumentos ou forem 
# invalidos, hoje menos 7 dias
#==============================================================================


try:
        
    dataI = datetime.strptime(sys.argv[2],'%d/%m/%Y')
    dataF = datetime.strptime(sys.argv[3],'%d/%m/%Y') #a data inicial tem que ser mais recente
    
        
    if dataI == dataF:
        dataI = datetime.now() + horaVerao
        dateF = datetime.now() + horaVerao - timedelta(days = datarange)
    
    if dataI < dataF:
        tempI = dataI
        tempF = dataF
        dataI = tempF
        dataF = tempI
        pass
    
    pass
except:
    dataI = datetime.now() + horaVerao - timedelta(days= 0)
    dataF = datetime.now() + horaVerao - timedelta(days= datarange)
    pass


print("Entrando com datas:")
print("dataI: " + dataI.strftime('%d/%m/%Y'))
print("dataF: " + dataF.strftime('%d/%m/%Y'))

#==============================================================================
#%% Abrindo arquivo de dados
#==============================================================================

temp = os.path.dirname(os.path.realpath(FILE)) + '/dados/dados.txt'

print('diretorio procurado: ',temp)
f = open(temp,'r')
sys.argv.append(temp)
pass


#==============================================================================
# 
#==============================================================================

temp = sys.argv[1].split('/')
fileName = temp[-1]
print ('filename: ',fileName)
dirPath = os.path.dirname(os.path.abspath(FILE)) + '/'
print ('dirPath: ',dirPath)
proName = os.path.basename(os.path.abspath(FILE))
print ('progName: ',proName)

dados = f.readlines()
f.close()

d = [aux.split(',') for aux in dados]

#filtro de linhas que não tenham 58 parametros
dellist = []     
for aux in range(len(d)):
    if len(d[aux]) != 58:
        dellist.append(aux)
        pass

for aux in reversed(dellist):
    del(d[aux])
    pass



#transforma os dados de horario em objeto datetime. Aqui se faz a correção de horario caso necessario.   
#transforma os dados da tabela em float  

dellist = []
for aux in range(len(d)):
    try:
        d[aux][0] = datetime.strptime(''.join(d[aux][0:5]),'%Y%m%d%H%M') + horaVerao
        for aux2 in range(5,57+1): #transforma os demais dados
            try:
                d[aux][aux2] = float(d[aux][aux2])
                pass
            except:
                dellist.append(aux)
            pass
        pass
    except:
        dellist.append(aux)
        pass

for aux in reversed(dellist):
    del(d[aux])
    pass

#temp = []
#for aux in d:
#    temp.append(aux[6])
#    pass
#
#np.nanmax(temp)

#==============================================================================
#%% Analisando data range
#==============================================================================

# Verificando se tem algum dado da tabela dentro do range escolhido para o site.
# Se não tiver, o programa forçará uma data dentro do range.

d.sort() # se certifica que a ultima linha da tabela está com a data de coleta mais recente.

if dataI > d[-1][0]:
    dataI = d[-1][0]
    dataF = d[-1][0] - timedelta(days= datarange)
    pass


#Tirando fora os dados que não estão no range escolhido.
dellist2 = []
for aux in range(len(d)):
    if d[aux][0] > (dataI + timedelta(days=1)) or d[aux][0] < dataF: # + timedelta (days=1) é para incluir o dia de hoje.
        dellist2.append(aux)
        pass
    pass

for aux in reversed(dellist2):
    del(d[aux]) #d é a lista de ondas. 
    pass


#%% filtrando dados com pandas

#==============================================================================
# Criando cabeçalho para dataset do pandas
#==============================================================================

h1 = ["Data0",'1','2','3','4',"Tensao5","Pressao6","Rumo7","Temp8","Pitch9","Roll10","Hs11","Dp12","Tp13"] #mag dir. #lista arquivo bruto.
for aux in range(1,22+1):
    h1.append(('mag%2.0f'%aux).replace(' ','0'))
    h1.append(('dir%2.0f'%aux).replace(' ','0'))
    pass

dp = pd.DataFrame(d,columns = h1)
dp = pd.DataFrame(d)
dp.columns = h1
dp.columns

#with open('css-table.css','r') as f:
#    css = f.read()
#    f.close()
#    pass

dptemp = dp.iloc[:,1].as_matrix().astype(np.float16)

link = []

link.append('https://cdnjs.cloudflare.com/ajax/libs/fixed-data-table/0.6.4/fixed-data-table-base.css')
link.append('https://cdnjs.cloudflare.com/ajax/libs/fixed-data-table/0.6.4/fixed-data-table-base.min.css')
link.append('https://cdnjs.cloudflare.com/ajax/libs/fixed-data-table/0.6.4/fixed-data-table-style.css')
link.append('https://cdnjs.cloudflare.com/ajax/libs/fixed-data-table/0.6.4/fixed-data-table-style.min.css')
link.append('https://cdnjs.cloudflare.com/ajax/libs/fixed-data-table/0.6.4/fixed-data-table.css')
link.append('https://cdnjs.cloudflare.com/ajax/libs/fixed-data-table/0.6.4/fixed-data-table.js')
link.append('https://cdnjs.cloudflare.com/ajax/libs/fixed-data-table/0.6.4/fixed-data-table.min.css')
link.append('https://cdnjs.cloudflare.com/ajax/libs/fixed-data-table/0.6.4/fixed-data-table.min.js')

dphtml = ''
for aux in link:
    dphtml += r'<link rel="stylesheet" type="text/css" media="screen" href="%s" />'%aux + '\n'
    pass


style = (r'<style>table {    border-collapse: collapse;    width: 100%;}th, td {    text-align: left;    padding: 8px;}tr:nth-child(even){background-color: #f2f2f2}</style>')
dphtml += style
dphtml += dp.to_html()

 
    

##########################################
#%%filtrando os dados com velocidade corrente irreal
##########################################
# Vou repetir os dados das colunas anteriores 
dellist2 = []
for aux in range(len(d)):
#    for aux2 in range(-2,-45,-2):
    for aux2 in range(14,56+1,2):                                                                                                                                   
        if d[aux][aux2] > 3:
            if aux2 <= 14  : #no caso da primeira camada, não há dado da anterior.
#                d[aux][aux2] = copy.deepcopy(d[aux][aux2+2])
                d[aux][aux2] = np.nan
                pass
            else:# para os demais casos.
                d[aux][aux2] =  np.nan
                pass
            dellist2.append(aux)
#            break #- ativado quando deletava a coleta inteira.
            pass
        pass
    pass



#for aux in reversed(dellist2): #deletar a coleta nao esta sendo um bom negocio pois some com dados de onda
#    print('dados com velocidade irreal')
#    print(d[aux][0])
#    del(d[aux]) #d é a lista de ondas. 
#    pass

##########################################
#%%filtrando dados com direcao corrente irreal
##########################################
dellist2 = []
for aux in range(len(d)):
#    for aux2 in range(-1,-44,-2):
    for aux2 in range(15,57+1,2):
        if d[aux][aux2] > 360 or d[aux][aux2] < 0 or isnan(d[aux][aux2]):
            if aux2 <= 15: #no caso da primeira camada, não há dado da anterior.
#                d[aux][aux2] = copy.deepcopy(d[aux][aux2+2])
                d[aux][aux2] = np.nan
                pass
            else:# para os demais casos.
#                d[aux][aux2] = copy.deepcopy(d[aux][aux2-2])
                d[aux][aux2] = np.nan
                pass
            dellist2.append(aux)
#            break
            pass
        pass
    pass

#==============================================================================
#%% Filtrando todos os dados pelo limite aceitavel
#==============================================================================

#maremed = np.nanmean([d[aux][6] for aux in xrange(len(d))])

for aux in xrange(len(d)):
    if d[aux][11] > 6 or d[aux][11]< 0.4: #filtro de Hs
#        print d[aux][11]
        d[aux][11] = np.nan
        pass
    
    if d[aux][12] > 360: #filtro de Dp
#        print d[aux][12]
        d[aux][12] = np.nan
        pass
    if d[aux][13] > 20 or d[aux][13] < 3: #Filtro de Tp
#        print d[aux][13]
        d[aux][13] = np.nan
        pass
    if d[aux][6] > 40 or d[aux][6] <  10: #Filtro de Nivel
#        print d[aux][5]
        d[aux][6] = np.nan
    pass



#==============================================================================
#%% Criando uma segunda lista de correntes, já que a lista de correntes atualiza de 10 em 10 minutos.
#==============================================================================
d2 = copy.deepcopy(d)


#Tirando os intervalos de minutos da coleta de onda, já que ocorre somente de 1 em 1 hora. (d[aux][0].minute) -> escolher minuto que atualiza
dellist2 = []
for aux in range(len(d)):
    if d[aux][0] > (dataI + timedelta(days=2)) or d[aux][0] < dataF or d[aux][0].minute < 11 or d[aux][0].minute > 29:
        dellist2.append(aux)
        pass
    pass

#sys.exit(3)

for aux in reversed(dellist2):
    del(d[aux])
    pass


#==============================================================================
#==============================================================================
#==============================================================================
#%% # # Correntes
#==============================================================================
#==============================================================================
#==============================================================================

#==============================================================================
#%% Dados de corrente Resultante das 22 camadas
#==============================================================================

d2np = np.array(d2)
dp = pd.DataFrame(d2,columns=h1)


corRVelVect = []
corRVelEsca = []
corRDir = []


#Copiando dados de todas as camadas para fazer o calculo da resultante de correntes de todo o periodo selecionado.


for aux in range(len(dp)):
        
#    tempVel = [d2[aux][aux2] for aux2 in (range(-32,-44,-2))] #copia dados de velocidade de correntes
#    tempVel = [d2[aux][aux2] for aux2 in (range(-2,-45,-2))] #copia dados de velocidade de correntes
#    tempVel = np.array(tempVel)
#    tempDir = [d2[aux][aux2] for aux2 in (range(-31,-43,-2))] #copia dados de direcao de correntes
#    tempDir = [d2[aux][aux2] for aux2 in (range(-1,-44,-2))] #copia dados de direcao de correntes
#    tempDirRad = [np.deg2rad(tempDir)]
    

    tempVel = dp.iloc[aux].loc['mag15'::2].loc['mag15':'mag21'].values.astype('float')
    tempDir = dp.iloc[aux].loc['dir15'::2].loc['dir15':'dir21'].values.astype('float')
    tempDirRad = np.deg2rad(tempDir)

        
    tempDirXRad = np.cos(tempDirRad)*tempVel #acha os vetores em x
    tempDirYRad = np.sin(tempDirRad)*tempVel #acha os vetores em y

    tempDirMeanX = np.nanmean(tempDirXRad) #faz a média dos vetores em X
    tempDirMeanY = np.nanmean(tempDirYRad) #faz a média dos vetores em Y
    
    tempDirMean = np.rad2deg(np.arctan2(tempDirMeanY,tempDirMeanX)) #faz a soma vetoria e acha a direção resultante
    if tempDirMean < 0:
        tempDirMean += 360
        pass
    
    tempVelMeanVect = pow(pow(tempDirMeanX,2) + pow(tempDirMeanY,2),0.5) # Acha a velocidade vetorial resultante
    tempVelMeanEsca = np.nanmean(tempVel) # Acha a velocidade escalar resultante
    
    corRVelVect.append(tempVelMeanVect) 
    corRVelEsca.append(tempVelMeanEsca)
    corRDir.append(tempDirMean)
    pass
    

#%% 
   
#dTX = pd.DataFrame(index=[u'Hs(m)',u'Tp(s)',u'Dp(°)',u'CorVel(m/s)',u'CorDir(°)'],columns=['Atual','Max','Min','Med','Std'])

def estatisticaCor2(velocidade,direcao): #entrar com lista d2, posVel = -2, posDir = -1 pra primeira camada.
    corVelMax = np.nanmax(velocidade)
    corVelMin = np.nanmin(velocidade)
    corVelMean = np.nanmean(velocidade)
    corVelStd = np.nanstd(velocidade)
         
    #Dados estatisticos de corDir, corrente direcao
    corDirY = np.nanmean(np.sin(np.deg2rad(direcao)))
    corDirX = np.nanmean(np.cos(np.deg2rad(direcao)))
    corDirMean = np.arctan2(corDirY,corDirX)*(180/np.pi) 
    if corDirMean < 0:
        corDirMean += 360
        pass
    
    estatList = "%3.2f,%3.2f,%3.2f,%3.2f,%3.0f,%3.2f,%3.0f"%(corVelMax,corVelMin,corVelMean,corVelStd,corDirMean,velocidade[-1],direcao[-1])
    
    pdCorVel = pd.DataFrame(data = [[corVelMax,corVelMin,corVelMean,corVelStd,velocidade[-1]]],index=[u'CorVel(m/s)'],columns=['Max','Min','Med','Std','Atual'])
    pdCorDir = pd.DataFrame([[corDirMean,direcao[-1]]],index=[u"CorDir(°)"],columns=['Med','Atual'])
    
    return estatList,corVelMax,corVelMin,corVelMean,corVelStd,corDirMean,velocidade[-1],direcao[-1],pdCorVel,pdCorDir 
    
 
corRString,corRVelMax,corRVelMin,corRVelMean,corRVelStd,corRDirMean,corRVelNow,corRDirNow,pdCorVel,pdCorDir = estatisticaCor2(corRVelVect,corRDir)

#corRVelNow = corRVelVect[-1]
#corRDirNow = corRDir[-1]
dTX=pdCorVel.combine_first(dTX)
dTX=pdCorDir.combine_first(dTX)


#%%
xdic.update(dict(
        corRVelMax = '%.2f'%corRVelMax,
        corRVelMin = '%.2f'%corRVelMin,
        corRVelMean = '%.2f'%corRVelMean,
        corRVelStd = '%.2f'%corRVelStd,
        corRDirMean = '%.0f'%corRDirMean,
        corRVelNow = '%.2f'%corRVelNow,
        corRDirNow = '%.0f'%corRDirNow
        )
)
    

datasCor = [aux[0] + timedelta(hours=bokehTime) for aux in d2] #o +bokehtime compensa o horario do grafico. Pra string do dado, será feito -bokehtime para voltar ao que era antes.

corRVelVectS  = ["%3.2f"%(aux*1.94384) for aux in corRVelVect]
corRDirS = ["%3.0f"%(aux) for aux in corRDir]


#==============================================================================
#%% Criando source list para bokeh.
#==============================================================================
alturaAux = [0.3*(10**7) for _ in datasCor]
alturaAux2 = [(0.7*(10**7))*0.75 for _ in datasCor] 

#dirI e dirF sao responsaveis por abrir ou fechar o raio da seta em funcao do periodo.
       
#for aux in range(len(dirI)):
#    dirI[aux] = dirI[aux] - (0.005 * periodo[aux]**2)
#    dirF[aux] = dirF[aux] + (0.005 * periodo[aux]**2)
#    pass

#sys.exit(10)

corRVelVect = (np.nan_to_num(corRVelVect))#[::-1]
corRDir = (np.nan_to_num(corRDir))#[::-1]
#datasCor.reverse()


corRVelVectStr = ['%1.2f m/s'%aux for aux in corRVelVect]
datasStr = [(aux+timedelta(hours=-bokehTime)).strftime("%Y/%m/%d %H:%M") for aux in datasCor]
posSeta = [-0.05 for _ in datasCor]
corRDir = np.deg2rad(np.asarray(corRDir))
corRDirStr = [u'%1.0f°'%(np.rad2deg(aux)) for aux in corRDir]

#Corrigindo o valor numerico para a plotagem. 
corRDir = (corRDir[:] * -1) - (np.pi/2) #Arruma a direcao da seta para o plot na figura. 
dirI = [aux - 0.09 for aux in corRDir]
dirF = [aux + 0.09 for aux in corRDir]  


source2 = ColumnDataSource(
            data=dict(
                    corRVelVect = corRVelVect[::-3],
                    corRDir = corRDir[::-3],
                    datasCor = datasCor[::-3],
                    corRVelVectStr = corRVelVectStr[::-3],
                    corRDirStr = corRDirStr[::-3],
                    datasStr = datasStr[::-3],
                    posSeta = posSeta[::-3],
                    dirI = dirI[::-3],
                    dirF = dirF[::-3],
                    alturaAux2 = alturaAux2[::-3],
                    )
            )
             
#corRVelVectS = corRVelVectS,
#corRDirS = corRDirS,            
#==============================================================================
#%% Figura Corrente         
#==============================================================================


TOOLS = ['xwheel_zoom','reset','save','xpan',
          HoverTool(names=['corrente'],
                    tooltips=[("Velocidade","@corRVelVectStr"),("Direcao","@corRDirStr"),("datasStr","@datasStr")])]
          

output_file(os.path.basename(FILE)+"correntes.html")
#550 200

try:
    x_rangei = datasCor[-288]
except:
    x_rangei = datasCor[0]    
    pass

p = figure(width=500, height=250, x_axis_type="datetime",y_range=(-0.1,0.3),
            toolbar_location="above",toolbar_sticky=False,
            tools=TOOLS,title="Velocidade e Direcao de Corrente",
            background_fill_alpha=0.9,
            border_fill_alpha=0.9,
            x_range = (time.mktime(x_rangei.timetuple())*1000,time.mktime((datasCor[-1]+timedelta(hours=2)).timetuple())*1000))





low_box = BoxAnnotation(top=0.1, fill_alpha=0.1, fill_color='green')
mid_box = BoxAnnotation(bottom=0.1, top=0.15, fill_alpha=0.1, fill_color='yellow')
high_box = BoxAnnotation(bottom=0.15, fill_alpha=0.1, fill_color='red')

p.add_layout(low_box)
p.add_layout(mid_box)
p.add_layout(high_box)
p.yaxis.bounds = (0,corRVelMax+(corRVelMax/20))

#p.ygrid.grid_line_dash = [1,10]

p.annular_wedge('datasCor', 'posSeta',  inner_radius=0, outer_radius=0.2*(10**7), source = source2,
                start_angle='dirI', end_angle='dirF' ,color="black", alpha=0.8, legend="Dp(°)")
p.ray('datasCor', 'posSeta' , length = 'alturaAux2' , angle='corRDir', source = source2, 
      angle_units="rad", color="black", line_width=1,alpha=0.8)


p.xaxis[0].axis_label = 'Data'
p.yaxis[0].axis_label = 'Velocidade(m/s)'


p.line('datasCor', 'corRVelVect', color='navy', alpha=0.5,source=source2,legend="Vel(m/s)", name = 'corrente')
p.square('datasCor', 'corRVelVect', color='navy', alpha=0.5,source=source2,size=1)


#p.circle('datasCor','corRDir', color='green',alpha=0.5,y_range_name="CorRDirBar",size=4,source=source2,legend="Dir(°)")
#p.extra_y_ranges = {"CorRDirBar": Range1d(start=0, end=359)}
#p.add_layout(LinearAxis(y_range_name="CorRDirBar",axis_label='Direcao(°)'), 'right')


p.legend.orientation = "vertical"
p.legend.location = "top_left"
p.grid.grid_line_color = "gray"
p.grid.grid_line_alpha = 0.7
#p.legend.background_fill_alpha=0.7


#==============================================================================
# 
#==============================================================================

#==============================================================================
# 
#==============================================================================
script, div = components(p)

xdic.update(
        dict(
            grafCorrentes = div + script
            )
        )

show(p)



#f = open(os.path.basename(FILE)+"_graf_correntes.html","w")
#f.write(div)
#f.write(script)
#f.close()



#==============================================================================
#==============================================================================
#==============================================================================
#%% # # Criando figura Ondas
#==============================================================================
#==============================================================================
#==============================================================================

#==============================================================================
#%% Dados de ondas
#==============================================================================
          
periodo = [aux[13] for aux in d]

#filtro para se todas os periodos forem nan.
if np.isnan(periodo).all():
    periodo = np.asarray(periodo)
    periodo[:] = 0
    pass

direcaograus = [aux[12] for aux in d]
direcao = [(aux[12])*np.pi/180 for aux in d] 
    
    
#filtro para se todas as direcoes forem nan.
if np.isnan(direcao).all():
    direcao = np.asarray(direcao)
    direcao[:] = 0
    pass    

#filtro para se todas as direcoes forem nan.
if np.isnan(direcaograus).all():
    direcaograus = np.asarray(direcaograus)
    direcaograus[:] = 0
    pass    
 
   


altura = [aux[11] for aux in d] #a lista altura possui as alturas de onda
datas = [aux[0] + timedelta(hours=bokehTime)for aux in d] #lista datas possui as datas de coleta (Não sei bem o porque tive que adicionar o timezone aqui... Parece que o bokeh tá plotando em relacao ao UTC... vai saber).
#media = np.nanmean(altura)  
media = -1
media = [media for aux in datas] #lista repetitiva. Posicao de plot das setas no grafico de ondas.  

if np.isnan(media).all():
    media = np.asarray(media)
    media[:] = 0
    pass

#filtro para se todas as alturas forem nan.
if np.isnan(altura).all():
    altura = np.asarray(altura)
    altura[:] = 0
    pass

#Altura aux eh o responsavel por tentar regular o raio da seta em funcao da altura de onda
#alturaAux = [(aux**4)*0.4*(10**7) for aux in altura]

#alturaAux2 eh o responsavel por fazer o rabo da seta             
#alturaAux2 = [((aux**4)*0.4*(10**7))*1.5 for aux in altura]              

#Datos estatisticos do Hs
HsMax = np.nanmax(altura)
HsMin = np.nanmin(altura)
HsMean = np.nanmean(altura)
HsStd = np.nanstd(altura)
HsString = "%3.2f,%3.2f,%3.2f,%3.2f,"%(HsMax,HsMin,HsMean,HsStd)

temp = pd.DataFrame(data=[[HsMax,HsMin,HsMean,HsStd,altura[-1]]],index=['Hs(m)'],columns=['Max','Min','Med','Std','Atual'])
dTX = dTX.combine_first(temp)

#Dados estatisticos do Tp
TpMax = np.nanmax(periodo)
TpMin = np.nanmin(periodo)
TpMean = np.nanmean(periodo)
TpStd = np.nanstd(periodo)
TpString = "%3.2f,%3.2f,%3.2f,%3.2f,"%(TpMax,TpMin,TpMean,TpStd)
temp = pd.DataFrame(data=[[TpMax,TpMin,TpMean,TpStd,periodo[-1]]],index=['Tp(s)'],columns=['Max','Min','Med','Std','Atual'])
dTX = dTX.combine_first(temp)

#Dados estatisticos do Dp
Dp = direcao
DpY = np.nanmean(np.sin(np.deg2rad(Dp)))
DpX = np.nanmean(np.cos(np.deg2rad(Dp)))
DpMean = np.arctan2(DpY,DpX)*(180/np.pi) 
if DpMean < 0:
    DpMean += 360
    pass
DpString = "%3.1f"%DpMean

temp = pd.DataFrame(data=[[DpMean,direcao[-1]]],index=[u'Dp(°)'],columns=['Med','Atual'])
dTX = dTX.combine_first(temp)

xdic.update(
        dict(
            HsMax = '%.2f'%HsMax,
            HsMin = '%.2f'%HsMin,
            HsMean ='%.2f'%HsMean,
            HsStd = '%.2f'%HsStd,   
            TpMax = '%.2f'%TpMax,
            TpMin = '%.2f'%TpMin,
            TpMean ='%.2f'%TpMean,
            TpStd = '%.2f'%TpStd,
            DpMean = '%.2f'%DpMean
             )
        )

#==============================================================================
# Filtro de nan, para não chegar nan no bokeh. Javascript não tolera nan
# O Estou colocando esse filtro aqui para o nan ENTRAR na estatistica.
# Mas a partir daqui ele precisa sair para não dar problema no gráfico
#==============================================================================
for aux in range(len(periodo)):
    if isnan(periodo[aux]):
        periodo[aux] = 0.0
        pass
    
    if isnan(altura[aux]):
        altura[aux] = 0.0
        alturaAux[aux] = 0.0
        alturaAux2[aux] = 0.0
        pass
    if isnan(dirI[aux]):
        dirI[aux] = 0.0
        dirF[aux] = 0.0
        pass
    pass


    

#==============================================================================
# Source lista
#==============================================================================
direcao = np.asarray(direcao)
direcaograus = np.rad2deg(direcao)

alturaStr = ['%3.1fm'%aux for aux in altura]
periodoStr = ['%3.1fs'%aux for aux in periodo]
direcaoStr = [u'%3.0f°'%aux for aux in direcaograus]
datasStr = [(aux+timedelta(hours=-bokehTime)).strftime('%Y/%m/%d %H:%M') for aux in datas]

alturaAux = [0.3*(10**7) for aux in altura]
alturaAux2 = [(0.7*(10**7))*1.1 for aux in altura] 

#dirI e dirF sao responsaveis por abrir ou fechar o raio da seta em funcao do periodo.

#passando de cartesiano para esferico.
direcao = (direcao[:]*-1) + np.pi/2
#dirI = [aux - 0.3 for aux in direcao]
#dirF = [aux + 0.3 for aux in direcao]   
dirI = direcao[:] - 0.3
dirF = direcao[:] + 0.3

            
data=dict(
           periodo=periodo,
           direcao=direcao,
           direcaograus=direcaograus,
           altura=altura,
           datas=datas,
           media=media,
           dirI = dirI,
           dirF = dirF,
           alturaAux2 = alturaAux2,
           alturaStr = alturaStr,
           periodoStr = periodoStr,
           direcaoStr = direcaoStr,
           datasStr = datasStr
           )


#criando ColumnDataSource  para o bokeh;
source = ColumnDataSource(
        data=data
    )
        
        
for aux in data.keys():
    try:
        if isnan(data[aux]):
            print data[aux]        
            pass
        pass
    except:
#        print(data[aux])
        pass
    pass

#==============================================================================
#%% Figura Ondas        
#==============================================================================

try:
    x_rangei2 = datas[-48]
    pass
except:
    x_rangei2 = datas[0]
    pass

TOOLS2 = ['xwheel_zoom','reset','save','xpan',
          HoverTool(tooltips=[("Hs","@alturaStr"),("Tp","@periodoStr"),(u"Dp","@direcaoStr"),('Data','@datasStr')])]          

output_file(os.path.basename(FILE)+"ondas.html")
#
p2 = figure(width=500, height=250, x_axis_type="datetime",y_range=(-2, 
            4),toolbar_location="above",toolbar_sticky=False,
            tools=TOOLS2,title="Altura, Periodo e Direção de onda", background_fill_alpha=0.9,
            border_fill_alpha=0.9,
            x_range = (time.mktime(x_rangei2.timetuple())*1000,time.mktime((datas[-1]+timedelta(hours=2)).timetuple())*1000))


p2.xaxis[0].axis_label = 'Data'
p2.yaxis[0].axis_label = 'Hs (m)'
p2.yaxis.bounds = (0,4)


low_box = BoxAnnotation(top=1.5, fill_alpha=0.1, fill_color='green')
mid_box = BoxAnnotation(bottom=1.5, top=2.5, fill_alpha=0.1, fill_color='yellow')
high_box = BoxAnnotation(bottom=2.5, fill_alpha=0.1, fill_color='red')


p2.add_layout(low_box)
p2.add_layout(mid_box)
p2.add_layout(high_box)


p2.line('datas', 'altura', color='navy', alpha=0.5,source=source)
p2.square('datas', 'altura', color='navy', alpha=0.5,source=source,size=3,legend="Hs(m)")


p2.line('datas','periodo', color='green',alpha=0.5,y_range_name="TpBar",source=source)
p2.circle('datas','periodo', color='green',alpha=0.5,y_range_name="TpBar",size=4,source=source,legend="Tp(s)")
p2.extra_y_ranges = {"TpBar": Range1d(start=0, end=16)}

p2.add_layout(LinearAxis(y_range_name="TpBar",axis_label='Tp (s)'), 'right')
#p2.yaxis.bounds = (4,16)



p2.annular_wedge('datas', 'media',  inner_radius=0, outer_radius=0.20*(10**7), source = source,
                start_angle='dirI', end_angle='dirF' ,color="black", alpha=0.8, legend="Dp(°)")
p2.ray('datas', 'media' , length = 'alturaAux2' , angle='direcao', source = source, 
      angle_units="rad", color="black", line_width=1,alpha=0.8)



p2.legend.orientation = "vertical"
p2.legend.location = "top_left"
p2.legend.background_fill_alpha=1
p2.grid.grid_line_color = "gray"
p2.grid.grid_line_alpha = 0.5

script, div = components(p2)

xdic.update(
        dict(
            grafOndas = div+script,
            )
        )


#f = open(os.path.basename(FILE)+"_graf_ondas.html","w")
#f.write(div)
#f.write(script)
#f.close()

show(p2)


#==============================================================================
#==============================================================================
#==============================================================================
#%% #Mare 
#==============================================================================
#==============================================================================
#==============================================================================

date = [aux[0] + timedelta(hours=bokehTime) for aux in d]
dateString = [aux[0].strftime("%Y/%m/%d %H:%M:%S") for aux in d]
mare = [aux[6] for aux in d] #lista com medidas da profundidade

temp = np.nanmean(mare) #media da mare para retirar das profundidades
mare = [aux - temp for aux in mare]

mare = np.asarray(mare,dtype = 'float')
for aux in xrange(len(mare)):
    if np.isnan(mare[aux]):
        mare[aux] = 0
        pass
    pass


#Criando date Stamp para criar funcao de interpolacao
dateStamp = [time.mktime(aux.timetuple()) for aux in date]
dateStamp = np.asarray(dateStamp,dtype='int')

#Criando funcao de interpolacao

#temp = np.arange(dateStamp[0],dateStamp[-1],dateStamp[1]-dateStamp[0])
mareFunc = interpolate.interp1d(dateStamp,mare,kind='slinear') #interpolando eixo de datas como timestamp



#Criando novas datas para usar na funcao de interpolacao                   
dateNew = []
aux = date[0]
while aux < date[-1]:
    aux += timedelta(seconds=600)
    dateNew.append(aux)
    pass

dateStringNew = [aux.strftime("%Y/%m/%d %H:%M:%S") for aux in dateNew]

#Transformando a nova lista em timestamp
dateNewStamp = [time.mktime(aux.timetuple()) for aux in dateNew]    

#Criando as novas medidas de mare em funcao da funcao retornada pela interpolação.
mareNew = mareFunc(dateNewStamp)



#==============================================================================
#%% source lista para bokeh
#==============================================================================

#criando ColumnDataSource  para o bokeh;
source3 = ColumnDataSource(
        data=dict(
                mare = mareNew,
                date = dateNew,
                dateString = dateStringNew
           )
    )


#==============================================================================
#%% Criando figura mare
#==============================================================================
#TOOLS3 = ['xwheel_zoom','reset','save','xpan',
#          HoverTool(tooltips=[("mare","@mare"),("data","@dateString")])]
TOOLS3 = ['xwheel_zoom','reset','save','xpan']
          

output_file(os.path.basename(FILE) + "mare.html")
#550 200

p3 = figure(width=500,
           height=250,
           x_axis_type="datetime",
#           y_range=(np.nanmin(mareNew)*1.20,np.nanmax(mareNew)*1.20),
           y_range=(np.nanmean(mareNew)-(np.nanstd(mareNew)*4),np.nanmean(mareNew)+(np.nanstd(mareNew)*4)),
           x_range = (time.mktime(x_rangei.timetuple())*1000,time.mktime((datasCor[-1]+timedelta(hours=2)).timetuple())*1000),
           toolbar_location="above",
           toolbar_sticky=False,
           tools=TOOLS3,
           title=u"Nível",
           background_fill_alpha=0.9,
           border_fill_alpha=0.9,
           )

 
p3.xaxis[0].axis_label = 'Data'
p3.yaxis[0].axis_label = '(m)'


p3.line('date', 'mare', color='navy', alpha=0.5,source=source3)#,legend="Altura(cm)"
#p.square('datasCor', 'corRVelVect', color='navy', alpha=0.5,source=source2,size=3)


#p.circle('datasCor','corRDir', color='green',alpha=0.5,y_range_name="CorRDirBar",size=4,source=source2,legend="Dir(°)")
#p.extra_y_ranges = {"CorRDirBar": Range1d(start=0, end=359)}
#p.add_layout(LinearAxis(y_range_name="CorRDirBar",axis_label='Direcao(°)'), 'right')


p3.legend.orientation = "vertical"
p3.legend.location = "top_left"
p3.grid.grid_line_color = "gray"
p3.grid.grid_line_alpha = 0.7
#p.legend.background_fill_alpha=0.7

script, div = components(p3)


xdic.update(
        dict(
            grafMare = div+script,
            )
        )

show(p3)

#%%
# =============================================================================
# Dado para bokehplot rosa
# =============================================================================

HsNow = altura[-1]
if np.isnan(HsNow):
    HsNow = 'null'
TpNow = periodo[-1]
if np.isnan(TpNow):
    TpNow = 'null'
DpNow = direcaograus[-1]
if np.isnan(DpNow):
    DpNow = 'null'
Tensao = dp.iloc[-1].loc['Tensao5'] 
if np.isnan(Tensao):
    Tensao = 'null'   
Pressao = dp.iloc[-1].loc['Pressao6'] 
if np.isnan(Pressao):
    Pressao = 'null' 
Pitch = dp.iloc[-1].loc['Pitch9'] 
if np.isnan(Pitch):
    Pitch = 'null' 
Roll = dp.iloc[-1].loc['Roll10'] 
if np.isnan(Roll):
    Roll = 'null'   

xdic.update(
        dict(
            dataI = d2[0][0].strftime("%d/%m/%y %H:%M"),
            dataF = d2[-1][0].strftime("%d/%m/%y %H:%M"),
            HsNow = HsNow,
            TpNow = TpNow,
            DpNow = DpNow,
            Tensao = Tensao,
            Pressao = Pressao,
            Pitch = Pitch,
            Roll = Roll,
            )
        )
 
 
data = json.dumps(xdic,allow_nan=True)        

try:
    sys.argv[2]
    print data
    pass
except:
    pass

with open(dirPath + fileName + '_json.txt','w') as f:
    f.write("_marcadordivisao")
    f.write(data)
    f.close
    pass