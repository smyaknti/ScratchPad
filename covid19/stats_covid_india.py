#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import json_normalize, DataFrame
import time
import json
import statistics
from colorama import Fore, init
init(autoreset=True)

# In[2]:


url = 'https://api.covid19india.org/raw_data.json'


# In[3]:


data = pd.read_json(url)


# In[4]:


import urllib, json

response = urllib.request.urlopen(url)
data = json_normalize(json.loads(response.read())["raw_data"])
print(f'{Fore.YELLOW}Update Time: {time.ctime()}')


# In[5]:


data = DataFrame(data, columns = ['_d180g','agebracket','backupnotes','contractedfromwhichpatientsuspected','currentstatus','dateannounced','detectedcity','detecteddistrict','detectedstate','estimatedonsetdate','gender','nationality','patientnumber','statuschangedate'])
data = DataFrame(data.loc[data['detectedstate']!=''])
data.dateannounced = pd.to_datetime(data.dateannounced,dayfirst=True)
data.statuschangedate = pd.to_datetime(data.statuschangedate, dayfirst=True)
#data


# In[31]:


deceased = DataFrame(data.loc[data['currentstatus']=='Deceased'], columns = ['dateannounced','detectedcity','detectedstate','patientnumber','statuschangedate','_d180g','agebracket'])


# In[7]:


total = len(data)
hosp = len(DataFrame(data.loc[data['currentstatus']=='Hospitalized']))
deaths = len(DataFrame(data.loc[data['currentstatus']=='Deceased']))
recv = total-(hosp+deaths)
mean_recv = pd.to_numeric(DataFrame(data.loc[data['currentstatus']=='Recovered'])["agebracket"]).mean()
mean_death = pd.to_numeric(DataFrame(data.loc[data['currentstatus']=='Deceased'])["agebracket"]).mean()
stdev_calc = DataFrame(data.loc[data['agebracket']!=''])
stdev_recv = statistics.stdev(pd.to_numeric(DataFrame(stdev_calc.loc[data['currentstatus']=='Recovered']).dropna()["agebracket"]))
stdev_death = statistics.stdev(pd.to_numeric(DataFrame(stdev_calc.loc[data['currentstatus']=='Deceased']).dropna()["agebracket"]))



print(f'{Fore.CYAN}Total cases: {total}\n{hosp} in progress\nDeaths: {deaths}\nRecoveries: {recv}')
print(f'{Fore.GREEN}Recovery rate: {(recv/total)*100:.2f}%\nMean Age: {mean_recv:.2f} years\nStd. Dev.: {stdev_recv:.2f} years')
print(f'{Fore.RED}Mortality rate: {(deaths/total)*100:.2f}%\nMean age: {mean_death:.2f} years\nStd. Dev. : {stdev_death:.2f} years')


# In[30]:


recovered = DataFrame(data.loc[data['currentstatus']=='Recovered'], columns = ['dateannounced','detectedcity','detectedstate','patientnumber','statuschangedate','_d180g','agebracket'])
recovered['timetaken'] = recovered.statuschangedate - recovered.dateannounced
recovered_clean = DataFrame(recovered.loc[recovered['timetaken']>pd.Timedelta(days=1)])
stdev_recv_days = statistics.stdev(pd.to_numeric(recovered_clean["timetaken"].dt.days))
mean_recv_days = statistics.mean(pd.to_numeric(recovered_clean["timetaken"].dt.days))

print(f'{Fore.GREEN}Mean Recovery time: {mean_recv_days:.2f} days\nStd. Dev.: {stdev_recv_days:.2f} days')
print(f'{Fore.CYAN}Death to Recovery ratio: {(deaths/recv)*100:.2f}%')

# In[32]:


#temp = DataFrame(data.loc[data['currentstatus']=='Hospitalized'])
#temp
#DataFrame(temp.loc[temp['_d180g'].isnull()])


# In[ ]:





# In[33]:


# indians = len(DataFrame(data.loc[data['nationality']=='India']))
# Nationality = DataFrame(data.loc[data['nationality']!=''])
# non_indians=len(DataFrame(Nationality.loc[Nationality['nationality']!='India']))
# unknown_nationality = total - indians - non_indians

# print(f'Out of {total} people, there are {indians} Indians and {non_indians} Non Indians. And for the rest {unknown_nationality} people, their data is not there.')


# In[34]:


#len(DataFrame(data.loc[data['_d180g']=='Details awaited']))


# In[ ]:





# In[ ]:




