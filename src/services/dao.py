# -*- coding: utf-8 -*-
'''
Created on 3 Nov, 2014

@author: wangyi
'''

from core.DAO.Database import Database
from utils.jsonConfig import config, configx, SQL_TEMPLATES

import queue

message = queue.Queue()

class Task(object):
    
    def __init__(self, id, name, data = None, *args, **hint):
        self.id = id
        self.name = name
        self.data = data
        self.args = args
        self.hint = hint

class DataRetriever(object):
    
    def __init__(self):
        self.message = message
    
    
    def read_datetime_ranges_from_db(self, callback=None, *args, **keywords):
        db = Database(**config['ERIconfig'])
    
    ## get meters by id
        MIDs = db.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_MID_QUERY_TEMPLATE'])
        
    ## set up querying range 
        from datetime import date, datetime
        import calendar
              
        for entry in MIDs:
            mid = entry['global_MID']
            
            ranges = db.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_MID_FATCH_TEMPLATE'],
                              'ntu_scada_hdata_mirror.ntu_scada_hdata_historic_mirror',
                              mid
                              )
            max_datetime = datetime.fromtimestamp( max(ranges) )
            min_datetime = datetime.fromtimestamp( min(ranges) )
            
            callback(max_datetime, min_datetime, ranges, mid=mid, message=self.message, taskFac=Task  )


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
                callback(datetime(*start_date), datetime(*end_date), series, mid=mid, message=self.message, taskFac=Task)
                # for test purpose
                # break
            except IndexError as err:
                print('ERROR!:', entry, ' series : ', series.__len__() )
            except Exception as inst:
                print(inst)


class DataPusher(object):
    
    def __init__(self):
        self.message = message
         
    def write_BMS_analysis_2_db(self, callback = None, *args, **keywords):
        while True:
            try:
                task = self.message.get(block=False)
                
                id   = task.id
                name = task.name
                data = task.data
                args = task.args
                hint = task.hint
                
                # data converter gateway
                callback(id, name, data, args, hint)
                
            except queue.Empty:
                break