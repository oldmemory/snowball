# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 15:16:39 2021

@author: these
"""
from S_sim_class import *
from options_class import *
def pricing_MC0(payoff_func,S_sim):
    pass

def pricing_snowball_basic_MC(self,payoff_func,Spast,K,startdate,enddate,curdate,r,b,sigma,\
                           T_year_interest,T_day_interest_noofdays_func,\
                           mu,knock_out_dates,knock_out_ratio,\
                           knock_out_payoff_yearly_rates,knock_in_ratio,knock_in_option_payoff,\
                           nothing_happens_payoff_yearly_rates,S_sim_class,\
                           T_year_S_sim=tday_year,date_series_funcs=tday_interval,date_noofdays_funcs=tday_noofdays,\
                           date_series_gen_args={},S_gen_args={'freq':1,'MC_M':10},tag3=''):
    if curdate==enddate:
        temp=payoff_func(Spast,K=K,startdate=startdate,enddate=enddate,curdate=curdate,\
                         knock_out_dates=knock_out_dates,knock_out_ratio=knock_out_ratio,\
                         T_day_interest_noofdays_func=T_day_interest_noofdays_func,T_year_interest=T_year_interest,\
                         knock_in_option_payoff=knock_in_option_payoff,\
                        knock_out_payoff_yearly_rates=knock_out_payoff_yearly_rates,knock_in_ratio=knock_in_ratio,\
                        nothing_happens_payoff_yearly_rates=nothing_happens_payoff_yearly_rates)
        return({'pricing':temp['payoff_amount'],'pricing_detail':temp['payoff_amount'],'tag':tag3+'over;'})
    past_knock_out_dates=[i for i in knock_out_dates if i in Spast.index[:-1]]
    if len(past_knock_out_dates)>0:
        if Spast.loc[past_knock_out_dates].iloc[:-1,0].max()>K*knock_out_ratio:
            return({'pricing':None,'pricing_detail':[],'tag':tag3+'already_over;'})
    if curdate in knock_out_dates:
        if Spast.loc[curdate,0]>K*knock_out_ratio:
            temp=knock_out_payoff_yearly_rates*T_day_interest_noofdays_func(startdate,curdate)/T_year_interest
            return({'pricing':temp,'pricing_detail':[temp],'tag':tag3+'over;'})
    Sfuture=S_sim_class(startdate=curdate,enddate=enddate,S0=Spast.iloc[-1,0],r=r,b=b,\
                     sigma=sigma,T_year=T_year_S_sim,date_series_funcs=date_series_funcs,\
                     date_noofdays_funcs=date_noofdays_funcs,tag='')
    Sfuture.date_series_gen(**date_series_gen_args)
    Sfuture.S_gen(**S_gen_args)
    pricing_result=[]
    for i in range(Sfuture.S.shape[1]):
        Sall=pd.concat([Spast.iloc[:-1,0],Sfuture.S.iloc[:,i]])
        temp=payoff_func(Sall,K=K,startdate=startdate,enddate=enddate,curdate=curdate,\
                         knock_out_dates=knock_out_dates,knock_out_ratio=knock_out_ratio,\
                         T_day_interest_noofdays_func=T_day_interest_noofdays_func,T_year_interest=T_year_interest,\
                         knock_in_option_payoff=knock_in_option_payoff,\
                        knock_out_payoff_yearly_rates=knock_out_payoff_yearly_rates,knock_in_ratio=knock_in_ratio,\
                        nothing_happens_payoff_yearly_rates=nothing_happens_payoff_yearly_rates)
        if temp["payoff_time"]>=curdate:
            discount_days=date_noofdays_funcs(curdate,temp["payoff_time"])
            pricing_result.append(temp["payoff_amount"]*np.exp(-r*discount_days/T_year_S_sim))
#            discount_days=naturalday_noofdays(curdate,temp["payoff_time"])
#            pricing_result.append(temp["payoff_amount"]*np.exp(-r*discount_days/T_year_interest))
    return({'pricing':np.mean(pricing_result),'pricing_detail':pricing_result,'tag':tag3+';'+Sfuture.tag})
snowball_basic.pricing_snowball_basic_MC=pricing_snowball_basic_MC

def greeks_basic_diff(self,pricing_func,Spast,K,sigma,r,b,enddate,margin,requirements,**other_pricing_func_args):
    SpastToday=Spast.iloc[-1,0]
    Spast_plus=Spast.copy(deep=True)
    Spast_plus.iloc[-1,0]=SpastToday*(1+margin)
    Spast_minus=Spast.copy(deep=True)
    Spast_minus.iloc[-1,0]=SpastToday*(1-margin)
    result={}
    if 'delta' in requirements:
        result['delta']=(pricing_func(Spast=Spast_plus,r=r,b=b,K=K,sigma=sigma,enddate=enddate,**other_pricing_func_args)['pricing']-\
               pricing_func(Spast=Spast_minus,r=r,b=b,K=K,sigma=sigma,enddate=enddate,**other_pricing_func_args)['pricing'] )*K/(2*margin*SpastToday)
    if 'gamma' in requirements:
        result['gamma']=(pricing_func(Spast=Spast_plus,r=r,b=b,K=K,sigma=sigma,enddate=enddate,**other_pricing_func_args)['pricing']+\
              pricing_func(Spast=Spast_minus,r=r,b=b,K=K,sigma=sigma,enddate=enddate,**other_pricing_func_args)['pricing']-\
              2*pricing_func(Spast=Spast,r=r,b=b,K=K,sigma=sigma,enddate=enddate,**other_pricing_func_args)['pricing'] )*K/(margin**2)/(SpastToday**2)
    
    if 'vega' in requirements:
        result['vega']=(pricing_func(Spast=Spast,r=r,b=b,K=K,sigma=sigma*(1+margin),enddate=enddate,**other_pricing_func_args)['pricing']-\
              pricing_func(Spast=Spast,r=r,b=b,K=K,sigma=sigma*(1-margin),enddate=enddate,**other_pricing_func_args)['pricing'] )*K/(2*margin*sigma)
    
    r_plus=(1+margin)*r
    b_plus=(1+margin)*r-(r-b)
    r_minus=(1-margin)*r
    b_minus=(1-margin)*r-(r-b)
    if 'rho' in requirements:
        result['rho']=(pricing_func(Spast=Spast,r=r_plus,b=b_plus,K=K,sigma=sigma,enddate=enddate,**other_pricing_func_args)['pricing']-\
              pricing_func(Spast=Spast,r=r_minus,b=b_minus,K=K,sigma=sigma,enddate=enddate,**other_pricing_func_args)['pricing'] )*K/(2*margin*r)
    
    return(result)
options.greeks_basic_diff=greeks_basic_diff

#snow1.greeks_basic_diff(snow1.pricing_snowball_basic_MC,Spast,K,sigma,r,b,enddate,0.01,\
#                        startdate=startdate,payoff_func=payoff_func,curdate=curdate,\
#                           T_year_interest=T_year_interest,T_day_interest_noofdays_func=T_day_interest_noofdays_func,\
#                           mu=mu,knock_out_dates=knock_out_dates,knock_out_ratio=knock_out_ratio,\
#                           knock_out_payoff_yearly_rates=knock_out_payoff_yearly_rates,knock_in_ratio=knock_in_ratio,knock_in_option_payoff=knock_in_option_payoff,\
#                           nothing_happens_payoff_yearly_rates=nothing_happens_payoff_yearly_rates,S_sim_class=S_sim_class,\
#                           T_year_S_sim=tday_year,date_series_funcs=tday_interval,date_noofdays_funcs=tday_noofdays,\
#                           date_series_gen_args={},S_gen_args={'freq':1,'MC_M':1000},tag3='',requirements=['delta','gamma'])
#quickly_set_params(snow1.greeks_basic_diff,snow1)
#temp_args=quickly_set_params(snow1.pricing_snowball_basic_MC,snow1)
#temp_args[2]
#snow1.greeks_basic_diff(pricing_func=snow1.pricing_snowball_basic_MC,sigma=0.3,mu=snow1.b,S_sim_class=S_sim_BS,requirements=['delta'],margin=0.01,**dict(temp_args[0],**temp_args[1]))
