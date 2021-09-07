#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: changxu
"""

import pandas as pd
import numpy as np

location = '/Users/changxu/PR_demonstration/final_data_sessions.xls'
performance_df = pd.read_excel(location)

performance_mean_df = pd.DataFrame()
for ID in np.unique(performance_df['ID'].values):
    breakpoint_sessions = performance_df[(performance_df['ID']==ID)&(performance_df['Performance parameter']=='Breakpoint')]['Value'].values
    brealpoint_mean = np.mean(breakpoint_sessions)
    group = np.unique(performance_df[performance_df['ID']==ID]['Group'].values)[0]
    performance_mean_df = performance_mean_df.append(pd.DataFrame([[group,brealpoint_mean,'Breakpoint']], 
                                                     columns=['Group','Value','Performance parameter']),sort=True)
    
    RCL_session_mean = performance_df[(performance_df['ID']==ID)&(performance_df['Performance parameter']=='RCL_mean')]['Value'].values
    RCL_all_mean = np.mean(RCL_session_mean)
    performance_mean_df = performance_mean_df.append(pd.DataFrame([[group,RCL_all_mean,'RCL']], 
                                                     columns=['Group','Value','Performance parameter']),sort=True)
    
    PRP_session_mean = performance_df[(performance_df['ID']==ID)&(performance_df['Performance parameter']=='PRP_mean')]['Value'].values
    PRP_all_mean = np.mean(PRP_session_mean)
    performance_mean_df = performance_mean_df.append(pd.DataFrame([[group,PRP_all_mean,'PRP']], 
                                                     columns=['Group','Value','Performance parameter']),sort=True)   
    
    
    FIR_session_mean = performance_df[(performance_df['ID']==ID)&(performance_df['Performance parameter']=='FIR_rate')]['Value'].values
    FIR_all_mean = np.mean(FIR_session_mean)
    performance_mean_df = performance_mean_df.append(pd.DataFrame([[group,FIR_all_mean,'FIR']], 
                                                     columns=['Group','Value','Performance parameter']),sort=True)

    BIR_session_mean = performance_df[(performance_df['ID']==ID)&(performance_df['Performance parameter']=='BIR_rate')]['Value'].values
    BIR_all_mean = np.mean(BIR_session_mean)
    performance_mean_df = performance_mean_df.append(pd.DataFrame([[group,BIR_all_mean,'BIR']], 
                                                     columns=['Group','Value','Performance parameter']),sort=True)

    magazine_session_mean = performance_df[(performance_df['ID']==ID)&(performance_df['Performance parameter']=='MagazineEntry_rate')]['Value'].values
    magazine_all_mean = np.mean(magazine_session_mean)
    performance_mean_df = performance_mean_df.append(pd.DataFrame([[group,magazine_all_mean,'MER']], 
                                                     columns=['Group','Value','Performance parameter']),sort=True)

performance_mean_df.to_excel('final_data_session_mean.xls', index = False)

