#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/6/16 12:11
# @Author : LuoWen
# @Site : 
# @File : calculate.py
# @Software: PyCharm
import numpy as np
import io
import json
humanCoordinate ={}
with io.open("humanCoordinate.json",'r',encoding='utf-8') as json_file:
#with io.open("girl.json",'r',encoding='utf-8') as json_file:
    humanCoordinate=json.load(json_file)
if(len(humanCoordinate.keys())>=2):
    Coordinate = humanCoordinate['person0']
print(Coordinate)


a = abs(np.array(Coordinate)-np.array([[0,humanCoordinate['L/B'][1]]]))
print(a)
print(a[0][0])