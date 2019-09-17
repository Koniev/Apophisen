# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 09:57:22 2019

@author: carreeg
"""
import datetime as dt
import sys
import pandas as pd

"""
Setup correct columns names
"""
colNames = ['nbKills', 'time']
date = dt.date(2019, 1, 1)

"""
Read from csv provided by RiotApi.py
"""
data = pd.read_csv(sys.path[0] + "\\dataAPIriot.txt", parse_dates=[1], names=colNames, header = None)
data['time'] = pd.to_datetime(data['time'])
"""
Index the datetime to have a correct dataset, then replace the date component (not useful for us)
"""
data.set_index('time', inplace=True)
data.index = data.index.map(lambda t: t.replace(year=2019, month=1, day=1))
"""
Group by 30minutes to have the correct dataset then plot it
"""
data = data.groupby(data.index.floor('30min')).mean().plot(kind='bar', title='mean of nbKills by time')
print(data)