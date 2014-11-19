# -*- coding: utf-8 -*-
'''
Created on 10 Nov, 2014

@author: wangyi
'''
from __future__ import division
from math import fmod
from operator import add

from utils.Sci.series import Weeks
from pandas import DataFrame

weekday = {'Mon': '0', 'Tue': '1', 'Wed': '2', 'Thu': '3', 'Fri': '4', 'Sat': '5', 'Sun': '6'}

class TypicalWeek(Weeks):
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}):
        super(TypicalWeek, self).__init__(startdatetime, enddatetime, data, type=type)

    def __str__(self):
        return "Typical Week:"

    def getTypicalWeek(self):
        return (self.indexes, self.typicalWeek)

    def buildTypicalWeek(self):
        
        indexes = list(
                       map(
                           fmod,
                           range(1, 25),
                           [24] * 24
                           )
                       )
        
        indexes = list(
                       map(
                           int,
                           indexes
                           )
                       )
        
        self.indexes = list(
                            map(
                                str,
                                indexes
                                )
                            )

        self.typicalWeek = {
                            "Mon":[DataFrame(data = 0.0, columns = ['power_kw'],index = indexes), 0],
                            "Tue":[DataFrame(data = 0.0, columns = ['power_kw'],index = indexes), 0],
                            "Wed":[DataFrame(data = 0.0, columns = ['power_kw'],index = indexes), 0],
                            "Thu":[DataFrame(data = 0.0, columns = ['power_kw'],index = indexes), 0],
                            "Fri":[DataFrame(data = 0.0, columns = ['power_kw'],index = indexes), 0],
                            "Sat":[DataFrame(data = 0.0, columns = ['power_kw'],index = indexes), 0],
                            "Sun":[DataFrame(data = 0.0, columns = ['power_kw'],index = indexes), 0],
                            }        
        
        for daynode in self.treeIndex['dayly']:
            if   daynode.startdatetime.weekday() == 0:
                if daynode.dt_min != 0:
                    self.typicalWeek["Mon"][0]['power_kw'] = self.typicalWeek["Mon"][0].values + daynode.data.values
                    self.typicalWeek["Mon"][1] += 1
            elif daynode.startdatetime.weekday() == 1:
                if daynode.dt_min != 0:
                    self.typicalWeek["Tue"][0]['power_kw'] = self.typicalWeek["Tue"][0].values + daynode.data.values
                    self.typicalWeek["Tue"][1] += 1 
            elif daynode.startdatetime.weekday() == 2:
                if daynode.dt_min != 0:
                    self.typicalWeek["Wed"][0]['power_kw'] = self.typicalWeek["Wed"][0].values + daynode.data.values
                    self.typicalWeek["Wed"][1] += 1                                   
            elif daynode.startdatetime.weekday() == 3:
                if daynode.dt_min != 0:
                    self.typicalWeek["Thu"][0]['power_kw'] = self.typicalWeek["Thu"][0].values + daynode.data.values
                    self.typicalWeek["Thu"][1] += 1 
            elif daynode.startdatetime.weekday() == 4:
                if daynode.dt_min != 0:
                    self.typicalWeek["Fri"][0]['power_kw'] = self.typicalWeek["Fri"][0].values + daynode.data.values
                    self.typicalWeek["Fri"][1] += 1
            elif daynode.startdatetime.weekday() == 5:
                if daynode.dt_min != 0:
                    self.typicalWeek["Sat"][0]['power_kw'] = self.typicalWeek["Sat"][0].values + daynode.data.values
                    self.typicalWeek["Sat"][1] += 1                                          
            elif daynode.startdatetime.weekday() == 6:
                if daynode.dt_min != 0:
                    self.typicalWeek["Sun"][0]['power_kw'] = self.typicalWeek["Sun"][0].values + daynode.data.values
                    self.typicalWeek["Sun"][1] += 1  
                    
        self.typicalWeek["Mon"][0] = self.typicalWeek["Mon"][0] / self.typicalWeek["Mon"][1] 
        self.typicalWeek["Tue"][0] = self.typicalWeek["Tue"][0] / self.typicalWeek["Tue"][1]                         
        self.typicalWeek["Wed"][0] = self.typicalWeek["Wed"][0] / self.typicalWeek["Wed"][1] 
        self.typicalWeek["Thu"][0] = self.typicalWeek["Thu"][0] / self.typicalWeek["Thu"][1] 
        self.typicalWeek["Fri"][0] = self.typicalWeek["Fri"][0] / self.typicalWeek["Fri"][1]
        self.typicalWeek["Sat"][0] = self.typicalWeek["Sat"][0] / self.typicalWeek["Sat"][1] 
        self.typicalWeek["Sun"][0] = self.typicalWeek["Sun"][0] / self.typicalWeek["Sun"][1]  
    
        return self
## event trigger function 

def onTest_read(start_date, end_date, series, *args, **keywords):
    
    ids, tw = TypicalWeek(start_date, end_date, series).setup().buildtree().buildTypicalWeek().getTypicalWeek()
    mid = keywords['mid']
    message = keywords['message']
    taskFac = keywords['taskFac']
    
    id_pre = start_date.strftime("%y%V") + end_date.strftime("%y%V")
    id_suc = mid[-3:]
    
    data = []
    # convert tw to records:

    for k, v in tw.items():
        idx = list(
                   map(add, [id_pre + id_suc + weekday[k]] * 24, ids)
                   )
        
        v[0]['idx'] = idx
        
        v[0].index.name = 'hour'
        v[0].reset_index(level=0, inplace=True)
        records = v[0].to_dict('records')
        dict = {}
        dict['weekday'] = k
        dict['values'] = records
        data.append(dict)  
    
    message.put( taskFac(
                        None, 
                        'BMS_typical_week_by_meter', 
                        data,
                        start=start_date,
                        end=end_date,
                        mid=mid,  
                        ) )
    
def onTest_write(id, name, data, args, hint):
    from core.DAO.Database import Database
    from utils.jsonConfig import config, configx, SQL_TEMPLATES
     
    start = hint['start']
    end   = hint['end']
    pm_id = hint['mid']
    
    db = Database(db = 'ict_data_tran', **configx['ERIconfig'])
    
    for record in data:   
        db.insert(SQL_TEMPLATES['INSERT']['ERI_BMS_TYPICAL_WEEK'], 
                  start,
                  end,
                  pm_id,
                  record['weekday'],
                  record['values'])