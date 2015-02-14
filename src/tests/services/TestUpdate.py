# -*- coding: utf-8 -*-
'''
Created on 17 Dec, 2014

@author: wangyi
'''

from services.dao2 import reader, writer

class TestUpdate(object):
    
    def __init__(self):
        pass
    
    def test_update(self):
        from services.FillingData import onTestPull, onTestPush
        
        reader().update(onTestPull)
        
        writer().update(onTestPush)
        
        


if __name__ == "__main__":
    TestUpdate().test_update()