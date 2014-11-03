# -*- coding: utf-8 -*-
'''
Created on 29 Oct, 2014

@author: wangyi
'''
from core.DAO.Database import Database
from utils.jsonConfig import config, SQL_TEMPLATES
from utils.Sci.Stats import neuro_train, neuro_train_validation

# -- improting date utils
from dateutil.relativedelta import relativedelta
# -- importing sci computation package --
import pandas as R
import numpy as matrixarray

class SeriesNode(object):
    
    def __init__(self, name, series_data):
        self.name = name
        self.series_data = series_data
        
        self.father = None
        self.children = list()
   
    def add_child(self, seriesnode):
        self.children.append(seriesnode)  
    
    def add_children(self, seriesnodes):
        self.children = seriesnodes
    
    def set_father(self, father):
        self.father = father
        father.childer.add_child(self)       

class SeriesTree(object):
    
    def __init__(self, json, start, end):
        
        # this line might be deprecated in the future
        self.raw = R.DataFrame(data = json)
    
        # transform data into inner series
        self.data = R.DataFrame(data  = self.raw['power_kw'].tolist(),
                                 columns = ['power_kw'],
                                 index = R.to_datetime( 
                                                         self.raw['timestamp_utc'].astype(int),
                                                         unit='s'
                                                         ), 
                                ) 
        self.start = start
        self.end = end
        
        self.tree = {} 
        self.node_queue = []   
    
    def toMatrix(self):
        return self.data.as_matrix()
    
    def aggregate(self, start, end, delta, data, lable):
        self.tree[lable] = []
        # set up querying range
        s = start    
        while s < end:
            e = s + delta 
            subdf = data[s:e]#subdf = data.loc[(data.loc['timestamp_utc'] >= s) & (data.loc['timestamp_utc'] < e)] 
            seriesnode = SeriesNode(lable + str(start), subdf)
            self.tree[lable].append(seriesnode)
            s = e
        
    def build_tree(self):
        self.tree['root'] = SeriesNode('root', None)
        
        self.aggregate(self.start, self.end, relativedelta(weeks = 1), self.data, 'week')
        self.aggregate(self.start, self.end, relativedelta(hours = 24), self.data, 'day')
            
        
    def __str__(self):
        return str(self.data)  

class DataRetriever(object):
    
    def __init__(self):
        pass
    
    @staticmethod
    def main(start_date, end_date, callback = None):
        db = Database(**config['ERIconfig'])
        
    ##  get meters by id    
        MIDs = db.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_MID_QUERY_TEMPLATE'])
        
        for entry in MIDs:
            print(entry)
    ## set up querying range
        from datetime import date, datetime
        import calendar
    
        start_timestamp = calendar.timegm( date(*start_date).timetuple() ) #date(2014, 5, 26)
        end_timestamp = calendar.timegm( date(*end_date).timetuple() ) #date(2014, 7, 28)
    
    ##  retrieve data from database 
        for entry in MIDs:
            mid = entry['global_MID']
             
            series = db.query(SQL_TEMPLATES['SELECT']['BMS_SCANDA_TIMESTAMPS_QUERY_TEMPLATE'], 
                              {'tb_col':'power_kw','db_table':'ntu_scada_hdata_historic_mirror','global_MID':mid},
                              start_timestamp,
                              end_timestamp,
                              )
            try: 
                print( mid, series.__len__(), series[series.__len__() - 1]['timestamp_utc'], end_timestamp)
                # To do Sci Computation
                print(series)
                
                X = []
                timeseries = []
                i = 0
                for entry in series:
                    param = datetime.utcfromtimestamp(entry['timestamp_utc'])
                    
                    X.append([
                              param.hour,
                              param.day,
                              param.weekday(),
                              ])
                    timeseries.append(param)
                    i = i + 1
                    
                    if i > 24 * 7:
                        break                    
                
                
                
                
                Y = []
                j = 0
                for entry in series:     
                    Y.append(entry['power_kw'])
                    j = j + 1
                    
                    if j > 24 * 7:
                        break
                   
                print(matrixarray.array(X).shape, matrixarray.array(Y).shape)
                    
#                neuro_train(matrixarray.array(X), matrixarray.array(Y), timeseries)
                neuro_train_validation(matrixarray.array(X), matrixarray.array(Y), timeseries)
                #test(matrixarray.array(X), matrixarray.array(Y), timeseries)    
                             
            except IndexError as err:
                print('ERROR!:', entry, ' series : ', series.__len__() )
                from core.DAO.sqlParser import SQLparser
                sqls = SQLparser(SQL_TEMPLATES['SELECT']['BMS_SCANDA_TIMESTAMPS_QUERY_TEMPLATE'], 
                                 {'tb_col':'power_kw','db_table':'ntu_scada_hdata_historic_mirror','global_MID':mid},
                                 start_timestamp,
                                 end_timestamp,
                                 ).begin()
                for sql in sqls:
                    print(sql) 
                    
                raise(err)

def test(x,y, timeseries):
    import neurolab as nl
    import numpy as np
    
    size = len(x)
    
    inp = x.reshape(size,3)
    tar = y.reshape(size,1)
    
    # data preprocessing
    mean_tar = tar.mean(axis=0)[0]
    std_tar = tar.std(axis=0)[0]

    tar = (tar - mean_tar) / (2 * std_tar)
    
    # Create network with 3 layers
    net = nl.net.newff([[0, 24], [0, 31], [0, 6]],[10, 10, 1])
    # Train network
    error = net.train(inp, tar, epochs=500, show=100, goal=0.02)
    
    # Simulate network
    out = net.sim(inp).reshape(size)
    
    out = out * 2 * std_tar + mean_tar
    
    # Plot result
    import pylab as pl
    pl.subplot(211)
    pl.plot(error)
    pl.xlabel('Epoch number')
    pl.ylabel('error (default SSE)')
    
    pl.subplot(212)
    pl.plot(timeseries, y, '.-r', timeseries, out, 'p-b')
    pl.legend(['train target', 'net output'])
    pl.show()


if __name__ == '__main__':
    DataRetriever.main( (2014, 5, 26), (2014, 7, 28) )