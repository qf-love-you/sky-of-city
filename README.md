Hello! Before playing this game, please be sure to take a look at this:
----------------------------------------------------------
Game version: v0.1.1
Introduction: Game difficulty is extremely difficult! It's not about cheating or being unable to handle by experts (the author himself couldn't handle it)
Expected updates:
1. Archive function:
Save game progress!
2. Fix the bug in the Hell Map:
What else do you expect to see?
    
----------------------------------------------------------
Background:
You are traveling in the wilderness, getting lost, and encountering monsters. Only by defeating the monsters can you escape

----------------------------------------------------------
w, a, s, d: Control up, down, left, and right
k: Swipe and chop, - (subtract) magic=5, damage=random. randint (40, 60) ->(select random numbers within 40 to 60)
j: Launch a sword, cd=1s, - magic=10, damage=random. randint (200, 300) ->(select a random number within 200 to 300)
i: Returning blood once, add_health=200, cd=15s, - magic=30
f: Explosion, damage=100 (can be triggered many times within 10 seconds), cd=10 seconds, show_time=2.55 seconds, - magic=50
Space: Pause game
CTRL: Upgrade interface

----------------------------------------------------------
Recent updates:
1. Boss
2. Fix stuttering when throwing weapons

----------------------------------------------------------
'images': Image folder
'maps': Map folder, which contains three types of maps:
Hell (currently not done well, don't play for now),
Sky (the most complete map, replace it with gunfight/var. py, information can be found in info1 at the bottom of the txt file),
Mountain (the background is quite emmm... only a part has been made, replaced with gunfight/var. py, please refer to info2 at the bottom of the txt file for information)
'sound ': Sound folder

----------------------------------------------------------
Monster Introduction:
Sky:   

Green Slime:
Health: 500
Damage: 50/s
Part drop probability: 1/5

Blue Slim:
Health: 850
Damage: 100/s
Miss probability: 1/3
Part drop probability: 1/3
Bottom drop probability: 1/5

Purple slime:
Health: 900
Damage: 2000/s
Part drop probability: 1/3

Blue slime (large):
Health: 2000
Damage: 500/s
Part drop probability: 1/2

Mountain:

Green Slime:
Health: 500
Damage: 50/s

Hell:

Skull:
(There are still some bugs, so there are currently no monsters in the map hell)

----------------------------------------------------------
Import the source code of the library (I mean you can install these libraries in advance):
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
Side effects and drawbacks:
1. There will be a gap between the player's first and second movements
2. There are some issues with the monster's pathfinding mechanism
3. Mac players may have some differences
4. Only users who shift between Chinese and English keys can enjoy the option of not manually switching between Chinese and English keys
5. This game cannot be saved (temporary)
6. There may be some unknown issues for the author, thank you for raising them to me!

----------------------------------------------------------
Info1: Wave number: 11, difficulty level is 5 stars (highly recommended for this map)
Info2: Wavenumber: 3, difficulty 1 star

----------------------------------------------------------
Game commands:
Exit: Exit
OpenMode - mode: Enable a game mode called mode ["debug"]
