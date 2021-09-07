#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: changxu
"""
import pandas as pd
import numpy as np

location = '/Users/changxu/PR_demonstration/ResponseInterval_sessions.xls'
interval_df = pd.read_excel(location)

interval_mean_df = pd.DataFrame()
for ID in np.unique(interval_df['ID'].values):
    ID_data = interval_df[interval_df['ID']==ID]
    group = np.unique(ID_data[ID_data['ID']==ID]['Group'].values)[0]
    for RR in np.unique(ID_data['Response Requirment'].values):
        Interval_RRsessions = ID_data[(ID_data['ID']==ID)&(ID_data['Response Requirment']==RR)]['Inter Resonse Interval'].values
        Interval_RR_mean = np.mean(Interval_RRsessions)
        interval_mean_df = interval_mean_df.append(pd.DataFrame([[group,ID,Interval_RR_mean,RR]], 
                                                         columns=['Group','ID','Inter-interval','Response requirment']),sort=True)

interval_mean_df.to_excel('ResponseInterval_mean2.xls', index = False)
