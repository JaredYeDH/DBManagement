# -*- coding: utf-8 -*-
from pandas import DataFrame, to_datetime, concat

weekday = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}

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

    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def push(self, args):
        self.fixedData = args[1]
        
        print( DataFrame(self.fixedData) )
        
        pass    
        
    def pull(self, data, sample, mid, message, job):
        self.mid     = mid
        self.message = message
        self.job     = job
        ## initialization
        ## set data      
        self.data = DataFrame(data)
        ## set sample
        self.sample = DataFrame(sample)
        ## set index
        self.data.set_index('timestamp_utc', inplace=True)
        self.sample.set_index(['hour','weekday'], inplace=True)
        ## verbose
        self.data.index = to_datetime(self.data.index.astype(int), unit='s')
        # find the trend
        self.Draw()
        # get the missing data
        self.find_positions_of_missing_data(0.000000001, self.getDelta() )
        
        # fix data
        self.fixData()
        # push job back
        self.message.put( self.job(
                                  self.mid,
                                  self.fixedData,
                                  ) )

    
    def getDelta(self):
        from dateutil.relativedelta import relativedelta
        return relativedelta(hours=1)
    
    def fixData(self):
        fixedData = []
        
        for index, row in self.missdata.iterrows():
            id   = to_datetime(row[0])
            
            hour = id.hour
            wkdn = id.weekday()
            wkds = weekday[wkdn]
            
            data = self.sample.xs((hour,wkds), level=('hour','weekday'))['power_kw'].values[0]
            
            print('mod data:', data)
            print('ori data:', row[1])
            
            fixedData.append({'tt':str(id), 'pwk':data})
        
        self.fixedData = fixedData
    
    def find_positions_of_missing_data(self, epilon, delta):
        missdata = []
        testdata = []
        
        pre  = 0
        curr = 0
        for index, row in self.data.diff().iterrows():
            curr= 0
            if  row['power_kw'] <= epilon and row['power_kw'] >= -epilon:                
                missdata.append( [self.data.loc[index].name, self.data.loc[index]['power_kw']] )
                
                curr = 1
                
                if  pre == 0 and curr == 1:
                    testdata.append( [self.data.loc[index - delta].name, self.data.loc[index - delta]['power_kw']] )
            pre = curr     
                    
        self.missdata = DataFrame(missdata)
        self.testdata = DataFrame(testdata)    
    
        print( 'miss:\n', DataFrame(missdata) )
        print( 'pre:\n', DataFrame(testdata) )
        
    def Draw(self, Recursive=True):
        import matplotlib.pyplot as plt

        self.sample.plot(style='g-o')
        
        filename = self.mid + '_tyw_' + '.pdf'
        plt.savefig(filename)

        ## here draw
        filename = self.mid + '_origin_' + '.pdf'
        self.data.plot(style='g-o')
        plt.savefig(filename)
        
        filename = self.mid + '_diff_' + '.pdf'
        self.data.diff().plot(style='r-*')
        plt.savefig(filename)
        ## just save the pictures   
        #  plt.show()

def onTestPull(data, sample, mid, message, job):
    dataFixer().pull(data, sample, mid, message, job)
    
def onTestPush(args, hint): 
    dataFixer().push(args)
     
    hint['auto_debug'] = False
    hint['multi'] = True    