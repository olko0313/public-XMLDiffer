# -*- coding: utf-8 -*-
'''
Created on 6 лют. 2016 р.

@author: olko
'''
import os
from lxml import etree
import ConfigParser
nc_object = ''
nc_ot_id = ''
param = ''
param_id = ''
value = ''
allobj = {}
obj = {}
objs = {}
allobjs = []

def xml_compare(x1):
    global nc_object,param,param_id,value,allobj,allobjs,nc_ot_id
    if x1.tag == 'nc_object':
        nc_object = x1.attrib.get('_type')
        if nc_object is None:
            nc_object = 'All'
    elif x1.tag == 'param':
        param = x1.attrib.get('_attr_name')
        param_id = x1.attrib.get('attr_id')
        allobjs.append([nc_object,param,param_id,nc_ot_id,''])
    elif x1.tag == 'object_type':
        nc_ot_id = x1.attrib.get('id')
    elif x1.tag == 'list_value':
        if len(x1.attrib)>0:
            obj[nc_object+'`'+param_id] = [nc_object,param,param_id,x1.attrib.get('_list_value')]
    elif x1.tag == 'value':
        if len(x1.attrib)>0:
            obj[nc_object+'`'+param_id] = [nc_object,param,param_id,x1.attrib.get('value')]
    elif x1.tag == 'date_value':
        if len(x1.attrib)>0:
            obj[nc_object+'`'+param_id] = [nc_object,param,param_id,x1.attrib.get('date_value')]
    elif x1.tag == 'reference':
        if len(x1.attrib)>0:
            obj[nc_object+'`'+param_id] = [nc_object,param,param_id,x1.attrib.get('reference')]
                
    cl1 = x1.getchildren()
 
    for x in cl1:
        xml_compare(x)
    return True

def xml_com(x1):
    global obj,objs
    for x in obj.keys():
        q = x1.xpath('.//param[@attr_id="'+x[x.index('`')+1:]+'"]')
        if len(q)>0:
            if obj.get(x)[0:1][0] in objs.keys():
                objs[obj.get(x)[0:1][0]][q[0].attrib.get('column_name')] = obj.get(x)[-1]
            else:
                objs[obj.get(x)[0:1][0]] = {q[0].attrib.get('column_name'):obj.get(x)[-1]} 
    for x in allobjs:
        q = x1.xpath('.//param[@attr_id="'+x[2]+'"]')
        if len(q)>0:
            x[4] = q[0].get('column_name')

if __name__ == '__main__':
    tree = etree.parse('C:\TFNURG\config\ObjectsStructure_POC.xml')
    xml_compare(tree.getroot())
    tree = etree.parse('C:\TFNURG\config\ObjectsStructure_RBM.xml')
    xml_compare(tree.getroot())
    tree = etree.parse('C:\TFNURG\config\ObjectsStructure_TFNU.xml')
    xml_compare(tree.getroot())

    
    tree = etree.parse('C:\TFNURG\config\WorkbookStructure_POC.xml')
    xml_com(tree)
    tree = etree.parse('C:\TFNURG\config\WorkbookStructure_RBM.xml')
    xml_com(tree)
    tree = etree.parse('C:\TFNURG\config\WorkbookStructure_TFNU.xml')
    xml_com(tree)
    ot = set()
    ot_name = {}
    for x in allobjs:
        ot.add(x[0])
    for x in ot:
        for q in allobjs:
            if x == q[0]:
                ot_name[x] = q[3]
    i = 0
    j = 0
    g = 0
    for x in ot:
        print x +':'+ ot_name.get(x)
        for q in allobjs:
            if x == q[0]:
               print ' '*4 +q[1]+':'+q[2]+' ('+q[4]+')'
               i = i + 1
               
    #for x in objs.keys():
     #   print x
     #   print objs.get(x)
     #   print "="*50