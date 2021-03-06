#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import json_normalize, DataFrame
import json
import statistics
import json
from colorama import Fore, init
import time
import urllib.request as url_lib
init(autoreset=True)


# In[2]:


url = 'https://api.covid19india.org/raw_data.json'
url_key_data = 'https://api.covid19india.org/data.json'


# In[3]:


response = url_lib.urlopen(url)
data = json_normalize(json.loads(response.read())["raw_data"])
response = url_lib.urlopen(url_key_data)
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



print(f'{Fore.CYAN}Total cases are {total}, out of which {hosp} are still in progress.\nThere are {deaths} deaths and {recv} recoveries.')
print(f'{Fore.GREEN}Recovery rate is {(recv/total)*100:.2f}% and for {length_recovery} people with valid data: the Mean age group is {mean_recv:.2f} years and Std. Dev. is {stdev_recv:.2f} years.')
print(f'{Fore.RED}Mortality rate is {(deaths/total)*100:.2f}% and for {length_deceased} people with valid data: the Mean age group is {mean_death:.2f} years and Std. Dev. is {stdev_death:.2f} years.')


# In[8]:


recovered = DataFrame(data.loc[data['currentstatus']=='Recovered'], columns = ['dateannounced','detectedcity','detectedstate','patientnumber','statuschangedate','_d180g','agebracket'])
recovered['timetaken'] = recovered.statuschangedate - recovered.dateannounced
recovered_clean = DataFrame(recovered.loc[recovered['timetaken']>pd.Timedelta(days=1)])
length_recovery = len(recovered_clean["timetaken"])
stdev_recv_days = statistics.stdev(pd.to_numeric(recovered_clean["timetaken"].dt.days))
mean_recv_days = statistics.mean(pd.to_numeric(recovered_clean["timetaken"].dt.days))

print(f'{Fore.GREEN}Out of the {len(recovered)} recoveries, data is known for {length_recovery} people: the Mean time of recovery is {mean_recv_days:.2f} days, and Std. Dev. is {stdev_recv_days:.2f} days')
print(f'{Fore.CYAN}Death to Recovery ratio: {(deaths/recv)*100:.2f}%')

# In[ ]:




