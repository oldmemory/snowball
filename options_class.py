# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 08:46:23 2021

@author: these
"""
basedir=r'D:\西南证券\衍生品\定价\雪球\程序'
import numpy as np
import pandas as pd
import os
os.chdir(basedir)
from pre_param import *
from abc import ABCMeta, abstractmethod

result_names1=["delta","gamma","vega","theta","rho"]
result_names2=['volga','vanna','vegat','charm','theta_1tday','vegat_1tday','charm_1tday']    
result_names3=["delta_1%S","gamma_1%S",'vega_1%sigma','vega_1%',"vanna_1%S1%sigma","vanna_1%S1%",'volga_1%sigma','volga_1%']
result_names4=["delta_dayS","gamma_dayS","vanna_dayS1%sigma","vanna_dayS1%"]
result_names5=['vegat_1day1%sigma','vegat_1day1%','charm_1day1%S','charm_1daydayS']

class options():
    def __init__(self,name,startdate,enddate,curdate,underlying,r,b,isPathDependent,\
                 greeks_names=result_names1+result_names2+result_names3+\
                 result_names4+result_names5):
        self.name=name
        self.startdate=startdate
        self.enddate=enddate
        self.curdate=curdate
        self.underlying=underlying
        self.r=r
        self.b=b
        self.isPathDependent=isPathDependent
        self.pricing=pd.DataFrame(np.array([]))
        self.greeks=pd.DataFrame(np.array([[] for i in greeks_names]),index=greeks_names)
        
        @abstractmethod
        def payoff_func(self):
            pass
        
class vanilla_european(options):
    def __init__(self,name,startdate,enddate,curdate,underlying,Spast,r,b,\
                 T_day_interest_noofdays_func=naturalday_noofdays,option_payoff=vanilla_put_payoff,\
                 isPathDependent=False,T_year_S_sim=tday_year,T_year_interest=naturalday_year,greeks_names=result_names1+result_names2+result_names3+\
                 result_names4+result_names5):
        super(vanilla_european,self).__init__(name,startdate,enddate,curdate,underlying,r,b,isPathDependent)
        self.Spast=Spast
        self.K=Spast.loc[startdate][0]
        self.T_year_S_sim=T_year_S_sim
        self.T_year_interest=T_year_interest
        self.T_day_interest_noofdays_func=T_day_interest_noofdays_func
        self.payoff_func=option_payoff
#    def pricing_ana(self,S=self):
#        d1 = (log(S/X) + (b + sigma * sigma/2) * Time)/(sigma * sqrt(Time))
#        d2 = d1 - sigma * sqrt(Time)
#    if (TypeFlag == "c") 
#        result = S * exp((b - r) * Time) * CND(d1) - X * exp(-r * 
#            Time) * CND(d2)
#    if (TypeFlag == "p") 
#        result = X * exp(-r * Time) * CND(-d2) - S * exp((b - 
#            r) * Time) * CND(-d1)

#基础版本雪球，敲出价格不变，敲入观察日为每一天,敲入和敲出的K是相同的
class snowball_basic(options):
    def __init__(self,name,startdate,enddate,curdate,underlying,Spast,r,b,\
                 knock_out_ratio,knock_in_ratio,knock_out_dates,knock_out_payoff_yearly_rates,nothing_happens_payoff_yearly_rates,\
                 T_day_interest_noofdays_func=naturalday_noofdays,knock_in_option_payoff=vanilla_put_payoff,\
                 isPathDependent=True,T_year_S_sim=tday_year,T_year_interest=naturalday_year,greeks_names=result_names1+result_names2+result_names3+\
                 result_names4+result_names5):
        super(snowball_basic,self).__init__(name,startdate,enddate,curdate,underlying,r,b,isPathDependent)
        self.knock_out_ratio=knock_out_ratio
        self.knock_in_ratio=knock_in_ratio
        self.knock_out_dates=knock_out_dates
        self.knock_out_payoff_yearly_rates=knock_out_payoff_yearly_rates
        self.nothing_happens_payoff_yearly_rates=nothing_happens_payoff_yearly_rates
        self.Spast=Spast
        self.K=Spast.loc[startdate][0]
        self.T_year_S_sim=T_year_S_sim
        self.T_year_interest=T_year_interest
        self.T_day_interest_noofdays_func=T_day_interest_noofdays_func
        self.knock_in_option_payoff=knock_in_option_payoff
        
        def payoff_func(S=self.Spast,K=self.K,startdate=self.startdate,enddate=self.enddate,curdate=self.curdate,\
                        knock_out_dates=self.knock_out_dates,knock_out_ratio=self.knock_out_ratio,\
                        T_day_interest_noofdays_func=self.T_day_interest_noofdays_func,T_year_interest=self.T_year_interest,\
                        knock_in_option_payoff=self.knock_in_option_payoff,\
                        knock_out_payoff_yearly_rates=self.knock_out_payoff_yearly_rates,knock_in_ratio=self.knock_in_ratio,\
                        nothing_happens_payoff_yearly_rates=self.nothing_happens_payoff_yearly_rates):
            knock_out_dates=[i for i in knock_out_dates if i in S.index]
            already_knock_out=False
            if len(knock_out_dates)>0:
                if S.loc[knock_out_dates].values.max()>=K*knock_out_ratio:
                    payoff_time=knock_out_dates[np.where(S.loc[knock_out_dates].values>K*knock_out_ratio)[0][0]]
                    delta_days=T_day_interest_noofdays_func(startdate,payoff_time)
                    payoff_amount=knock_out_payoff_yearly_rates*delta_days/T_year_interest
                    already_knock_out=True
            if already_knock_out==False:
                if S.values.min()<K*knock_in_ratio:
                    payoff_amount=-knock_in_option_payoff(S.iloc[-1],K)
                    payoff_time=enddate
                else:
                    payoff_time=enddate
                    delta_days=T_day_interest_noofdays_func(startdate,payoff_time)
                    payoff_amount=nothing_happens_payoff_yearly_rates*delta_days/T_year_interest
                
            return({"payoff_amount":payoff_amount,"payoff_time":payoff_time})
            
        self.payoff_func=payoff_func

#        def pricing_overall_func(self,pricing_func, payoff_func,**kwargs,tag3):
#            pricing_func(self.payoff_func,**kwargs,tag3)
#        def greeks_overall_func(self,greeks_func,payoff_func,**kwarts,tag3):
#            greeks_func(self.payoff_func,**kwargs,tag3)


#class guaranteed_snowball(snowball_basic):
    

