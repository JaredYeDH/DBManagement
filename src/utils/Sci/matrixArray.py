# -*- coding: utf-8 -*-
'''
Created on 18 Sep, 2014

PyMatrix implementation based on pure python oop charisma

@author: wangyi
'''
from copy import *
from operator import *

def callNext(Func):
    def NewFunc(*args, **key):
        if   args[1] == "sign":
            return args[0] 
        elif args[1] == {'transpose'}:
            return args[0].transpose()
         
        elif True:    
            obj = Func(*args, **key)
            return obj
    return NewFunc

class matrixArray(list):
    '''
    classdocs
    '''          
    class matrixIterator(object):
        def __init__(self, matrixArray):
            self.matrixArray = matrixArray
            self.counter = self.__counter__()
            
        def __iter__(self):
            return self

        def __counter__(self):
            size = self.matrixArray.shap()
            
            i = 0
            j = 0
            while True:
                yield [i,j]
                j = j + 1
                if   j >= size['col']:
                    j = 0
                    i = i + 1
                    if i >= size['row']:
                        break 
     
        def __next__(self):
            try:
                index = next(self.counter)
                return self.matrixArray[index]
            except StopIteration as e:
                raise StopIteration()   
    
        def nextIndex(self):
            try:
                index = next(self.counter)
                return index
            except StopIteration as e:
                raise StopIteration()             
    
    def __init__(self, *args):
        '''
        Constructor
        '''
#       super(matrixArray, self).__init__()
        
        self.row = None
        self.col = None
         
        if   args != None:
    
            numberOfargs = len(args)
            if   numberOfargs == 0:
                super(matrixArray, self).__init__()            
                self.row = 0
                self.col = 0
            elif numberOfargs == 1:           
                if   isinstance(args[0], list):
                    # if list is a py matirx
                    super(matrixArray, self).__init__()
                    self.list2Matrix(args[0])                  
                elif True:
                    self.col = self.r = args[0]
                    super(matrixArray, self).__init__() 
                    self.nullNMatrix()        
            elif numberOfargs == 2:
                self.row = args[0]
                self.col = args[1]
                super(matrixArray, self).__init__()                
                self.nullNMatrix()              
            elif True:
                self.row = args[0]
                self.col = args[1]
                self.nullNMatrix()
                
                it = self.__iter__()
                it2= args[2].__iter__()
                while True:
                    try:
                        p = it.nextIndex()
                        q = it2.__next__()
                        self[p] = q                  
                    except StopIteration as e:
                        break
                
                print('?')                                      
        elif True:
            pass
        
        
    def __str__(self):
        print(self.__name__())
        str = "["
        str = str + '{:1s}'.format(' ')
        
        # column vector
        if   self.col == 1:
            for i in range(0, self.row):
                str = str + '{:<.2f} '.format(self[i])
                
                if i + 1 < self.row:
                    str = str + "\n  "
        # row vector
        elif self.row == 1:
            for j in range(0, self.col - 1):
                str = str + '{:<10.2f}'.format(self[j])
            str = str + '{:<.2f}'.format(self.col - 1)
            str = str + '{:1s}'.format(' ')
        # matrix
        elif True:        
            for i in range(0, self.row):
                for j in range(0, self.col):
                    
                    if   j + 1 < self.col:
                        try:
                            str = str + '{:<10.2f}'.format(self[i][j])#.format(super(matrixArray, self).__getitem__(i).__getitem__(j))
                        except TypeError as e:
                            if   e.__str__() == 'non-empty format string passed to object.__format__':
                                str = str + '{:10s}'.format('null')
                    elif True:
                        try:
                            str = str + '{:<.2f}'.format(self[i][j])#.format(super(matrixArray, self).__getitem__(i).__getitem__(j))
                            str = str + ' '
                        except TypeError as e:
                            if   e.__str__() == 'non-empty format string passed to object.__format__':
                                str = str + '{:s}'.format('null') 
                                str = str + ' '                                   
                    
                if i + 1 < self.row:
                    str = str + '\n'
                    str = str + '{:1s}'.format('  ')
                    
        str = str + "]"
        return str
    
    def __name__(self):
        return "matrixArray:"
    
#   @ConstructorAssign
#   @matrixArray.__setitem__
    def __call__(self, l):
        if   isinstance(l, list):#return self[rid][cid]#super(matrixArray, self).__getitem__(rid).__getitem__(cid)   
            self.clear()
            return self.list2Matrix(l)
        elif isinstance(l, tuple):
            self.clear()
            return self.list2Matrix(l)
            pass
        
    def __setitem__(self, key, value):
        
        print("call set item", key)
        if   isinstance(key, tuple):
            if   key.__len__() == 1:
                super(matrixArray, self).__setitem__(key[0], value)
            elif key.__len__() == 2:
                try:               
                    super(matrixArray, self).__getitem__(key[0]).__setitem__(key[1], value)#this method should not use this strategy#self[key[0]][key[1:]] = value #this function will call __getitem__() recursively
                except:
                    if  key[0] == 0:
                        super(matrixArray, self).__setitem__(key[1], value)
            elif True:
                len = key.__len__()
                
                i = 1
                t = super(matrixArray, self).__getitem__(key[0])
                while i < len - 1:
                    t = t[key[i]]
                t.__setitem__(key[len-1], value)
                 
        elif isinstance(key, int):
            super(matrixArray, self).__setitem__(key, value)
        
    def __getitem__(self, key):
        if   isinstance(key, int):
            result = super(matrixArray, self).__getitem__(key)#how can we get sub matrixArray, i.e. mat is result : True
            if   isinstance(result, list):                
                return matrixArray(result)# this method is bad
            elif True:
                return result
        elif isinstance(key, tuple):
            if   key.__len__() == 0:
                pass
            elif key.__len__() == 1:
                return self[key[0]] # call user defined
            elif True:
                try:
                    return self[key[0]][key[1:]]
                except:
                    flag = 1
                    for item in key[1:]:
                        if item != 0:
                            flag = 0
                            break
                    if  flag == 1:
                        return self[key[0]]
        elif isinstance(key, list):
            if   key.__len__() == 0:
                pass
            elif key.__len__() == 1:
                return self[key[0]]
            elif True:
                return self[key[0]][key[1:]]
                
        
    def __setattr__(self, name, value):
        if   isinstance(name, tuple):
            pass
        elif True:
            self.__dict__[name] = value   
    
    def __iter__(self):
        return self.matrixIterator(self)
    
 ## initialization       
    def list2Matrix2(self, list):    
        # Assume list is a two dimensional matrix
        # by default we deem a one dimensional list as a column vector
        row = list.__len__()
        col = [None] * row
        
        for r in range(0, row):
            try:
                col[r] = list[r].__len__()
            except AttributeError as e:
                col[r] = 1
        if   max(col) == min(col):
            self.row = row
            self.col = min(col)
             
        elif True:
            self.row = row
            self.col = max(col)                
        
                
# This function is element wise referenced not list wise referenced, hence deprecated    
    def list2Matrix(self, list):
        # Assume list is a two dimensional matrix
        # by default we deem a one dimensional list as a column vector
        row = list.__len__()
        col = [None] * row
        
        for r in range(0, row):
            try:
                col[r] = list[r].__len__()
                self.append([])
                for c in range(0,col[r]):
                    self[r].append(list[r][c])#self[r][c] = list[r][c]
                    
            except AttributeError as e:
                col[r] = 1
                self.append(list[r])      
            
        if   max(col) == min(col):
            self.row = row
            self.col = min(col)
             
        elif True:
            self.row = row
            self.col = max(col)
              
            #To Do: fill empty elements
                   
    def nullNMatrix(self):
        super(matrixArray, self).clear()          
#       self.head = [None] * self.row
        if   self.row > 1:
            row = [None] * self.col
            
            for r in range(0, self.row):
    #           self.head[r] = deepcopy(row)
                super(matrixArray, self).append(deepcopy(row))
        elif self.row == 1:
            for i in range(0, self.col):
                self.append(None)  
    
    def shape(self):
        return (self.row, self.col)

## for operation
    def __add__(self, object):
        pass
    @callNext
    def __sub__(self, object):
        pass
    @callNext
    def __gt__(self,  object):
        pass
 
## for linear algebra
    def transpose(self):
        mat = matrixArray(self.col, self.row) 
        
        for i in range(mat.row):
            for j in range(mat.col):
                mat[i,j] = self[j,i]
                
        return mat
            
            
## for computation
##    
    def map(self, Func, *iterables):
        mapobject = map(Func, self, *iterables)
        
        return matrixArray(self.row, self.col, [m for m in mapobject])
    
    @staticmethod
    def main():
        pass

# MATRIXDILIMITERPATTER = "\[ (\n  )* \]"
# MATRIXOBJECTPATTER    = "(format(number)*number)*"

x = 'sign'
_x_ = x

T = 'transpose'
_T_ = T

if __name__ == '__main__':
    mat = matrixArray(2,4)
    
#     l = [1,2,3]
#     list2matrixArray(l)
#     print(mat)
    
#     mat = matrixArray(5,2)
#     print(mat)
#  
#     mat(1,1)
#     
#     mat[0,1] = 500
#     
#     mat[0,1]
#  
#     print(mat)
    
    mat([1,2,3,4,10,12])
    
    t = 1
    print(mat)

    mat[0,0]
    
    print(mat-x>{T})
    
    a = matrixArray(3, 1, [1, 2, 3])
    b = matrixArray(3, 1, [1, 2, 3])
    
    pass
    
