# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 09:01:49 2021

@author: these
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 15:25:21 2021

@author: these
"""
import pandas as pd
import numpy as np
import re
knock_out_dates=['2021-06-25','2021-07-26','2021-08-25','2021-09-27','2021-10-25','2021-11-25','2021-12-27','2022-01-25','2022-02-25','2022-03-25']
Spast=pd.DataFrame([100],index=['2021-03-25'])
snow1=snowball_basic(name='testNo1',startdate='2021-03-25',enddate='2022-03-25',\
                     curdate='2021-03-25',underlying='000905.SH',Spast=Spast,\
                     r=0.04,b=0.04,knock_out_ratio=1.03,knock_in_ratio=0,knock_in_option_payoff=nothing_payoff,\
                     knock_out_dates=knock_out_dates,\
                     knock_out_payoff_yearly_rates=0.1,\
                     nothing_happens_payoff_yearly_rates=0.03)

temp=snow1.pricing_snowball_basic_MC(snow1.payoff_func,Spast,snow1.K,snow1.startdate,snow1.enddate,snow1.curdate,snow1.r,snow1.b,0.3,\
                           snow1.T_year_interest,snow1.T_day_interest_noofdays_func,\
                           snow1.b,snow1.knock_out_dates,1.05,\
                           0.05,snow1.knock_in_ratio,snow1.knock_in_option_payoff,\
                           -0.05,S_sim_class=S_sim_BS,T_year_S_sim=snow1.T_year_S_sim,\
                           date_series_funcs=tday_interval,date_noofdays_funcs=tday_noofdays,\
                           date_series_gen_args={},S_gen_args={'freq':1,'MC_M':1000},tag3='')
temp['pricing']
np.mean(temp['pricing_detail'])
np.std(temp['pricing_detail'])/np.mean(temp['pricing_detail'])



payoff_func,Spast,K,startdate,enddate,curdate,r,b,sigma,\
                           T_year_interest,T_day_interest_noofdays_func,\
                           mu,knock_out_dates,knock_out_ratio,\
                           knock_out_payoff_yearly_rates,knock_in_ratio,knock_in_option_payoff,\
                           nothing_happens_payoff_yearly_rates,S_sim_class=\
                           snow1.payoff_func,Spast,snow1.K,snow1.startdate,snow1.enddate,snow1.curdate,snow1.r,snow1.b,0.3,\
                           snow1.T_year_interest,snow1.T_day_interest_noofdays_func,\
                           snow1.b,snow1.knock_out_dates,1.05,\
                           0.05,snow1.knock_in_ratio,snow1.knock_in_option_payoff,\
                           -0.05,S_sim_BS
T_year_S_sim=snow1.T_year_S_sim
date_series_funcs=tday_interval
date_noofdays_funcs=tday_noofdays
date_series_gen_args={}
S_gen_args={'freq':1,'MC_M':1000}
tag3=''
