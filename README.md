你好!游玩此游戏前请务必先看看这个:
----------------------------------------------------------
游戏版本:v0.1.0
介绍:游戏难度贼难!不是开挂或者高手根本玩不过去(作者自己都没能玩过去)
预期更新:
1. boss:
    这你都不知道?
2. 存档功能:
    保存游戏进度!
3. 将地狱地图bug修复:
    你还指望看些啥?
    
----------------------------------------------------------
背景:
你在野外旅游,迷路了,还遇到了怪物,只有打败怪物,才能逃脱.

----------------------------------------------------------
w,a,s,d:控制上,下,左,右
k:挥砍, -(减)magic=5, damage=random.randint(40, 60)->(40到60之内选随机数)
j:发射一只剑, cd=1s, -magic=10, damage=random.randint(200, 300)->(200到300之内选随机数)
i:回一次血, add_health=200, cd=15s, -magic=30
f:爆炸, damage=100(在10s内可触发很多次), cd=10s, show_time=2.55s, -magic=50
space:暂停游戏
ctrl:升级界面

----------------------------------------------------------
最近更新:
1. 升级界面
2. 8零件增加最大血量300(现在处于测试阶段!)
3. 您不再需要切换中英键(只适用于shift切换中英的用户)
4. 波数的显示
5.紫色史莱姆

----------------------------------------------------------
'images':图片文件夹
'maps':地图文件夹,里面有3种地图:
    hell(地狱,目前没做好,暂时先不要玩),
    sky(最完全的一个地图, 将它替换为枪战/var.py, 信息请看txt文件最下面的info1),
    mountain(背景较为emmm......只做了一部分, 将它替换为枪战/var.py, 信息请看txt文件最下面的info2).
'sound':声音文件夹

----------------------------------------------------------
怪物简介:
    sky:
        绿史莱姆:
            health:500
            damage:50/s
            part drop probability:1/5
        蓝史莱姆:
            health:850
            damage:100/s
            miss probability:1/3
            part drop probability:1/3
            bottle drop probability:1/5
        紫史莱姆:
            health:900
            damage:200/s
            part drop probability:1/3

    mountain:
        绿史莱姆:
            health:500
            damage:50/s
    hell:
        骷髅:
            (还有一些bug, 所以地图hell暂无怪物)

----------------------------------------------------------
导入库的源码(我是指你可以提前安装这些库):
import copy
import ctypes
import math
import os
import random as rd
import threading as thr
import time
import tkinter as tk
from tkinter import messagebox as me
import keyboard as kb
import pygame
from PyQt5 import QtWidgets, QtCore, QtGui

----------------------------------------------------------
副作用和不好的地方:
1. 它可能会导致您的输入不便
2. 它可能会很吵
3. 玩家的第一次和第二次移动可能会有间隔
4. 怪物的寻路机制有些问题
5. mac玩家可能会有一些差异
6. 只有shift切换中英键的用户能享受不用手动切换中英键
7. 您可能看不懂波数的字体(它稍微有些连笔了)
8. 你可能看不懂此介绍或不喜欢此介绍
9. 按j,剑碰到怪物的一瞬间会卡
10. 长按j可能会造成卡顿
11. 此游戏无法存档(暂时的)
12. 可能还有一些作者未知的问题,感谢向我提出!

----------------------------------------------------------
info1:波数:6, 难度5星(此地图极力推荐)
info2:波数:3, 难度1星

----------------------------------------------------------
游戏命令:
exit:退出
openMode -mode:开启名为mode的游戏模式["debug"]