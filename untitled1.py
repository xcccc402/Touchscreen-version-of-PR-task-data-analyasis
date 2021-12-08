#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 19:29:03 2021

@author: changxu
"""

import pandas as pd
import numpy as np

location = '/Users/changxu/PR_demonstration/ResponseInterval_sessions.xls'
interval_df = pd.read_excel(location)

interval_mean_df = pd.DataFrame()
ID_data = interval_df[interval_df['ID']==22]
group = np.unique(ID_data[ID_data['ID']==22]['Group'].values)[0]
for RR in np.unique(ID_data['Response Requirment'].values):
    Interval_RRsessions = ID_data[(ID_data['ID']==22)&(ID_data['Response Requirment']==RR)]['Inter Resonse Interval'].values
    print(Interval_RRsessions)
    Interval_RR_mean = np.mean(Interval_RRsessions)
    print(Interval_RR_mean)
    interval_mean_df = interval_mean_df.append(pd.DataFrame([[group,ID,Interval_RR_mean,RR]], 
                                                     columns=['Group','ID','Inter-interval','Response requirment']),sort=True)