# -*- coding: utf-8 -*-
from myExcelWriter import ExcelWriter
import os
from lxml import etree
import ConfigParser

def log(message):
    print message
    return True


def xmlparsestatkeys(dir1):
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
    return dicts
    

def generateKey(x):
    tag = x.tag
    if tag == 'project':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'reference':
        key = tag+'[@reference="'+x.attrib['reference']+'"]'
    elif tag == 'external_item':
        key = tag+'[@_id="'+x.attrib['_id']+'"]'
    elif tag == 'object_type':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'param':
        key = tag+'[@attr_id="'+x.attrib['attr_id']+'"]'
    elif tag == 'nc_object':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'configuration_item':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'list_value':
        key = tag+'[@list_value_id="'+x.attrib['list_value_id']+'"]'
    elif tag == 'value':
        key = tag+'[@value="'+x.attrib['value']+'"]'
    elif tag == 'date_value':
        key = tag+'[@date_value="'+x.attrib['date_value']+'"]'
    elif tag == 'object_class':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'binding':
        key = tag+'[@object_type_id="'+x.attrib['object_type_id']+'"]'
    elif tag == 'attr_type_def':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'isdisplayed':
        key = tag+'[@flag="'+x.attrib['flag']+'"]'
    elif tag == 'show_history':
        key = tag+'[@flag="'+x.attrib['flag']+'"]'
    elif tag == 'nc_attribute':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'nc_attr_type_def':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'attr_group':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'required':
        key = tag+'[@flag="'+x.attrib['flag']+'"]'
    elif tag == 'attr_type':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    elif tag == 'meta_reference':
        key = tag+'[@ref_attr_id="'+x.attrib['ref_attr_id']+'"]'
    elif tag == 'attr_schema':
        key = tag+'[@id="'+x.attrib['id']+'"]'
    else:
        key = '//'+tag
    return key

def compareXMLasText(x1,x2):
    return etree.tostring(x1) == etree.tostring(x2)

def compareXMLasElements(x1,x2):
    if not compareXMLasText(x1, x2):
        if x1.tag != x2.tag:
            log('Tags do not match: %s and %s' % (x1.tag, x2.tag))
        for name, value in x1.attrib.items():
            if x2.attrib.get(name) != value:
                log('Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
        for name, value in x2.attrib.items():
            if name not in x1.attrib:
                log('Attribute deleted: %s=%r'
                         % (name, value))
        chs1 = x1.getchildren()
        chs2 = x2.getchildren()
        if len(chs1) == len(chs2) == 1:
            compareXMLasElements(chs1[0],chs2[0])
        else: 
            chsk1 = []
            chsk2 = []
            for x in chs1:
                chsk1.append(generateKey(x))
            for x in chs2:
                chsk2.append(generateKey(x))
            ea = []
            em = []
            ec = []
            for x in chsk1:
                if x in chsk2:
                    ec.append(x)
                else:
                    ea.append(x)
            for x in chsk2:
                if x not in ec:
                    em.append(x)
            for x in ea:
                log('Element added: %s=%s'% (x1.xpath(x)[0].tag, etree.tostring(x1.xpath(x)[0])))
            for x in em:
                log('Element deleted: %s=%s'% (x2.xpath(x)[0].tag, etree.tostring(x2.xpath(x)[0])))
            for x in ec:
                compareXMLasElements(x1.xpath(x)[0], x2.xpath(x)[0])
    

def dirsDiff(dir1,dir2):
    fadded = []
    fdiff = []
    walkdir1 = os.walk(dir1)
    for d, dirs, files in walkdir1:
        for f in files:
            fpath = os.path.relpath(os.path.join(d,f), dir1)
            if os.path.exists(dir2+fpath):
                fdiff.append(fpath)
            else:
                fadded.append(fpath)
    return fdiff,fadded

if __name__ == '__main__':
    excelFile = ExcelWriter()
    configParser = ConfigParser.RawConfigParser()
    configParser.read('XMLDiff.properties')
    dir1 = configParser.get('Folders', 'dir_1')
    dir2 = configParser.get('Folders', 'dir_2')
    #fdiff,fadded = dirsDiff(dir1,dir2)
    #for x in fadded:
    #    log('File added: %s'% (x))
    '''
    for x in fdiff:
        x = price_value\42\obj_9142862208565599942.xml
        tree1 = etree.parse(os.path.join(dir1,x))
        tree2 = etree.parse(os.path.join(dir2,x))
        compareXMLasElements(tree1.getroot(), tree2.getroot())
    '''
    x = r'price_value\42\obj_9142862208565599942.xml'
    tree1 = etree.parse(os.path.join(dir1,x))
    tree2 = etree.parse(os.path.join(dir2,x))
    compareXMLasElements(tree1.getroot(), tree2.getroot())
    
   
        
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
