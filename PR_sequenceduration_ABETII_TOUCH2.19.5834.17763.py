#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: changxu
"""

'''
This scripts help to calculate total response time for each trial 
1. Create a folder and load data files of all PR sessions. 
   Data are saved in csv files
   Other files are acceptable but you need to edit the code.
2. Input foler location.
3. Run the PR_sequenceduration.py file.

'''

import pandas as pd
import os

location = '/Users/changxu/PR_demonstration'
def get_sequenceduration(path):             
    files =os.listdir(path)     
    file_list = []
    for file in files:
        if not os.path.isdir(path + file): 
            f_name = str(file)
            if f_name[-3:] == 'csv':
                tr = '/'  
                filename = path + tr + f_name        
                file_list.append(filename) 
    
    performance_df = pd.DataFrame()
    for file_path in file_list:
        session_data_header = pd.read_csv(file_path,sep = ',', nrows = 16)
        Group = session_data_header.iloc[10,1]
        ID = session_data_header.iloc[8,1]
        Session = session_data_header.iloc[14,1][:10]
        session_data = pd.read_csv(file_path, sep = ',', header = 17)
    
        ImageTouched = session_data[(session_data['EffectText'] == 'Image Touched')]['Time'].values
        FeederPulse = session_data[(session_data['EffectText'] == 'Feeder #1')]['Time'].values      
        
        for i in range(len(FeederPulse)):
            if i == 0:
                performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,0,1+i*4]], 
                                                       columns=['Group','ID','Session','TotalResponseTime','Response requirment']),sort=True)
            else:
                SequenceDuration = ImageTouched[2*i*i+3*i]-ImageTouched[i*(2*i-1)]
                performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,SequenceDuration,1+i*4]], 
                                                             columns=['Group','ID','Session','TotalResponseTime','Response requirment']),sort=True)

    return performance_df

Duration_df = get_sequenceduration(location)
Duration_df.to_excel('sequence_duration_final.xls', index = False)

