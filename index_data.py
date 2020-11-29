import pandas as pd
import numpy as np
import datetime

vix_raw = pd.read_csv('VIX.csv')
sp_raw = pd.read_csv('GSPC.csv')

#: functions to separate dates
def getYear(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d').year
def getMonth(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d').month
def getDay(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d').day

#: raw data
vix = vix_raw.get(['Date', 'Close'])
sp = sp_raw.get(['Date', 'Close'])

#: dates split up as new columns
vix_with_date = (
    vix
    .assign(Year= vix.get('Date').apply(getYear))
    .assign(Month= vix.get('Date').apply(getMonth))
    .assign(Day= vix.get('Date').apply(getDay))
)
sp_with_date = (
    sp
    .assign(Year= vix.get('Date').apply(getYear))
    .assign(Month= vix.get('Date').apply(getMonth))
    .assign(Day= vix.get('Date').apply(getDay))
)

#: data for dates interested in
relevant_vix = (
    vix_with_date[(vix_with_date.get('Year') >= 2020)
                  & (vix_with_date.get('Month') >= 3)
                  & (vix_with_date.get('Month') <= 10)
                  & (vix_with_date.get('Day') <= 27)]
)
relevant_sp = (
    sp_with_date[(sp_with_date.get('Year') >= 2020)
                 & (sp_with_date.get('Month') >= 3)
                 & (sp_with_date.get('Month') <= 10)
                 & (sp_with_date.get('Day') <= 27)]
)


grouped_vix = relevant_vix.groupby(['Year','Month', 'Day']).sum()
grouped_sp = relevant_sp.groupby(['Year','Month', 'Day']).sum()


#: index data merged
grouped_table = (
    grouped_sp.merge(grouped_vix, left_index = True, right_index = True)
)
merged_table = (
    grouped_table
    .assign(SP_500 = grouped_table.get('Close_x'))
    .assign(VIX = grouped_table.get('Close_y'))
    .drop(columns = ['Close_x', 'Close_y'])
)
merged_table


#: returns index data as matrix
sp_matrix = np.matrix(merged_table.get('SP_500'))
vix_matrix = np.matrix(merged_table.get('VIX'))
