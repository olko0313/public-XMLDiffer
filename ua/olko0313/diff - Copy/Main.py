# -*- coding: utf-8 -*-
'''
Created on 6 лют. 2016 р.

@author: olko
'''
import os
import lxml
from lxml import etree
import ConfigParser
#from ua.olko0313.diff.myExcelWriter import ExcelWriter
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
        

fadded = []
fmiss = []
faccordance = []
tree = etree.ElementTree
    
def xml_compare(x1, x2,path):
    global tree, filename,xpath,SCMPackage,ObjectID,Name,FromTemplate,Typeofchange,ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID
    lxpath = path+x1.tag+'/'
    
    if x1.tag != x2.tag:
        print('Tags do not match: %s and %s' % (x1.tag, x2.tag))
    if x1.tag == 'configuration_item':
        SCMPackage = x1.attrib.get('package')
        ObjectID = x1.attrib.get('id')
        Name = x1.attrib.get('name')
        OldValue = x2.attrib.get('name')
    elif x1.tag == 'param':
        ChangedAttrID = x1.attrib.get('attr_id')
        ChangedAttrName = x1.attrib.get('_attr_name')
    elif x1.tag == 'value':
        OldValue = x2.attrib.get('value')
        NewValue = x1.attrib.get('value')
    elif x1.tag == 'list_value_id':
        OldValue = x2.attrib.get('_list_value')
        OldID = x2.attrib.get('list_value_id')
        NewValue = x1.attrib.get('_list_value')
        NewID = x1.attrib.get('list_value_id')
    elif x1.tag == 'date_value':
        OldValue = x2.attrib.get('date_value')
        NewValue = x1.attrib.get('date_value')
    
    for name, value in x1.attrib.items():
        if x2.attrib.get(name) != value:
            print('Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
            excelFile.write((SCMPackage,ObjectID,Name,FromTemplate,'Updated',ChangedAttrID,ChangedAttrName,x2.attrib.get(name),OldID,value,NewID,xpath))
            
    #for name in x2.attrib.keys():
    #    if name not in x1.attrib:
    #        print('x2 has an attribute x1 is missing: %s'
    #                    % name)
            
    if not text_compare(x1.text, x2.text):
        print('text: %r != %r' % (x1.text, x2.text))
        
    if not text_compare(x1.tail, x2.tail):
        print('tail: %r != %r' % (x1.tail, x2.tail))
        
    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    
    def generateKeys(cl1):
        dcl1 = {}
        for x in cl1:
            key = x.tag
            if x.tag == 'param':
                key = x.tag+x.attrib.get('attr_id')
            if x.tag == 'reference':
                key = x.tag+x.attrib.get('reference')
            if x.tag in ('value','list_value_id','date_value'):
                key = x.tag+x.attrib.get(x.tag)
            dcl1[key] = x
        return dcl1
    
    def compare2dict(a,b):
        global filename,xpath,SCMPackage,ObjectID,Name,FromTemplate,Typeofchange,ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID
        added = set()
        accordance = set()
        for x in a.keys():
            if x in b.keys():
                accordance.add(x)
                faccordance.append((SCMPackage,ObjectID,Name,FromTemplate,'Updated',ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID,xpath))
            else:
                added.add(x)
                fadded.append((SCMPackage,ObjectID,Name,FromTemplate,'Updated',ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID,xpath))
        miss = set(b.keys()) - accordance
        for x in miss:
            fmiss.append((SCMPackage,ObjectID,Name,FromTemplate,'Removed',ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID,xpath))
        return added,miss,accordance
    
    dict1 = generateKeys(cl1)
    dict2 = generateKeys(cl2)
    added,miss,accordance = compare2dict(dict1, dict2)

    if len(added) != 0:
        print('Added:')
        print(added)
    if len(miss) != 0:
        print('Miss')
        print(miss)
    for x in accordance:
        print tree.getpath(x1)
        xml_compare(dict1.get(x), dict2.get(x),lxpath)
    return True

def text_compare(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()

if __name__ == '__main__':
    excelFile = ExcelWriter()
    filename = ''
    xpath = ''
    SCMPackage = ''
    ObjectID = ''
    Name = ''
    FromTemplate = ''    
    Typeofchange = ''
    ChangedAttrID = ''
    ChangedAttrName = '' 
    OldValue = ''
    OldID = ''
    NewValue = ''  
    NewID = ''
    configParser = ConfigParser.RawConfigParser()
    configParser.read('XMLDiff.properties')
    print(os.path.curdir)
    dir_1 = configParser.get('Folders', 'dir_1')
    dir_2 = configParser.get('Folders', 'dir_2')
    fo = []
    fc = []
    fdiff = []
    fadded = []
    fos = os.walk(dir_1)
    fcs = os.walk(dir_2)
    print(os.path.abspath(os.path.curdir))
    for d, dirs, files in fos:
        for f in files:
            fo.append(os.path.join(d,f).replace(dir_1+'/',''))
    for f in fo:
        if os.path.exists(os.path.join(dir_2,f)):
            fdiff.append(f)
        else:
            fadded.append(f)
    print('New files')
    for x in fadded:
        print(x)
    print(' ')
    #tree = lxml.etree.parse(os.path.join(os.path.abspath(os.curdir), os.path.join(dir_1, fdiff[1][1])), parser=None, base_url=None)
    for x in fdiff:
        tree1 = etree.parse(os.path.join(os.path.join(dir_1, x)))
        tree2 = etree.parse(os.path.join(os.path.join(dir_2, x)))
        tree = tree1
        filename = x
        xpath = ''
        SCMPackage = ''
        ObjectID = ''
        Name = ''
        FromTemplate = ''    
        Typeofchange = ''
        ChangedAttrID = ''
        ChangedAttrName = '' 
        OldValue = ''
        OldID = ''
        NewValue = ''  
        NewID = ''
        xml_compare(tree1.getroot(), tree2.getroot(),'')
#    for x in faccordance:
#        excelFile.write(x)
    excelFile.save()
