import warnings
import itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import datalab.storage as gcs
from google.cloud import storage
import os
warnings.filterwarnings("ignore")

def query_to_dataframe(query):
  return pd.read_gbq(query,
                     project_id='healthy-battery-340007',
                     dialect='standard')

query = """
select
    *
from
    `healthy-battery-340007.aimlproject.dfdata`
where
    time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24*15 HOUR);
"""

query1 = """
select
    *
from
    `healthy-battery-340007.aimlproject.dfdata`
where hostname='server0001';
"""


df = query_to_dataframe(query)

df['time'] = df['time'].astype('datetime64[ns]')
df['hostname1'] = df['hostname']+"_"+df['Mounted']

df_avail = pd.DataFrame(columns =['time','hostname','Mounted','avail','space_check'])
df_FS = pd.DataFrame()

for node in df['hostname1'].unique():
    check_val = df[df['hostname1'] == node]['size'].unique().mean()/10
    df_s1 = df[df['hostname1'] == node][['time','avail']]
    df_s1 = df_s1.set_index('time')
    df_s1 = df_s1.resample('1d').mean()
    if df_s1.shape[0] > 10:
        Additive = Holt(df_s1['avail'], damped_trend=True, initialization_method="estimated").fit(
        smoothing_level=0.8, smoothing_trend=0.2)
        Additive_cast = Additive.forecast(5)
        for i in range(len(Additive_cast)):
            if Additive_cast.values[i] <= check_val:
                space_check1 = "yes"
            else:
                space_check1 = "No"
            list = [Additive_cast.index[i],node.split('_')[0],node.split('_')[1],Additive_cast.values[i],space_check1]
            df_avail.loc[len(df_avail)] = list


df_avail['avail'] = df_avail['avail'].apply(np.round)
df_avail['avail'] = np.where(df_avail['avail'] < 0, 0, df_avail['avail'])

for host in df_avail[df_avail['space_check'] == 'yes']['hostname'].unique():
    df_s2 = df[df['hostname'] == host ][['time','hostname','avail','Mounted']]
    df_s3 = df_avail[df_avail['hostname'] == host ][['time','hostname','avail','Mounted']]
    df_FS1 = pd.concat([df_s2,df_s3],ignore_index=True, sort=False)
    df_FS = df_FS.append(df_FS1, ignore_index=True)



gcs.Bucket('healthy-battery-340007-aiml').item('df_data/df_forecast.csv').write_to(df_FS.to_csv(),'text/csv')
