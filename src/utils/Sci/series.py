# -*- coding: utf-8 -*-
'''
Created on 3 Nov, 2014

@author: wangyi
'''

from pandas import DataFrame, to_datetime
from core.Scheduler.delta import delta

## ---- Core Methods ----

class Node(object):
    
    def __init__(self, name, data):
        self.name = name
        self.data = data
        
        self.father = None
        self.children = list()
   
    def __str__(self):
        return str(self.data)
   
    def add_child(self, child):
        self.children.append(child)  
    
    def add_children(self, children):
        self.children = self.children.extend(children)
        
    def set_children(self, children):
        self.children = children
    
    def set_father(self, father):
        self.father = father
        father.childer.add_child(self)
        
    def get_children(self):
        for child in self.children:
            print(child)
        return self.children
    
    def get_father(self):
        return self.father

class SeriesNode(Node):
    
    class seriesIterator(object):
        def __init__(self, SeriesNode, start, end, delta):
            self.SeriesNode = SeriesNode
            self.counter = self.__counter__()
            self.start = start
            self.end = end
            self.delta = delta
            
        def __iter__(self):
            return self
        
        def __counter__(self):
            start = self.start
            end   = start + self.delta
            while True:
                if  start >= self.end:
                    break        
                yield (start, end)
                
                start = end
                end   = start + self.delta
        
        def __next__(self):
            try:
                start, end = next(self.counter)
                return (start, end, self.SeriesNode.data[start:end])
            except StopIteration as err:
                raise(err)
    
    def __init__(self, startdatetime, enddatetime, data, type='json'):
        if  type == 'json':
            self.raw = DataFrame(data)
            
            self.data = DataFrame(data  = self.raw['power_kw'].tolist(),
                                  columns = ['power_kw'],
                                  index = to_datetime( 
                                              self.raw['timestamp_utc'].astype(int),
                                              unit='s'
                                              ),
                          )            
        elif type == 'dataframe':
            self.data = data
        
        super(SeriesNode, self).__init__(startdatetime.strftime("%Y%m%d%H%M"), self.data)
            
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime
        self.treeIndex = {'monthly':[], 'weekly':[], 'dayly':[], 'daytime':[], 'nighttime':[], 'hourly':[]} 

    def __iter__(self):
        return self.seriesIterator(self, 
                                   self.startdatetime, 
                                   self.enddatetime, 
                                   self.span) 
               
    def setup(self):        
        self.treeIndex['monthly'].clear()
        self.treeIndex['weekly'].clear()
        self.treeIndex['dayly'].clear()
        self.treeIndex['daytime'].clear()
        self.treeIndex['nighttime'].clear() 
        
        self.id        = self.startdatetime.strftime("%Y%m%d%H%M")
        self.date_time = self.startdatetime
        
        return self
    
        # vertical grouping
    @staticmethod
    def up2down(child, self):
        raise NotImplementedError()
    
    # horizontal groupign
    @staticmethod
    def left2right(child, self):
        raise NotImplementedError() 
    
    def buildtree(self):
        raise NotImplementedError()
    
    def aggregate(self, obj, *callback, **keywords):
        it = self.__iter__()
        #elegant loop
        while True:
            try:
                # get data
                start, end, data = it.__next__()
                # create a child
                child = obj(start, end, data, 'dataframe', self.treeIndex)

                for call in callback:
                    call(self, 
                         child.setup()
                         )
                
            except StopIteration as err:
                break        
              
    def statistic(self):
        Peaks = {}        
        means = None
#       stds  = None #standard deviation
        ubds  = None #unbiased deviation
        
        columns = self.data.columns.values
        
        ids = [self.data[col].idxmax() for col in columns]
        Peaks['Max'] = [self.data.loc[ids[i]][col] for i, col in enumerate(columns)]#[self.raw.loc[ids[i]][col] for i, col in enumerate(columns)]
        Peaks['Max_Time'] = [self.data.loc[ids[i]].name for i, col in enumerate(columns)]#[self.raw.loc[ids[i]]['timestamp_utc'] for i, col in enumerate(columns)]

        ids = [self.data[col].idxmin() for col in columns]
        Peaks['Min'] = [self.data.loc[ids[i]][col] for i, col in enumerate(columns)]#[self.raw.loc[ids[i]][col] for i, col in enumerate(columns)]
        Peaks['Min_Time'] = [self.data.loc[ids[i]].name for i, col in enumerate(columns)]#[self.raw.loc[ids[i]]['timestamp_utc'] for i, col in enumerate(columns)]
        
        means = [self.data[column].mean() for column in columns]     
        ubds  = [self.data[column].std() for column in columns]
        
        param = {
                 'peaks':Peaks,
                 'means':means,
                 'ubds' :ubds,
                 }
        
        self.value = means[0]
        self.std = ubds[0]
        self.max = Peaks['Max'][0]
        self.min = Peaks['Min'][0]      
        self.dt_max = Peaks['Max_Time'][0]#datetime.utcfromtimestamp(Peaks['Max_Time'][0])
        self.dt_min = Peaks['Min_Time'][0]#datetime.utcfromtimestamp(Peaks['Min_Time'][0])
        
        return param        

## ---- Aggregation Nodes ----

class Month(SeriesNode):
    span = delta(weeks = 1)
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}):
        super(Month,self).__init__(startdatetime, enddatetime, data, type=type)
        
        if  treeIndex != {}:
            self.treeIndex = treeIndex  
        
    def __str__(self):
        return 'Month ' + self.id + ':'
    
    def buildtree(self):
        self.aggregate(Week, self.up2down, self.left2right)
        
        return self
    
    # vertical grouping
    @staticmethod
    def up2down(self, child):
        self.add_child(child)
        ## up2down
        child.statistic()
        child.buildtree()
    
    # horizontal groupign
    @staticmethod
    def left2right(child, self):
        self.treeIndex['weekly'].append(child)        

class Week(SeriesNode):
    span = delta(days=1)
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}): 
        super(Week, self).__init__(startdatetime, enddatetime, data, type=type)
        
        if  treeIndex != {}:
            self.treeIndex = treeIndex
        
    def __str__(self):
        return 'Week ' + self.id + ':' 
    
    def buildtree(self):
        self.aggregate(Day, self.up2down, self.left2right)
        
        return self    
    
    # vertical grouping
    @staticmethod
    def up2down(self, child):
        self.add_child(child)
        
        ## up2down
        child.statistic()
        child.buildtree()
    
    # horizontal groupign
    @staticmethod
    def left2right(child, self):
        self.treeIndex['dayly'].append(child)  
        
class Day(SeriesNode):
    span = delta(hours=1)
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}):
        super(Day, self).__init__(startdatetime, enddatetime, data, type=type) 
        
        if  treeIndex != {}:
            self.treeIndex = treeIndex
            
    def __str__(self):
        return 'Day' + self.id + ':'
    
    def buildtree(self):
        self.aggregate(Hour, self.up2down, self.left2right)
        
        return self 
    
    # vertical grouping
    @staticmethod
    def up2down(self, child):
        self.add_child(child)
        ## up2down
        child.statistic()
        ## uncomment the following line if it is not leaf ADS
        #child.buildtree()
    
    # horizontal groupign
    @staticmethod
    def left2right(child, self):
        self.treeIndex['hourly'].append(child)              

class Hour(SeriesNode):
    span = delta(hours=1)
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}):
        super(Hour, self).__init__(startdatetime, enddatetime, data, type=type) 
        
        if  treeIndex != {}:
            self.treeIndex = treeIndex

    def __str__(self):
        return 'Hour' + self.id + ':'
   
## event trigger function 
        
def onTest(start_date, end_date, series, *args, **keywords):
    print('series-tree test: begin')
    seriesnode = SeriesNode(start_date, end_date, series)
    # test set up
    seriesnode.setup()
    # test statistic
    print(
          str(
              seriesnode.statistic()
              )
          )
    # test build tree for month
    print('\t build hirarchical tree, begin ... ...')
    Month(start_date, end_date, series).setup().buildtree()#.get_children()
    print('\t buld hirarchical tree, end!')

    # test leaf confi
    Day(start_date, end_date, series).setup().buildtree().get_children()
    
    print('series-tree test: End')   