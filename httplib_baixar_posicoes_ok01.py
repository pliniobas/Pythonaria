# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:23:28 2018

@author: Plinio Bueno
"""

import httplib
conn = httplib.HTTPConnection(r'ambiporto.ddns.net')
r1 = conn.request("GET", r"http://ambiporto.ddns.net/ok01/?tipo=csv&data=240")
r1 = conn.getresponse()
dir(r1)
r1.status
d = r1.read()
d1 = d.split('\n')
d1 = [aux.split(',') for aux in d1]
del(d1[0])
import pandas as pd
df = pd.DataFrame(data=d1)
df.loc[:,29] = pd.to_numeric(df.loc[:,29],errors='coerce')
df.loc[:,30] = pd.to_numeric(df.loc[:,30],errors='coerce')

df.iloc[:,29] = df.iloc[:,29] / 60000
df.iloc[:,30] = df.iloc[:,30] / 60000

df.iloc[:,[29,30,1]].to_csv('posicoesok01_s.txt',float_format='%.8f',index=False)
