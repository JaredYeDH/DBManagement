# -*- coding: utf-8 -*-
'''
Created on 10 Nov, 2014

@author: wangyi
'''

from services.dao import DataRetriever, DataPusher

class TestTW(object):
    
    def __init__(self):
        pass
    
    def test_getTypicalWeek(self):
        from services.typicalWeek import onTest_read
        
        dr = DataRetriever()
        
        # test get_typcial_weekday
        dr.read_BSM_series_from_db(
                                   (2014, 5, 26), 
                                   (2014, 7, 28), 
                                   onTest_read
                                   )
    def test_writeTypicalWeek(self):
        from services.typicalWeek import onTest_read, onTest_write
        
        dr = DataRetriever()
        
        # test get_typcial_weekday
        dr.read_BSM_series_from_db(
                                   (2014, 5, 26), 
                                   (2014, 7, 28), 
                                   onTest_read
                                   )
        
        dp = DataPusher()
        
        # test write_typical_weekday
        dp.write_BMS_analysis_2_db(onTest_write)
    
        
if __name__ == "__main__":
    TestTW().test_writeTypicalWeek()
        
        