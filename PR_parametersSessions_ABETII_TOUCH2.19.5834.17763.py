#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: chang xu/beibei peng
"""
'''
This scripts help to calculate several performance parameters, including the breakpoint,blank touch rate, 
mean post-reinforcement pause, mean reward collection latency, magazineEntry_rate and IR beam break rate.
1. Create a folder and load data files of all PR sessions. 
   Data are saved in csv files
   Other files are acceptable but you need to edit the code.
2. Input foler location.
3. Run the PR_parameters.py file.
'''

import pandas as pd
import numpy as np
import os

location = '/Users/changxu/PR_demonstration'

def get_performance(path):             
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
        Trial_Timer = session_data[session_data['EffectText'] == '_Trial_Timer']['Time'].values
        if len(Trial_Timer) != 2:
            Session_len = int(input("session duration:"))
        else:
            Session_len = Trial_Timer[1]
        
        
        MagazineEntry = session_data[(session_data['EffectText'] == 'Tray #1')& 
                                     (session_data['Group'] == 10)&
                                     (session_data['EventText'] == 'Input Transition On Event')]['Time'].values
    
        MagazineEntry_all = session_data[(session_data['EffectText'] == 'Tray #1')& 
                                         (session_data['EventText'] == 'Input Transition On Event')]['Time'].values
    
        ImageTouched = session_data[(session_data['EffectText'] == 'Image Touched')]['Time'].values
        FeederPulse = session_data[(session_data['EffectText'] == 'Feeder #1')]['Time'].values      
        
        Grid1 = session_data[session_data['EffectText'] == 'GRID 1 BLANK TOUCH']['Time'].values
        Grid2 = session_data[session_data['EffectText'] == 'GRID 2 BLANK TOUCH']['Time'].values
        Grid4 = session_data[session_data['EffectText'] == 'GRID 4 BLANK TOUCH']['Time'].values
        Grid5 = session_data[session_data['EffectText'] == 'GRID 5 BLANK TOUCH']['Time'].values
        
        
        ##breakpoint: the number of target location responses emitted by an animal in the last successfully completed trial of a session. 
        Breakpoint = 1 + 4*(len(FeederPulse)-1)
        # Breakpoint =  4*(len(MagazineEntry))-3
        performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,Breakpoint,'Breakpoint']], 
                                                     columns=['Group','ID','Session','Value','Performance parameter']),sort=True)
        
        BlankTouch_No = len(Grid1) + len(Grid2) + len(Grid4) + len(Grid5)
        BlankTouch_Rate = BlankTouch_No/Session_len
        performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,BlankTouch_No,'BlankTouch_Number']], 
                                                     columns=['Group','ID','Session','Value','Performance parameter']),sort=True)
        performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,BlankTouch_Rate,'BlankTouch_Rate']], 
                                                     columns=['Group','ID','Session','Value','Performance parameter']),sort=True)
        
        ## post-reinforcement pause (PRP): the interval between exit from the magazine following reward delivery and the first target touch of the next trial
        ## on linear +4 basis (i.e. 1, 5, 9, 13 etc.) 
        PRP_list = session_data[session_data['EffectText'].isin(['Tray #1','Image Touched']) & 
                                session_data['Group'].isin([7,11])].reset_index(drop=True)
        
        Exit_magazine_index = np.array(np.where(np.diff(PRP_list['Group']) == -4)).flatten() 
        NextTrailTouch_index = Exit_magazine_index + 1
        Time_Exit = np.array(PRP_list['Time'][Exit_magazine_index])
        Time_NextTrailTouch = np.array(PRP_list['Time'][NextTrailTouch_index])
        Pause = Time_NextTrailTouch - Time_Exit
        Pause_mean = np.mean(Pause)
        performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,Pause_mean,'PRP_mean']], 
                                                     columns=['Group','ID','Session','Value','Performance parameter']),sort=True)
        
        ## reward collection latency (RCL): time between the completion of the final target touch of a trial and entry to the reward magazine for reward collection
        LatencyToReward = MagazineEntry - FeederPulse[:len(MagazineEntry)] 
        LatencyToReward_mean = np.mean(LatencyToReward)
        performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,LatencyToReward_mean,'RCL_mean']], 
                                                    columns=['Group','ID','Session','Value','Performance parameter']),sort=True)
        
        ### IR beam break rate: number of breaks/session duration
        ### BIR: rear beam = 3 cm from magazine port
        ### FIR: front beam = 6 cm from screen            
        BIR = session_data[(session_data['EffectText'] == 'BIRBeam #1') & 
                           (session_data['EventText'] == 'Input Transition On Event')].reset_index(drop=True)
        BIR_Rate = len(BIR)/Session_len
        performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,BIR_Rate,'BIR_rate']], 
                                                     columns=['Group','ID','Session','Value','Performance parameter']),sort=True)
        
        FIR = session_data[(session_data['EffectText'] == 'FIRBeam #1') &
                           (session_data['EventText'] == 'Input Transition On Event')].reset_index(drop=True)
        FIR_Rate = len(FIR)/Session_len
        performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,FIR_Rate,'FIR_rate']], 
                                                     columns=['Group','ID','Session','Value','Performance parameter']),sort=True)

        MagazineEntry_rate = len(MagazineEntry_all)/Session_len
        performance_df = performance_df.append(pd.DataFrame([[Group,ID,Session,MagazineEntry_rate,'MagazineEntry_rate']], 
                                                     columns=['Group','ID','Session','Value','Performance parameter']),sort=True)        
       
    return performance_df

performance_df = get_performance(location)
performance_df.to_excel('final_data_sessions.xls', index = False)