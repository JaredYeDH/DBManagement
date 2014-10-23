# -*- coding: utf-8 -*-
'''
Created on 17 Oct, 2014

@author: wangyi
'''
class SQLparser(object):
    
    def __init__(self, sql_str, *args_str, **hint_str):
        self.args = args_str
        self.hint  = hint_str
        self.sql_str = sql_str
                
        self.operate_stack = []
        self.operant_queue = []
        self.sql_clist  = []
        self.backup  = []
        
        self.operant_dict = {}
        self.operant_list = []
        
    def load_data(self, data_str):
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
                    self.operant_dict[key] = value
                elif True:
                    self.operant_list.append(word)
    
                word = ""
            except IndexError as e:
                if   key != "":
                    value = word
                    self.operant_dict[key] = value
                elif True:
                    self.operant_list.append(word)
                       
                break    

    def stackloop(self, sign_in, sign_out, data_str):
        # counter
        i = 1
        
        # word
        words  = ''
        
        # no stack dismatch handling needed 
        while True:
            try:
                if   data_str[i] == sign_out:
                    self.operate_stack.pop()
                    if   self.operate_stack.__len__() != 0:
                        words += data_str[i]
                    elif True:
                        break
                elif data_str[i] == sign_in:
                    self.operate_stack.append(sign_in)
                    words += data_str[i]
                elif True:
                    words += data_str[i]
                i += 1
            except IndexError as e:
                break
        return i + 1, words

    def sqlParser(self, sql):
        j = 0
         
        while True:
            try:
                if   sql[j] == '%' and sql[j + 1] == 's':
                    pre = sql[:j]
                    
                    try:
                        value = self.operant_list.pop()
                    except:
                        raise TypeError('not all arguments converted during string formatting')
                    
                    succ = sql[j + 2:]
                    sql = pre + value + succ#operant_stack.pop() + succ
                    
                    j = j - 1 + value.__len__() + 1
                    
                elif sql[j] == '%' and sql[j + 1] == '(':
                    pre = sql[:j]
                    
                    key = ""
                    k = 2
                    while sql[j + k] != ')':
                        key += sql[j + k]
                        k += 1
    
                    try:
                        value = self.operant_dict.pop(key)
                    except:
                        raise TypeError('not all arguments converted during string formatting')
                        
                    succ = sql[j + k + 2:]
                    sql = pre + value + succ
                    
                    j = j - 1 + value.__len__()  + 1    
    
                elif sql[j] == '{':
                    # this version of string substitution is under development
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
                self.sql_clist.append(sql)
                break 
            except TypeError as e:
                e.sql = sql
                raise(e)    

    # main entry
    def dataParser(self, data_str, sql_str):
    
        try:
            if   data_str == '':
                pass   
            
            elif data_str[0] == '[':
                self.operate_stack.append('[')
                
    
                index, words = self.stackloop('[', ']', data_str)
                
                # load one row data: words = 'x,y'        
                self.dataParser(words, sql_str)
                self.dataParser(data_str[index:], sql_str)
                           
            elif data_str[0] == '{':
                self.operate_stack.append('{')
    
                # To do get all data splited by ',' between '{ }' into stack             
                index, words = self.stackloop('{', '}', data_str)
                
                self.dataParser(words, sql_str)
                self.dataParser(data_str[index:], sql_str)
            
            elif data_str[0] == ',' or data_str[0] == ' ' or data_str[0] == '\t':
                self.dataParser(data_str[1:], sql_str)
            
            elif True:
                self.load_data(data_str)
                self.sqlParser(sql_str)            
        except IndexError as e:
            pass
        except TypeError as e:
            raise(e)
    
    # main loop    
    def begin(self):
        for data in self.args:
            try:
                self.dataParser(data.__str__(), self.sql_str)
            except TypeError as e:
                self.backup.append(self.sql_str)
                self.sql_str = e.sql
                
        return self.sql_clist

