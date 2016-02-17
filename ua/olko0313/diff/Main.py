# -*- coding: utf-8 -*-
'''
Created on 6 лют. 2016 р.

@author: olko
'''
import os
from lxml import etree
import ConfigParser
from ua.olko0313.diff.myExcelWriter import ExcelWriter

fadded = []
fmiss = []
faccordance = []
tree = etree.ElementTree

def xml_compare(x1, x2,path):
    global tree, filename,xpath,SCMPackage,ObjectID,Name,FromTemplate,Typeofchange,ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID
    lxpath = path+x1.tag+'/'
    if x1.tag != x2.tag:
        print('Tags do not match: %s and %s' % (x1.tag, x2.tag))
    ChangedAttrName = x1.tag
    OldValue = ''
    OldID = ''
    NewValue = ''    
    NewID = ''
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
    key = x1.tag
    if x1.tag == 'param':
        key = x1.tag+'[@attr_id = "'+x1.attrib.get('attr_id')+'"]'
    elif x1.tag == 'reference':
        key = x1.tag+'[@reference = "'+x1.attrib.get('reference')+'"]'
    elif x1.tag == 'value':
        key = x1.tag+'[@value = "'+x1.attrib.get('value')+'"]'
    elif x1.tag == 'list_value':
        if x1.attrib.get('list_value_id') is not None: 
            subkey = x1.attrib.get('list_value_id')
        else:
            subkey = x1.attrib.get('id')
        key = x1.tag+'[@list_value_id = "'+subkey+'"]'
    elif x1.tag == 'date_value':
        key = x1.tag+'[@date_value = "'+x1.attrib.get('date_value')+'"]'
      
        key = x1.tag+x1.attrib.get(x1.tag)
    key = './/'+ key
    
    for name, value in x1.attrib.items():
        if x2.attrib.get(name) != value:
            print('Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
            excelFile.write((SCMPackage,ObjectID,Name,FromTemplate,'updated',ChangedAttrID,ChangedAttrName+' ('+name+')',x2.attrib.get(name),OldID,value,NewID,key,filename,''))
            
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
                key = x.tag+'[@attr_id = "'+x.attrib.get('attr_id')+'"]'
            elif x.tag == 'reference':
                key = x.tag+'[@reference = "'+x.attrib.get('reference')+'"]'
            elif x.tag == 'value':
                key = x.tag+'[@value = "'+x.attrib.get('value')+'"]'
            elif x.tag == 'list_value':
                if x.attrib.get('list_value_id') is not None: 
                    subkey = x.attrib.get('list_value_id')
                else:
                    subkey = x.attrib.get('id')
                key = x.tag+'[@list_value_id = "'+ subkey +'"]'
            elif x.tag == 'date_value':
                key = x.tag+'[@date_value = "'+x.attrib.get('date_value')+'"]'
            dcl1[key] = x
        return dcl1
    
    def compare2dict(a,b):
        global filename,xpath,SCMPackage,ObjectID,Name,FromTemplate,Typeofchange,ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID
        added = set()
        accordance = set()
        for x in a.keys():
            if x in b.keys():
                accordance.add(x)
                faccordance.append((SCMPackage,ObjectID,Name,FromTemplate,'Updated',ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID,key,filename))
            else:
                added.add(x)
                fadded.append((SCMPackage,ObjectID,Name,FromTemplate,'Updated',ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID,key,filename))
        miss = set(b.keys()) - accordance
        for x in miss:
            fmiss.append((SCMPackage,ObjectID,Name,FromTemplate,'Removed',ChangedAttrID,ChangedAttrName,OldValue,OldID,NewValue,NewID,key,filename))
        return added,miss,accordance
    
    dict1 = generateKeys(cl1)
    dict2 = generateKeys(cl2)
    added,miss,accordance = compare2dict(dict1, dict2)

    if len(added) != 0:
        print('Added:')
        print(added)
        for x in added:
            excelFile.write((SCMPackage,ObjectID,Name,FromTemplate,'added',ChangedAttrID,ChangedAttrName,'','',value,NewID,key,filename,etree.tostring(dict1.get(x))))
    if len(miss) != 0:
        print('Miss')
        print(miss)
        for x in miss:
            excelFile.write((SCMPackage,ObjectID,Name,FromTemplate,'miss',ChangedAttrID,ChangedAttrName,'','',value,NewID,key,filename,''))
    for x in accordance:
        #print tree.getpath(x1)
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
    for d, dirs, files in fos:
        for f in files:
            fo.append(os.path.join(d,f).replace(dir_1,''))
    for f in fo:
        if os.path.exists(dir_2+f):
            fdiff.append(f)
        else:
            fadded.append(f)
    print('New files')
    for x in fadded:
        print(x)
    print(' ')
    for x in fdiff:
        tree1 = etree.parse(dir_1+x)
        tree2 = etree.parse(dir_2+x)
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
    excelFile.save()
