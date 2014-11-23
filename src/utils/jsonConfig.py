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

configx= {
    'ERIconfig':{
        'host'    : '172.19.209.15',
        'port'    : '3306',
        'user'    : 'root',
        'passwd'  : 'whying123',
        'charset' : 'utf8'
        },
    }

# CONFIG SQLs Here

SQL_TEMPLATES = {
## -- create -- ##
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

    'ERI_BMS_STA_TYPICAL_WEEK_TEMPLATE': """
    
CREATE TABLE `pm_hdada_typ_week` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start` datetime DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  `weekday` varchar(45) DEFAULT NULL,
  `hour` int(11) DEFAULT NULL,
  `power_kw` double DEFAULT NULL,
  `pm_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `start_end_uni` (`start`,`end`)
) ENGINE=InnoDB AUTO_INCREMENT=1513 DEFAULT CHARSET=utf8;    
"""       
    },
                 
## -- insert -- ##                 
    'INSERT':{
              
    'ERI_STATISTIC_INSERT_TEMPLATE' :"""
    
INSERT IGNORE INTO %s (`id`, `time`, `value`, `ubds`, `peakmax`, `peakmin`) VALUES (NULL, %(time)s, %(means)s, %(ubds)s, %(peakmax)s, %(peakmin)s, '%(meter_id)s')
""",

    'ERI_BMS_TYPICAL_WEEK':"""
    
INSERT IGNORE INTO `ict_data_tran`.`pm_hdada_typ_week`
(`start`,`end`, `pm_id`,`weekday`, `id`, `hour`,`power_kw`) VALUES (
'%(start)s', '%(end)s', '%(pm_id)s', '%(weekday)s', '%(idx)s',  %(hour)s, %(power_kw)s)
""",# %s 1: start, %s 2: end, %s 3: pm_id, %s 4: weekday

    'ERI_BMS_STAT_INSERT_TEMPLATE' :"""
    
INSERT IGNORE INTO `ict_data_tran`.`%s`
(`id`, `date_time`, `value`, `std`, `max`, `dt_max`, `min`, `dt_min`, `pm_id`, `remark`)
VALUES ( '%(id)s', '%(date_time)s', %(value)s, %(std)s, %(max)s, '%(dt_max)s', %(min)s, '%(dt_min)s', '%(pm_id)s', NULL);    
"""
    }, # %s : pm_bms_sci_hour
 
## -- seclect -- ##                 
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

    'BMS_SCANDA_TIMESTAMPS_FETCH_TEMPLATE':"""
    
SELECT timestamp_utc, %(tb_col)s
FROM %(db_table)s
WHERE global_MID = '%(global_MID)s'
ORDER BY timestamp_utc ASC
""",

    'ict_typcial_week_template':"""
SELECT * FROM ict_data_tran.pm_hdada_typ_week
WHERE pm_id = '%s';    
"""
    },


## -- update --##
    'UPDATE':{
              
    'ict_BMS_data_clean':"""

SET SQL_SAFE_UPDATES=0;
UPDATE `ict_data_tran`.`pm_hdata_tpy_clean`
SET
`power_kw` = %(pwk)s,
`remarks` = 'modified'
WHERE 
`timestamp_utc` = TIMESTAMP('%(tt)s', '09:00:00') AND
`global_MID` = '%s';  
"""          
              }               
}
