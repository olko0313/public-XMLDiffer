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
    outputfile = 'detailed_changes.xls'
    wb = xlwt.Workbook
    font0 = xlwt.Font
    style0 = xlwt.Style
    ws = xlwt.Worksheet
    line = 0
    filename = ''
    xpath = ''
    SCMPackage = ''
    ObjectID = ''
    Name = ''    
    Typeofchange = ''
    changedAttrID = ''
    changedAttrName = ''
    changedAttribute = '' 
    OldValue = ''
    OldID = ''
    NewValue = ''    
    NewID = ''
    xmlPart = ''
    tag = ''

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
        self.ws.write(self.line,0,'filename')
        self.ws.write(self.line,1,'xpath')
        self.ws.write(self.line,2,'SCMPackage')
        self.ws.write(self.line,3,'ObjectID')
        self.ws.write(self.line,4,'Name')
        self.ws.write(self.line,5,'Type of change')
        self.ws.write(self.line,6,'Tag')
        self.ws.write(self.line,7,'Changed Attr ID')
        self.ws.write(self.line,8,'Changed Attr Name')
        self.ws.write(self.line,9,'changedAttribute')
        self.ws.write(self.line,10,'Old Value')
        self.ws.write(self.line,11,'Old ID')
        self.ws.write(self.line,12,'New Value')
        self.ws.write(self.line,13,'New ID')
        self.ws.write(self.line,14,'Filter')
        self.ws.write(self.line,15,'xmlPart')
        self.line = self.line+1
        
    def cleareFields(self):
        self.filename = ''
        self.xpath = ''
        self.SCMPackage = ''
        self.ObjectID = ''
        self.Name = ''    
        self.Typeofchange = ''
        self.changedAttrID = ''
        self.changedAttrName = ''
        self.changedAttribute = '' 
        self.OldValue = ''
        self.OldID = ''
        self.NewValue = ''    
        self.NewID = ''
        self.xmlPart = ''
        self.tag = ''                                          

    def showfields(self):
        print self.filename
        print self.xpath
        print self.SCMPackage
        print self.ObjectID
        print self.Name    
        print self.Typeofchange
        print self.changedAttrID
        print self.changedAttrName
        print self.changedAttribute 
        print self.OldValue
        print self.OldID
        print self.NewValue    
        print self.NewID
        print self.xmlPart  
        
    
    def write(self):
        self.ws.write(self.line,0,self.filename)
        self.ws.write(self.line,1,self.xpath)
        self.ws.write(self.line,2,self.SCMPackage)
        self.ws.write(self.line,3,self.ObjectID)
        self.ws.write(self.line,4,self.Name)
        self.ws.write(self.line,5,self.Typeofchange)
        self.ws.write(self.line,6,self.tag)
        self.ws.write(self.line,7,self.changedAttrID)
        self.ws.write(self.line,8,self.changedAttrName)
        self.ws.write(self.line,9,self.changedAttribute)
        self.ws.write(self.line,10,self.OldValue)
        self.ws.write(self.line,11,self.OldID)
        self.ws.write(self.line,12,self.NewValue)
        self.ws.write(self.line,13,self.NewID)
        self.ws.write(self.line,14,'')
        self.ws.write(self.line,15,self.xmlPart)
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
        
    def remove(self,fileName,xpath,atrName):
        print 'remove'
        tree = etree.ElementTree
        if self.fileexists(fileName):
            tree = etree.parse(fileName[fileName.index('\\')+1:])
        else:
            tree = etree.parse(self.dir+fileName)
        print xpath
        print fileName
        x = tree.xpath(xpath)[0]
        x.getparent().remove(x)
        print 'res\\'+fileName[0:fileName.index('obj_')]
        try:
            os.makedirs('res\\'+fileName[0:fileName.index('obj_')])
        except WindowsError:
            print 'sss'
        test = etree.tostring(tree, encoding="UTF-8")
        f = open('res\\'+fileName, 'a+') 
        f.write(test)
        f.close()
        tree.write_c14n(self.dir+fileName)
        
    def change(self,fileName,xpath,newvalue,atrName):
        print 'change'
        tree = etree.ElementTree
        if self.fileexists(fileName):
            tree = etree.parse(fileName[fileName.index('\\')+1:])
        else:
            tree = etree.parse(self.dir+fileName)
        
        print newvalue
        tree.xpath(xpath)[0].attrib[atrName] = newvalue
        try:
            os.makedirs('res\\'+fileName[0:fileName.index('\\')])
        except WindowsError:
            print 'sss'
        test = etree.tostring(tree, encoding="UTF-8")
        f = open('res\\'+fileName, 'w') 
        f.write(test)
        f.close()
        tree.write_c14n(self.dir+fileName)

        
        
class ExcelReader(object):
    inputfile = 'detailed_changes.xls'
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
            if row[14] != '':
                type = row[5] 
                print row[1]
                if type == 'add':
                    self.xmlWriter.add(row[1], row[2], row[10])
                elif type == 'delete':
                    self.xmlWriter.remove(row[0], row[1],row[9])
                elif type == 'update':
                    self.xmlWriter.change(row[0], row[1], row[12], row[9])
                #print self.sheet.row_values(rownum) 
                    
        
        
if __name__ == '__main__':
    exr = ExcelReader()
    exr.read()        
    #os.remove(XMLWriter.dir)
        
        
        
        
        
        
        
    
