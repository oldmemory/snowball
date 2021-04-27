# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 15:25:17 2021

@author: these
"""
import re
from WindPy import w
w.start()
hist_close=w.wsd("000905.SH", "close", "2020-09-09", "2021-03-26", "")

snows=[]
pricing_seq=[]
delta_seq=[]
sigma=0.3
for hist_i in range(0,len(hist_close.Times),1):
    curdate=str(hist_close.Times[hist_i])
    print(curdate)
    Spast=pd.DataFrame(hist_close.Data[0][:(hist_i+1)],index=[str(i) for i in hist_close.Times[:(hist_i+1)]])
    snow1=snowball_basic(name='东兴7号',startdate='2020-09-09',enddate='2022-09-08',\
                         curdate=curdate,underlying='000905.SH',Spast=Spast,\
                         r=0.05,b=0.05,knock_out_ratio=1.03,knock_in_ratio=0.75,\
                         knock_out_dates=knock_out_dates_dongxingNo7,\
                         knock_out_payoff_yearly_rates=0.225,\
                         nothing_happens_payoff_yearly_rates=0.225)
    temp=snow1.pricing_snowball_basic_MC(snow1.payoff_func,Spast,snow1.K,snow1.startdate,snow1.enddate,snow1.curdate,snow1.r,snow1.b,sigma,\
                           snow1.T_year_interest,snow1.T_day_interest_noofdays_func,\
                           snow1.b,snow1.knock_out_dates,snow1.knock_out_ratio,\
                           snow1.knock_out_payoff_yearly_rates,snow1.knock_in_ratio,snow1.knock_in_option_payoff,\
                           snow1.nothing_happens_payoff_yearly_rates,T_year_S_sim=snow1.T_year_S_sim,S_sim_class=S_sim_BS,date_series_gen_args={},S_gen_args={'freq':1,'MC_M':5000},tag3='')
    pricing_seq.append(temp['pricing'])
    temp_args=quickly_set_params(snow1.pricing_snowball_basic_MC,snow1)
    temp_args[1]['S_gen_args']={'freq':1,'MC_M':5000}
    temp_greeks=snow1.greeks_basic_diff(pricing_func=snow1.pricing_snowball_basic_MC,sigma=sigma,mu=snow1.b,S_sim_class=S_sim_BS,requirements=['delta'],margin=0.01,**dict(temp_args[0],**temp_args[1]))
    delta_seq.append(temp_greeks['delta'])
    if len(re.findall('over',temp['tag']))>0:
        break
np.save(basedir+'/20210329/pricing_seq.npy',np.array(pricing_seq))
np.save(basedir+'/20210329/delta_seq.npy',np.array(pricing_seq))

portfolio_name='雪球对冲_现货'
w.wupf(portfolio_name,'','','','','reset=true')
w.wupf(portfolio_name,'2020-09-09','CNY', 1e6, "1","Direction=Short;Method=BuySell;CreditTrading=No;Owner=W6382199183;type=flow")
delta_seq_change=np.diff([0]+delta_seq)
PL_seq0=[]
for hist_i in range(0,len(delta_seq),1):
    curdate=str(hist_close.Times[hist_i])
    Spast=pd.DataFrame(hist_close.Data[0][:(hist_i+1)],index=[str(i) for i in hist_close.Times[:(hist_i+1)]])
    w.wupf(portfolio_name,curdate,'000905.SH', str(delta_seq_change[int(hist_i)]), str(Spast.iloc[-1,0]),"Direction=Long;Method=BuySell;CreditTrading=No;Owner=W6382199183;type=flow")
    #temp_PL=w.wpf(portfolio_name,'TotalPL','view=PMS','startDate=20201109','endDate=20210308','sectorcode=101','displaymode=1')
    temp_PL=w.wpf(portfolio_name,'NetHoldingValue','view=PMS','date='+curdate,'sectorcode=101','displaymode=1')
    PL_seq0.append(np.sum(temp_PL.Data[3]))
PL_all=[PL_seq0[i]-pricing_seq[i]*snow1.K-1e6 for i in range(len(PL_seq0))]
np.min(PL_all>11)

'000905.SH'
w_wsd_data=w.wsd("IC.CFE", "close", "2021-02-27", "2021-03-28", "")
w_wsd_data.Data
w_wsd_data=w.wsd("IC2103.CFE", "close", "2020-09-09", "2020-09-28", "")

##直接读取
portfolio_name='雪球对冲_现货'
delta_seq=np.load(basedir+'/20210329/delta_seq.npy')
pricing_seq=np.load(basedir+'/20210329/pricing_seq.npy')
delta_seq_change=np.diff([0]+delta_seq)
PL_seq0=[]
from WindPy import w
w.start()
hist_close=w.wsd("000905.SH", "close", "2020-09-09", "2021-03-26", "")
for hist_i in range(0,len(delta_seq),1):
    curdate=str(hist_close.Times[hist_i])
    temp_PL=w.wpf(portfolio_name,'NetHoldingValue','view=PMS','date='+curdate,'sectorcode=101','displaymode=1')
    PL_seq0.append(np.sum(temp_PL.Data[3]))
PL_all=[PL_seq0[i]-pricing_seq[i]*snow1.K-1e6 for i in range(len(PL_seq0))]

