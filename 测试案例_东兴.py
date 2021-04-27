# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:37:39 2021

@author: these
"""
import pandas as pd
import numpy as np
import re
#############读取中证500的历史价格
from WindPy import w
w.start()
hist_close=w.wsd("000905.SH", "close", "2020-09-09", "2021-03-26", "")

snows=[]
pricing_seq=[]
knock_out_dates_dongxingNo7=['2020-12-08','2021-01-08','2021-02-08','2021-03-08','2021-04-08','2021-05-07','2021-06-08',\
                                          '2021-07-08','2021-08-09','2021-09-08','2021-10-08','2021-11-08','2021-12-08','2022-01-07',\
                                          '2022-02-08','2022-03-08','2022-04-08','2022-05-09','2022-06-08','2022-07-08','2022-08-08','2022-09-08']
#knock_out_dates_6month=['2020-12-08','2021-01-08','2021-02-08','2021-03-08']

for hist_i in range(0,len(hist_close.Times),10):
    start=time.time()
    curdate=str(hist_close.Times[hist_i])
    print(curdate)
    Spast=pd.DataFrame(hist_close.Data[0][:(hist_i+1)],index=[str(i) for i in hist_close.Times[:(hist_i+1)]])
    snow1=snowball_basic(name='东兴7号',startdate='2020-09-09',enddate='2022-09-08',\
                         curdate=curdate,underlying='000905.SH',Spast=Spast,\
                         r=0.05,b=0.05,knock_out_ratio=1.03,knock_in_ratio=0.75,\
                         knock_out_dates=knock_out_dates_dongxingNo7,\
                         knock_out_payoff_yearly_rates=0.2,\
                         nothing_happens_payoff_yearly_rates=0.2)
    temp=snow1.pricing_snowball_basic_MC(snow1.payoff_func,Spast,snow1.K,snow1.startdate,snow1.enddate,snow1.curdate,snow1.r,snow1.b,0.2,\
                           snow1.T_year_interest,snow1.T_day_interest_noofdays_func,\
                           snow1.b,snow1.knock_out_dates,snow1.knock_out_ratio,\
                           snow1.knock_out_payoff_yearly_rates,snow1.knock_in_ratio,snow1.knock_in_option_payoff,\
                           snow1.nothing_happens_payoff_yearly_rates,T_year_S_sim=snow1.T_year_S_sim,S_sim_class=S_sim_BS,date_series_gen_args={},S_gen_args={'freq':1,'MC_M':150000},tag3='')
    pricing_seq.append(temp['pricing'])
    end=time.time()
    print(end-start)
    if len(re.findall('over',temp['tag']))>0:
        break
    
payoff_func=snow1.payoff_func
K=snow1.K
startdate,enddate,curdate,r,b,sigma=snow1.startdate,snow1.enddate,snow1.curdate,snow1.r,snow1.b,0.25
T_year_interest,T_day_interest_noofdays_func=snow1.T_year_interest,snow1.T_day_interest_noofdays_func
mu,knock_out_dates,knock_out_ratio=snow1.b,snow1.knock_out_dates,snow1.knock_out_ratio
knock_out_payoff_yearly_rates,knock_in_ratio,knock_in_option_payoff=snow1.knock_out_payoff_yearly_rates,snow1.knock_in_ratio,snow1.knock_in_option_payoff
nothing_happens_payoff_yearly_rates= snow1.nothing_happens_payoff_yearly_rates
T_year_S_sim=snow1.T_year_S_sim                         
date_series_funcs=tday_interval
date_noofdays_funcs=tday_noofdays
S_sim_class=S_sim_BS
date_series_gen_args={}
S_gen_args={'freq':1,'MC_M':200000}
tag3=''
