# -*- coding: utf-8 -*-
'''
Created on 17 Nov, 2014

@author: wangyi
'''

class TestMatBase(object):
    
    def __init__(self):
        pass

    def test_NMat_iterator(self):
        pass
    
    def test_list2Mat(self):
        from utils.Sci.matrixArray2 import matrixArrayBase
        
        pass
    
    def test_NMatirx(self):
        from utils.Sci.matrixArray import matrixArray
        
        a = matrixArray(3, 1, [1, 2, 3, 4])
        
        print(a)
        
    def test_get_shape_array(self):
        from utils.Sci.matrixArray2 import matrixArrayBase
        
        b = matrixArrayBase(
                            [
                             [[1,2], [3, 4], [5, 6]], 
                             [[11, 22, 33], [33, 44, 44, 55, 66], [55, 66]], 
                             [[111, 222], [333, 444], [555, 666]]
                            ]
                            )
        
        print(b)
        
        c = b.get_shape_array()
        
        print(c)
        
    def test_iteration_1(self):
        from utils.Sci.matrixArray2 import matrixArrayBase
        
        b = matrixArrayBase(
                            [
                             [[1,2], [3, 4], [5, 6]], 
                             [[11, 22, 33], [33, 44, 44, 55, 66], [55, 66]], 
                             [[111, 222], [333, 444], [555, 666]]
                            ]
                            )
        
                
        it = b.__iter__()
        
        while True:
            try:
                p = it.nextIndex()
                print(p)
            except StopIteration as e:
                break
    
    def test_set_data(self):
        from utils.Sci.matrixArray2 import matrixArrayBase
        
        b = matrixArrayBase(
                            [
                             [[1,2], [3, 4], [5, 6]], 
                             [[11, 22, 33], [33, 44, 44, 55, 66], [55, 66]], 
                             [[111, 222], [333, 444], [555, 666]]
                            ]
                            )  
        print(b[0,0,3]) 
             
        b[0,0,3] = 100
        
        print(b[0,0,3])
        print(b)        
    
    def test_get_data(self):
        from utils.Sci.matrixArray2 import matrixArrayBase
        
        b = matrixArrayBase(
                            [
                             [[1,2], [3, 4], [5, 6]], 
                             [[11, 22, 33], [33, 44, 44, 55, 66], [55, 66]], 
                             [[111, 222], [333, 444], [555, 666]]
                            ]
                            )       
        
        print(b[0,0,3])
            
    def test_iteration_2(self):
        from utils.Sci.matrixArray2 import matrixArrayBase
        
        b = matrixArrayBase(
                            [
                             [[1,2], [3, 4], [5, 6]], 
                             [[11, 22, 33], [33, 44, 44, 55, 66], [55, 66]], 
                             [[111, 222], [333, 444], [555, 666]]
                            ]
                            )
        for e in b:
            print(e)        
            
    def test_selector_get_data(self):
        from utils.Sci.matrixArray2 import matrixArrayBase
        
        b = matrixArrayBase(
                            [
                             [[1,2], [3, 4], [5, 6]], 
                             [[11, 22, 33], [33, 44, 44, 55, 66], [55, 66]], 
                             [[111, 222], [333, 444], [555, 666]]
                            ]
                            )
        
        print(b[1:, 0, 0])    
        
    def test_selector_set_data(self):
        pass    

if __name__ == "__main__":
    TestMatBase().test_set_data()