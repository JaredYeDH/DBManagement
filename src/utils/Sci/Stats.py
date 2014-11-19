# -*- coding: utf-8 -*-
'''
Created on 30 Oct, 2014

@author: wangyi
'''
## neuro net work

def neuro_train(x, y, timeseries, name):
    import neurolab as nl
    import numpy as np
    
    size = len(x)
    
    inp = x.reshape(size,3)
    tar = y.reshape(size,1)
    
    # data preprocessing
    mean_tar = tar.mean(axis=0)[0]
    std_tar = tar.std(axis=0)[0]

    tar = (tar - mean_tar) / (2 * std_tar)
    
    inp2 = np.zeros(size)
    # add another feature
    for i, k in enumerate(x):
        inp2[i] = tar[i - 1][0] 
        
    inp2 = inp2.reshape(size,1)
    
    inp = np.concatenate((inp,inp2), axis=1)           
    
    # Create network with 3 layers
    net = nl.net.newff([[0, 24], [0, 31], [0, 6], [0, 1]],[10, 10, 1])
    # Train network
    error = net.train(inp, tar, epochs=500, show=100, goal=0.02)
    
    import os, stat
    cwd = os.getcwd() 
    sub_dir = cwd + '/training_models/neuro_network'
    #os.chmod(sub_dir, stat.S_IWRITE)
    filename = 'model_' + name
    #net.save( os.path.join(sub_dir, filename) )
    net.save( filename )

    # Plot result
    import pylab as pl
    pl.subplot(111)
    pl.plot(error)
    pl.xlabel('Epoch number')
    pl.ylabel('error (default SSE)')
    pl.show()
    
def neuro_validate(x, y, timeseries, name):
    import neurolab as nl
    import numpy as np
    
    size = len(x)
    
    inp = x.reshape(size,3)
    tar = y.reshape(size,1)
    
    # data preprocessing
    mean_tar = tar.mean(axis=0)[0]
    std_tar = tar.std(axis=0)[0]
    
    tar = (tar - mean_tar) / (2 * std_tar)
    
    # add another feature
    inp2 = np.zeros(size)
    # add another feature
    for i, k in enumerate(y):
        inp2[i] = tar[i - 1][0] 
        
    inp2 = inp2.reshape(size,1)
    
    inp = np.concatenate((inp,inp2), axis=1)  

    import os
    cwd = os.getcwd() 
    sub_dir = cwd + '/training_models/neuro_network'
    filename = 'model_' + name 
    #net = nl.load( os.path.join(sub_dir, filename) )
    net = nl.load(filename)
    
    # Simulate network
    out = net.sim(inp).reshape(size)
    
    out = out * 2 * std_tar + mean_tar
    
    # Plot result
    import pylab as pl
    
    pl.subplot(111)
    pl.plot(timeseries, y, '.-r', timeseries, out, 'p-b')
    pl.legend(['train target', 'net output'])
    pl.show()

def neuro_predict(x0, y0, y, name):
    import neurolab as nl 
    import numpy as np 
    
    size = len(y)
    
    inp = np.concatenate((x0, y0), axis=1)
    tar = y.reshape(size,1) 
    
    # data preprocessing
    mean_tar = tar.mean(axis=0)[0]
    std_tar = tar.std(axis=0)[0] 
 
    import os
    cwd = os.getcwd() 
    sub_dir = cwd + '/training_models/neuro_network'
    filename = 'model_' + name   
    #net = nl.load( os.path.join(sub_dir, filename) )
    net = nl.load(filename)
    
    out = net.sim(inp).reshape(size)
    
    out = out * 2 * std_tar + mean_tar
    
    return out
 
 
def onTest(start_date, end_date, series, *args, **keywords):
    from datetime import datetime
    # -- importing sci computation package --
    import pandas as R
    import numpy as M
    
    # data prepareation
    Y = []
    X = []
    timeseries = []
    for entry in series:
        param = datetime.utcfromtimestamp(entry['timestamp_utc'])
        
        Y.append(entry['power_kw'])
        X.append([
                  param.hour,
                  param.day,
                  param.weekday(),
                  ])
        timeseries.append(param)   
        
    # train models
    name = keywords['mid']
    
    x = M.array(X)
    y = M.array(Y)
    ## train model
    neuro_train(x, y, timeseries, name)
    ## validate model
    neuro_validate(x, y, timeseries, name) 
                       
    
    
            
