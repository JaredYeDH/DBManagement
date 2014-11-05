# -*- coding: utf-8 -*-
'''
Created on 28 Oct, 2014

@author: wangyi
'''
from dateutil.relativedelta import relativedelta

class delta(relativedelta):
    
    def __init__(self, **key):
        super(delta, self).__init__(**key)
        
    def __radd__(self, other):
        if   self.months > 0:
            other = other + relativedelta(
                                          days = - other.day + 1,
                                          hours = - other.hour,
                                          minutes =- other.minute,
                                          seconds =- other.second
                                          )
        
        elif self.days >= 7:
            other = other + relativedelta(
                                          days= - other.weekday(),
                                          hours = - other.hour,
                                          minutes =- other.minute,
                                          seconds =- other.second
                                          )
        elif self.days > 0:
            other = other + relativedelta(
                                          hours = -other.hour,
                                          minutes =- other.minute,
                                          seconds =- other.second
                                          )
            
        return self.__add__(other)
        
if __name__ == "__main__":
    from datetime import datetime
    
    start = datetime(2014, 7, 10) + delta(months = 1) 
    
    print(start)    
        