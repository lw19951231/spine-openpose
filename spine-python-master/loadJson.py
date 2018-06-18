#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/6/16 14:02
# @Author : LuoWen
# @Site : 
# @File : loadJson.py
# @Software: PyCharm
import json
import io
import numpy as np

def calculateAngle(Coords1,Coords2,Coords3):
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
    return angle2-angle1


def calculateAngle_low(Coords1,Coords2,Coords3):
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

    print(k1)
    print(k2)
    print(angle2)
    print(angle1)
    return (angle2-angle1)

humanCoordinate ={}
with io.open("humanCoordinate.json",'r',encoding='utf-8') as json_file:
#with io.open("girl.json",'r',encoding='utf-8') as json_file:
    humanCoordinate=json.load(json_file)
if(len(humanCoordinate.keys())>=2):
    Coordinate = humanCoordinate['person0']
    Coordinate = abs(np.array(Coordinate) - np.array([[0, humanCoordinate['L/B'][0]]]))

else:
    print("no person!")

torso = calculateAngle([0,(Coordinate[8][1]+Coordinate[11][1])/2],[(Coordinate[8][0]+Coordinate[11][0])/2,(Coordinate[8][1]+Coordinate[11][1])/2],Coordinate[1])
neck = calculateAngle([0,Coordinate[1][1]],Coordinate[1],Coordinate[0])-90 if calculateAngle([0,Coordinate[1][1]],Coordinate[1],Coordinate[0])>=0 else calculateAngle([0,Coordinate[1][1]],Coordinate[1],Coordinate[0])+90

rightshoulder = calculateAngle([0,Coordinate[2][1]],Coordinate[2],Coordinate[3])-90
leftshoulder = calculateAngle([0,Coordinate[5][1]],Coordinate[5],Coordinate[6])-90

rightarm = calculateAngle(Coordinate[2],Coordinate[3],Coordinate[4])
leftarm = calculateAngle(Coordinate[5],Coordinate[6],Coordinate[7])

rightupperleg = calculateAngle([0,Coordinate[8][1]],Coordinate[8],Coordinate[9])-180
leftupperleg = calculateAngle([0,Coordinate[11][1]],Coordinate[11],Coordinate[12])-180

rightlowerleg = calculateAngle(Coordinate[8],Coordinate[9],Coordinate[10])
leftlowerleg = calculateAngle(Coordinate[11],Coordinate[12],Coordinate[13])

print('torso',torso)
print('neck',neck)
print('rightshoulder',rightshoulder)
print('rightarm',rightarm)
print('leftshoulder',leftshoulder)
print('leftarm',leftarm)

print('rightupperleg',rightupperleg)
print('rightlowerleg',rightlowerleg)
print('leftupperleg',leftupperleg)
print('leftlowerleg',leftlowerleg)

with io.open("pyguts/examples/data/spineboy_test.json",'r',encoding='utf-8') as json_file:
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
with io.open("pyguts/examples/data/1.json",'w',encoding='utf-8') as json_file:
    json_file.write(unicode(json.dumps(humanAnimation, ensure_ascii=False)))
