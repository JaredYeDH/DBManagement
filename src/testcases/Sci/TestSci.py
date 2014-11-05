# -*- coding: utf-8 -*-
'''
Created on 3 Nov, 2014

@author: wangyi
'''
from services.dao import DataRetriever
from utils.Sci.series import onTrigger

if __name__ == '__main__':
    dr = DataRetriever()
    
    dr.write_to_db(
                   (2014, 5, 26), 
                   (2014, 7, 28), 
                   onTrigger,
                   ) 