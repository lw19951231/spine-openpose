#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/6/16 14:02
# @Author : LuoWen
# @Site :
# @File : creategroupSpinejsons.py
# @Software: PyCharm
import json
import io
import os
import numpy as np
import cross
import shutil

def calculateAngle_cross(Coords1,Coords2,Coords3):
    """
    计算一条直线到另一条直线旋转的角度，+代表逆时针，-代表顺时针
    :param Coords1:第一条直线的起始坐标
    :param Coords2:第一条直线的终点坐标，也是第二条直线的起始坐标
    :param Coords3:第二条直线的终点坐标
    :return:
    """
    Coords1x = Coords1[0] ;Coords1y = Coords1[1] ;Coords2x = Coords2[0] ;Coords2y = Coords2[1]
    Coords3x = Coords2[0] ;Coords3y = Coords2[1]; Coords4x = Coords3[0] ;Coords4y = Coords3[1]
    k1 = (Coords2y-Coords1y)/(float(Coords2x-(Coords1x+0.001)))
    k2 = (Coords4y-Coords3y)/(float(Coords4x-(Coords3x+0.001)))
    angle1 = np.arctan(k1)*180/np.pi
    angle2 = np.arctan(k2)*180/np.pi
    if angle1<0:
        angle1 = 180+angle1
    if angle2<0:
        angle2 = 180+angle2
    if(cross.Intersec(Coords1,Coords2,Coords3)):
        return (angle2-angle1)+180
    else:
        return (angle2-angle1)


def saveAngle(Coordinate,prepath,savepath,json_index):
    """
    计算每个关键点的角度并持久化存储
    :param Coordinate: 关键点坐标
    :param prepath: 根据prepath来进行修改
    :param savepath: 保存的路径
    :param json_index: 保存的名称index
    """
    torso = calculateAngle_cross([0, (Coordinate[8][1] + Coordinate[11][1]) / 2],
                                 [(Coordinate[8][0] + Coordinate[11][0]) / 2,
                                  (Coordinate[8][1] + Coordinate[11][1]) / 2], Coordinate[1])
    neck = calculateAngle_cross(
        [(Coordinate[8][0] + Coordinate[11][0]) / 2, (Coordinate[8][1] + Coordinate[11][1]) / 2], Coordinate[1],
        Coordinate[0])

    rightshoulder = calculateAngle_cross(
        [(Coordinate[8][0] + Coordinate[11][0]) / 2, (Coordinate[8][1] + Coordinate[11][1]) / 2],[Coordinate[1][0],Coordinate[1][1]-1],
        Coordinate[3])
    leftshoulder = calculateAngle_cross(
        [(Coordinate[8][0] + Coordinate[11][0]) / 2, (Coordinate[8][1] + Coordinate[11][1]) / 2],[Coordinate[1][0],Coordinate[1][1]-1],
        Coordinate[6])

    rightarm = calculateAngle_cross(Coordinate[2],[Coordinate[3][0],Coordinate[3][1]+0.5],Coordinate[4])#+0.5是为了解决线段平行X轴的问题，这样保证一定不会有平行X轴的情况
    leftarm = calculateAngle_cross(Coordinate[5],[Coordinate[6][0],Coordinate[6][1]+0.5],Coordinate[7])

    rightupperleg = calculateAngle_cross([0,Coordinate[8][1]],Coordinate[8],Coordinate[9])-180
    leftupperleg = calculateAngle_cross([0,Coordinate[11][1]],Coordinate[11],Coordinate[12])-180

    rightlowerleg = calculateAngle_cross(Coordinate[8],[Coordinate[9][0],Coordinate[9][1]+0.5],Coordinate[10])
    leftlowerleg = calculateAngle_cross(Coordinate[11],[Coordinate[12][0],Coordinate[12][1]+0.5],Coordinate[13])

    with io.open(prepath,'r',encoding='utf-8') as json_file:
        humanAnimation =json.load(json_file)

        humanAnimation["bones"][2]["rotation"] = leftupperleg
        humanAnimation["bones"][3]["rotation"] = leftlowerleg

        humanAnimation["bones"][5]["rotation"] = rightupperleg
        humanAnimation["bones"][6]["rotation"] = rightlowerleg

        humanAnimation["bones"][8]["rotation"] = torso
        humanAnimation["bones"][9]["rotation"] = neck

        humanAnimation["bones"][11]["rotation"] = rightshoulder
        humanAnimation["bones"][12]["rotation"] = rightarm

        humanAnimation["bones"][14]["rotation"] = leftshoulder
        humanAnimation["bones"][15]["rotation"] = leftarm
    with io.open(savepath+str(json_index)+".json",'w',encoding='utf-8') as json_file:
        json_file.write(unicode(json.dumps(humanAnimation, ensure_ascii=False)))

def createSpinejsons():
    path = 'data/openposejsons/'
    savepath = 'data/Spinejsons/'
    prepath = "data/SpineExample/example.json"#直接根据这个文件修改角度即可

    if(os.path.exists(savepath)):
        shutil.rmtree(savepath)
        os.makedirs(savepath)
    else:
        os.makedirs(savepath)

    json_file_before = io.open(path + "humanCoordinate0.json", 'r', encoding='utf-8')
    Coordinate0 = json.load(json_file_before)
    Coordinate_before = Coordinate0['person0']
    for i in range(18):
        assert Coordinate_before[i][0] != -1 #保证第一帧图片的人的点存在
    Coordinate_before = abs(np.array(Coordinate_before) - np.array([[0, Coordinate0['L/B'][0]]]))
    saveAngle(Coordinate_before,prepath,savepath,0)

    for json_index in range(len(os.listdir(path))-1):
        json_file = io.open(path+"humanCoordinate"+str(json_index+1)+".json",'r',encoding='utf-8')
        humanCoordinate=json.load(json_file)
        if(len(humanCoordinate.keys())>=2):
            Coordinate = humanCoordinate['person0']
            for i in range(18):
                if(Coordinate[i][0]==-1):
                    Coordinate[i] = Coordinate_before[i]
            Coordinate_before = Coordinate
            Coordinate = abs(np.array(Coordinate) - np.array([[0, humanCoordinate['L/B'][0]]]))
            saveAngle(Coordinate, prepath, savepath, json_index+1)
        else:
            Coordinate = Coordinate_before
            Coordinate = abs(np.array(Coordinate) - np.array([[0, humanCoordinate['L/B'][0]]]))
            saveAngle(Coordinate, prepath, savepath, json_index+1)
            print("Warning! the "+str(json_index)+"th has no person!")
