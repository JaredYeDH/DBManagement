# -*- coding: utf-8 -*-
'''
Created on 23 Oct, 2014

@author: wangyi
'''

from core.DAO.sqlParser import *

sql_insert_template = """
INSERT IGNORE INTO %s (`id`, `time`, `value`, `ubds`, `peakmax`, `peakmin`) VALUES (NULL, %(time)s, %(value)s, %(ubds)s, %(peakmax)s, %(peakmin)s)
        """     
sql_query_template ="""
SELECT timestamp_utc, %(tb_col)s
FROM %(db_table)s
WHERE global_MID = '%(global_MID)s' AND
    timestamp_utc >= %s AND timestamp_utc < %s
ORDER BY timestamp_utc ASC
        """        

if __name__ == '__main__':
    sqls = SQLparser(
                     sql_query_template, 
                     {'tb_col':'power_kw','db_table':'ntu_scada_hdata_mirror.ntu_scada_hdata_historic_mirror','global_MID':'M00000048A'}, 
                     100, 
                     200,
                     ).begin()
              
    for sql in sqls:
        print(sql)
        
    sqls = SQLparser(
                     sql_insert_template,
                     'shard#1',
                     [{'time':'2008-09-01 00:11:22', 'value':'101', 'ubds':'1000', 'peakmax':'2000', 'peakmin':'500'}, 
                      {'time':'2010-09-01 00:11:22', 'value':'303', 'ubds':'1000', 'peakmax':'1500', 'peakmin':'200'}],
                     ).begin()
              
    for sql in sqls:
        print(sql)   