# -*- coding: utf-8 -*-
'''
Created on 9 лют. 2016 р.

@author: olko
'''
import xlwt
import xlrd
from lxml import etree
import ConfigParser
import os
import shutil

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
        print 'init'
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
        self.ws.write(self.line,12,'FilePath')
        self.ws.write(self.line,13,'for added')
        self.line = self.line+1
        
                                                

    
    def write(self,vset=()):
        print 'write'
        self.ws.write(self.line,0,vset[0])
        self.ws.write(self.line,1,vset[1])
        self.ws.write(self.line,2,vset[2])
        self.ws.write(self.line,3,vset[3])
        self.ws.write(self.line,4,vset[4])
        self.ws.write(self.line,5,vset[5])
        self.ws.write(self.line,6,vset[6])
        self.ws.write(self.line,7,vset[7])
        self.ws.write(self.line,8,vset[8])
        self.ws.write(self.line,9,vset[9])
        self.ws.write(self.line,10,vset[10])
        self.ws.write(self.line,11,vset[11])
        self.ws.write(self.line,12,vset[12])
        self.ws.write(self.line,13,vset[13])
        self.line = self.line+1
        
    def save(self):
        self.wb.save(self.outputfile)
            
            
class XMLWriter(object):
    import shutil
    dir = ''
    
    def fileexists(self,filename):
        if os.path.exists('res\\'+filename):
            if os.path.exists(filename):
                os.remove(filename)
            shutil.move('res\\'+filename,filename[filename.index('\\')+1:])
            return True
        return False
        
    
    def __init__(self):
        configParser = ConfigParser.RawConfigParser()
        configParser.read('XMLDiff.properties')
        self.dir = configParser.get('Folders', 'dir_2')
    
    def add(self,filename,xpath,element):
        print 'add'
        
    def remove(self,filename,xpath,atrName):
        print 'remove'
    def change(self,fileName,xpath,newvalue,atrName):
        print 'change'
        tree = etree.ElementTree
        if self.fileexists(fileName):
            tree = etree.parse(fileName[fileName.index('\\')+1:])
        else:
            tree = etree.parse(self.dir+fileName)
        test = etree.tostring(tree, encoding="UTF-8")
        atr = atrName[atrName.index('(')+1:atrName.index(')')]
        tree.xpath(xpath)[0].attrib[atr] = newvalue
        try:
            os.makedirs('res\\'+fileName[0:fileName.index('\\')])
        except WindowsError:
            print 'sss'
            
        f = open('res\\'+fileName, 'w') 
        f.write(test)
        f.close()
        #tree.write_c14n(self.dir+fileName)
        
        
class ExcelReader(object):
    inputfile = 'detailed_change.xls'
    rb = xlrd.Book
    sheet = xlrd.sheet
    xmlWriter = XMLWriter()
    
    def __init__(self):
        self.rb = xlrd.open_workbook(self.inputfile,formatting_info=True,encoding_override="UTF-8")
        #encoding="UTF-8"
        self.sheet = self.rb.sheet_by_index(0)
    
    def read(self):
        for rownum in range(self.sheet.nrows):
            row = self.sheet.row_values(rownum) 
            if row[4] == 'added':
                self.xmlWriter.add(row[12], row[11], row[13])
            elif row[4] == 'miss':
                self.xmlWriter.remove(row[12], row[11],row[6])
            elif row[4] == 'updated':
                self.xmlWriter.change(row[12], row[11], row[9],row[6])
            #print self.sheet.row_values(rownum) 
                    
        
        
if __name__ == '__main__':
    exr = ExcelReader()
    exr.read()        
    #os.remove(XMLWriter.dir)
        
        
        
        
        
        
        
    
