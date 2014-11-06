Objective
---------
This Project is developed for purpose of easy interacting with DB as a part data oriented work, which is fully immersive in industry envrionment. 

Layout
------

src->
    core->
        DAO->
            sqlparser.py 
Pending to be changed in the future, and will be wrapped in Class name space for ease of use

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
