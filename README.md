Objective
---------
This Project is developed for purpose of easy interacting with DB as a part data oriented work, which is fully immersive in industry envrionment. 

Layout
------

    src->
        core->
            DAO->
                sqlparser.py 

This version is a powerful substitution for old sql template parser, which was developed as sql template lexical parsing tool under the influence of mysql-python-connector. Native Mysql-Python-Connector by MySQL is not elegent for string substitution, hence I decided to write my own. It is a little like PHP style. But the philosophy is different! I consider it as an alternitive to Object Relationship Mapping (ORM) like Django 'Model' in python or Hybernate framework in Java

    src->
        core->
            DAO->
                Database.py
This file defined master-slave database model to handle users' data connection with database.

    src->
        core->
            Scheduler->
                delta.py
This is aimed as an extention to the 'dateutils.relativedelta'. The 'delta' class is a subclass of relativedelta exclusively for series analysis routine

    src->                    
        utils->
            Sci->
                matrixArray.py
naive implementation for N-Dimension matrix Container. The mothod used for this implementation is dramatically different from 'numpy'. It is purely based on beautiful python syntax and programmed in pythonic manners. No C++ libs needed and hence accorss platforms. It is aimed to be a naive algebra tool easy to use like Octave or Matlab in python according to my own customer experience!

    src->
        utils->
            Sci->
                series.py
naive tool for series data Aggregation and horizontal and vertical tree building. It is easy to interacte with database and report statistic information. Explore test module and service module(pending to publish for RESTful API framework)

Methodology
-----------
1. sql template lexical parser : Finite Sates Machine
2. database : basic event-loop and master-slaves architecture. Database shards system is just another wrap upon this model, which is very easy to use.


Userful Sci Tool Test
---------------------

###normal matrix initialization testing###

#####matrixArray(2,4)#####
    matrixArray:

    [ null      null      null      null 
      null      null      null      null ]
#####row vector matrixArray(1,4)#####

    matrixArray:

    [ null      null      null      null ]
#####col vector matrixArray(4,1)#####
    
    matrixArray:

    [ null 
      null 
      null 
      null ]

###normal vector set value/get value testing###
c[1] = 100, c = [1, 2, 3, 4]
c[0, 0, 0, 1] = 200
d[1] = 101, d = [1, 2, 3, 4]
d[1, 0, 0, 0] = 201

    100
    101
    c[1]:  200
    c[0, 0, 0, 1]:  200
    d[1]:  201
    d[1, 0, 0, 0]:  201

###normal matrix reset testing###

#####mat after reset: mat([1,2,3,4,10,12]#####

    matrixArray:
    [ 1.00 
      2.00 
      3.00 
      4.00 
      10.00 
      12.00 ]

###normal vector set value/get value testing###

#####mat Transpose#####

    matrixArray:

    [ 1.00      2.00      3.00      4.00      10.00     12.00 ]

###R style new matirx initialization testing###

#####matrixArray(3, 1, [1, 2, 3])#####

    matrixArray:

    [ 1.00 
      2.00 
      3.00 ]
#####matrixArray(2, 3, [1, 2, 3, 4, 5, 6])#####

    matrixArray:

    [ 1.00      2.00      3.00 
      4.00      5.00      6.00 ]

###numric matirx basic operation###

#####matrix add#####

    a + b
    matrixArray:
    [ 2.00 
      4.00 
      6.00 ]

#####matirx minus#####

    a - a
    matrixArray:
    [ 0.00 
      0.00 
      0.00 ]

#####matrix negtive##### 

    -a 
    matrixArray:
    [ -1.00 
      -2.00 
      -3.00 ]

#####matrix multiply#####

    b * a: 2 * 3 matrix multiply 3 * 1 vector or matrix 
    matrixArray:
    [ 14.00 
      32.00 ]
