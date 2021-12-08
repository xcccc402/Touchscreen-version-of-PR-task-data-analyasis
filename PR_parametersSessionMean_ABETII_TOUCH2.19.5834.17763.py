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
3. Run file.
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


sequenceduration_df = get_sequenceduration(location)
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

def get_reponseinterval(path):             
    files =os.listdir(path)     
    file_list = []
    for file in files:
        if not os.path.isdir(path + file): 
            f_name = str(file)
            if f_name[-3:] == 'csv':
                tr = '/'  
                filename = path + tr + f_name        
                file_list.append(filename) 
    
    ResponseInterval_df = pd.DataFrame()
    
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
                pass
            else:
                FirstPress = i*(2*i-1) 
                idx = 0
                while FirstPress + idx < (2*i*i+3*i):
                    ResonseInterval = ImageTouched[FirstPress+idx+1]-ImageTouched[FirstPress+idx]
                    ResponseInterval_df = ResponseInterval_df.append(pd.DataFrame([[Group,ID,Session,ResonseInterval,idx+1,1+i*4]], 
                                                                     columns=['Group','ID','Session','Inter Resonse Interval','index','Response Requirment']),sort=True)
                    idx += 1

    return ResponseInterval_df

interval_df = get_reponseinterval(location)
interval_mean_df = pd.DataFrame()
for ID in np.unique(interval_df['ID'].values):
    ID_data = interval_df[interval_df['ID']==ID]
    group = np.unique(ID_data[ID_data['ID']==ID]['Group'].values)[0]
    for RR in np.unique(ID_data['Response Requirment'].values):
        Interval_RRsessions = ID_data[(ID_data['ID']==ID)&(ID_data['Response Requirment']==RR)]['Inter Resonse Interval'].values
        Interval_RR_mean = np.mean(Interval_RRsessions)
        interval_mean_df = interval_mean_df.append(pd.DataFrame([[group,ID,Interval_RR_mean,RR]], 
                                                         columns=['Group','ID','Inter-interval','Response requirment']),sort=True)

interval_mean_df.to_excel('ResponseInterval_mean.xls', index = False)


