# -*- coding: utf-8 -*-
'''
Created on 28 Oct, 2014

@author: wangyi
'''

config = {
    'ERIconfig':{
        'host'    : '172.19.209.15',
        'port'    : '3306',
        'user'    : 'root',
        'passwd'  : 'whying123',
        'db'      : 'ntu_scada_hdata_mirror',
        'charset' : 'utf8'
        },    
    }

# CONFIG SQLs Here

SQL_TEMPLATES = {
    'CREATE':{
    'ERI_STATISTIC_CREATE_TEMPLAE' : """   
CREATE TABLE `%s` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `means` double DEFAULT NULL,
  `ubds` double DEFAULT NULL,
  `peakmax` double DEFAULT NULL,
  `peakmin` double DEFAULT NULL,
  `meter_id` varchar(45) DEFAULT NULL,  
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=latin1;   
""",       
    },
    'INSERT':{
    'ERI_STATISTIC_INSERT_TEMPLATE' :"""
INSERT IGNORE INTO %s (`id`, `time`, `value`, `ubds`, `peakmax`, `peakmin`) VALUES (NULL, %(time)s, %(means)s, %(ubds)s, %(peakmax)s, %(peakmin)s, `%(meter_id)s`)
""",
    },
    'SELECT':{
    'BMS_SCANDA_MID_QUERY_TEMPLATE' :"""
SELECT DISTINCT global_MID FROM ntu_scada_hdata_historic_mirror order by global_MID desc;        
""",
    'BMS_SCANDA_TIMESTAMPS_QUERY_TEMPLATE':"""
SELECT timestamp_utc, %(tb_col)s
FROM %(db_table)s
WHERE global_MID = '%(global_MID)s' AND
    timestamp_utc >= %s AND timestamp_utc < %s
ORDER BY timestamp_utc ASC
""",
    },
               
}
