# -*- coding: utf-8 -*-
'''
Created on 19 Nov, 2014

@author: wangyi
'''

from services.dao import DataRetriever, DataPusher

class TestDataFixer(object):
    '''
    Created on 19 Nov, 2014
    
    @author: wangyi, Researcher Associate @ EIRAN, Nanyang Technological University
    
    @email: L.WANG@ntu.edu.sg
    
    @copyright: 2014 www.yiak.co. All rights reserved.
    
    @license: license
    
    @param: 
    
    @decription:
    
    @param: 
    '''

    def __init__(self):
        pass
    
    def test_fixdata_by_typical_week(self):
        from services.FillingData import onTestPull, onTestPush
        
        dr = DataRetriever()
        
        dr.read_datetime_ranges_from_db( onTestPull )
    
        dp = DataPusher()
        
        dp.write_ict_missdata_2_db( onTestPush )
    
if  __name__ == "__main__":
    TestDataFixer().test_fixdata_by_typical_week()