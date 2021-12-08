#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: changxu
"""
import pandas as pd
import numpy as np

location = '/Users/changxu/PR_demonstration/sequence_duration_final.xls'
sequenceduration_df = pd.read_excel(location)

SequenceDuration_mean_df = pd.DataFrame()
for ID in np.unique(sequenceduration_df['ID'].values):
    ID_data = sequenceduration_df[sequenceduration_df['ID']==ID]
    for RR in np.unique(ID_data['Response requirment'].values):
        SD_RRsessions = ID_data[(ID_data['ID']==ID)&(ID_data['Response requirment']==RR)]['TotalResponseTime'].values
        SD_RR_mean = np.mean(SD_RRsessions)
        group = np.unique(ID_data[ID_data['ID']==ID]['Group'].values)[0]
        SequenceDuration_mean_df = SequenceDuration_mean_df.append(pd.DataFrame([[group,SD_RR_mean,RR]], 
                                                                   columns=['Group','TotalResponseTime','Response requirment']),sort=True)

SequenceDuration_mean_df.to_excel('SequenceDuration_mean.xls', index = False)
