# -*- coding: utf-8 -*-
from myExcelWriter import ExcelWriter
import os
from lxml import etree
import ConfigParser

def log(message):
    #print message
    excelFile.write()
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
        if 'list_values' == x.getparent().tag:
            key = tag+'[@id="'+x.attrib['id']+'"]'
        else:
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
    return '//'+key

def prepareFilds(x,x2):
    tag = x.tag
    excelFile.tag = tag
    if tag == 'project':
        excelFile.changedAttrID = ''
        excelFile.changedAttrName = tag
    elif tag == 'reference':
        excelFile.NewID = x.attrib['reference']
        excelFile.NewValue = x.attrib['_obj_name']
    elif tag == 'external_item':
        excelFile.changedAttrID = ''
        excelFile.changedAttrName = tag
    elif tag == 'object_type':
        excelFile.changedAttrID = ''
        excelFile.changedAttrName = tag
    elif tag == 'param':
        excelFile.changedAttrID = x.attrib['attr_id']
        excelFile.changedAttrName = x.attrib['_attr_name']
    elif tag == 'nc_object':
        excelFile.ObjectID = x.attrib['id']
        excelFile.Name = x.attrib['name']
    elif tag == 'configuration_item':
        if x.attrib.get('type') not in ['nc_attribute','nc_attr_type_def']:
            excelFile.SCMPackage = x.attrib['package']
    elif tag == 'list_value':
        excelFile.NewID = x.attrib['list_value_id']
        excelFile.NewValue = x.attrib['_list_value']
    elif tag == 'value':
        excelFile.NewID = ''
        excelFile.NewValue = x.attrib['value']
    elif tag == 'date_value':
        excelFile.NewID = ''
        excelFile.NewValue = x.attrib['date_value']
    elif tag == 'object_class':
        excelFile.changedAttrID = x.attrib['id']
        excelFile.changedAttrName = x.attrib['_type_name']
    elif tag == 'binding':
        excelFile.changedAttrID = x.attrib['object_type_id']
        excelFile.changedAttrName = x.attrib['object_type_name']
    elif tag == 'attr_type_def':
        excelFile.changedAttrID = x.attrib['id']
        excelFile.changedAttrName = x.attrib['_type_def_name']
    elif tag == 'isdisplayed':
        excelFile.changedAttrID =''
        excelFile.changedAttrName = tag
    elif tag == 'show_history':
        excelFile.changedAttrID =''
        excelFile.changedAttrName = tag
    elif tag == 'nc_attribute':
        excelFile.changedAttrID = x.attrib['id']
        excelFile.changedAttrName = x.attrib['name']
    elif tag == 'nc_attr_type_def':
        excelFile.changedAttrID = x.attrib['id']
        excelFile.changedAttrName = x.attrib['name']
    elif tag == 'attr_group':
        excelFile.changedAttrID = x.attrib['id']
        excelFile.changedAttrName = x.attrib['_group_name']
    elif tag == 'required':
        excelFile.changedAttrID =''
        excelFile.changedAttrName = tag
    elif tag == 'attr_type':
        excelFile.changedAttrID = x.attrib['id']
        excelFile.changedAttrName = x.attrib['_type_name']
    elif tag == 'meta_reference':
        excelFile.changedAttrID = x.attrib['ref_attr_id']
        excelFile.changedAttrName = x.attrib['_ref_attr_name']
    elif tag == 'attr_schema':
        excelFile.changedAttrID = x.attrib['id']
        excelFile.changedAttrName = x.attrib['_schema_name']
    else:
        excelFile.changedAttrName = tag


def compareXMLasText(x1,x2):
    return etree.tostring(x1) == etree.tostring(x2)

def compareXMLasElements(x1,x2):
    if 'operation' in x1.attrib.keys():
        excelFile.changedAttribute = 'operation'
        excelFile.NewValue = x1.attrib.get('operation')
        excelFile.Typeofchange = 'update/delete'
        excelFile.xmlPart = etree.tostring(x1)
        log('')
        return True
    prepareFilds(x1,x2)
    if not compareXMLasText(x1, x2):
        if x1.tag != x2.tag:
            log('Tags do not match: %s and %s' % (x1.tag, x2.tag))
        for name, value in x1.attrib.items():
            if name in x2.attrib.keys():
                if x2.attrib.get(name) != value:
                    print name
                    excelFile.NewValue = value
                    excelFile.changedAttribute = name
                    excelFile.OldValue = x2.attrib.get(name)
                    excelFile.Typeofchange = 'update'
                    excelFile.xmlPart = etree.tostring(x1)
                    log('Attributes do not match: %s=%r, %s=%r'
                             % (name, value, name, x2.attrib.get(name)))
            else:
                excelFile.NewValue = value
                excelFile.changedAttribute = name
                excelFile.Typeofchange = 'add'
                excelFile.xmlPart = etree.tostring(x1)
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
            nuse = []
            nuse2 = []
            for x in chs1:
                if len(x.xpath('../'+x.tag)) == len(chs2[0].xpath('../'+x.tag)) == 1:
                    q = generateKey(x2)+'/'+x.tag
                    nuse.append(x)
                    nuse2.append(chs2[0].xpath('../'+x.tag)[0])
                    if 'configuration_item' in q:
                        q = '/'+q
                    else:
                        q = '//'+q
                    chsk1.append(q)
                    chsk2.append(q)
            
            for x in chs1:
                if x not in nuse:
                    chsk1.append(generateKey(x))

            for x in chs2:
                if x not in nuse2:
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
                excelFile.xpath = x
                excelFile.Typeofchange = 'add'
                excelFile.xmlPart = etree.tostring(x1)
                excelFile.tag = x1.tag
                log('Element added: %s=%s'% (x1.xpath(x)[0].tag, etree.tostring(x1.xpath(x)[0])))
            for x in em:
                prepareFilds(x2.xpath(x)[0], x2.xpath(x)[0])
                excelFile.xpath = x
                excelFile.Typeofchange = 'delete'
                excelFile.xmlPart = etree.tostring(x2)
                excelFile.tag = x2.xpath(x)[0].tag
                log('Element deleted: %s=%s'% (x2.xpath(x)[0].tag, etree.tostring(x2.xpath(x)[0])))
            for x in ec:
                excelFile.xpath = x
                print x
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
    
    fdiff,fadded = dirsDiff(dir1,dir2)
    for x in fadded:
        log('File added: %s'% (x))
    
    for x in fdiff:
        print x
        tree1 = etree.parse(os.path.join(dir1,x))
        tree2 = etree.parse(os.path.join(dir2,x))
        excelFile.cleareFields()
        excelFile.filename = x
        compareXMLasElements(tree1.getroot(), tree2.getroot())
    '''
    x = r'billing_specification\obj_9142740953965572511.xml'
    tree1 = etree.parse(os.path.join(dir1,x))
    tree2 = etree.parse(os.path.join(dir2,x))
    excelFile.cleareFields()
    excelFile.filename = x
    compareXMLasElements(tree1.getroot(), tree2.getroot())
    '''
    excelFile.save()
