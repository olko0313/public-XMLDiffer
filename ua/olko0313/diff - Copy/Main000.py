# -*- coding: utf-8 -*-
'''
Created on 6 лют. 2016 р.

@author: olko
'''
import os
from lxml import etree
import ConfigParser

def sortByAttrId(node):
    return node.attrib.get('attr_id')

def sortByShowOrder(node):
    return node.attrib.get('reference')
    
def xml_compare(x1, x2):
    if x1.tag != x2.tag:
        print('Tags do not match: %s and %s' % (x1.tag, x2.tag))
        
    for name, value in x1.attrib.items():
        if x2.attrib.get(name) != value:
            print('Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
            
    for name in x2.attrib.keys():
        if name not in x1.attrib:
            print('x2 has an attribute x1 is missing: %s'
                         % name)
            
    if not text_compare(x1.text, x2.text):
        print('text: %r != %r' % (x1.text, x2.text))
        
    if not text_compare(x1.tail, x2.tail):
        print('tail: %r != %r' % (x1.tail, x2.tail))
        
    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
            
    if len(cl1) > 0:
        if dict(cl1[0].attrib).has_key('attr_id'):
            cl1.sort(key=sortByAttrId)
            cl2.sort(key=sortByAttrId)
        if dict(cl1[0].attrib).has_key('show_order'):
            cl1.sort(key=sortByShowOrder)
            cl2.sort(key=sortByShowOrder)
    
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
        added = set()
        accordance = set()
        for x in a.keys():
            if x in b.keys():
                accordance.add(x)
            else:
                added.add(x)
        miss = set(b.keys()) - accordance
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
        xml_compare(dict1.get(x), dict2.get(x))

    return True

def text_compare(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()

if __name__ == '__main__':
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
            fo.append(os.path.join(d,f).replace(dir_1,''))
    for f in fo:
        if os.path.exists(os.path.join(dir_2,f)):
            fdiff.append(f)
        else:
            fadded.append(f)
    print('New files')
    for x in fadded:
        print(x)
    print('='*79)
    #tree = lxml.etree.parse(os.path.join(os.path.abspath(os.curdir), os.path.join(dir_1, fdiff[1][1])), parser=None, base_url=None)
    for x in fdiff:
        tree1 = etree.parse(os.path.join(os.path.join(dir_1, x)))
        tree2 = etree.parse(os.path.join(os.path.join(dir_2, x)))
        print(x)
        xml_compare(tree1.getroot(), tree2.getroot())

