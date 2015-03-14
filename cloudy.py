
# coding: utf-8

# In[1]:

cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }


https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE,TIME


# In[2]:

import requests
import sqlite3 as lite
import datetime

api_key = "a1d9d1bb210da8a54ee0b0580e917c92"
url = 'https://api.forecast.io/forecast/' + api_key

cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }


# In[3]:

end_date = datetime.datetime.now()


# In[4]:

con = lite.connect('weather.db')
cur = con.cursor()


# In[5]:

cities.keys()
with con:
    cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, Atlanta REAL, Austin REAL, Boston REAL, Chicago REAL, Cleveland REAL);')


# In[6]:

query_date = end_date - datetime.timedelta(days=30)

with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)


# In[12]:

for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        print url +'/'+ v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00')
        r = requests.get(url +'/'+ v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
       

        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))

        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day


con.close() 


# In[13]:

import pandas as pd
import sqlite3 as lite

con = lite.connect('weather.db')
cur = con.cursor()


# In[18]:

df = pd.read_sql_query("SELECT * FROM daily_temp ORDER BY day_of_reading",con,index_col='day_of_reading')


# In[27]:

df.mean()


# In[28]:

df.max()


# In[29]:

df.min()


# In[30]:

df.var()


# In[31]:

df.max()-df.min()


# In[32]:

df.plot()


# In[33]:

df['Atlanta'].plot(0)


# In[34]:

from pandas.tools.plotting import autocorrelation_plot


# In[35]:

plt.figure()


# In[38]:

autocorrelation_plot(df['Atlanta'])


# In[39]:

autocorrelation_plot(df['Austin'])


# In[40]:

autocorrelation_plot(df['Boston'])


# In[41]:

autocorrelation_plot(df['Chicago'])


# In[42]:

autocorrelation_plot(df['Cleveland'])


# In[ ]:



