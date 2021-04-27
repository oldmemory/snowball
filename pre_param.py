# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 09:41:25 2021

@author: these
"""

import numpy as np
import pandas as pd
import datetime
import time

##填写函数的更有效的方式
###看哪些参数是object1里面有的，归总到b_in_dict里面，
#####在b_in_defaults中的，也可以直接传递
##因此可以直接用**dict(b_in_dict,**b_in_defaults)传递
##这样如果b_in_dict和b_in_defaults有重复，以函数的b_in_defaults为准，而不是类对象的b_in_dict为准
##在b_notin_list中的，需要单独设置参数值
import inspect
def quickly_set_params(function1,object1):
    a=object1.__dict__##类的内部成员变量
    b=inspect.getfullargspec(function1).args#函数的参数表
    if 'self' in b:
        b.remove('self')#去掉self参数
    b_in_dict=dict([(i,a[i]) for i in b if i in a.keys()])#字典化object中已有的参数
    
    b_defaults_values=inspect.getfullargspec(function1).defaults
    if b_defaults_values:
        b_defaults=b[-len(b_defaults_values):]
        b_in_defaults=dict(zip(b_defaults,b_defaults_values))
    else:
        b_defaults=[]
        b_in_defaults=[]
    b_notin_list=[i for i in b if not ( (i in b_in_dict.keys()) or (i in b_defaults))]
    return([b_in_dict,b_in_defaults,b_notin_list])


tdays=pd.read_csv('tdays.csv',index_col=0)
date_tdays=np.array([datetime.datetime.strptime(i,'%Y-%m-%d') for i in tdays['x']])

def tday_noofdays(startday,endday,tou=False,wei=True):
  if isinstance(startday,str):
      startday=datetime.datetime.strptime(startday,'%Y-%m-%d')
  if isinstance(endday,str):  
      endday=datetime.datetime.strptime(endday,'%Y-%m-%d')
  
  new_startday=np.where(date_tdays<=startday)
  if(len(new_startday[0])>1):
    new_startday=new_startday[0][-1]
    if(tou==True):
      if(date_tdays[new_startday]==startday ):
        new_startday=new_startday-1
      
  new_endday=np.where(date_tdays>=endday)
  if(len(new_endday[0])>1):
    new_endday=new_endday[0][0]
    if(wei==False):
      if(date_tdays[new_endday]==endday ):
        new_endday=new_endday-1
    
  noofdays=new_endday-new_startday
  return(noofdays)

def tday_interval(startday,endday,tou=False,wei=True):
  if isinstance(startday,str):
      startday=datetime.datetime.strptime(startday,'%Y-%m-%d')
  if isinstance(endday,str):  
      endday=datetime.datetime.strptime(endday,'%Y-%m-%d')
  
  new_startday=np.where(date_tdays<=startday)
  if(len(new_startday[0])>1):
    new_startday=new_startday[0][-1]
    if(tou==True):
      if(date_tdays[new_startday]==startday ):
        new_startday=new_startday-1
  
  new_endday=np.where(date_tdays>=endday)
  if(len(new_endday[0])>1):
    new_endday=new_endday[0][0]
    if(wei==False):
      if(date_tdays[new_endday]==endday ):
        new_endday=new_endday-1
    
  if(new_startday>=new_endday):
      return([])
  result=pd.DataFrame([str(date_tdays[i].date()) for i in range((new_startday+1),(new_endday+1))],columns=tdays.columns)
  return(result)
  #as.character(date(result))



def naturalday_noofdays(startday,endday,tou=False,wei=True):
  if isinstance(startday,str):
      startday=datetime.datetime.strptime(startday,'%Y-%m-%d')
  if isinstance(endday,str):  
      endday=datetime.datetime.strptime(endday,'%Y-%m-%d')
    
  noofdays=(endday-startday).days
  if tou==True:
      noofdays=noofdays+1
  if wei==False:
      noofdays=noofdays-1
      
  return(noofdays)

def naturalday_interval(startday,endday,tou=False,wei=True):
  if isinstance(startday,str):
      startday=datetime.datetime.strptime(startday,'%Y-%m-%d')
  if isinstance(endday,str):  
      endday=datetime.datetime.strptime(endday,'%Y-%m-%d')
  
  if startday>endday:
      bool_increase=False
      early=endday
      later=startday
      bool_early=wei
      bool_later=tou
  else:
      bool_increase=True
      early=startday
      later=endday
      bool_early=tou
      bool_later=wei
  
  result=[i for i in pd.date_range(early,later)]
  if bool_early==False:
      result=result[1:]
  if bool_later==False:
      result=result[:-1]
  if bool_increase==False:
      result.reverse()
  return(result)
  
tday_year=244
naturalday_year=365

def vanilla_put_payoff(S,K):
    return(max(0,1-S/K))
def minus_vanilla_put_payoff(S,K):
    return(-max(0,1-S/K))
def vanilla_call_payoff(S,K):
    return(max(0,S/K-1))
def minus_vanilla_call_payoff(S,K):
    return(-max(0,S/K-1))
def nothing_payoff(*args,**kwargs):
    return(0)
def binary_call_payoff(S,K):
    if S>K:
        return(1)
    else:
        return(0)
def binary_put_payoff(S,K):
    if S<K:
        return(1)
    else:
        return(0)