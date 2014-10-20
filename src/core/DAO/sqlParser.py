# -*- coding: utf-8 -*-
'''
Created on 17 Oct, 2014

@author: wangyi
'''

import ast

## for testing
import re
import mysql.connector
from datetime import date, datetime
##

"""
considering the following situations, you can do understand my brief idea
>>> s
'{key:word}'
>>> s = "{'key':'word'}"
>>> ast.literal_eval(s)
{'key': 'word'}
>>> r = ast.literal_eval(s)
>>> r.__str__()
"{'key': 'word'}"
>>> 
"""

query_sql_temp = """
SELECT `dayly`.`id`,
    `dayly`.`time`,
    `dayly`.`value`,
    `dayly`.`ubds`,
    `dayly`.`peakmax`,
    `dayly`.`peakmin`
FROM `ERI_Statistic_Analysis`.`dayly`;    
    """

insert_sql_temp ="""
INSERT INTO %s (`id`, `time`, `value`, `ubds`, `peakmax`, `peakmin`) VALUES (NULL, %(time)s, %(value)s, %(ubds)s, %(peakmax)s, %(peakmin)s)
        """  

data_str = [{'time':'2008-09-01', 'value':'100', 'ubds':'1000', 'peakmax':'2000', 'peakmin':'500'}, {'time':'2008-09-01', 'value':'100', 'ubds':'1000', 'peakmax':'2000', 'peakmin':'500'}].__str__()

sql_clist = []

operate_stack = []
operant_queue = []

operant_dict = {}
operant_list = []

def load_data(data_str):
    # temp term
    key = ""
    word = ""    
    value = ""
    i = 0

    while True:
        try:
            while True:
                if   data_str[i] == ',':
                    i += 1
                    break
                elif data_str[i] == ':':
                    key = word
                    word = ""
                    i += 1
                elif data_str[i] == "'" or data_str[i] == ' ' or data_str[i] == "\t":
                    i += 1
                    continue
                elif True:
                    word += data_str[i]
                    i += 1
            
            if   key != "":
                value = word
                operant_dict[key] = value
            elif True:
                operant_list.append(word)
                
#            operant_stack.append(word)
            word = ""
        except IndexError as e:
            if   key != "":
                value = word
                operant_dict[key] = value
            elif True:
                operant_list.append(word)
                   
            break    

def stackloop(sign_in, sign_out, data_str):
    # counter
    i = 1
    
    # word
    words  = ''
    
    # no stack dismatch handling needed 
    while True:
        try:
            if   data_str[i] == sign_out:
                operate_stack.pop()
                
                if   operate_stack.__len__() != 0:
                    words += data_str[i]
                elif True:
                    break
            elif data_str[i] == sign_in:
                operate_stack.append(sign_in)
                
                words += data_str[i]
            elif True:
                words += data_str[i]
                
            i += 1
        except IndexError as e:
            break

    return i + 1, words    

# def stackProc(sql, words, data_str):
#     r_str_list = reversed(words)
#     new_str = "".join(r_str_list) + data_str
#     dataParser(sql, new_str)

def sqlParser(sql):        
    j = 0
     
    while True:
        try:
            if   sql[j] == '%' and sql[j + 1] == 's':
                pre = sql[:j]
                
                try:
                    value = operant_list.pop()
                except:
                    raise TypeError('not all arguments converted during string formatting')
                
                succ = sql[j + 2:]
                sql = pre + value + succ#operant_stack.pop() + succ
                
                j = j - 1 + value.__len__() + 1
                     
#                 if operant_list.__len__() == 0 and j < sql.__len__():
#                     raise TypeError('not all arguments converted during string formatting')
                
            elif sql[j] == '%' and sql[j + 1] == '(':
                pre = sql[:j]
                
                key = ""
                k = 2
                while sql[j + k] != ')':
                    key += sql[j + k]
                    k += 1
#               value = ("%(" + key + ")s") % ast.literal_eval( "{" + operant_stack.pop() + "}")
                try:
                    value = operant_dict.pop(key)
                except:
                    raise TypeError('not all arguments converted during string formatting')
                    
                succ = sql[j + k + 2:]
                sql = pre + value + succ
                
                j = j - 1 + value.__len__()  + 1    
                          
#                 if operant_dict.__len__() == 0 and j < sql.__len__():
#                     raise TypeError('not all arguments converted during string formatting')

            elif sql[j] == '{':
                pre = sql[:j]
                
                key = ""
                k = 1
                while sql[j + k] != '}':
                    key += sql[j + k]
                    k += 1
                    
                # To Do: produce value
                value = None
                                           
                succ = sql[j + k + 1:]
                sql = pre + value + succ
                j = j - 1 + value.__len__() + 1
                
            elif True:
                j = j + 1
            
        except IndexError as e:
            # since this layer just process one row data, so
            sql_clist.append(sql)
            break 
        except TypeError as e:
            e.sql = sql
            raise(e) 
# main loop
def dataParser(data_str, sql_str):
    try:
        if   data_str == '':
            pass   
        
        elif data_str[0] == '[':
            operate_stack.append('[')
            
            # To do get all data splited by ',' between '[ ]' into stack 
            # data inside '[ ]' could be nested, like '[[x,y],[r,s]]' , '[{x,y},{r,s},{}]' or '[(x,y), [r,s], {p,q}]'
            # one travel: after the first loop, words = '[x,y],[r,s]' | '{x,y},{r,s}'
            # two travel: words = 'x,y', data_str[index:] = '[r,s]'
            index, words = stackloop('[', ']', data_str)

#             # stack processing
#             stackProc(sql, words, data_str[index:])
            
            # load one row data: words = 'x,y'        
            dataParser(words, sql_str)
            dataParser(data_str[index:], sql_str)
                       
        elif data_str[0] == '{':
            operate_stack.append('{')

            # To do get all data splited by ',' between '{ }' into stack             
            index, words = stackloop('{', '}', data_str)
            
#             # stack processing
#             stackProc(sql, words, data_str[index:])
            
            dataParser(words, sql_str)
            dataParser(data_str[index:], sql_str)
        
        elif data_str[0] == ',' or data_str[0] == ' ' or data_str[0] == '\t':
            dataParser(data_str[1:], sql_str)
        
        elif True:
            load_data(data_str)
            sqlParser(sql_str)            
    except IndexError as e:
        pass
    except TypeError as e:
        raise(e)               

def sql_data_parser(sql_str, *args_str, **keywords):
    for data_str in args_str:
        try:
            dataParser(data_str, sql_str)
        except TypeError as e:
            sql_str = e.sql
        
        
class SQLparser(object):
    
    def __init__(self, sql_str, *args_str, **hint_str):
        self.args = args_str
        self.hints = hint_str
        self.slq_str = sql_str          
## old version sql parser, tend to deprecated in the next generaton of DB API, Lei Wang
## This version is developed based mysql-python connector API, and dramatically misleading

def sqlparser(self, sql, *args, **keywords):
    if  keywords != {}:
        value = []
        for k, v in keywords.items():
            pattern = re.compile('%\(' + k + '\)s')
            if   isinstance(v, date):
                v = v.strftime("%Y%m%d")
            elif isinstance(v, datetime):
                v = v.strftime("%Y%m%d")    
                
            elif True:
                v = str(v)
            value.append(v)
            sql = pattern.sub(v, sql, count = 1)
        try:    
            sql =  sql % args
        except TypeError as e: #suppose the user needs data, if that is wrong,
            if   e.__str__() == 'not enough arguments for format string': 
                print('Warning: you should transfer dic parameter into tuple or list---->')
                print("transfoming unordered dic into tuple or list prone errors ")
                newargs = [i for i in args] + value
                sql = self.sqlparser(sql, *newargs)
            elif e.__str__() == 'format requires a mapping':
                pattern = re.compile("%\((\w*)\)s")
                keys = re.findall(pattern, sql)
                newkeywords = dict(zip(keys, args))
                sql = self.sqlparser(sql, **newkeywords)
                                           
        return sql
    else:
        try:
            return sql % args
        except TypeError as e:
            # multiple rows intended:
            if   e.__str__() == 'format requires a mapping':
                
                if   isinstance(args[0], dict) or isinstance(args[0], list) or isinstance(args[0], tuple):
                    raise TypeError('not all arguments converted during string formatting')
                
                pattern = re.compile("%\((\w*)\)s")
                keys = re.findall(pattern, sql)
                
                if args.__len__() > keys.__len__():
                    raise TypeError('not all arguments converted during string formatting')
                
                newdict = {}
                for i, k in enumerate(keys):
                    newdict[k] = args[i]

                return self.sqlparser(sql, *args[i + 1 :], **newdict)
                sql = self.sqlparser(sql, **newkeywords)
            elif e.__str__() == 'not enough arguments for format string':
                raise(e)
            elif e.__str__() == 'not all arguments converted during string formatting':
                raise(e)
            
if __name__ == '__main__':
    sql_data_parser(insert_sql_temp, 'nihao', data_str)