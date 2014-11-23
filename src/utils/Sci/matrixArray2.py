# -*- coding: utf-8 -*-
'''
Created on 18 Sep, 2014

PyMatrix implementation based on pure python oop charisma

Description:

@author: wangyi
'''
from copy import *
from operator import *

def enhance(Func):
    def NewFunc(*args, **key):
        if   args[1] == "sign":
            return args[0] 
        elif args[1] == {'transpose'}:
            return args[0].transpose()
         
        elif True:    
            obj = Func(*args, **key)
            return obj
    return NewFunc

def Union(*Mats):
    
    def Union2Mat(Matl, Matr):
        
        if  isinstance(Matl, matrixArrayBase) and isinstance(Matr, matrixArrayBase):
            sizel = Matl.get_shape_array()
            sizer = Matr.get_shape_array()

            for i in range(0, max(sizel[0],sizer[0])):
                r = Matl[i]
                if   r != None:
                    # see documentation for difference between () and []
                    Matl(i,   Matr[i])
                    
                elif r == None:
                    # do assignment
                    Matl[i] = Matr[i]
    
    # create an empty matrix            
    mat = matrixArrayBase()
    
    # loop
    for obj in Mats:
        Union2Mat(mat, obj)
    
    return mat

def Intersection():
    pass

def rowTtf():
    pass

def colTtf():
    pass

class matrixArrayBase(list):
    '''
    Created on 17 Nov, 2014
    
    @author: wang yi/Lei, Researcher Associate @ EIRAN, Nanyang Technological University
    
    @email: L.WANG@ntu.edu.sg
    
    @copyright: 2014 www.yiak.co. All rights reserved.
    
    @license: license
    
    @decription: N-Matrix container for objects of any type. It then could be 2 or demensions numeric matrix for computation
    
    @param:
    '''
    def __init__(self, *args, **hint):   
        self.row = None
        self.col = None
        
        numberOfargs = len(args)
        if   numberOfargs == 0:
            if   hint == {}:
                pass
            # no element specified
            elif hint != {}:
                # set up empty matrix
                # no, row, col or dimensions
                super(matrixArrayBase, self).__init__()
             
        elif numberOfargs == 1:
            if   isinstance(args[0], int):
                # create square null matrix
                # just for 2-D cases
                # what is about 3-D?
                super(matrixArrayBase, self).__init__()
                # To do: specify n * n null matirx
            elif isinstance(args[0], list):
                # copy or convert
                super(matrixArrayBase, self).__init__(args[0])        
                 
        elif numberOfargs == 2:
            if   isinstance(args[0], int) and isinstance(args[1], int):
                super(matrixArrayBase, self).__init__()    
                # To do: specify m * n null matrix
                 
                 
            elif isinstance(args[0], int) and isinstance(args[1], list):
                super(matrixArrayBase, self).__init__()
                # To do: specify n * n null matrix
 
                 
        elif numberOfargs >= 3:
            for i in range( 0, len(args) ):
                if not isinstance(args[i], int):
                    break
 
            if  i == 0 and isinstance(args[  0  ], list):
                # To do: matrix cantenation
                super(matrixArrayBase, list).__init__()
                
                self = Union(*args) 
                                  
            if  i != 0 and isinstance(args[i + 1], list):
                # To do: specify 
                super(matrixArrayBase, list).__init__()
                self.fillUp(args[i+1:])

                     
        self.shape()
    
    class matrixIterator(object):
        def __init__(self, matrixArrayBase):
            self.matrixArray = matrixArrayBase
            self.counter = self.__counter__()
            
        def __iter__(self):
            return self

        ## ! just for two dimensions for the moment
        def __counter__(self):
            size = self.matrixArray.get_shape_array()

            tier = len(size)
            iter = tier * [0]
            
            while True:
                yield iter
                
                def routine(iter, size, curr):
                    iter[curr] += 1         
                    if  iter[curr] >= size[curr]:
                        if   curr == 0:
                            return 0
                        elif True:
                            iter[curr] = 0
                            return routine(iter, size, curr - 1)              
                    return 1
                     
                signal = routine(iter, size, tier - 1)
        
                if  signal == 0:
                    break
# compare to the old version you might find it much more universal ^ ^                
# the following codes just used for 2-demension matrix container        
#             i = 0
#             j = 0
#             while True:
#                 yield [i,j]
#                 j = j + 1
#                 if  j >= size['col']:
#                     j = 0
#                     i = i + 1
#                     if  i >= size['row']:
#                         break 
     
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
            
    def name(self):
        return "matrixArrayBase:"
    
    def shape(self):
        dems = self.get_shape_array()
        
        if len(dems) - 1 == 0:
            self.row  = 0
            self.col  = 0
            return {'row':self.row, 'col':self.col}
        if len(dems) - 1 == 1:
            self.row = dems[0]
            self.col = 1
            return {'row':self.row, 'col':self.col}
        if len(dems) - 1 == 2:
            self.row = dems[0]
            self.col = dems[1]
            return {'row':self.row, 'col':self.col}
        if len(dems) - 1 >= 3:
            self.row = dems[0]
            self.col = dems[1]
            return dems
    
    def __call__(self, key, value=None):
        if   value == None:
            return super(matrixArrayBase, self).__getitem__(key)
        elif value != None:
            self(key).extend(value)
            return self
        
    def __setitem__(self, key, value):   
        # currently set method doesn't support selector     
        if   isinstance(key, int):
            while True:
                try:
                    # old method
                    super(matrixArrayBase, self).__setitem__(key, value)
                    break  
                except Exception as inst:
                    print(inst)
                    self.append(None)
                
        elif isinstance(key, tuple) or isinstance(key, list):
            if   key.__len__() == 1:
                self[key[0]] = value
            elif key.__len__() == 2:  
                if  self.row == 1 and key[0] == 0:
                    self[key[1]] = value
                    return
                if  self.col == 1 and key[1] == 0:
                    self[key[0]] = value
                    return
                # get list
                while True:
                    try:
                        # old method
                        t = super(matrixArrayBase, self).__getitem__(key[0])
                        break
                    except IndexError as e:
                        print(e)
                        self.append(None)
                    
                if  t == None:
                    t  = []
                    super(matrixArrayBase, self).__setitem__(key[0], t)
                
                while True:
                    try:
                        t[key[1]] = value
                        break
                    except Exception as inst:
                        print(inst)
                        t.append(None)
#               self[key[0]][key[1]] = value              
            elif len(key) >= 3:
                l = len(key) 
                # iteration part
                i = 1
                
                while True:
                    try:
                        # old method
                        t = super(matrixArrayBase, self).__getitem__(key[0])
                        break
                    except IndexError as e:
                        print(e)
                        self.append(None)
                    
                if  t == None:
                    t  = []
                    super(matrixArrayBase, self).__setitem__(key[0], t)
                
                while i < l - 1:
                    while True:
                        try:
                            s = t
                            t = s[key[i]]
                            break
                        except IndexError as e:
                            print(e)
                            s.append(None)
                    
                    if  t == None:
                        t = []
                        s[key[i]] = t
                    
                    i += 1
                # get list
                while True:
                    try:
                        t[key[l-1]] = value
                        # do not need to process error
                        break
                    except Exception as inst:
                        print(inst)
                        t.append(None)
#               self[key[:l-1]][key[l-1]] = value
#               print(self)

        elif True:
            raise TypeError("index must be int or slice")
        
    def __getitem__(self, key):
        if   isinstance(key, int):
            try:
                result = super(matrixArrayBase, self).__getitem__(key)#how can we get sub matrixArray, i.e. mat is result : True
            except IndexError as e:
                print(e)
                return None
            if   isinstance(result, list):                
                return matrixArrayBase(result)# this method is bad
            elif True:
                return result
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            results = [ matrixArrayBase( self(i) ) for i in range(start, stop, step)] 

            return results
            
        elif isinstance(key, tuple) or isinstance(key, list) :
            if   key.__len__() == 0:
                return self
            elif key.__len__() == 1:
                return self[key[0]] # call user defined
            elif key.__len__() >= 2:
                try:
                    if   isinstance(key[0], int):
                        return self[key[0]][key[1:]]
                    elif isinstance(key[0], tuple) or isinstance(key[0], list):
                        # I would like to change it in the future to support logic vecotrs like matlab, honestly speaking this is the very cool characteristics in matlab
                        return self[key[0]][key[1:]]
                    elif isinstance(key[0], slice):
                        results = self[key[0]]
                        # in the future, I will change it to canecation matrix
                        results = [ Mat[key[1:]] for Mat in results]
                        return matrixArrayBase(results)
                except Exception as inst:
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
                    
                    # universial purpose
                    if  str(inst) == 'list index out of range':
                        return None
                    
            elif True:
                raise TypeError("index must be int or slice")
        
    def __setattr__(self, name, value):
        if   isinstance(name, tuple):
            pass
        elif True:
            self.__dict__[name] = value   
    
    def __iter__(self):
        return self.matrixIterator(self)
    
    def get_shape_array(self):
        queue = []
        dems = []
        axis= 0
        
        # updating current axis
        dems.append( self.__len__() )
        # updating axis 
        axis += 1
        
        # start processing
        queue.append( (self, axis) )
        # compute next demensions      
        def routines(obj, dems, axis, queue):
            while queue.__len__() > 0:
                obj, axis = queue.pop(0)
                # temporary storage
                tm = []
                
                if   isinstance(obj, list):
                    if   obj.__len__() == 0:
                        tm.append(0)
                    elif obj.__len__() >= 1:
                        # broadth first searching
                        for i in range(0, obj.__len__() ):
                            if   isinstance(obj[i], list):
                                tm.append( obj[i].__len__() )
                                # broadth first
                                queue.append( (obj[i], axis + 1) )
                            elif True:
                                tm.append( 1 )
                         
                        # updating current axis - Mat lenth
                        # axis control the looping layer        
                        try:
                            if  dems[axis] < max( tm ):
                                dems[axis] = max( tm )
                        except:
                            dems.append( max( tm ) )
                             
                elif True:
                    pass             
                      
        routines(self, dems, axis, queue)  
        
        return dems    
    
    def setUp(self, l=None):
        # clearn up
        self.clear()
        # set up container values
        self.extend(l)
        # modify shape accordingly

    def fillUp(self, *iterators):
        obj = self
        
        for itx in iterators:
            itl = obj.__iter__()
            itr = itx.__iter__()
            while True:
                try:
                    p = itl.nextIndex()
                    q = itr.__next__()
                    # use redefined method
                    obj[p] = q                  
                except StopIteration as e:
                    break 
        
        return self
    
    def nil(self, r, c):
        super(matrixArrayBase, self).clear()          
#       self.head = [None] * self.row
        if   r > 1:
            row = [None] * c
            
            for r in range(0, r):
#               self.head[r] = deepcopy(row)
                super(matrixArrayBase, self).append(deepcopy(row))
        elif r == 1:
            for i in range(0, c):
                self.append(None)  
                
    def Zeors(self):
        pass 
        
class matrixArray(matrixArrayBase):
    '''
    Created on 15 Nov, 2014
    
    @author: wangyi, Researcher Associate @ EIRAN, Nanyang Technological University
    
    @email: L.WANG@ntu.edu.sg
    
    @copyright: 2014 www.yiak.co. All rights reserved.
    
    @license: license
    
    @decription:
    
    @param: 
    '''
    
    def __init__(self, *args, **hint):
        '''
        Constructor
        '''
        super(matrixArray, self).__init__(*args, **hint)
        
        
#===============================================================================
# 2 - D Matrix Array Representation: 
#===============================================================================
    def __str__(self):
        size = self.get_shape_array()
        
        if  len(size) - 1 > 2:
            return super(matrixArray, self).__str__()
        
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

    @enhance
    def __add__(self, object):
        self.equal_size(object)
        return self.map(add, object)
    
    @enhance
    def __sub__(self, object):
        self.equal_size(object)
        return self.map(sub, object)
    
    @enhance
    def __mul__(self, object):
        self.tolerate(object)
        return self.dot(object)
    
    @enhance
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