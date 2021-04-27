# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 15:20:53 2021

@author: these
"""
from pre_param import *
import pandas as pd
import numpy as np
from scipy.stats import norm
import time, datetime
from abc import ABCMeta, abstractmethod
class S_sim():
    def __init__(self,startdate,enddate,T_year,date_series_funcs,date_noofdays_funcs,tag=''):
        self.tag=tag
        self.startdate=startdate
        self.enddate=enddate
        self.S=pd.DataFrame([])
        self.date_series_funcs=date_series_funcs
        self.date_noofdays_funcs=date_noofdays_funcs
        self.T_year=T_year
        
    
    #在S_gen之前必须先生成date_series。一般默认startdate不在date_series中，即
    #date_noofdays第一个不是0
    def date_series_gen(self,**kwargs):
        temp=self.date_series_funcs(self.startdate,self.enddate,**kwargs)
        self.date_series=temp.values.reshape([1,-1]).tolist()[0]
        self.date_noofdays=[self.date_noofdays_funcs(self.startdate,i,**kwargs) for i in self.date_series]
        
    @abstractmethod    
    def S_gen(self,**kwargs):
        pass

##################提高MC收敛速度的函数
def gen_more_MC_method1(rdarray):
    new_rdarray=np.concatenate((rdarray,-rdarray),axis=0)
    return(new_rdarray)
#####################################        
    
    
class S_sim_BS(S_sim):
    #r,b等都是按照年化来的，date_series的频率可能不是以天为单位，故T_year代表了一年在date_series里面的长度
    #date_series_funcs生成日期序列，和周期无关
    #date_noofdays_funcs生成日期间隔天数，和周期有关
    def __init__(self,startdate,enddate,S0,r,b,sigma,T_year,date_series_funcs,date_noofdays_funcs,\
                 mu=np.nan,tag=''):
        super(S_sim_BS,self).__init__(startdate,enddate,T_year,date_series_funcs,date_noofdays_funcs,tag)
        self.S0=S0
        self.r=r
        self.b=b
        self.sigma=sigma
        if np.isnan(mu):
            mu=b
        self.mu=mu
        self.date_series=None
        self.tag='BS;r='+str(r)+';b='+str(b)+';sigma='+str(sigma)+';mu='+str(mu)+\
            ';date_series_funcs='+str(date_series_funcs.__name__)+';'+tag+';'
        
        
    def S_gen(self,freq=1,MC_M=10000,gen_more_MC=gen_more_MC_method1):
        self.MC_M=MC_M
        rdmatrix = np.random.randn(self.MC_M, len(self.date_series)) 
        rdarray = np.array(rdmatrix)
        rdarray=gen_more_MC(rdarray)
        M = rdarray.shape[0] # M为模拟次数
        N = rdarray.shape[1] # N为观察次数
        dt = np.diff([0]+self.date_noofdays) # 观察日序列
        W = np.multiply(rdarray,np.sqrt(dt/self.T_year)).cumsum(1) # 布朗运动累加
        # 初始化价格序列矩阵，多了一列为期初价格
        St = np.ones((M, N + 1)) * self.S0
        # 几何布朗运动序列
        St[:, 1:] = self.S0 * np.exp(np.dot((self.b - 1/2 * self.sigma**2)/self.T_year,self.date_noofdays)+ \
          self.sigma*W)
        St=pd.DataFrame(St,columns=[self.startdate]+self.date_series)
        St=St.transpose()
        self.S=St
        return({"S":St,"tag":self.tag})

    
        
        

#############案例
#v1=S_sim_BS('2021-1-26','2021-3-10',100,0.04,0.03,0.2,252,tday_interval,tday_noofdays,MC_M=10)
#v1=S_sim_BS(startdate='2021-1-26',enddate='2021-3-10',S0=100,r=0.04,b=0.04,sigma=0.2,T_year=252,\
#            date_series_funcs=tday_interval,date_noofdays_funcs=tday_noofdays)
#v1.date_series_gen()
#Ss=v1.S_gen(MC_M=10)
