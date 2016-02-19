# -*- coding: utf-8 -*-
from myExcelWriter import ExcelWriter
import os
from lxml import etree
import ConfigParser


#def xmlparse(x):
    

def generateKey(x):
    tag = x.tag
    if tag == 'project':
        key = '//[@id="]'+x.attrib['id']+'"'
    elif tag == 'reference':
        key = '//[@reference="]'+x.attrib['reference']+'"'
    elif tag == 'external_item':
        key = '//[@_id="]'+x.attrib['_id']+'"'
    elif tag == 'object_type':
        key = '//[@id="]'+x.attrib['id']+'"'
    elif tag == 'param':
        key = '//[@attr_id="]'+x.attrib['attr_id']+'"'
    elif tag == 'nc_object':
        key = '//[@id="]'+x.attrib['id']+'"'
    elif tag == 'configuration_item':
        key = '//[@id="]'+x.attrib['id']+'"'
    elif tag == 'list_value':
        key = '//[@list_value_id="]'+x.attrib['list_value_id']+'"'
    elif tag == 'value':
        key = '//[@value="]'+x.attrib['value']+'"'
    elif tag == 'date_value':
        key = '//[@date_value="]'+x.attrib['date_value']+'"'
    elif tag == 'object_class':
        key = '//[@id="]'+x.attrib['id']+'"'
    else:
        key = tag
    return key
    

def dirsDiff(dir1,dir2):
    fadded = []
    fdiff = []
    walkdir1 = os.walk(dir1)
    #walkdir2 = os.walk(dir2)
    for d, dirs, files in walkdir1:
        for f in files:
            fpath = os.path.relpath(os.path.join(d,f), dir1)
            if os.path.exists(dir2+fpath):
                fdiff.append(fpath)
            else:
                fadded.append(fpath)
            #f.append(os.path.join(d,f).replace(dir1,''))
    return fdiff,fadded

if __name__ == '__main__':
    excelFile = ExcelWriter()
    configParser = ConfigParser.RawConfigParser()
    configParser.read('XMLDiff.properties')
    print(os.path.curdir)
    dir1 = configParser.get('Folders', 'dir_1')
    dir2 = configParser.get('Folders', 'dir_2')
   # fdiff,fadded = dirsDiff(dir1,dir2)
   # print fdiff
   # print len(fadded)
   
    dicts = {}
    walkdir1 = os.walk(dir1)
    for d, dirs, files in walkdir1:
        for f in files:
            tree = etree.parse(os.path.join(d,f), parser=None, base_url=None)
            for x in tree.xpath('//*'):
                if x.tag in dicts.keys():
                    for xa in x.attrib:
                        if xa not in dicts.get(x.tag):
                            dicts.get(x.tag).append(xa)
                else:
                    xa = []
                    for xxa in x.attrib:
                        xa.append(xxa)
                    dicts[x.tag] =  xa
    print dicts
        
        #print x.tag + x.attrib.__str__()
    ''' print('New files')
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
    '''
        #xml_compare(tree1.getroot(), tree2.getroot(),'')
        #for x in stat:
        #    print x
    excelFile.save()
