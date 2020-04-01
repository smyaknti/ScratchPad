#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import json_normalize, DataFrame
import json
import statistics
import urllib, json
from colorama import Fore, init
import time
init(autoreset=True)


# In[2]:


url = 'https://api.covid19india.org/raw_data.json'
url_key_data = 'https://api.covid19india.org/data.json'


# In[3]:


response = urllib.request.urlopen(url)
data = json_normalize(json.loads(response.read())["raw_data"])
response = urllib.request.urlopen(url_key_data)
key_values = DataFrame(json_normalize(json.loads(response.read())["statewise"]))
key_values = DataFrame(key_values.loc[key_values['state']=='Total'])
print(f'{Fore.YELLOW}Update Time: {time.ctime()}')


# In[4]:


key_values = key_values.to_dict()
total = int(key_values['confirmed'][0])
hosp = int(key_values['active'][0])
deaths = int(key_values['deaths'][0])
recv = int(key_values['recovered'][0])


# In[5]:


data = DataFrame(data, columns = ['_d180g','agebracket','backupnotes','contractedfromwhichpatientsuspected','currentstatus','dateannounced','detectedcity','detecteddistrict','detectedstate','estimatedonsetdate','gender','nationality','patientnumber','statuschangedate'])
data = DataFrame(data.loc[data['detectedstate']!=''])
data.dateannounced = pd.to_datetime(data.dateannounced,dayfirst=True)
data.statuschangedate = pd.to_datetime(data.statuschangedate, dayfirst=True)


# In[6]:


deceased = DataFrame(data.loc[data['currentstatus']=='Deceased'], columns = ['dateannounced','detectedcity','detectedstate','patientnumber','statuschangedate','_d180g','agebracket'])


# In[7]:


mean_recv = pd.to_numeric(DataFrame(data.loc[data['currentstatus']=='Recovered'])["agebracket"]).mean()
mean_death = pd.to_numeric(DataFrame(data.loc[data['currentstatus']=='Deceased'])["agebracket"]).mean()
stdev_calc = DataFrame(data.loc[data['agebracket']!=''], columns = ['agebracket','currentstatus'])
length_recovery = len(DataFrame(stdev_calc.loc[data['currentstatus']=='Recovered']).dropna()["agebracket"])
length_deceased = len(DataFrame(stdev_calc.loc[data['currentstatus']=='Deceased']).dropna()["agebracket"])
stdev_recv = statistics.stdev(pd.to_numeric(DataFrame(stdev_calc.loc[data['currentstatus']=='Recovered']).dropna()["agebracket"]))
stdev_death = statistics.stdev(pd.to_numeric(DataFrame(stdev_calc.loc[data['currentstatus']=='Deceased']).dropna()["agebracket"]))



print(f'{Fore.CYAN}Total cases: {total}:\n{hosp} in progress\n{Fore.RED}{deaths} Deaths\n{Fore.GREEN}{recv} Recoveries')
print(f'{Fore.GREEN}Recovery rate: {(recv/total)*100:.2f}%\n{length_recovery} people with valid data:\nMean age:{mean_recv:.2f} years\nStd. Dev.: {stdev_recv:.2f} years')
print(f'{Fore.RED}Mortality rate: {(deaths/total)*100:.2f}%\n{length_deceased} people with valid data:\nMean age: {mean_death:.2f} years\nStd. Dev.: {stdev_death:.2f} years')


# In[8]:


recovered = DataFrame(data.loc[data['currentstatus']=='Recovered'], columns = ['dateannounced','detectedcity','detectedstate','patientnumber','statuschangedate','_d180g','agebracket'])
recovered['timetaken'] = recovered.statuschangedate - recovered.dateannounced
recovered_clean = DataFrame(recovered.loc[recovered['timetaken']>pd.Timedelta(days=1)])
length_recovery = len(recovered_clean["timetaken"])
stdev_recv_days = statistics.stdev(pd.to_numeric(recovered_clean["timetaken"].dt.days))
mean_recv_days = statistics.mean(pd.to_numeric(recovered_clean["timetaken"].dt.days))

print(f'{Fore.GREEN}{length_recovery} people have valid data:\nMean Recovery Time: {mean_recv_days:.2f} days\nStd. Dev.: {stdev_recv_days:.2f} days')
print(f'{Fore.CYAN}Death to Recovery ratio: {(deaths/recv)*100:.2f}%')

# In[ ]:




