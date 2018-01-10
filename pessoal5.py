# -*- coding: utf-8 -*-
"""
Created on Wed May 31 10:57:51 2017

@author: VPNUser
"""

import numpy as np
import os
from datetime import datetime
import fnmatch
import sys

#import threading
#import subprocess

#==============================================================================
# 
#==============================================================================
def DirVelToComp(tdir,tvel):
    if type(tdir) is np.ndarray or list:
        dirRad = [np.deg2rad(tdir[ix]) for ix,aux in enumerate(tdir)]
        U = [np.cos(dirRad[ix])*tvel[ix] for ix,aux in enumerate(dirRad)]
        V = [np.sin(dirRad[ix])*tvel[ix] for ix,aux in enumerate(dirRad)]
        return dict(U=U,V=V)
            
    else:
        dirRad = np.deg2rad(tdir)
        U = np.cos(dirRad)*tvel
        V = np.sin(dirRad)*tvel
        return dict(U=U,V=V)
    pass
    

#import pessoal as p

#dirr = [random.random()*360 for aux in xrange(100)]
#vell = [random.random()*10 for aux in xrange(100)]
#
#comp = [p.DirVelToComp(dirr[ix],vell[ix]) for ix,aux in enumerate(vell)]
#comp[0]['U']
#comp[0]['V']

#ou 

#p.DirVelToComp(dirr,vell)



#%%
#==============================================================================
# 
#==============================================================================
def CompToDirVel(u,v):
    
    if type(u) is np.ndarray or list:
        print('np.ndarray or list')
        tdir = [np.rad2deg(np.arctan2(v[ix],u[ix])) for ix,aux in enumerate(u)]
        for ix,aux in enumerate(tdir):
            if tdir[ix] < 0:
                tdir[ix] += 360
            pass
        tvel = [pow(pow(u[ix],2) + pow(v[ix],2),0.5) for ix,aux in enumerate(u)]            
        return dict(dir=tdir,vel=tvel)
    
    else:
        print('float')
        tdir = np.rad2deg(np.arctan2(v,u)) #faz a soma vetoria e acha a direção resultante
        if tdir < 0:
            tdir += 360
            pass
        
        tvel = pow(pow(u,2) + pow(v,2),0.5) # Acha a velocidade vetorial resultante
        return dict(dir=tdir,vel=tvel)
        pass


#%%
#if type(np.asarray(U)) is np.ndarray:
#    print('ok')
#%%
#type(U[0])

#==============================================================================
#     
#==============================================================================
def estatSerie(velocidade,direcao): #entrar com lista d2, posVel = -2, posDir = -1 pra primeira camada.
    velMax = np.nanmax(velocidade)
    velMin = np.nanmin(velocidade)
    velMean = np.nanmean(velocidade)
    velStd = np.nanstd(velocidade)
         
    v = np.nanmean(np.sin(np.deg2rad(direcao)))
    u = np.nanmean(np.cos(np.deg2rad(direcao)))
    dirMean = np.arctan2(v,u)*(180/np.pi) 
    if dirMean < 0:
        dirMean += 360
        pass
    
    d = dict(velMax=velMax,
             velMin=velMin,
             velMean=velMean,
             velStd=velStd,
             dirMean=dirMean,           
            )
    
    return d 
    pass
#%%
    
def filter_ascii(x):
    #se for tipo lista, faz um list.pop() retirando os dados nao ascii e retorna a lista
    if type(x) == list:
        from copy import deepcopy
        x = deepcopy(x)
        lpop = []
        for ix,aux in enumerate(x):
            if all(ord(c) < 128 for c in aux):
                pass
            else:
                lpop.append(ix)
                pass
            pass
        lpop.reverse()
        for aux in lpop:
            x.pop(aux)
            pass
        return x
        pass
    
    #se for tipo string, retorna True caso seja ASCII e False caso contrario
    elif type(x) == str:
        for c in x:
            if ord(c) < 128:
                pass
            else:
                return False
            pass
        return True

    else:
        raise ValueError('essa funcao nao suporta %s '%str(type(x)))
    
    
#x = []
#type(x) == list
#
#x = 'string'
#type(x) == str
        

    
#%%
    

#def finderAnti(path,what):
#    
#    dirr= []
#    filee = []
#    found = []
#    try:
#        for aux in os.listdir(path):
#            if os.path.isdir(path+aux+'/'):
#                dirr.append(path+aux+'/')
#                fileTemp,dirTemp,foundTemp = finder(path+aux+'/',what)
#                filee = filee + fileTemp
#                dirr = dirr + dirTemp 
#                found = found + foundTemp
#                if (path+aux).find(what) >= 0:
#                    print ('pasta: ' + aux)
#                    found.append(path+aux)
#                    pass
#                pass
#            elif os.path.isfile(path+aux):
#                filee.append(path+aux)
#                if (path+aux).find(what) >= 0:
#                    datec = os.path.getctime(path+aux)
#                    datec = datetime.fromtimestamp(datec)
#                    datem = os.path.getmtime(path+aux)
#                    datem = datetime.fromtimestamp(datem)
#                    found.append([path+aux,datec,datem])
#                    print ('arquivo: ' + path + aux)
#
#                    pass
#                pass
#            else:
#                pass
#            pass
#        found.sort(key = lambda temp: temp[2], reverse = True)
#        
#    except:
#        print('acesso negado: ' + aux)
#        pass
#    
#        
#    return(filee,dirr,found)   
#
#
#def finderEx(what,where):
#    matches = []
#    for root, dirnames, filenames in os.walk(where):
#        for filename in fnmatch.filter(filenames, what):
#            matches.append(os.path.join(root, filename))
#    return matches



#%%

def finder(**kwargs):
    import os
    from fnmatch import fnmatch
    import re
    
    print('lookup in: ',kwargs['where'])
    print('look for: ' ,kwargs['what'])
    if kwargs.has_key('inside'):
        print('look inside files enable')
        r = re.compile(kwargs['what'])
        pass
    if kwargs.has_key('index'):
        print('make index_fider enable')
        pass
    
    d = [] #contem os caminhos dos arquivo match com kwargs['what']
    din = [] #contem os caminhos dos arquivo match com dados internos
    index = [] #contem todos os arquivos encontrados. 
    
    for root,dirr,files in os.walk(kwargs['where']):
        for aux in files:
            #Se tiver a key index, grava o indice de todos os arquivos pesquisados
            if kwargs.has_key('index'):
                index.append(os.path.join(root,aux))
                pass
            
            #Se tiver a key inside, procura dentro dos arquivos abertos por um match
            if kwargs.has_key('inside'):
                try:
                    with open(os.path.join(root,aux),'r') as f:
                        data = f.read()
                        f.close()
                        pass
                    if r.search(data) is not None:
                        din.append(os.path.join(root,aux))
                    pass    
                except Exception as e:
                    print (e, 'acesso negado em: ', os.path.join(root,aux) )
                    pass
                
            #Se encontrar o what no caminho do arquivo, grava o caminho na lista d
            if fnmatch(aux,kwargs['what']):
                print (os.path.join(root,aux))
                d.append(os.path.join(root,aux))
                pass
            pass
        pass
    
    #grava os caminhos achados no arquivo index.txt
    if kwargs.has_key('index'):
        with open(os.path.join(kwargs['where'],'index_fider.txt'),'w') as f:
            print('gravando arquivo em :' ,os.path.join(kwargs['where'],'index_fider.txt') )
            for aux in index:
                f.write(aux + '\n')
                pass
            f.close()
            pass
        pass
    return d,din
    
#    import shutil as sh
#    for aux in d:
#        sh.move(aux,'c:/Google Drive/ZZZ/' + os.path.basename(aux))
#        pass

#d = finder(where=r"c:\Google Drive",what='')
#d,din = finder(where=r'C:\Google Drive\AMBIDADOS-Pasta online compartilhada\Dados Processados\Boia4_e_Boia10_historico',what='2016,10',index='',inside='')


#%%

if __name__ == '__main__':
    
#    try: 
#        print(sys.argv)
##        finder(where=sys.argv[1],what=sys.argv[2],index=sys.argv[3])
#        print('finder finalizado')
##        sys.exit(2)
#        pass
#    except Exception as e:
#        print(e)
#        print('nothing to search')
#        pass
    
#%%    
#    tem0 = finderEx('*ascapaf*','c:/google drive/')
#    tem = [os.path.realpath(aux) for aux in tem0]
    
    import pandas as pd
    from random import random
    import time
    import numpy as np
    
    t = time.clock()
    np.random.rand()
    print(time.clock() - t)
    t = time.clock()
    random()
    print(time.clock() - t)
#%%
    d = [aux for aux in xrange(1000)]
    d[8] = '////'
    d[80] = '////'
    
    dic = dict(a = [np.random.rand() for aux in range(1000)],\
                b = [np.random.rand() for aux in range(1000)],\
                c = [np.random.rand() for aux in range(1000)],\
                d = d)

    
    df0 = pd.DataFrame(dic)

#%%    
    
    df1 = df0.loc[lambda x: x.loc[:,'b'] > 0.9]
    df1 = df0[lambda x: x.loc[:,'b'] > 0.9]
    
    dl1 = [aux for aux in df0.loc[:,'b'] if aux > 0.9]

#%%

    df2 = df0.loc[lambda x: x.loc[:,'d'] != '////']
    
    t = time.clock()
    df2 = df0[lambda x: x.loc[:,'d'] != '////']
    print(time.clock() - t)

    t = time.clock()    
    dl2 = [aux for ix,aux in enumerate(df0.loc[:,'d']) if aux != '////']
    print(time.clock() - t)

    list(df2['d'].values)

#%%
    
    df3 = df0.drop(df0[lambda x: x.loc[:,'d'] != '////'].index)

    dl3 = [df0[lambda x: x.loc[:,'d'] != '////'].index]
    
    list(df2.columns.values)
    
    
#%%    
    a = lambda x: x[x.iloc[:,3] != '////'].index
    a(df0)


# =============================================================================
#%% Selecionado e substituindo valores em tabelas
# =============================================================================
    import pandas as pd
    import numpy as np

    l1 = []
    l2 = []
    a = 0
    for aux in range(5):
        l1.append(range(a,a+5,1))
        a +=1 
        pass
    
    b = 0
    for aux in range(4):
        l2.append(range(b,b-5,-1))
        b -= 1
        
    
    df1 = pd.DataFrame(l1) #cria df1
    df2 = pd.DataFrame(l2) #cria df2
    
    
    df3 = df1[np.logical_and(df1 >= 0, df1 <= 3)] #cria um df3 copiando somente os valores >= 1 e <=3 de df1
    df3[np.logical_or(df3 < 2 , df3 > 2)] = df2 #substitui os valores diferentes de 2 em df3 pelos valores de df2
    df3[pd.isnull(df3)] = df1 # seleciona todos os dados nan de df3 e preenche com dados de df1
    
# =============================================================================
# %% Comparando tabelas de tamanhos diferentes.
# =============================================================================
    #Substituindo dados de uma tabela em outra através de comparação no indice
    import pandas as pd
    import numpy as np
    import time
    
    l1 = []
    l2 = []
    a = 0
    for aux in range(96):
#    for aux in range(int(1e6)):
        l1.append(range(a,a+5,1))
        a +=1 
        pass
    
    a = 0
    for aux in range(10):
#    for aux in range(int(40e3)):
        l2.append(range(a,a+5,1))
        a += -1
    
    
    left = pd.DataFrame(l1)
    right = pd.DataFrame(l2)
    
    
    

    left.index = pd.date_range(pd.to_datetime('2000 01 01'),freq='h',periods=96)
    left.loc[:,'Data'] = left.index
    left.columns = ['a','b','c','d','e','Data']
    
    right.index = pd.date_range(pd.to_datetime('2000 01 01'),freq='D',periods=10)
    right.loc[:,'Data'] = right.index
    right.columns = ['a','b','c','d','f','Data']
    
#%%    
       
    df3 = left
    df3[[df3.index[ix] in right.index for ix,aux in enumerate(df3.index)]] = right
       
    
#%%    
#    print(time.clock() - t0)
    
    t0 = time.clock()    
    #O segredo do merge é ter uma coluna como key, iguais nos dois dataframes. Nesse caso estou usando o indice. 
    
    
    # left_index=True Combina,mantem e usa o indice como key. As colulas on=[a,b,c e Data] são mantidas de left.
    df_outer = pd.merge(left,right,how='outer',indicator=True,left_index=True,right_index=True)

    df_inner = pd.merge(left,right,how='inner',indicator=True,left_index=True,right_index=True,on=['a','b','c','Data'])

    df_right = pd.merge(left,right,how='right',indicator=True,left_index=True,right_index=True,on=['a','b','c','Data'])
    
    df_left = pd.merge(left,right,how='left',indicator=True,left_index=True,right_index=True,on=['a','b','c','Data'])
    
    
    #Sem o indice como key, utiliza apenas linhas iguais para combinar. Quase uma soma entre uma e outra.
    df_outer_no_key = pd.merge(left,right,how='outer',indicator=True,on=['a','b','c'])

    df_inner_no_key = pd.merge(left,right,how='inner',indicator=True,on=['a','b','c'])

    df_right_no_key = pd.merge(left,right,how='right',indicator=True,on=['a','b','c'])
    
    df_left_no_key = pd.merge(left,right,how='left',indicator=True,on=['a','b','c'])
    
    #Com uma coluna como key, as celulas sao mescladas, porem o indice é descartado.
    df_outer_with_key = pd.merge(left,right,how='outer',indicator=True,on=['Data'])

    df_inner_with_key = pd.merge(left,right,how='inner',indicator=True,on=['Data'])

    df_right_with_key = pd.merge(left,right,how='right',indicator=True,on=['Data'])
    
    df_left_with_key = pd.merge(left,right,how='left',indicator=True,on='Data')
    
    #Combina e substitui os valores de left em right
    df_combine = right.combine_first(left)
    
    print(time.clock() - t0)
   
    
    #%%Combinando duas series
    
    s1 = left.iloc[:,0]
    s2 = right.iloc[:,0]
#    pd.merge(s1,s2,how='outer') #err0
#    s1.combine(s2)    
#    pd.isnull(s1)
    
    df_s1 = pd.DataFrame(s1)
    df_s2 = pd.DataFrame(s2)
    df3 = pd.merge(df_s1,df_s2,how='outer')

# =============================================================================
# %% Trabalhando com multindex do pandas
# =============================================================================
    
    import pandas as pd
    import numpy as np
    
    index = [[str(aux) for aux in range(10)],[str(aux) for aux in range(-89,91,1)]]
    mindex = pd.MultiIndex.from_product(index,names=['prof','lat'])
    columns = [str(aux) for aux in range(-179,181,1)]
    
    df = pd.DataFrame(index = mindex,columns = columns)
    df[:] = np.random.randn(1800,360)
    
    df.columns.name = 'lon'
    
    df.xs('0',level='lat')['0'] #todos as profundidades da lat = 0 e lon = 0
    df.xs('5',level='prof')#todas as lat e lon da profundidade 5
    df1 = df.xs(slice('0','1'),level = 'prof')


#%% Criando uma tabela com 3 indices.
    datarange = pd.date_range(pd.datetime(2016,12,01),pd.datetime(2016,12,31),freq='3h')
    latrange = np.arange(77.5,-77.5 - 0.5,-0.5).astype(str)
    lonrange = np.arange(-179.5,180 + 0.5,0.5).astype(str)
    
    #index = [[str(aux) for aux in range(10)],[str(aux) for aux in range(-75,91,1)],[]]
    index = [datarange,latrange,['hs','tp','dp']]
    mindex = pd.MultiIndex.from_product(index,names=['Data','Lat','param'])
    
    df = pd.DataFrame(index = mindex,columns = lonrange)
    
    df[:] = np.random.randn(224853,720).astype(np.float16)


# =============================================================================
# %% HDF experimental Store object objeto 
# =============================================================================
    import pandas as pd
    import numpy as np
    import time    
    
    df = pd.DataFrame(np.random.randn(int(1e5),3),columns=['int','float','ascii'])
    df['int'] = range(len((df['int'])))
    df['ascii'] = 'bac'
    df.index.name = 'Data'
    df.index = pd.date_range(pd.datetime.today(),freq = 'h', periods = len(df))
        
    #%%
    
    t0 = time.clock()
    df.to_hdf('df_blosc.hdf','df',mode = 'w', complevel = 0,compression = 'blosc')#1.09s 34.242Mb
    print(time.clock() - t0)
    
    t0 = time.clock()
    df.to_hdf('df_bzip2.hdf','df',mode = 'w')#1.05s #34.242Mb
    print(time.clock() - t0)
    
    t0 = time.clock()
    df.to_pickle('df_pickle.pkl')#1.25s  #33.206Mb
    print(time.clock() - t0) 
    
    t0 = time.clock()
    df.to_pickle('df_pickle_infer.bz2') #5.57s #13.780Mb
    print(time.clock() - t0) 
    
    t0 = time.clock()
    df.to_pickle('df_pickle.gzip',compression='gzip') #22.5s 15.704Mb
    print(time.clock() - t0) 
    
    t0 = time.clock()
    df.to_pickle('df_pickle.bz2',compression='bz2')  #5.7s 13.780Mb
    print(time.clock() - t0)

#    t0 = time.clock()    
#    sa = pd.HDFStore('store_blosc_append.h5',complevel = 9,complib = 'blosc',mode = 'a', format = 'table',append = True)
#    sa['df'] = df
#    sa.close()
#    print(time.clock() - t0) #1.18s 13.780Mb
    
    t0 = time.clock()    
    sw = pd.HDFStore('store_blosc_write.h5',complevel = 9,complib = 'blosc',mode = 'w', format = 'table',append = True)
    sw['df'] = df
    sw.close()
    print(time.clock() - t0)
    
    t0 = time.clock()    
    sw = pd.HDFStore('store_blosc_write0.h5',complevel = 0,complib = 'blosc',mode = 'w', format = 'table',append = True)
    sw['df'] = df
    sw.close()
    print(time.clock() - t0)

    temp = pd.read_hdf('store_blosc_write.h5')    
    temp.to_hdf('temp_hdf.h5','tables',complevel=9,compression = 'blasc',mode = 'w')
    
    #%% Usando o format fixed = default (Não é appendable)
    storew = pd.HDFStore('store_blosc_write.h5',complevel = 9,complib = 'blosc',mode = 'w') #Usar somente para criar o H5, se abrir com o modo w, ira apagar tudo.
    storew['df'] = df

#    temp = storew.df.iloc[:,[1,2]]
#    storew.df.iloc[0,0] = 1000
#    storew.df.iloc[0,0]
    
    t0 = time.clock()
    storew.close()
    print(time.clock() - t0)
    
#    store = pd.HDFStore('store_zlib.h5',complevel = 9,complib = 'zlib',mode = 'w')
#    store['df'] = df
#    t0 = time.clock()
#    store.close()
#    print(time.clock() - t0)
#    
#    store = pd.HDFStore('store_bzip2.h5',complevel = 9,complib = 'bzip2',mode = 'w')
#    store['df'] = df
#    t0 = time.clock()
#    store.close()
#    print(time.clock() - t0)
    
    #%% Usando o format fixed = default (Não é appendable)
    storea = pd.HDFStore('store_blosc_append.h5',complevel = 9,complib = 'blosc',mode = 'a', format = 'table',append = True)
    storea['df'] = df
    storea['df'] = pd.DataFrame(np.random.randn(4,4))
    
#    temp = store.df.iloc[:,[1,2]]
#    storea.df.iloc[5,0] = 1000 #nao pode
#    storea.df.iloc[1,0]
    
    t0 = time.clock()
    storea.close()
    print(time.clock() - t0)


    
    
#    store = pd.HDFStore('store_zlib.h5',complevel = 9,complib = 'zlib',mode = 'a',format = 'table')
#    store['df'] = df
#    t0 = time.clock()
#    store.close()
#    print(time.clock() - t0)
#    
#    store = pd.HDFStore('store_bzip2.h5',complevel = 9,complib = 'bzip2',mode = 'a',format = 'table')
#    store['df'] = df
#    t0 = time.clock()
#    store.close()
#    print(time.clock() - t0)
#    
    
    
#%%


    
   #%%
#    %timeit(df.to_csv('store_csv_gzip.csv',compression='gzip'))
#    %timeit(df.to_csv('store_csv_bz2.csv',compression='bz2'))
#    %timeit(df.to_csv('store_csv_nada.csv'))

    
# =============================================================================
#%% Decorators
# =============================================================================
    
    def echo_funcname(func):
        
        def finterna(*args, **kwargs):
            print "Chamando funcao: %s()"  % (func.__name__) #aqui eu executo uma funcao antes de executar a funcao que chamei

            a = args[0] + 1 # aqui eu posso modificar o argumento de entrada, no caso estou somando + 1
            return func(a, **kwargs) #poderia também retornar todos os args return func(*args, **kwargs) 
        
#        print('aqui') #O que estiver nessa area, serah execuando quando @wrapear a funcao. Não deve ter nada aqui.
        return finterna
 
   
    #criando as funcoes wraped
    @echo_funcname
    def dobro(x):
        x = x - 1 #vai retornar o dobro porque estou somando 1 na função wrapper
        return x*2
    
    @echo_funcname
    def soma(x):
        return x
    
    # executando as funções
    print(dobro(10))
    print(soma(1))
#%%
    def paragrapher(func):
        def finterna(*args): #o argumento da função func entra nessa funcao como argumento.
            return '<p>{}</p>'.format(args[0])
            
        return finterna

    @paragrapher
    def comando(x):
        print(x)
    
    comando('sudo su')
    
#%%    
    import time
        

# =============================================================================
#%% Generators
# =============================================================================
    print('''Ao criar um loop de linha com [] cria-se uma lista. Se usar () no 
          lugar de [], sera criado uma função generetor''')
        
    t0 = time.clock()
    generetor = (aux for aux in xrange(1000000))
   
    
#    t0 = time.clock()
    for aux in generetor:
#        print aux
        pass
    print(time.clock() - t0)
    
#%%
    def gen():
        x = [1,2,3,4,5,6,7,8,9]
        for aux in x:
            yield aux
            
    print(type(gen()))
    print('''A função criada com yield não retorna um valor. Ela retorna um generator
          Para usa-la, é necessario iterar sobre ela com um loop for ou while''')
        
    for aux in gen():
        a = aux
#%%
    def gen2(aux):
        x = [1,2,3,4,5,6,7,8,9,aux]
        for aux in x:
            yield aux
            pass
        pass
            
    for aux in gen2(0):
        print aux
        
#%%
    print('''Depois de criado, o generator x só pode ser utilizado uma vez.
          Depois de utilizado até a sua exaustão, pode ser descartado
          Eh possível ver no loop que ''')
    x = gen2(0)        
    
#%%

    for aux in x:
        print(aux)
        pass
    
    for aux in x:
        print(aux)
        pass
    
# =============================================================================
# %% Multi Threading
# =============================================================================
import threading
import time
class mt (threading.Thread):
    def __init__(self,x):
        threading.Thread.__init__(self) #necessario ter para fazer o .start()
        self.texto = x #todas as variaveis internas da Thread precisam ser self.var
        self.msm = ''
        pass
    def run(self):
        print(self.texto)
        self.msm = 'completado'
        pass
    
obj = mt('aqui\n') 
obj.start() 
print(obj.isAlive())
print(obj.msm) #para acessar alguma variavel calculada pela Thread

# =============================================================================
#%% Criando direcoes
# =============================================================================
CtrlDirNum = 8

direcoes = []
for aux in range(16):
    direcoes.append(aux * 22.5)
    pass
            
direcoesnomes = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
                 'S','SSO','SO','OSO','O','ONO','NO','NNO']
direcoes = dict(zip(direcoes,direcoesnomes))

dirI = []
dirM = []
dirF = []
for aux2 in range(CtrlDirNum):
    di = aux2 * 360/CtrlDirNum - 360/(CtrlDirNum*2) #determinando a direcao inicial
    if di < 0:
        di = di + 360
        pass
    df = aux2 * 360/CtrlDirNum + 360/CtrlDirNum - 360/(CtrlDirNum*2) #determinando a direcao final
    if df > 360:
            df = df - 360
            pass
    dm = aux2 * 360/CtrlDirNum
    if di == df:
        di = 0 
        df = 359.99
        
    dirI.append(di)    
    dirF.append(df)        
    dirM.append(dm)    
    pass    


#%%Separando um df por direcoes

data = range(0,359,1)
df = pd.DataFrame(data,columns = ['dp'])

dfl = []
if CtrlDirNum > 1:
    for aux in range(CtrlDirNum):
        print aux
        if aux == 0:
            dfl.append(df.loc[np.logical_or(dirI[aux] <= df.loc[:,'dp'],df.loc[:,'dp'] < dirF[aux])])
            pass
        else:
            dfl.append(df.loc[np.logical_and(dirI[aux] <= df.loc[:,'dp'],df.loc[:,'dp'] < dirF[aux])])
            pass
        pass
else:
    dfl.append(df)
    pass

    
    
    
from scipy.special import gamma
from scipy.optimize import fsolve
from scipy.integrate import quad
import numpy as np


class ln():
   
    def __doc__(s):
        print(''' Must import these libraries
        from scipy.integrate import quad
        import numpy as np              
        ''')
    
    def __init__ (s):
        pass
    
    def fit(s,X):
        s.xi = s.xiLn(X)
        s.lamb = s.lambLn(X)
        return s.xi,s.lamb
    
    def xiLn(s,X):
        return np.sqrt(np.log(1 + (X.std() /  X.mean())**2)) # esse é o calculo do parametro xi
            
    def lambLn(s,X):
        return np.log(X.mean()) - 0.5*s.xi**2 #esse é o calculo do parametro lambda
            
    def pdf(s,x): #funcao lognormal distribuição
        return (1/(np.sqrt(2*np.pi)*x*s.xi))*np.exp(-0.5*(((np.log(x)-s.lamb)**2)/(s.xi**2)))
         
    def cdf(s,x):
        return quad(lambda x: s.pdf(x),0,x)[0]
    pass


class wei():
    
#    from scipy.stats import norm,weibull_min
#    from scipy.special import gamma
#    from scipy.optimize import fsolve
#    import numpy as np
#    from scipy.optimize import root
    
    def __doc__(s):
        print(''' Must import these libraries
        from scipy.special import gamma
        from scipy.optimize import fsolve
        from scipy.integrate import quad,nquad
        import numpy as np              
        ''')
        
    def __init__ (s):

        pass
    
    def fit(s,X):
        s.lambW = s.lambWei(X)
        s.alphaW = s.alphaWei(X)
        return s.alphaW,s.lambW
   
    def lambWei(s,X):
        cofVar = np.nanstd(X)/np.nanmean(X) 
        lambW = fsolve(lambda y: (np.sqrt(gamma((2/y) + 1) - gamma((1/y) + 1)**2) / gamma((1/y)+1)) - cofVar ,3)
        return lambW
    
    def alphaWei(s,X):
        
        cofVar = np.nanstd(X)/np.nanmean(X) 
        lambW = fsolve(lambda y: (np.sqrt(gamma((2/y) + 1) - gamma((1/y) + 1)**2) / gamma((1/y)+1)) - cofVar ,3)
        return np.nanmean(X)/gamma(1/lambW + 1)

    def pdf(s,x):
        return ((x**(s.lambW-1)) / (s.alphaW**s.lambW)) * s.lambW * np.exp(-(x/s.alphaW)**s.lambW)

    def cdf(s,x):
        return quad(lambda x: s.pdf(x),0,x)[0]

        