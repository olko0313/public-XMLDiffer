# -*- coding: utf-8 -*-
'''
Created on 9 лют. 2016 р.

@author: olko
'''
import xlwt

class ExcelWriter(object):
    '''
    classdocs
    '''
    outputfile = 'detailed_change.xls'
    wb = xlwt.Workbook
    font0 = xlwt.Font
    style0 = xlwt.Style
    ws = xlwt.Worksheet
    line = 0

    def __init__(self):
        '''
        Constructor
        '''
        self.font0 = xlwt.Font()
        self.font0.name = 'Times New Roman'
        self.font0.colour_index = 2
        self.font0.bold = True
        
        self.style0 = xlwt.XFStyle()
        self.style0.font = self.font0
        
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet('Detailed changes')
        self.ws.write(self.line,0,'SCM Package')
        self.ws.write(self.line,1,'Object ID')
        self.ws.write(self.line,2,'Name')
        self.ws.write(self.line,3,'From Template')
        self.ws.write(self.line,4,'Type of change')
        self.ws.write(self.line,5,'Changed Attr ID')
        self.ws.write(self.line,6,'Changed Attr Name')
        self.ws.write(self.line,7,'Old Value')
        self.ws.write(self.line,8,'Old ID')
        self.ws.write(self.line,9,'New Value')
        self.ws.write(self.line,10,'New ID')
        self.ws.write(self.line,11,'xpath')
        self.line = self.line+1
        
                                                

    
    def write(self,set=()):
        self.ws.write(self.line,0,set[0])
        self.ws.write(self.line,1,set[1])
        self.ws.write(self.line,2,set[2])
        self.ws.write(self.line,3,set[3])
        self.ws.write(self.line,4,set[4])
        self.ws.write(self.line,5,set[5])
        self.ws.write(self.line,6,set[6])
        self.ws.write(self.line,7,set[7])
        self.ws.write(self.line,8,set[8])
        self.ws.write(self.line,9,set[9])
        self.ws.write(self.line,10,set[10])
        self.ws.write(self.line,11,'')
        self.line = self.line+1
        
    def save(self):
        self.wb.save(self.outputfile)
        