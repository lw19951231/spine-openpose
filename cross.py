#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/6/18 17:00
# @Author : LuoWen
# @Site : 
# @File : cross.py
# @Software: PyCharm

def cross(p1,p2,p3):#跨立实验
    x1=p2[0]-p1[0]
    y1=p2[1]-p1[1]
    x2=p3[0]-p1[0]
    y2=p3[1]-p1[1]
    return x1*y2-x2*y1

def IsIntersec(p1,p2,p3,p4): #判断两线段是否相交

    #快速排斥，以l1、l2为对角线的矩形必相交，否则两线段不相交
    if(max(p1[0],p2[0])>=min(p3[0],p4[0])    #矩形1最右端大于矩形2最左端
    and max(p3[0],p4[0])>=min(p1[0],p2[0])   #矩形2最右端大于矩形最左端
    and max(p1[1],p2[1])>=min(p3[1],p4[1])   #矩形1最高端大于矩形最低端
    and max(p3[1],p4[1])>=min(p1[1],p2[1])): #矩形2最高端大于矩形最低端

    #若通过快速排斥则进行跨立实验
        if(cross(p1,p2,p3)*cross(p1,p2,p4)<=0
           and cross(p3,p4,p1)*cross(p3,p4,p2)<=0):
            D=1
        else:
            D=0
    else:
        D=0
    return D

def Intersec(first ,center ,second):#判断两条线段和水平线有几个交点
    p1 = [center[0] - 100,center[1]+0.1]
    p2 = [center[0] + 100, center[1]+0.1]
    upIntersec0 = IsIntersec(p1,p2,first,center)
    upIntersec1 = IsIntersec(p1,p2,center,second)

    p1 = [center[0] - 100,center[1]-0.1]
    p2 = [center[0] + 100, center[1]-0.1]
    downIntersec0 = IsIntersec(p1,p2,first,center)
    downIntersec1 = IsIntersec(p1,p2,center,second)

    #print(upIntersec0,upIntersec1,downIntersec0,downIntersec1)
    if((upIntersec0==1&upIntersec1==1)or((downIntersec0==1&downIntersec1==1))):
        return 1
    else:
        return 0


