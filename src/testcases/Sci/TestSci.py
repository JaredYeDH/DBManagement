# -*- coding: utf-8 -*-
'''
Created on 3 Nov, 2014

@author: wangyi
'''
from services.dao import DataRetriever
from utils.Sci.series import onTest

if __name__ == '__main__':
    dr = DataRetriever()
    
    dr.read_BSM_series_from_db(
                   (2014, 5, 26), 
                   (2014, 7, 28), 
                   onTest,
                   ) 