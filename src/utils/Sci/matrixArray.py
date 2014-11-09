# -*- coding: utf-8 -*-
'''
Created on 18 Sep, 2014

PyMatrix implementation based on pure python oop charisma

Description:

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

        ## ! just for two dimensions now
        def __counter__(self):
            size = self.matrixArray.shape()
            
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
        elif True:
            pass
        
        
    def __str__(self):
        str = self.name() + '\n' 
        str = str + "["
        str = str + '{:1s}'.format(' ')
        
        # column vector
        if  self.col == 1:
            for i in range(0, self.row):
                try:
                    str = str + '{:<.2f} '.format(self[i])
                except TypeError as e:
                    str = str + '{:s}'.format('null ')
                
                if  i + 1 < self.row:
                    str = str + "\n  "
        # row vector
        elif self.row == 1:
            for j in range(0, self.col - 1):
                try:
                    str = str + '{:<10.2f}'.format(self[j])
                except TypeError as e:
                    str = str + '{:<10s}'.format('null')
            try:
                str = str + '{:<.2f}'.format(self[self.col - 1])
            except TypeError as e:
                str = str + '{:s}'.format('null')
            str = str + '{:1s}'.format(' ')
        # matrix
        elif True:        
            for i in range(0, self.row):
                for j in range(0, self.col):
                    
                    if   j + 1 < self.col:
                        try:
                            str = str + '{:<10.2f}'.format(self[i][j])#.format(super(matrixArray, self).__getitem__(i).__getitem__(j))
                        except TypeError as e:
                            if  e.__str__() == 'non-empty format string passed to object.__format__':
                                str = str + '{:10s}'.format('null')
                    elif True:
                        try:
                            str = str + '{:<.2f}'.format(self[i][j])#.format(super(matrixArray, self).__getitem__(i).__getitem__(j))
                            str = str + ' '
                        except TypeError as e:
                            if  e.__str__() == 'non-empty format string passed to object.__format__':
                                str = str + '{:s}'.format('null') 
                                str = str + ' '                                   
                    
                if i + 1 < self.row:
                    str = str + '\n'
                    str = str + '{:1s}'.format('  ')
                    
        str = str + "]"
        return str
    
    def name(self):
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
        if   isinstance(key, tuple) or isinstance(key, list):
            if   key.__len__() == 1:
                super(matrixArray, self).__setitem__(key[0], value)
            elif key.__len__() == 2:
                if self.row == 1 and key[0] == 0:
                    super(matrixArray, self).__setitem__(key[1], value)
                    return
                if self.col == 1 and key[1] == 0:
                    super(matrixArray, self).__setitem__(key[0], value)
                    return
                              
                super(matrixArray, self).__getitem__(key[0]).__setitem__(key[1], value)#this method should not use this strategy#self[key[0]][key[1:]] = value #this function will call __getitem__() recursively

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
        elif isinstance(key, tuple) or isinstance(key, list):
            if   key.__len__() == 0:
                pass
            elif key.__len__() == 1:
                return self[key[0]] # call user defined
            elif True:
                try:
                    return self[key[0]][key[1:]]
                except:
                    # if column vector
                    if  self.col == 1:
                        flag = 1
                        for item in key[1:]:
                            if item != 0:
                                flag = 0
                                raise( TypeError("wrong index") )
                        if  flag == 1:
                            return self[key[0]]
                        
                    # if row vector
                    if  self.row == 1:
                        flag = 1
                        for item in key[:key.__len__()-1 ]:
                            if item != 0:
                                flag = 0
                                raise( TypeError("wrong index") )
                        if flag == 1:
                            return self[key[key.__len__()-1]]
        
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
        return {'row':self.row, 'col':self.col}#(self.row, self.col)

## for operation
    def equal_size(self, object):
        sizel = self.shape()
        sizer = object.shape()
        
        if sizel['row'] != sizer['row']:
            raise( TypeError('matrix size unmatched') )
        if sizel['col'] != sizer['col']:
            raise( TypeError('matrix size unmatched') )

    def __neg__(self):
        return self.map(neg)

    @callNext
    def __add__(self, object):
        self.equal_size(object)
        return self.map(add, object)
    
    @callNext
    def __sub__(self, object):
        self.equal_size(object)
        return self.map(sub, object)
    
    def __mul__(self, object):
        self.tolerate(object)
        return self.dot(object)
    
    @callNext
    def __gt__(self,  object):
        pass

## just for 2-D matrix 
## for linear algebra
    def transpose(self):
        mat = matrixArray(self.col, self.row) 
        
        for i in range(mat.row):
            for j in range(mat.col):
                mat[i,j] = self[j,i]
                
        return mat
    
    # test wether two matrix can tolerate each other
    def tolerate(self, object):
        sizel = self.shape()
        sizer = object.shape()
        
        if  sizel['col'] == sizer['row']:
            return
        raise( TypeError("matrix does not tolerate to the object!") )
    
    def dot(self, object):
        self.tolerate(object)
        
        mat = matrixArray(self.row, object.col)
        
        for i in range(mat.row):
            for j in range(mat.col):
                sum = 0.0
                for k in range(self.col):
                    sum += self[i,k] * object[k,j]
                mat[i,j] = sum
                
        return mat
        
            
## just for 2-D matirx            
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
    print('\n\n**-**-**normal matrix initialization testing**-**-**\n\n')
    mat = matrixArray(2,4)
    print('\t matrixArray(2,4)\n', mat)
    
    c = matrixArray(1,4)
    print('\t row vector matrixArray(1,4)\n', c)
    d = matrixArray(4,1)
    print('\t col vector matrixArray(4,1)\n', d)

    print('\n\n**-**-**normal vector set value/get value testing**-**-**\n\n')
    c[1] = 100
    print(c[1])
    d[1] = 101
    print(d[1])
    
    c[0, 1] = 200
    print('c[1]: ', c[1])
    print('c[0, 0, 0, 1]: ', c[0, 0, 0, 1])
    
    d[1, 0] = 201
    print('d[1]: ', d[1])
    print('d[1, 0, 0, 0]: ', d[1, 0, 0, 0])
    
    print('\n\n**-**-**normal matrix reset testing**-**-**\n\n')
    mat([1,2,3,4,10,12])
    print('\t mat after reset: mat([1,2,3,4,10,12]\n', mat)
    
    print('\n\n**-**-**normal vector set value/get value testing**-**-**\n\n')
    print('\t mat Transpose, mat-x>{T}\n', mat-x>{T})
    
    print('\n\n**-**-**R style new matirx initialization testing**-**-**\n\n')
    a = matrixArray(3, 1, [1, 2, 3])
    print('\t matrixArray(3, 1, [1, 2, 3])\n', a)
    b = matrixArray(2, 3, [1, 2, 3, 4, 5, 6])
    print('\t matrixArray(2, 3, [1, 2, 3, 4, 5, 6])\n', b)
    
    
    print('\n\n**-**-**numric matirx basic operation**-**-**\n\n')
    print('\t a + b\n', a + a)
    
    print('\t a - a\n', a - a)
    
    print('\t -a \n', - a)
    
    print('\t b * a: 2 * 3 matrix multiply 3 * 1 vector or matrix \n', b * a )
    
    pass
    
