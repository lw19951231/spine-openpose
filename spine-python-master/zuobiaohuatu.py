#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/6/17 14:47
# @Author : LuoWen
# @Site : 
# @File : zuobiaohuatu.py
# @Software: PyCharm
import cv2
import json
import io
import numpy as np
CocoPairs = [
    (1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10), (1, 11),
    (11, 12), (12, 13), (1, 0), (0, 14), (14, 16), (0, 15), (15, 17), (2, 16), (5, 17)
]   # = 19
CocoPairsRender = CocoPairs[:-2]

humanCoordinate ={}
with io.open("humanCoordinate0.json",'r',encoding='utf-8') as json_file:
    humanCoordinate=json.load(json_file)

personCoordinate = humanCoordinate['person0']
img = np.zeros((humanCoordinate['L/B'][0], humanCoordinate['L/B'][1], 3), np.uint8) # 创建一张黑色的图像
centers = {}
for i in range(18):
    cv2.circle(img, (personCoordinate[i][0],personCoordinate[i][1]), 3, (255,255,255), thickness=3, lineType=8, shift=0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    center = (personCoordinate[i][0],personCoordinate[i][1])
    centers[i] = center
    cv2.putText(img, str(i), (personCoordinate[i][0],personCoordinate[i][1]), font, 0.5, (255, 255, 255), 1)
print(centers)


for pair_order, pair in enumerate(CocoPairsRender):
    if centers[pair[0]][0] == -1 or centers[pair[1]][0] == -1:
        continue

    cv2.line(img, centers[pair[0]], centers[pair[1]], (255,255,255), 3)


cv2.imshow('Draw', img)
cv2.waitKey(0)
cv2.destroyAllWindows()