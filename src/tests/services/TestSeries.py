# -*- coding: utf-8 -*-
'''
Created on 12 Nov, 2014

@author: wangyi
'''

from services.dao import DataRetriever, DataPusher

class TestSeries(object):
    
    def __init__(self):
        pass
    
    def test_pushSeries(self):
        from services.series import onTest_read_write_series
        
        dr = DataRetriever()
        
        dr.read_BSM_series_from_db(
                                   (2014, 5, 26), 
                                   (2014, 7, 28), 
                                   onTest_read_write_series
                                   )

if __name__ == "__main__":
    TestSeries().test_pushSeries()