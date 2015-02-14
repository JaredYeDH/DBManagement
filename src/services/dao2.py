# -*- coding: utf-8 -*-
'''
Created on 17 Dec, 2014

@author: wangyi
'''
from core.DAO.Database import Database
from utils.jsonConfig import config, configx, SQL_TEMPLATES

import queue
message = queue.Queue()

import threading

counter = 0

class job(object):
    
    def __init__(self, *args, **hint):
        threading.Thread.__init__(self)
        
        self.args = args
        self.hint = hint
        
class reader(threading.Thread):
    
    def __init__(self):
        
        self.message = message
        self.counter = counter
        
    def get_meters(self, db):  
        ## get meters by id
        MIDs = db.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_MID_QUERY_TEMPLATE'])
        
        return MIDs
    
    def get_timerange(self, mid, table_name, db):
        sqltemplate = """
    
SELECT MAX(timestamp_utc), MIN(timestamp_utc), %(tb_col)s
FROM %(db_table)s
WHERE global_MID = '%(global_MID)s'
ORDER BY timestamp_utc ASC
"""
        ranges = db.query(sqltemplate,
                          {'tb_col':'power_kw','db_table':table_name,'global_MID':mid}#'ntu_scada_hdata_historic_mirror'
                          )
        
        return ranges
    
    def get_typ_week(self, mid, db):
        twpdtd = db.query(SQL_TEMPLATES['SELECT']['ict_typcial_week_template'], mid)     
        
        return twpdtd
    
    def get_series(self, start, end, mid, db):
        series = db.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_TIMESTAMPS_QUERY_TEMPLATE'],
                                {'tb_col':'power_kw','db_table':'ntu_scada_hdata_historic_mirror','global_MID':mid},
                                start,
                                end,
                                ) 
        
        return series 
    
    def push_data(self, start, end, mid, db1, db2):
        pass
    
    def update(self, callback=None):
        db_hdata = Database(**config['ERIconfig'])
        db_ict   = Database(db='ict_data_tran', **configx['ERIconfig'])        
        
        #get meters
        meters   = self.get_meters(db_hdata)
        
        ## set up querying range
        from datetime import date, datetime
        import calendar
        
        for entry in meters:
            mid = entry['global_MID']
            
            #get new data ranges
            old_range = self.get_timerange(mid, 'pm_hdata_clean', db_ict)
            new_range = self.get_timerange(mid, 'ntu_scada_hdata_historic_mirror', db_hdata)
            
            start_timestamp = datetime.fromtimestamp( new_range[0]['MIN(timestamp_utc)'] ) #date(2014, 5, 26)
            end_timestamp = datetime.fromtimestamp( new_range[0]['MAX(timestamp_utc)'] ) #date(2014, 7, 28)
            
            print(mid)
            print('old_range: ', old_range[0]['MIN(timestamp_utc)'], old_range[0]['MAX(timestamp_utc)'])
            print('new_range: ', start_timestamp, end_timestamp)
         
            ranges = {}
            
            ranges['MIN(timestamp_utc)'] = old_range[0]['MAX(timestamp_utc)'].timestamp()
            ranges['MAX(timestamp_utc)'] = new_range[0]['MAX(timestamp_utc)']
            
            twpdta = self.get_typ_week(mid, db_ict)
            
            series = self.get_series(ranges['MIN(timestamp_utc)'], 
                                     ranges['MAX(timestamp_utc)'], 
                                     mid, 
                                     db_hdata)
            
            self.counter += 1
            
            try:
                # callback routine
                # threading.Thread(target=callback, args=(ranges, twpdta, mid, self.message, job), name=mid + '_reader').start()
                callback(series, twpdta, mid, self.message, job)
                # for test purpose
                # break
            except Exception as inst:
                print(inst)
                
class writer(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.message = message
        self.counter = counter 
        
    def update(self, callback=None):
        db = Database(db = 'ict_data_tran', **configx['ERIconfig']) 
        
        while True:
            try:
                job  = self.message.get(block=True, timeout = 5)
    
                args = job.args
                hint = job.hint
                
                # data converter gateway
                callback(args, hint)
                
                #run db routine        
                db.insert(SQL_TEMPLATES['UPDATE']['ict_BMS_data_clean'],
                          *args,
                          **hint)
                print(self.name, args, hint)
                
                self.counter -= 1
                
                if  self.counter == 0:
                    break
                
            except queue.Empty:
                continue
        
    def run(self):
        
        self.updatedb()    
