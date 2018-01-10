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
    

def finderAnti(path,what):
    
    dirr= []
    filee = []
    found = []
    try:
        for aux in os.listdir(path):
            if os.path.isdir(path+aux+'/'):
                dirr.append(path+aux+'/')
                fileTemp,dirTemp,foundTemp = finder(path+aux+'/',what)
                filee = filee + fileTemp
                dirr = dirr + dirTemp 
                found = found + foundTemp
                if (path+aux).find(what) >= 0:
                    print ('pasta: ' + aux)
                    found.append(path+aux)
                    pass
                pass
            elif os.path.isfile(path+aux):
                filee.append(path+aux)
                if (path+aux).find(what) >= 0:
                    datec = os.path.getctime(path+aux)
                    datec = datetime.fromtimestamp(datec)
                    datem = os.path.getmtime(path+aux)
                    datem = datetime.fromtimestamp(datem)
                    found.append([path+aux,datec,datem])
                    print ('arquivo: ' + path + aux)

                    pass
                pass
            else:
                pass
            pass
        found.sort(key = lambda temp: temp[2], reverse = True)
        
    except:
        print('acesso negado: ' + aux)
        pass
    
        
    return(filee,dirr,found)   


def finderEx(what,where):
    matches = []
    for root, dirnames, filenames in os.walk(where):
        for filename in fnmatch.filter(filenames, what):
            matches.append(os.path.join(root, filename))
    return matches



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
    
    try: 
        print(sys.argv)
        finder(where=sys.argv[1],what=sys.argv[2],index=sys.argv[3])
        print('finder finalizado')
        sys.exit(2)
        pass
    except Exception as e:
        print(e)
        print('nothing to search')
        pass
    
#%%    
    tem0 = finderEx('*ascapaf*','c:/google drive/')
    tem = [os.path.realpath(aux) for aux in tem0]
    
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
    s1 = pd.DataFrame(s1)
    s2 = pd.DataFrame(s2)
    pd.merge(s1,s2,how='outer')
#    s1.combine(s2)    
#    pd.isnull(s1)
    
    df_s1 = pd.DataFrame(s1)
    df_s2 = pd.DataFrame(s2)
    df3 = pd.merge(df_s1,df_s2,how='outer')


# =============================================================================
# %% store object objeto
# =============================================================================
    df = pd.DataFrame(np.random.randn(int(1e6),3),columns=['int','float','ascii'])
    df['int'] = range(len((df['int'])))
    df['ascii'] = 'bac'
    df.index.name = 'Data'
    df.index = pd.date_range(pd.datetime.today(),freq = 'h', periods = len(df))
        
    #%%
    store = pd.HDFStore('store_blosc.h5',complevel = 9,complib = 'blosc',mode = 'w')
    store['df'] = df
    %timeit(store.close())
    
    store = pd.HDFStore('store_zlib.h5',complevel = 9,complib = 'zlib',mode = 'w')
    store['df'] = df
    %timeit(store.close())
    
    store = pd.HDFStore('store_bzip2.h5',complevel = 9,complib = 'bzip2',mode = 'w')
    store['df'] = df
    %timeit(store.close())
    
    store = pd.HDFStore('store_lzo.h5',complevel = 9,complib = 'lzo',mode = 'w')
    store['df'] = df
    %timeit(store.close())
    
    %timeit(df.to_csv('store_csv_gzip.csv',compression='gzip'))
    %timeit(df.to_csv('store_csv_bz2.csv',compression='bz2'))
    %timeit(df.to_csv('store_csv_nada.csv'))
    
# =============================================================================
# %%
# =============================================================================
    
    def echo_funcname(func):
     
        def finterna(*args, **kwargs):
            print "Chamando funcao: %s()"  % (func.__name__)
            return func(*args, **kwargs)
     
        return finterna
     
    @echo_funcname
    def dobro(x):
        return x*2
     
    
    dobro(10)
#%%
    def paragrapher(func):
        def finterna(*args): #o argumento da função func entra nessa funcao como argumento.
            return '<p>{}</p>'.format(args[0])
            
        return finterna

    @paragrapher
    def comando(x):
        print(x)
    
    print(comando('sudo su'))
    
#%%    
    import time
        

#%%    
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
    
#%%
    
    
    
    
