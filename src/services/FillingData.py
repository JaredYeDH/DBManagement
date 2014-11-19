# -*- coding: utf-8 -*-
from pandas import DataFrame, to_datetime

class dataFixer(object):
    '''
    Created on 19 Nov, 2014
    
    @author: wangyi, Researcher Associate @ EIRAN, Nanyang Technological University
    
    @email: L.WANG@ntu.edu.sg
    
    @copyright: 2014 www.yiak.co. All rights reserved.
    
    @license: license
    
    @decription:
    
    @param: 
    '''

    def __init__(self, start_datetime, end_datetime, data, *args, **hint):
        '''
        Constructor
        '''
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        
        ## initialization       
        self.data = DataFrame(data)
        ## set index
        self.data.set_index('timestamp_utc', inplace=True)
        ## verbose
        self.data.index = to_datetime(self.data.index.astype(int), unit='s')