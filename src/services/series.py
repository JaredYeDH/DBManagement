# -*- coding: utf-8 -*-
'''
Created on 12 Nov, 2014

@author: wangyi
'''

from utils.Sci.series import Month

#===============================================================================
# 
#===============================================================================
def onTest_read_write_series(start_date, end_date, series, *args, **keywords):
    
    from core.DAO.Database import Database
    from utils.jsonConfig import config, configx, SQL_TEMPLATES
    
    db = Database(db = 'ict_data_tran', **configx['ERIconfig'])
    
    # read
    seriesnode = Month(start_date, end_date, series).setup().buildtree()
    
    # write
    weeklydata= seriesnode.treeIndex['weekly']
    for entry in weeklydata:
        id = entry.id
        date_time = entry.startdatetime
        value = entry.value
        std = entry.std
        max = entry.max
        dt_max = entry.dt_max
        min = entry.min
        dt_min = entry.dt_min
        pm_id = keywords['mid']
        
        db.insert(
                  SQL_TEMPLATES['INSERT']['ERI_BMS_STAT_INSERT_TEMPLATE'],
                  'pm_bms_sci_week',
                  id + pm_id[-3:],
                  date_time,
                  value,
                  std,
                  max,
                  dt_max,
                  min,
                  dt_min,
                  pm_id
                  )    
    
    daylydata = seriesnode.treeIndex['dayly']
    for entry in daylydata:
        id = entry.id
        date_time = entry.startdatetime
        value = entry.value
        std = entry.std
        max = entry.max
        dt_max = entry.dt_max
        min = entry.min
        dt_min = entry.dt_min
        pm_id = keywords['mid']
        
        db.insert(
                  SQL_TEMPLATES['INSERT']['ERI_BMS_STAT_INSERT_TEMPLATE'],
                  'pm_bms_sci_day',
                  id + pm_id[-3:],
                  date_time,
                  value,
                  std,
                  max,
                  dt_max,
                  min,
                  dt_min,
                  pm_id
                  )        
    
    hourlydata = seriesnode.treeIndex['hourly']
    for entry in hourlydata:
        id = entry.id
        date_time = entry.startdatetime
        value = entry.value
        std = 0
        max = entry.max
        dt_max = entry.dt_max
        min = entry.min
        dt_min = entry.dt_min
        pm_id = keywords['mid']
         
        db.insert(
                  SQL_TEMPLATES['INSERT']['ERI_BMS_STAT_INSERT_TEMPLATE'],
                  'pm_bms_sci_hour',
                  id + pm_id[-3:],
                  date_time,
                  value,
                  std,
                  max,
                  dt_max,
                  min,
                  dt_min,
                  pm_id
                  )
        
    