# -*- coding: utf-8 -*-
'''
Created on 30 Oct, 2014

@author: wangyi
'''
def neuro_train(x, y, timeseries, name):
    import neurolab as nl
    import numpy as np
    
    size = len(x)
    
    inp = x.reshape(size,3)
    tar = y.reshape(size,1)
    
    # data preprocessing
    mean_tar = tar.mean(axis=0)[0]
    std_tar = tar.std(axis=0)[0]

    tar = (tar - mean_tar) / (1.5 * std_tar)
    
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
    net.save('model_' + name)

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
    
    tar = (tar - mean_tar) / (1.5 * std_tar)
    
    # add another feature
    inp2 = np.zeros(size)
    # add another feature
    for i, k in enumerate(y):
        inp2[i] = tar[i - 1][0] 
        
    inp2 = inp2.reshape(size,1)
    
    inp = np.concatenate((inp,inp2), axis=1)  
    
    net = nl.load('model' + name)
    # Simulate network
    out = net.sim(inp).reshape(size)
    
    out = out * 1.5 * std_tar + mean_tar
    
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
    
    net = nl.load('model' + name)
    
    out = net.sim(inp).reshape(size)
    
    out = out * 1.5 * std_tar + mean_tar
    
    return out
        
