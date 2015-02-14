# -*- coding: utf-8 -*-
'''
Created on 23 Oct, 2014

@author: wangyi
'''

from core.DAO.Database import *

config = {
    'ERISA':{
        'host'    : "localhost",
        'user'    : "root",
        'passwd'  : "020139ERIyiak",
        'db'      : "ERI_Statistic_Analysis",
        'charset' : 'utf8',              
        },
    'ERIconfig2':{
        'host'    : '172.19.209.15',
        'port'    : '3306',
        'user'    : 'user_ntu_01',
        'passwd'  : 'ntu111',
        'db'      : 'ntu_scada_hdata_mirror',
        'charset' : 'utf8',
        },     
    }

sql_query_template ="""
SELECT timestamp_utc, %(tb_col)s
FROM %(db_table)s
WHERE global_MID = '%(global_MID)s' AND
    timestamp_utc >= %s AND timestamp_utc < %s
ORDER BY timestamp_utc ASC
        """ 

import time

if __name__ == '__main__':
#     db = DataBase(**config['ERIconfig2'])
#     
#     results = db.query(
#              sql_query_template,
#              {'tb_col':'power_kw','db_table':'ntu_scada_hdata_mirror.ntu_scada_hdata_historic_mirror','global_MID':'M00000048A'},
#              1400824799,
#              1400857199, 
#              )
#     
#     print(results)
    
    db = DataAdv(**config['ERIconfig2'])
    
    db.register(
                'query',
                sql_query_template,
                {'tb_col':'power_kw','db_table':'ntu_scada_hdata_mirror.ntu_scada_hdata_historic_mirror','global_MID':'M00000048A'},
                1400824799,
                1400857199, 
                )

    db.register(
                'query',
                sql_query_template,
                {'tb_col':'id','db_table':'ntu_scada_hdata_mirror.ntu_scada_hdata_historic_mirror','global_MID':'M00000048A'},
                1400824799,
                1400857199, 
                )
    
    db.register(
                'query',
                sql_query_template,
                {'tb_col':'id','db_table':'ntu_scada_hdata_mirror.ntu_scada_hdata_historic_mirror','global_MID':'M00000048A'},
                1400824799,
                1400857199, 
                )
    
    results = db.dispatch()
    
    print(len(results), results)
    
    