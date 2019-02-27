#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 16:39:51 2019

@author: Christian
"""


import csv
from urllib.request import urlretrieve

import matplotlib.pyplot as plt, mpld3
from datetime import datetime
import xlrd
import numpy as np
import pandas as pd
import random
import plotly.graph_objs as go
from scipy.interpolate import interp1d
import seaborn as sns; sns.set()
from matplotlib.widgets import CheckButtons


#%% Data gathering and cleaning

price_data = []
for x in range(2016, 2019):
    url = 'https://www.nordpoolgroup.com/globalassets/marketdata-excel-files/elspot-prices_'+str(x)+'_hourly_dkk.xls'
    urlretrieve(url,'elspot-prices_'+str(x)+'_hourly_dkk.xls')
    filename='elspot-prices_'+str(x)+'_hourly_dkk.XLS'
    data= pd.read_html(filename)
    data=pd.DataFrame(data[0])
    data=data.iloc[:,[0,1,8,9]]
    data.columns=['date','time', 'DK_vest_pris', 'DK_øst_pris']
    price_data.append(data)

price_data = pd.concat(price_data, axis=0)

forecast_data = []
for x in range(2016, 2019):
    url = 'https://www.nordpoolgroup.com/globalassets/marketdata-excel-files/wind-power-dk-prognosis_'+str(x)+'_hourly.xls'
    urlretrieve(url,'wind-power-dk-prognosis_'+str(x)+'_hourly.xls')
    filename='wind-power-dk-prognosis_'+str(x)+'_hourly.xls'
    data= pd.read_html(filename)
    data=pd.DataFrame(data[0])
    data.columns=['date','time', 'DK_vest_forecast', 'DK_øst_forecast']
    forecast_data.append(data)

forecast_data = pd.concat(forecast_data, axis=0)

production_data = []
for x in range(2016, 2019):
    url = 'https://www.nordpoolgroup.com/globalassets/marketdata-excel-files/wind-power-dk_'+str(x)+'_hourly.xls'
    urlretrieve(url,'wind-power-dk_'+str(x)+'_hourly.xls')
    filename='wind-power-dk_'+str(x)+'_hourly.xls'
    data= pd.read_html(filename)
    data=pd.DataFrame(data[0])
    data.columns=['date','time', 'DK_vest_production', 'DK_øst_production']
    production_data.append(data)

production_data = pd.concat(production_data, axis=0)


data=pd.merge(price_data, forecast_data, on=['date','time'])
data=pd.merge(data, production_data, on=['date','time'])

data['date']=pd.to_date(data['date'])
data['date'] = data['date'].dt.date
data['month'] = pd.DatetimeIndex(data['date']).month
data['day'] = pd.DatetimeIndex(data['date']).day
data['year'] = pd.DatetimeIndex(data['date']).year
data['weekday'] = pd.DatetimeIndex(data['date']).weekday
data['hour']=data['time'].str.slice(0, 2)
data.hour = data.hour.astype(int)
data['forecasting_error_øst']=data['DK_øst_forecast'] - data['DK_øst_production']
data['forecasting_error_vest']=data['DK_vest_forecast']-data['DK_vest_production']


#%% Data description
#Overall development in prices, daily
fig, ax = plt.subplots(figsize=(12,7))
data.groupby(['date']).mean()[['DK_vest_pris']].plot(ax=ax)
plt.xlabel('Date')
plt.ylabel('Price (kr./MWh)')
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)
fig.tight_layout()
plt.show()

#Overall development in wind power production, monthly
fig, ax = plt.subplots(figsize=(12,7))
data.groupby(['year','month']).mean()[['DK_vest_production']].plot(ax=ax)
plt.xlabel('Date')
plt.ylabel('MWh)')
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)
fig.tight_layout()
plt.show()

d
#Over 24 hours
data[['DK_vest_pris','DK_øst_pris']].plot(figsize=(20,10), linewidth=5, fontsize=20)
plt.xlabel('Year', fontsize=20);

fig, ax = plt.subplots(figsize=(7,7))
data.groupby(['hour','weekday']).mean()['DK_vest_pris'].unstack().plot(ax=ax)
plt.legend(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
plt.xlabel('Time of the day')
plt.ylabel('Price (kr./MWh)')
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)
fig.tight_layout()
plt.show()








#%%

fig, ax = plt.subplots(figsize=(7,7))
data.groupby(['hour','weekday']).mean()['DK_vest_pris'].unstack().plot(ax=ax)
lines = ax.get_lines()
plt.legend(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
rax = plt.axes([0.05, 0.4, 0.1, 0.15])
labels = [str(label.get_text()) for label in ax.get_legend().get_texts()]
visibility = [line.get_visible() for line in lines]



plt.xlabel('Time of the day')
plt.ylabel('Price (kr./MWh)')

check = CheckButtons(rax, labels, visibility)
def func(label):
    lines[labels.index(label)].set_visible(not lines[labels.index(label)].get_visible())
    plt.draw()

check.on_clicked(func)

plt.show()
mpld3.save_html(fig)




