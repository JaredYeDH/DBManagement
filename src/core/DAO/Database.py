# -*- coding: utf-8 -*-
'''
Created on 20 Oct, 2014

@author: wangyi
'''
# -- sys --
import contextlib
import queue
import re
import sys
import threading

import mysql.connector

# -- master - slaves architecture --
# --third party--
# --local dependency--
#from core.DAO.Log.LogManagement import logManager
#from core.utils.timmer import timmer, delta

from core.DAO.sqlParser import SQLparser

__author__ = "Wang Yi/Lei"
__credits__= "all active authors in StackExchange, whom I learn a lot from"

# The prototype maintain global connector within an instance of the class life time
# As a part of data oriented work, data migration or converted from different servers are fairly frequent
# MySQL connector maintains a threads pool by default to create multiple connectors to a same database simutaneously  
class Database_Prototype(object):
    # default local machine DB config
    host     = "localhost"
    user     = "root"
    passwd   = ""
    db       = "ERI_Statistic_Analysis"
  
    # these mapping is used for general database querying, updating purpose, and should not be binded to models layer
    sqlMapping = {
        'alter' : {
            'create' : None,
            'insert' : None,
            'alter'  : None,
            'delete' : None,
        },
        'query' : {
            '_?_table' : """
SELECT * FROM INFORMATION_SCHEMA.TABLES
WHERE table_schema = '%s' AND
    table_name = '%s'             
            """,
            
        }
                   
    }
    
    def __init__(self, **config): 
# following method discarded, might be consider a universe initial method:
        
        # connection should lie in object domain, or simply put for enduring connection 
        if config == {}:     
            self.connection=mysql.connector.connect(host=self.host,  
                                            user=self.user,  
                                            passwd=self.passwd,  
                                            db=self.db,
                                            charset='utf8'
                    )
        else:
            self.connection=mysql.connector.connect(**config)

            self.db     = config['db']
            self.host   = config['host']
            self.user   = config['user']
            self.passwd = config['passwd']
            self.charset= config['charset']
            
            self.cursor = False
            
    def set_connector(self):
        
        raise NotImplementedError()
        
    def set_cursor(self):
        
        raise NotImplementedError()
    
    # cursor should lie in method domain
    # should consider transaction situations
    @contextlib.contextmanager
    def Cursor(self):
        # setup
        if  self.cursor_status == False:
            self.cursor = self.connection.cursor()
            self.cursor_status = True
        # teardown
        try:
            yield
        except mysql.connector.Error as err:
            print(err)
            self.connection.rollback()
            self.cursor.close()
            self.cursor = None
            self.cursor_status = False
        finally:
            self.corsor.close()
            self.cursor = None
            self.cursor_status = False  
    # This method can be safe
    def __del__(self):
        if self.connection:
#           print('\tdb deleted\t')
            self.connection.close()   
            

# the basic database is used for querying or non-transaction based database interacting
# the database alwasy returns Json style data in python             
class Database_Basic(Database_Prototype): 
    
    def __init__(self, **config):
        super(Database_Basic, self).__init__(**config)
        
        self._output = queue.Queue()
        
    def basic(self, sql_str, callback, *args, **hint):
        
        sqls = SQLparser(sql_str, 
                         *args, 
                         **hint
                         ).begin()
        
        with self.Cursor():
            for sql in sqls:
                callback(sql)
                
    def onQuery(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.json(results)
    
    def onAlter(self, sql):
        self.cursor.execute(sql)

## -- interface for user --    
    def query(self, sql, *args, **hint):
        
        self.basic(sql, self.onQuery, *args, **hint)

        list = []
        while True:
            try:
                list.append( self._output.get() )
            except queue.Empty:
                break
            
        return list            
    
    def insert(self, sql, *args, **hint):
        if hint != {}:
            sql_query_table = self.sqlMapping['query']['_?_table']
            
            status = self.query(sql_query_table, hint['table'], hint['db'])
                
            if not status:
                self.onAlter(hint['create'], hint['table'])    
         
        self.basic(sql, self.onAlter, *args, **hint)       

#-- datatype mapping function--
    
    def json(self,results):
        list = []
        for row in results:
            dict = {} 
            field = 0
            while True:
                try:
                    colname = self.cursor.description[field][0]
                    try:
                        dict[colname] = row[field].__unicode__()
                    except:
                        dict[colname] = row[field]
                    field = field +1
                except IndexError as e:
                    break
            list.append(dict)
        self._output.put(list)               

                 
class Database_Adv_Task_Loop(Database_Basic, threading.Thread):

    def __init__(self, **config):
        Database_Basic.__init__(self, **config)
        threading.Thread.__init__(self)
        
        self._info = queue.Queue()
        self._input = queue.Queue()
        self._output = queue.Queue()        
        self._subjobs = queue.Queue() 

        self.stoprequest = threading.Event()
        self.conlock = threading.Condition()
        
        self.input_status = True
        
        self.daemon()
        self.start()
    
    def register(self, task_str, sql_str, *args, **hint):
        if  self.input_status == True:
            self._info.put( Task(task_str) )
               
            sqls = SQLparser(
                             sql_str, 
                             *args, 
                             **hint
                             ).begin()
            
            for sql in sqls:
                self._input.put(sql)        
    
    def fetchall(self):
        
        while not self._subjobs.empty():
            job = self._subjobs.get()
            job.join()
            
        if  self.input_status == False:
            self.input_status = True
            return None
        
        list = []
        while not self._output.empty():
            results = self._output.get() 
            list.append(results)
            
        return list
        
        
    def run(self):
        
        while True:
            try:
                task = self._info.get(True, 0.5)
                
                with self.Cursor():
                    try:
                        self.taskCheck(task)
                    except mysql.connector.Error as err:
                        self.input_status = False
                        raise(err)
                    
            except queue.Empty:
                continue
    
    def taskCheck(self, task):
        if   task.name == 'mysqlerror':
            print(task.error)
            raise(task.error)
        elif task.name == 'insert': # insert, update, create
            self._subjobs.put( DBjob(
                                    self.conlock,
                                    self._info,
                                    self._input,
                                    self._output,
                                    self.onAlter,
                                     )
                                )
        elif task.name == 'query': # select
            self._subjobs.put( DBjob(
                                     self.conlock,
                                     self._info,
                                     self._input,
                                     self._output,
                                     self.onQuery,
                                     )
                                )
                     
class Task(object):
    
    def __init__(self, name, data=None, error=None):
        self.name = name
        self.data = data
        self.error= error 
 
        
class DBjob(threading.Thread):

    def __init__(self, conlock, _info, _input, _output, sql_job_exec = None):
        super(DBjob, self).__init__()
        
        self.info = _info
        self.input = _input
        self.output = _output
        self.conlock = conlock  
          
        self.sql_job_exec = sql_job_exec
        self.stoprequest = threading.Event()
    
        self.daemon = True
        self.start()
    
    def run(self): 
        while not self.stoprequest.isSet():
            try:
                args = self.input.get(True, 0.05)
                print(self.name + ':' + 'get a job, preprocessing')
                self.sql_job_exec(args)
                print(self.name + ':' + 'finished a job, idle')
            except queue.Empty:
                continue
            except mysql.connector.Error as err:
                self.info.put( Task('mysqlerror', error=err) )
                err.__str__()
                break
    
    def join(self):
        self.stoprequest.set()
        super(DBjob, self).join()      

Database = Database_Adv_Task_Loop        
