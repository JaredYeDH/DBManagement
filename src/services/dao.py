# -*- coding: utf-8 -*-
'''
Created on 3 Nov, 2014

@author: wangyi
'''

from core.DAO.Database import Database
from utils.jsonConfig import config, configx, SQL_TEMPLATES

import queue

message = queue.Queue()

class job(object):
    
    def __init__(self, *args, **hint):
        
        self.args = args
        self.hint = hint

class DataRetriever(object):
    
    def __init__(self):
        self.message = message
    
    
    def read_typical_week_from_db(self, mid):
        db = Database(db = 'ict_data_tran', **configx['ERIconfig'])
        
        tpw = db.query(SQL_TEMPLATES['SELECT']['ict_typcial_week_template'],
                 mid)
        
        return tpw
  
    
    def read_meter_from_db(self):
        db = Database(**config['ERIconfig'])
        
        MIDs = db.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_MID_QUERY_TEMPLATE'])
        
        return MIDs
        

    def read_datetime_ranges_from_db(self, callback=None):
        db_hdata = Database(**config['ERIconfig'])
        db_ict   = Database(db='ict_data_tran', **configx['ERIconfig'])
    
    ## get meters by id
        MIDs = db_hdata.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_MID_QUERY_TEMPLATE'])
        
    ## set up querying range 
        from datetime import date, datetime
        import calendar
              
        for entry in MIDs:
            mid = entry['global_MID']
            
            ranges = db_hdata.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_TIMESTAMPS_FETCH_TEMPLATE'],
                                    {'tb_col':'power_kw','db_table':'ntu_scada_hdata_historic_mirror','global_MID':mid}
                                    )
        
            twpdta = db_ict.query(SQL_TEMPLATES['SELECT']['ict_typcial_week_template'], mid)
            
            try:
                # callback routine
                callback(ranges, twpdta, mid, self.message, job)
                # for test purpose
                # break
            except Exception as inst:
                print(inst)


    def read_BSM_series_from_db(self, start_date, end_date, callback = None, *args, **keywords):
        db = Database(**config['ERIconfig'])
        
    ##  get meters by id    
        MIDs = db.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_MID_QUERY_TEMPLATE'])
        
        for entry in MIDs:
            print(entry)
    ## set up querying range
        from datetime import date, datetime
        import calendar
    
        start_timestamp = calendar.timegm( date(*start_date).timetuple() ) #date(2014, 5, 26)
        end_timestamp = calendar.timegm( date(*end_date).timetuple() ) #date(2014, 7, 28)
    
    ##  retrieve data from database 
        for entry in MIDs:
            mid = entry['global_MID']
             
            series = db.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_TIMESTAMPS_QUERY_TEMPLATE'], 
                              {'tb_col':'power_kw','db_table':'ntu_scada_hdata_historic_mirror','global_MID':mid},
                              start_timestamp,
                              end_timestamp,
                              )
            try:
                # Call back routines
                callback(datetime(*start_date), datetime(*end_date), series, mid, self.message, job)
                # for test purpose
                # break
            except IndexError as err:
                print('ERROR!:', entry, ' series : ', series.__len__() )
            except Exception as inst:
                print(inst)


class DataPusher(object):
    
    def __init__(self):
        self.message = message
         
    def write_BMS_analysis_2_db(self, callback = None):
        db = Database(db = 'ict_data_tran', **configx['ERIconfig']) 
        
        while True:
            try:
                # get task
                job  = self.message.get(block=False)
                
                args = job.args
                hint = job.hint
                
                # data converter gateway
                callback(args, hint)
                
                # run db routine
                db.insert(SQL_TEMPLATES['INSERT']['ERI_BMS_TYPICAL_WEEK'],
                          *args,
                          **hint
                          )
            except queue.Empty:
                break
            
    def write_ict_missdata_2_db(self, callback = None):
        db = Database(db = 'ict_data_tran', **configx['ERIconfig']) 
        while True:
            try:
                job  = self.message.get(block=False)

                args = job.args
                hint = job.hint
                
                # data converter gateway
                callback(args, hint)
                
                # run db routine        
                db.insert(SQL_TEMPLATES['UPDATE']['ict_BMS_data_clean'],
                          *args,
                          **hint)
                         
            except queue.Empty:
                break