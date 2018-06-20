#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/6/16 12:11
# @Author : LuoWen
# @Site :
# @File : calculateAction.py
# @Software: PyCharm

import io
import json
import os
from creategroupSpinejsons import createSpinejsons
def angeldiff(humanAnimation_index,rotation_origin_index):
    """
    解决动画抖动问题
    :param humanAnimation_index:
    :param rotation_origin_index:
    :return: 判断是否需要添加该帧
    """
    angeldiff = humanAnimation["bones"][humanAnimation_index]["rotation"]-rotation_origin[rotation_origin_index]
    if(abs(angeldiff)>15):
        rotation_origin[rotation_origin_index]=humanAnimation["bones"][humanAnimation_index]["rotation"]
        return True

def changerotation(humanAnimation):
    """
    返回需要变换的角度
    :param humanAnimation:
    :return:
    """
    diff = {}
    diff["leftupperlegdiffer"] = humanAnimation["bones"][2]["rotation"]-humanAnimation_origin["bones"][2]["rotation"]
    diff["leftlowerlegdiffer"] = humanAnimation["bones"][3]["rotation"]-humanAnimation_origin["bones"][3]["rotation"]

    diff["rightupperlegdiffer"] = humanAnimation["bones"][5]["rotation"]-humanAnimation_origin["bones"][5]["rotation"]
    diff["rightlowerlegdiffer"] = humanAnimation["bones"][6]["rotation"]-humanAnimation_origin["bones"][6]["rotation"]

    diff["torsodiffer"] = humanAnimation["bones"][8]["rotation"]-humanAnimation_origin["bones"][8]["rotation"]
    diff["neckdiffer"] = humanAnimation["bones"][9]["rotation"]-humanAnimation_origin["bones"][9]["rotation"]

    diff["rightshoulderdiffer"] = humanAnimation["bones"][11]["rotation"]-humanAnimation_origin["bones"][11]["rotation"]
    diff["rightarmdiffer"] = humanAnimation["bones"][12]["rotation"]-humanAnimation_origin["bones"][12]["rotation"]

    diff["leftshoulderdiffer"] = humanAnimation["bones"][14]["rotation"]-humanAnimation_origin["bones"][14]["rotation"]
    diff["leftarmdiffer"] = humanAnimation["bones"][15]["rotation"]-humanAnimation_origin["bones"][15]["rotation"]
    return diff

if __name__ == '__main__':
    createSpinejsons()
    timeinterval = 1/30.0 #fps，这里为了方便固定参数
    time = 0
    path = 'data/Spinejsons/'
    savepath = "data/showSpineboy.json"


    json_file_before= io.open(path+str(0)+'.json', 'r', encoding='utf-8')
    humanAnimation_origin = json.load(json_file_before)

    #起始角度
    rotation_origin = [humanAnimation_origin["bones"][2]["rotation"],humanAnimation_origin["bones"][3]["rotation"],
                       humanAnimation_origin["bones"][5]["rotation"],humanAnimation_origin["bones"][6]["rotation"],
                       humanAnimation_origin["bones"][8]["rotation"],humanAnimation_origin["bones"][9]["rotation"],
                       humanAnimation_origin["bones"][11]["rotation"],humanAnimation_origin["bones"][12]["rotation"],
                       humanAnimation_origin["bones"][14]["rotation"],humanAnimation_origin["bones"][15]["rotation"]]

    for json_index in range(1,len(os.listdir(path))):
        json_file_before = io.open(path+str(json_index)+'.json', 'r', encoding='utf-8')
        humanAnimation = json.load(json_file_before)

        diff = changerotation(humanAnimation)
        time = time + timeinterval

        if(angeldiff(2,0)):
            humanAnimation_origin["animations"]['walk']['bones']['left upper leg']['rotate'].append(
                {'time':time,'angle':diff["leftupperlegdiffer"]})
        if (angeldiff(5,2)):
            humanAnimation_origin["animations"]['walk']['bones']['right upper leg']['rotate'].append(
                {'time': time, 'angle': diff["rightupperlegdiffer"]})
        if (angeldiff(3, 1)):
            humanAnimation_origin["animations"]['walk']['bones']['left lower leg']['rotate'].append(
                {'time': time, 'angle': diff["leftlowerlegdiffer"]})
        if (angeldiff(6, 3)):
            humanAnimation_origin["animations"]['walk']['bones']['right lower leg']['rotate'].append(
                {'time': time, 'angle': diff["rightlowerlegdiffer"]})
        if(angeldiff(8,4)):
            humanAnimation_origin["animations"]['walk']['bones']['torso']['rotate'].append(
                {'time': time, 'angle': diff["torsodiffer"]})
        if (angeldiff(9, 5)):
            humanAnimation_origin["animations"]['walk']['bones']['neck']['rotate'].append(
                {'time': time, 'angle': diff["neckdiffer"]})
        if (angeldiff(14, 8)):
            humanAnimation_origin["animations"]['walk']['bones']['left shoulder']['rotate'].append(
                {'time': time, 'angle': diff["leftshoulderdiffer"]})
        if (angeldiff(11, 6)):
            humanAnimation_origin["animations"]['walk']['bones']['right shoulder']['rotate'].append(
                {'time': time, 'angle': diff["rightshoulderdiffer"]})
        if (angeldiff(15, 9)):
            humanAnimation_origin["animations"]['walk']['bones']['left arm']['rotate'].append(
                {'time': time, 'angle': diff["leftarmdiffer"]})
        if (angeldiff(12, 7)):
            humanAnimation_origin["animations"]['walk']['bones']['right arm']['rotate'].append(
                {'time': time, 'angle': diff["rightarmdiffer"]})

        with io.open(savepath, 'w', encoding='utf-8') as json_file:
            json_file.write(unicode(json.dumps(humanAnimation_origin, ensure_ascii=False)))