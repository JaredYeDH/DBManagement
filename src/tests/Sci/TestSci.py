# -*- coding: utf-8 -*-
'''
Created on 3 Nov, 2014

@author: wangyi
'''
from services.dao import DataRetriever

class TestSci(object):
    
    def __init__(self):
        pass
    
    def test_stats(self):
        from utils.Sci.stats import onTest
        
        dr = DataRetriever()
        
        # test series
        dr.read_BSM_series_from_db(
                       (2014, 5, 26), 
                       (2014, 6, 2), 
                       onTest,
                       ) 
    
    def test_series(self):
        from utils.Sci.series import onTest
        
        dr = DataRetriever()
        
        # test series
        dr.read_BSM_series_from_db(
                       (2014, 5, 26), 
                       (2014, 7, 28), 
                       onTest,
                       )                
        

if __name__ == '__main__':
    # Test stats
    ##TestSci().test_stats()
    
    # Test series
    TestSci().test_series()