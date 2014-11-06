# -*- coding: utf-8 -*-
'''
Created on 3 Nov, 2014

@author: wangyi
'''

from core.DAO.Database import Database
from utils.jsonConfig import config, SQL_TEMPLATES

class DataRetriever(object):
    
    def __init__(self):
        pass
    
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
                callback(datetime(*start_date), datetime(*end_date), series, mid=mid)
                # for test purpose
                # break
            except IndexError as err:
                print('ERROR!:', entry, ' series : ', series.__len__() )
                