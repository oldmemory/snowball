# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 15:25:21 2021

@author: these
"""

Spast=pd.DataFrame([100,100],index=['2021-1-1','2021-3-23'])
Spast=pd.DataFrame([100,100],index=['2021-1-1','2021-1-2])
snow1=snowball_basic(name='testNo1',startdate='2021-1-1',enddate='2023-1-1',\
                     curdate='2021-1-1',underlying='000905.SH',Spast=Spast,\
                     r=0.04,b=0.04,knock_out_ratio=1.03,knock_in_ratio=0.75,\
                     knock_out_dates=['2021-3-1','2021-4-1','2021-5-1','2021-6-1','2021-7-1','2021-8-1','2021-9-1','2021-10-1','2021-11-1',\
                                      '2021-12-1','2022-1-1','2022-2-1','2022-3-1','2022-4-1','2022-5-1','2022-6-1','2022-7-1','2022-8-1',\
                                      '2022-9-1','2022-10-1','2022-11-1','2022-12-1','2023-1-1'],knock_out_payoff_yearly_rates=0.1,\
                     nothing_happens_payoff_yearly_rates=0.2)
#Sfuture=pd.DataFrame([101,106,104],index=['2021-3-17','2021-3-18','2021-3-19'])
#K=snow1.K
#knock_out_dates=snow1.knock_out_dates
#knock_out_ratio=snow1.knock_out_ratio
#knock_out_payoff_yearly_rates=snow1.knock_out_payoff_yearly_rates
#knock_in_ratio=snow1.knock_in_ratio
#enddate=snow1.enddate
#r,b=snow1.r,snow1.b
#nothing_happens_payoff_yearly_rates=snow1.nothing_happens_payoff_yearly_rates
#snow1.payoff_func(S=Sfuture)
temp=snow1.pricing_snowball_basic_MC(snow1.payoff_func,Spast,snow1.K,snow1.startdate,snow1.enddate,snow1.curdate,snow1.r,snow1.b,0.15,\
                           snow1.T_year_interest,snow1.T_day_interest_noofdays_func,\
                           snow1.b,snow1.knock_out_dates,1.03,\
                           0.02,snow1.knock_in_ratio,snow1.knock_in_option_payoff,\
                           0.1,T_year_S_sim=snow1.T_year_S_sim,S_sim_class=S_sim_BS,date_series_gen_args={},S_gen_args={'freq':1,'MC_M':1000},tag3='')
temp['pricing']
np.mean(temp['pricing_detail'])
np.std(temp['pricing_detail'])/np.mean(temp['pricing_detail'])

snow1.greeks_basic_MC(snow1.payoff_func,Spast,snow1.K,snow1.startdate,snow1.enddate,snow1.curdate,snow1.r,snow1.b,0.15,\
                           snow1.T_year_S_sim,snow1.T_year_interest,snow1.T_day_interest_noofdays_func,\
                           snow1.b,snow1.knock_out_dates,1.03,\
                           0.02,snow1.knock_in_ratio,snow1.knock_in_option_payoff,\
                           0.1,S_sim_BS,{},{'freq':1,'MC_M':3000},tag3='',margin=0.01)



