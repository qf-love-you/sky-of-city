if __name__ == '__main__':
    import thirdParty as tP
import copy
import ctypes
import math
import os
import random as rd
import threading as thr
import time
# from pynput import keyboard as kbd
import tkinter as tk
from tkinter import messagebox as me

import keyboard as kb
import pygame
from PyQt5 import QtWidgets, QtCore, QtGui

import var

stop = False
exit_ = 0
debug = False
lock_ = thr.Lock()
run_time = 0

# subprocess.run(["gamecmd.bat"])

class Cloud(pygame.sprite.Sprite):
    
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        x = rd.randint(70, 100)
        self.image = pygame.transform.scale(self.image, (x, x / 2))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
    
    def update(self):
        if self.rect.x >= 500:
            self.rect.x = -self.rect.width
        self.rect.x += 1
        time.sleep(0.001)
    
    def see(self):
        thr.Thread(target=self.see__).start()
    
    def see__(self):
        for i in range(0, 100, 3):
            self.image.set_alpha(i)
            time.sleep(0.1)

class Block(pygame.sprite.Sprite):
    
    def __init__(self, path, x, y):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def move_right(self):
        global block_group
        for i in block_group:
            if pygame.sprite.collide_mask(player, i) is None:
                self.rect.x -= 5
                time.sleep(0.01)
                if pygame.sprite.collide_mask(player, i) is not None:
                    self.rect.x += 5
                    time.sleep(0.01)
            else:
                self.rect.x += 5
                time.sleep(0.01)
    
    def move_left(self):
        global block_group
        for i in block_group:
            if pygame.sprite.collide_mask(player, i) is None:
                self.rect.x += 5
                time.sleep(0.01)
                if pygame.sprite.collide_mask(player, i) is not None:
                    self.rect.x -= 5
                    time.sleep(0.01)
            else:
                self.rect.x -= 5
                time.sleep(0.01)
    
    def move_up(self):
        global block_group
        for i in block_group:
            if pygame.sprite.collide_mask(player, i) is None:
                self.rect.y += 5
                time.sleep(0.01)
                if pygame.sprite.collide_mask(player, i) is not None:
                    self.rect.y -= 5
                    time.sleep(0.01)
            else:
                self.rect.y -= 5
                time.sleep(0.01)
    
    def move_down(self):
        global block_group
        for i in block_group:
            if pygame.sprite.collide_mask(player, i) is None:
                self.rect.y -= 5
                time.sleep(0.01)
                if pygame.sprite.collide_mask(player, i) is not None:
                    self.rect.y += 5
                    time.sleep(0.01)
            else:
                self.rect.y += 5
                time.sleep(0.01)

class Player(pygame.sprite.Sprite):
    
    def __init__(self, path, x, y):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mirror = False
        self.move = True
        self.health = 4000
        self.maxhealth = 4000
        self.magic = 100
        self.maxmagic = 100
        self.parts = 10
        self.damage = 1
    
    def add_part(self):
        self.parts += 1
    
    def scan(self):
        if len(monster_group) > 0 and not stop:
            for i in monster_group:
                if pygame.sprite.collide_mask(i, self):
                    if not debuff_maxhealth:
                        if i.id == 1:
                            self.health -= 0.5
                        elif i.id == 3:
                            self.health -= 1
                        elif i.id == 4:
                            self.health -= 100
                            time.sleep(0.5)
                        elif i.id == 5:
                            self.health -= 500
                            time.sleep(1)
    
    def move_right(self):
        global block_group
        
        self.move = True
        
        for i in block_group:
            if pygame.sprite.collide_mask(self, i) is None:
                pass
            else:
                self.move = False
        
        if self.move:
            self.rect.x += 5
            if self.mirror:
                self.image = pygame.transform.flip(self.image, True, False)
                self.mirror = False
            for i in block_group:
                if pygame.sprite.collide_mask(self, i) is not None:
                    self.rect.x -= 5
                    break
            time.sleep(0.01)
    
    def move_left(self):
        global block_group
        
        self.move = True
        
        for i in block_group:
            if pygame.sprite.collide_mask(self, i) is None:
                pass
            else:
                self.move = False
        
        if self.move:
            self.rect.x -= 5
            if not self.mirror:
                self.image = pygame.transform.flip(self.image, True, False)
                self.mirror = True
            for i in block_group:
                if pygame.sprite.collide_mask(self, i) is not None:
                    self.rect.x += 5
                    break
            time.sleep(0.01)
        else:
            self.rect.x += 5
    
    def move_up(self):
        global block_group
        
        self.move = True
        
        for i in block_group:
            if pygame.sprite.collide_mask(self, i) is None:
                pass
            else:
                self.move = False
        
        if self.move:
            self.rect.y -= 5
            for i in block_group:
                if pygame.sprite.collide_mask(self, i) is not None:
                    self.rect.y += 5
                    break
            time.sleep(0.01)
        else:
            self.rect.y += 5
    
    def move_down(self):
        global block_group
        
        self.move = True
        
        for i in block_group:
            if pygame.sprite.collide_mask(self, i) is None:
                pass
            else:
                self.move = False
        
        if self.move:
            self.rect.y += 5
            for i in block_group:
                if pygame.sprite.collide_mask(self, i) is not None:
                    self.rect.y -= 5
                    break
            time.sleep(0.01)
        else:
            self.rect.y -= 5
    
    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y
    
    def and_health(self, health):
        if self.health < self.maxhealth:
            self.health += health
            if self.health > self.maxhealth:
                self.health = self.maxhealth

class Weapon(pygame.sprite.Sprite):
    
    def __init__(self, path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.mirror = True
        self.mirror_ = True
        self.new = True
        self.throw = False
        self.thread1 = None
    
    def update(self):
        
        if self.new and not stop:
            self.mirror_ = player.mirror
            if self.mirror_:
                self.rect.x = player.rect.x
                self.rect.y = player.rect.y + 14
                if self.mirror:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.mirror = False
            else:
                self.rect.x = player.rect.x + 25
                self.rect.y = player.rect.y + 14
                if not self.mirror:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.mirror = True
    
    def fight_cut(self):
        
        if player.magic - 5 >= 0 and not stop:
            cut_sound.play()
            if not self.mirror_:
                player.magic -= 5
                # self.new = False
                for i in range(4):
                    self.image = pygame.image.load('images/weapon/weapon1/weapon1_cut-' + str(i + 1) + '.png').convert_alpha()
                    self.image = pygame.transform.scale(self.image, (25, 25))
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.rect.x = player.rect.x + 25
                    self.rect.y = player.rect.y + 14
                    if len(monster_group) > 0:
                        for i in monster_group:
                            if pygame.sprite.collide_mask(i, self) is not None:
                                thr.Thread(target=i.hurt, args=(rd.randint(40 * player.damage, 60 * player.damage), part_sound, part_group)).start()
                for i in range(5):
                    if 4 - i >= 1:
                        self.image = pygame.image.load('images/weapon/weapon1/weapon1_cut-' + str(4 - i) + '.png').convert_alpha()
                    else:
                        self.image = pygame.image.load('images/weapon/weapon1/weapon1.png').convert_alpha()
                    self.image = pygame.transform.scale(self.image, (25, 25))
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.rect.x = player.rect.x + 25
                    self.rect.y = player.rect.y + 14
                    if len(monster_group) > 0:
                        for i in monster_group:
                            if pygame.sprite.collide_mask(i, self) is not None:
                                thr.Thread(target=i.hurt, args=(rd.randint(40 * player.damage, 60 * player.damage), part_sound, part_group)).start()
                    time.sleep(0.03)
                # self.new = True
            else:
                player.magic -= 5
                # self.new = False
                for i in range(4):
                    self.image = pygame.image.load('images/weapon/weapon1/weapon1_cut-' + str(i + 1) + '.png').convert_alpha()
                    self.image = pygame.transform.scale(self.image, (25, 25))
                    self.rect.x = player.rect.x
                    self.rect.y = player.rect.y + 14
                    if len(monster_group) > 0:
                        for i in monster_group:
                            if pygame.sprite.collide_mask(i, self) is not None:
                                thr.Thread(target=i.hurt, args=(rd.randint(40 * player.damage, 60 * player.damage), part_sound, part_group)).start()
                for i in range(5):
                    if 4 - i >= 1:
                        self.image = pygame.image.load('images/weapon/weapon1/weapon1_cut-' + str(4 - i) + '.png').convert_alpha()
                    else:
                        self.image = pygame.image.load('images/weapon/weapon1/weapon1.png').convert_alpha()
                    self.image = pygame.transform.scale(self.image, (25, 25))
                    self.rect.x = player.rect.x
                    self.rect.y = player.rect.y + 14
                    if len(monster_group) > 0:
                        for i in monster_group:
                            if pygame.sprite.collide_mask(i, self) is not None:
                                thr.Thread(target=i.hurt, args=(rd.randint(40 * player.damage, 60 * player.damage), part_sound, part_group)).start()
                    time.sleep(0.03)
                # self.new = True
    
    def fight_throw(self, _):
        
        if player.magic - 10 >= 0 and not stop:
            self.thread1 = thr.Thread(target=self.fight_throw_)
            self.thread1.start()
            time.sleep(1)
    
    def fight_throw_(self):
        player.magic -= 10
        weapon_t = Throw_weapon('images/weapon/weapon1/weapon1_cut-2.png', (self.rect.x, self.rect.y - 5))
        weapon_group.add(weapon_t)

class Throw_weapon(pygame.sprite.Sprite):
    
    def __init__(self, path, pos: tuple):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35))
        # self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.mirror = True
        self.mirror_ = player.mirror
        self.new = True
        cut_sound.play()
    
    def update(self):
        
        if self.new and not stop:
            if self.mirror_:
                self.rect.x -= 5
                if not self.mirror:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.mirror = True
            else:
                self.rect.x += 5
                if self.mirror:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.mirror = False
            
            for i in block_group:
                if pygame.sprite.collide_mask(self, i) is not None:
                    weapon_group.remove(self)
                    self.kill()
                    break
            
            for i in monster_group:
                if pygame.sprite.collide_mask(self, i) is not None:
                    thr.Thread(target=i.hurt, args=(rd.randint(200 * player.damage, 300 * player.damage), part_sound, part_group)).start()
                    weapon_group.remove(self)
                    self.kill()
                    break
            
            # clock.tick(50)
    
    def get_p(self):
        if pygame.sprite.spritecollideany(self, block_group) is not None:
            return False
        else:
            return True

class Monster(pygame.sprite.Sprite):
    
    def __init__(self, path, x, y):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 1, y
        self.health = 500
        self.cd = 0
        self.id = 1
        self.isalive = True
        self.moving = False
        monster_group.add(self)
    
    def moves(self):
        self.moving = True
        thr.Thread(target=self.moves_).start()
    
    def moves_(self):
        while True:
            if not stop:
                self.move()
            time.sleep(0.05)
    
    def move(self):
        if self.health > 0 and self.isalive and not stop:
            if player.rect.x + 10 > self.rect.x:
                self.rect.x += 1
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if player.rect.y + 15 < self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                self.rect.y -= 1
                                time.sleep(0.01)
                        elif player.rect.y + 15 > self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                self.rect.y += 1
                                time.sleep(0.01)
                        else:
                            for i in block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                    self.rect.x -= 1
                                    time.sleep(0.01)
            
            elif player.rect.x + 10 < self.rect.x:
                self.rect.x -= 1
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if player.rect.y + 15 < self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                self.rect.y -= 1
                                time.sleep(0.01)
                        elif player.rect.y + 15 > self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                self.rect.y += 1
                                time.sleep(0.01)
                        else:
                            for i in block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                    self.rect.y += 1
                                    time.sleep(0.01)
            
            elif player.rect.y + 15 < self.rect.y:
                self.rect.y -= 1
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if player.rect.x + 10 > self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                self.rect.x += 1
                                time.sleep(0.01)
                        elif player.rect.x + 10 < self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                self.rect.x -= 1
                                time.sleep(0.01)
                        else:
                            for i in block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                    self.rect.x -= 1
                                    time.sleep(0.01)
            
            elif player.rect.y + 15 > self.rect.y:
                self.rect.y += 1
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if player.rect.x + 10 > self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                self.rect.x += 1
                                time.sleep(0.01)
                        elif player.rect.x + 10 < self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                self.rect.x -= 1
                                time.sleep(0.01)
                        else:
                            for i in block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(player, self):
                                    self.rect.x += 1
                                    time.sleep(0.01)
    
    def hurt(self, health, _, _2):
        if self.cd == 0 and self.isalive and not stop:
            
            self.health -= health
            
            if self.health <= 0:
                try:
                    self.isalive = False
                    self.health = -1
                    # thr.Thread(target=self.scan).start()
                    for i in range(0, 255, 3):
                        self.image.set_alpha(255 - i)
                        time.sleep(0.01)
                    if rd.randint(0, 4) == 0:
                        tP.part1(player, part_sound, (self.rect.x, self.rect.y), player.add_part, part_group)

                    self.kill()
                except Exception as e:
                    win3.write('error', e)
            
            if self.health > 0:
                try:
                    # self.cd = 1

                    self.image_hurt()

                    thr.Thread(target=self.scan).start()

                    time.sleep(0.5)
                    # self.cd = 0
                except Exception as e:
                    win3.write('error', e)
    
    def image_hurt(self):
        thr.Thread(target=self.image_hurt_).start()
    
    def image_hurt_(self):
        if self.health > 0:
            try:
                self.image = pygame.image.load('images/monster/slime_hurt.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (31, 31))
                self.image = pygame.transform.flip(self.image, True, False)
                time.sleep(0.3)
                self.image = pygame.image.load('images/monster/slime.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (31, 31))
                self.image = pygame.transform.flip(self.image, True, False)
            except Exception as e:
                win3.write('error', e)
    
    def boom_(self):
        for i in boom_group:
            if pygame.sprite.collide_mask(self, i):
                self.hurt(100, '', '')
                time.sleep(0.05)
    
    def scan(self):
        if self.rect.x >= player.rect.x:
            if self.rect.y > player.rect.y + 15 - 5:
                self.rect.x += 20
                self.rect.y += 5
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
                        self.rect.y -= 5
            elif self.rect.y < player.rect.y + 5:
                self.rect.x += 20
                self.rect.y -= 5
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
                        self.rect.y += 5
            else:
                self.rect.x += 20
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
        elif self.rect.x < player.rect.x:
            if self.rect.y > player.rect.y + 15 - 5:
                self.rect.x -= 20
                self.rect.y += 5
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20
                        self.rect.y -= 5
            elif self.rect.y < player.rect.y + 5:
                self.rect.x -= 20
                self.rect.y -= 5
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20
                        self.rect.y += 5
            elif player.rect.y - 5 <= self.rect.y <= player.rect.y + 5:
                self.rect.x -= 20
                for i in block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20

class Bar:
    
    def __init__(self, color: tuple, pos: list, date: str = ''):
        self.color = color
        self.pos = pos
        self.gray_pos = copy.deepcopy(pos)
        # self.gray_pos[3] = self.gray_pos[3]/30
        self.width = copy.deepcopy(self.gray_pos)[3] / 2
        if date == 'health':
            self.text = font2.render(str(player.health) + '/' + str(player.maxhealth), True, (255, 255, 0))
        elif date == 'magic':
            self.text = font2.render(str(player.magic) + '/' + str(player.maxmagic), True, (255, 255, 0))
    
    def init(self, color: tuple, pos: list, date: str = ''):
        self.color = color
        self.pos = pos
        self.gray_pos = copy.deepcopy(pos)
        # self.gray_pos[3] = self.gray_pos[3]/30
        self.width = copy.deepcopy(self.gray_pos)[3] / 2
        if date == 'health':
            self.text = font2.render(str(player.health) + '/' + str(player.maxhealth), True, (255, 255, 0))
        elif date == 'magic':
            self.text = font2.render(str(player.magic) + '/' + str(player.maxmagic), True, (255, 255, 0))
    
    def fill(self):
        screen.fill((200, 200, 200), self.gray_pos)
        screen.fill(self.color, self.pos)
    
    def update(self, date):
        self.width = copy.deepcopy(self.gray_pos)[3] / 2
        if date == 'health':
            self.pos[2] = player.health / 20
            self.text = font2.render(str(int(player.health)) + '/' + str(player.maxhealth), True, (255, 255, 0))
        elif date == 'magic':
            self.pos[2] = player.magic
            self.text = font2.render(str(int(player.magic)) + '/' + str(player.maxmagic), True, (255, 255, 0))

class boom(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/effects/boom.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = player.rect.x - 30, player.rect.y - 40
        boom_group.add(self)
        boom_effect.play()
        self.hide_()
    
    def hide_(self):
        thr.Thread(target=self.hide).start()
    
    def hide(self):
        for i in range(255):
            self.image.set_alpha(255 - i)
            time.sleep(0.02)
        self.kill()

class RecoveryBottle(pygame.sprite.Sprite):
    
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.image.load('images/items/recoverybottle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
    
    def update(self):
        distance = math.dist((self.rect.centerx, self.rect.centery), (self.player.rect.centerx, self.player.rect.centery))
        
        if pygame.sprite.collide_mask(self, self.player):
            self.kill()
            self.player.health += 500
            if self.player.health > self.player.maxhealth:
                self.player.health = self.player.maxhealth
            self.kill()
        
        elif distance <= 50:
            direction_vector = pygame.math.Vector2(self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)
            
            velocity_vector = direction_vector.normalize() * 2
            
            self.rect.x += int(velocity_vector.x)
            self.rect.y += int(velocity_vector.y)

class inputer:
    
    def __init__(self):
        self.text = None
    
    def input(self, text):
        self.text = text
        if self.text == '0':
            return
        if self.text == '1314':
            self.pojie1()
    
    @staticmethod
    def pojie1():
        global debuff_maxhealth, win3
        debuff_maxhealth = True
        if debug:
            
            if len(str(math.floor(run_time / 60))) == 1:
                H = '0' + str(math.floor(run_time / 60))
            else:
                H = str(math.floor(run_time / 60))
            
            if len(str(run_time % 60)) == 1:
                S = '0' + str(run_time % 60)
            else:
                S = str(run_time % 60)
            
            win3.textView.appendPlainText(f"[{H}:{S}][main/info]:open property \"debuff_maxhealth\" successfully!")

class particle(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        self.pos = (x, y)
        
        self.angle = rd.randint(20, 90)
        
        self.image = pygame.Surface((7, rd.randint(2, 3))).convert_alpha()
        self.image.fill((255, 0, 0))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = 2
    
    def update(self):
        dx = math.cos(math.radians(self.angle))
        dy = -math.sin(math.radians(self.angle))
        
        self.rect.x += dx * 5
        self.rect.y += dy * 5
        
        if self.rect.right < 0 or self.rect.left > screen.get_width() or self.rect.bottom < 0 or not particle_open:
            self.kill()
    
    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center=self.pos)
        surf.blit(self.bullet, bullet_rect)

class red(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/effects/red.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.image.set_alpha(100)
        self.update()
    
    def update(self):
        thr.Thread(target=self.update_).start()
    
    def update_(self):
        global run_time, win3
        while True:
            for i in range(100, 255):
                # try:
                self.image.set_alpha(i)
                clock.tick(50)
                
                '''except Exception as e:
                    if debug:
                        
                        if len(str(math.floor(run_time / 60))) == 1:
                            H = '0' + str(math.floor(run_time / 60))
                        else:
                            H = str(math.floor(run_time / 60))
                        
                        if len(str(run_time % 60)) == 1:
                            S = '0' + str(run_time % 60)
                        else:
                            S = str(run_time % 60)
                        
                        win3.textView.appendPlainText(f"[{H}:{S}][main/warning]:{e} -args:{i}")'''
            
            for i in range(255, 100, -1):
                # try:
                self.image.set_alpha(i)
                clock.tick(50)
                    
                '''except Exception as e:
                    if debug:
        
                        if len(str(math.floor(run_time / 60))) == 1:
                            H = '0' + str(math.floor(run_time / 60))
                        else:
                            H = str(math.floor(run_time / 60))
        
                        if len(str(run_time % 60)) == 1:
                            S = '0' + str(run_time % 60)
                        else:
                            S = str(run_time % 60)
        
                        win3.textView.appendPlainText(f"[{H}:{S}][main/warning]:{e} -args:{i}")'''

class settings_win:
    
    def __init__(self):
        super().__init__()
        self.particle = None
        self.particle_ = None
        self.music = None
        self.music_ = None
        self.switch_state2 = None
        self.switch_state = None
        self.win = None
        thr.Thread(target=self.init).start()
    
    def init(self):
        global particle_open
        
        def toggle1():
            if self.switch_state.get() == "Off":
                self.switch_state.set("On")
                self.music.config(text='关', relief=tk.SUNKEN, bg="#00ffff", activebackground="#00ffff")
                pygame.mixer.music.set_volume(0)
            else:
                self.switch_state.set("Off")
                self.music.config(text='开', relief=tk.RAISED, bg="#00ffff", activebackground="#00ffff")
                pygame.mixer.music.set_volume(1)
        
        def toggle2():
            global particle_open
            if self.switch_state2.get() == "Off":
                self.switch_state2.set("On")
                self.particle.config(text='关', relief=tk.SUNKEN, bg="#00ffff", activebackground="#00ffff")
                particle_open = False
            else:
                self.switch_state2.set("Off")
                self.particle.config(text='开', relief=tk.RAISED, bg="#00ffff", activebackground="#00ffff")
                particle_open = True
        
        self.win = tk.Tk()
        
        self.switch_state = tk.StringVar()
        self.switch_state.set("Off")
        
        self.switch_state2 = tk.StringVar()
        self.switch_state2.set("Off")
        
        self.music_ = tk.Label(self.win, text='音乐:', background="#00ffff")
        self.music_.grid(row=0, column=0)
        
        self.music = tk.Button(self.win, text='开', background="#00ffff", command=toggle1)
        self.music.grid(row=0, column=1)
        
        self.particle_ = tk.Label(self.win, text='粒子:', background="#00ffff")
        self.particle_.grid(row=1, column=0)
        
        self.particle = tk.Button(self.win, text='开', background="#00ffff", command=toggle2)
        self.particle.grid(row=1, column=1)
        
        self.win.withdraw()
        
        self.win.overrideredirect(True)
        self.win["background"] = "#00ffff"
        self.win.attributes("-alpha", 0.8)
        
        self.win.mainloop()
    
    def show(self):
        user32 = ctypes.windll.user32
        screen_size0 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        
        self.win.geometry('200x200+' + str(rd.randint(0, screen_size0[0] - 200)) + '+' + str(rd.randint(0, screen_size0[1] - 200)))
        
        self.win.deiconify()
    
    def hide(self):
        self.win.withdraw()

class debug_win(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.resize(600, 400)
        
        self.textView = QtWidgets.QPlainTextEdit(self)
        self.textView.setGeometry(0, 0, self.width(), self.height())
        self.textView.setReadOnly(True)
        
        self.check = QtCore.QTimer(self)
        self.check.timeout.connect(self.if_debug)
        self.check.start(50)
    
    def if_debug(self):
        # self.update()
        if debug:
            self.show()
        # self.update()
    
    def closeEvent(self, a0):
        pass
    
    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.textView.setGeometry(0, 0, self.width(), self.height())
    
    def write(self, level='info', ms=''):
        if len(str(math.floor(run_time / 60))) == 1:
            H = '0' + str(math.floor(run_time / 60))
        else:
            H = str(math.floor(run_time / 60))
    
        if len(str(run_time % 60)) == 1:
            S = '0' + str(run_time % 60)
        else:
            S = str(run_time % 60)
        self.textView.appendPlainText(f"[{H}:{S}][main/{level}]:{ms}")
        

'''def move_up():
    def one(i):
        i.move_up()

    for i in block_group:
        thr.Thread(target=one, args=(i, )).start()'''

def updates():
    # while True:
    #     try:
    cloud_group.update()
    block_group.update()
    floor_group.update()
    damage_group.update()
    blood_bar.update('health')
    magic_bar.update('magic')
    monster_group.update()
    people_group.update()
    part_group.update()
    bottle_group.update()
    weapon_group.update()
    text_group.update()
    boom_group.update()
    particle_group.update()

def draw():
    global blood_bar, magic, screen, bottle_group
    
    cloud_group.draw(screen)
    
    block_group.draw(screen)
    
    floor_group.draw(screen)
    
    damage_group.draw(screen)
    
    blood_bar.fill()
    screen.blit(blood_bar.text, (blood_bar.gray_pos[0] + 20, blood_bar.gray_pos[1]))
    
    magic_bar.fill()
    screen.blit(magic_bar.text, (magic_bar.gray_pos[0] + 20, magic_bar.gray_pos[1]))
    
    a_bullet_group.draw(screen)
    
    monster_group.draw(screen)
    
    people_group.draw(screen)
    
    part_group.draw(screen)
    
    bottle_group.draw(screen)
    
    weapon_group.draw(screen)
    
    text_group.draw(screen)
    
    boom_group.draw(screen)
    
    red_group.draw(screen)
    
    particle_group.draw(screen)
    
    clock.tick(50)

def func1():
    while True:
        if not stop:
            kb.wait('j')
            weapon1.fight_throw('')
            time.sleep(2)

def func2():
    while True:
        for i in monster_group:
            if not i.moving:
                i.moves()
                i.moving = True
        clock.tick(50)

def func3():
    while True:
        if not stop:
            player.scan()
            for i in monster_group:
                for j in boom_group:
                    if pygame.sprite.collide_mask(i, j):
                        i.boom_()
        time.sleep(0.01)

def func4():
    while True:
        if not stop:
            if player.magic < player.maxmagic:
                player.magic += 2
                if player.magic > player.maxmagic:
                    player.magic = player.maxmagic
            elif player.magic < 0:
                player.magic = 0
            if player.health < player.maxhealth:
                player.health += 1
                if player.health > player.maxhealth:
                    player.health = player.maxhealth
            elif player.health < 0:
                player.health = 0
            time.sleep(0.3)

def func5():
    def up():
        while True:
            kb.wait('w')
            if not stop:
                player.move_up()
                time.sleep(0.01)
                # clock.tick(50)
    
    def down():
        while True:
            kb.wait('s')
            if not stop:
                player.move_down()
                time.sleep(0.01)
    
    def left():
        while True:
            kb.wait('a')
            if not stop:
                player.move_left()
                time.sleep(0.01)
    
    def right():
        while True:
            kb.wait('d')
            if not stop:
                player.move_right()
                time.sleep(0.01)
    
    thr.Thread(target=up).start()
    thr.Thread(target=down).start()
    thr.Thread(target=left).start()
    thr.Thread(target=right).start()

def func6():
    while True:
        if not stop:
            for monster in monster_group:
                if monster.id == 1:
                    monster.fight(a_bullet_group)
            time.sleep(3)

def func7():
    while True:
        kb.wait('i')
        if player.magic - 30 >= 0 and not stop:
            player.magic -= 30
            player.and_health(200)
            time.sleep(15)

def func8():
    while True:
        kb.wait('f')
        if player.magic - 50 >= 0 and not stop:
            player.magic -= 50
            boom()
            time.sleep(10)

def func9(_):
    global stop
    stop = True

# def func10():
#     while True:
#         for i in bottle_group:
#             i.scan()
#         time.sleep(0.01)

def exec_app():
    app.exec_()

def run_debug():
    global run_time, exit_
    while True:
        if exit_ == 0:
            run_time += 1
            
            time.sleep(1)
        else:
            break
    return

def run_command():
    try:
        global exit_, debug, win3
        print("游戏命令行:")
        print("\texit: 退出此游戏.")
        print("\topenMode -mode: 开启mode模式.\n")
        while True:
            # print(len(monster_group))
            command = input('command:')
            command = command.split(' ')
            if debug:
                
                if len(str(math.floor(run_time / 60))) == 1:
                    H = '0' + str(math.floor(run_time / 60))
                else:
                    H = str(math.floor(run_time / 60))
                
                if len(str(run_time % 60)) == 1:
                    S = '0' + str(run_time % 60)
                else:
                    S = str(run_time % 60)
                
                win3.textView.appendPlainText(f'[{H}:{S}][main/info]:' + command)
            if command[0] == 'exit':
                pygame.quit()
                for i in range(5):
                    os._exit()
                exit()
                exit_ = 1
                break
            
            elif command[0] == "openMode":
                if command[1] == "debug":
                    debug = True
                else:
                    print(f'We don\'t have \"{command[1]}\" arg.')
            
            else:
                print(f'We don\'t have \"{command[0]}\" command line.')
    except:
        pass
    return

def add_particles():
    while True:
        if rd.randint(1, 4) == 1 and particle_open:
            particle_group.add(particle(rd.randint(0, screen.get_width()), screen.get_height()))
        clock.tick(50)

def func11():
    global win3
    win3 = debug_win()

def buy_win():
    global see, win
    
    def show():
        global see, stop, lock
        
        def get_window():
            user32 = ctypes.windll.user32
            
            # 单显示器屏幕宽度和高度:
            screen_size0 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            
            return screen_size0
        
        if not see:
            win.deiconify()
            win2.hide()
            win.geometry('400x200+' + str(rd.randint(0, get_window()[0] - 200)) + '+' + str(rd.randint(0, get_window()[1] - 200)))
            see = True
            stop = True
            lock = True
        else:
            win.withdraw()
            see = False
            stop = False
            lock = False
    
    def win_init():
        global win, part_number
        
        def strong_sword():
            if player.parts >= 4:
                player.parts -= 4
                player.damage += 0.1
                player.damage = round(player.damage, 1)
                me.showinfo('提示:', '加强成功!现在伤害倍率:' + str(player.damage))
        
        def add_health():
            if player.parts >= 8:
                player.parts -= 8
                player.maxhealth += 300
                player.health = player.maxhealth
                blood_bar.init((255, 0, 0), [5, 30, player.health / 20, 15], 'health')
                me.showinfo('提示:', '加强成功!现在最大生命值:' + str(player.maxhealth))
        
        def get_window():
            user32 = ctypes.windll.user32
            
            # 单显示器屏幕宽度和高度:
            screen_size0 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            
            return screen_size0
        
        inputer1 = inputer()
        
        part_number = tk.Label(win, text='零件:' + str(player.parts), background="#00ffff")
        part_number.grid(row=0, column=0)
        
        button1 = tk.Button(win, text='加强剑(4零件)', background="#00ffff", command=strong_sword)
        button1.grid(row=1, column=0)
        
        button2 = tk.Button(win, text='加强生命(8零件)', background="#00ffff", command=add_health)
        button2.grid(row=2, column=0)
        
        entry1 = tk.Entry(win)
        entry1.grid(row=0, column=1)
        
        button3 = tk.Button(win, text='确定', background="#00ffff", command=lambda: inputer1.input(entry1.get()))
        button3.grid(row=1, column=1)
        
        win.geometry('400x200+' + str(rd.randint(0, get_window()[0] - 200)) + '+' + str(rd.randint(0, get_window()[1] - 200)))
        
        win.overrideredirect(True)
        win["background"] = "#00ffff"
        win.attributes("-alpha", 0.8)
        
        win.withdraw()
    
    def win_update():
        while True:
            part_number.config(text='零件:' + str(player.parts))
            clock.tick(50)
    
    win = tk.Tk()
    
    see = False
    
    win_init()
    
    thr.Thread(target=win_update).start()
    
    kb.add_hotkey('ctrl', show)
    
    win.mainloop()

def add_bottle(x, y, group, player):
    global bottle_group
    group.add(RecoveryBottle(x, y, player))

def game_stop():
    global stop
    if not lock:
        if stop:
            stop = False
            win2.hide()
        else:
            stop = True
            win2.show()

def english():
    time.sleep(0.2)
    kb.press_and_release('shift')

def next_b():
    global b
    b = 0
    z = var.monster_maps
    while True:
        try:
            if var.terrain == 'sky' or var.terrain == 'mountain':
                if len(monster_group) == 0:
                    x_, x, y, k = 1.5, 1.5, 3, 0
                    
                    for i in range(len(z[b])):
                        x = x_
                        y += 1
                        for j in z[b][i]:
                            x += 1
                            k += 1
                            if j == 1:
                                Monster('images/monster/slime.png', x * 30, y * 30)
                            if j == 2:
                                tP.Monster2('images/monster/blue_slime.png', x * 30, y * 30, player, monster_group, block_group, boom_group, text_group, bottle_group)
                            elif j == 3:
                                tP.Monster3('images/monster/purple_slime.png', x * 30, y * 30, player, monster_group, block_group, boom_group, text_group)
                            elif j == 4:
                                tP.Monster4('images/monster/blue_slime.png', x * 30, y * 30, player, monster_group, block_group, boom_group, text_group, make_monster)
                    
                    b += 1
            elif var.terrain == 'hell':
                if len(monster_group) == 0:
                    x_, x, y, k = 1.5, 1.5, 3, 0
                    
                    for i in range(len(z[b])):
                        x = x_
                        y += 1
                        for j in z[b][i]:
                            x += 1
                            k += 1
                            if j == 1:
                                monster = tP.Monster1('images/monster/skeleton.png', x * 30, y * 30, player, block_group)
                                monster_group.add(monster)
                    
                    b += 1
        
        except:
            pass
        time.sleep(0.01)

def set_var():
    try:
        global background, cut_sound, cloud_group, block_group, floor_group, people_group, \
            weapon_group, monster_group, player, weapon1, clock, font, screen, blood_bar, \
            magic_bar, font2, fail, damage_group, a_bullet_group, boom_group, text_group, \
            part_sound, part_group, boom_effect, see, stop, stop_, font3, lock, font4, bottle_group, \
            debuff_maxhealth, particle_group, red_effect, red_group, win2, particle_open, win3, \
            app
        
        app = QtWidgets.QApplication([])
    
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
    
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        
        see = False
        stop = False
        lock = False
        particle_open = True
        
        screen = pygame.display.set_mode((500, 500), pygame.SCALED)
        
        pygame.display.set_caption('sky of city-0.1.1')
        pygame.display.set_icon(pygame.image.load('images/icon.ico').convert_alpha())
        
        font = pygame.font.Font('fonts/font1.ttf', 20)
        font2 = pygame.font.Font('fonts/font1.ttf', 15)
        font3 = pygame.font.Font('fonts/font1.ttf', 50)
        # print("获取系统中所有可用字体", pygame.font.get_fonts())
        font4 = pygame.font.Font('fonts/font2.ttf', 20)
        
        if var.terrain == 'sky':
            background = pygame.image.load('images/background/sky.jpg').convert_alpha()
        elif var.terrain == 'mountain':
            background = pygame.image.load('images/background/sky2.jpg').convert_alpha()
        elif var.terrain == 'hell':
            background = pygame.image.load('images/background/hell.jpg').convert_alpha()
        
        player = Player('images/people/player.png', 0, 0)
        
        weapon1 = Weapon('images/weapon/weapon1/weapon1.png')
        
        cut_sound = pygame.mixer.Sound('sound/effect_sound/cut.mp3')
        part_sound = pygame.mixer.Sound('sound/effect_sound/get_part.wav')
        boom_effect = pygame.mixer.Sound('sound/effect_sound/boom.wav')
        # block1 = Block('images/block/砖块.gif', )
        clock = pygame.time.Clock()
        
        blood_bar = Bar((255, 0, 0), [5, 30, player.health / 20, 15], 'health')
        magic_bar = Bar((0, 0, 255), [5, 55, player.magic, 15], 'magic')
        
        fail = pygame.image.load('images/ui/fail.png').convert_alpha()
        fail = pygame.transform.scale(fail, (500, 250))
        
        stop_ = pygame.image.load('images/ui/stoping.png').convert_alpha()
        
        debuff_maxhealth = False
        
        win2 = settings_win()
        
        win3 = debug_win()
        
        bottle_group = pygame.sprite.Group()
        cloud_group = pygame.sprite.Group()
        block_group = pygame.sprite.Group()
        floor_group = pygame.sprite.Group()
        people_group = pygame.sprite.Group(player)
        weapon_group = pygame.sprite.Group(weapon1)
        monster_group = pygame.sprite.Group()
        damage_group = pygame.sprite.Group()
        a_bullet_group = pygame.sprite.Group()
        boom_group = pygame.sprite.Group()
        text_group = pygame.sprite.Group()
        part_group = pygame.sprite.Group()
        particle_group = pygame.sprite.Group()
        red_group = pygame.sprite.Group(red())
    except:
        pass

def make_monster(x, y, id_):
    if id_ == 1:
        Monster('images/monster/slime.png', x, y)
    if id_ == 2:
        tP.Monster2('images/monster/blue_slime.png', x, y, player, monster_group, block_group, boom_group, text_group, bottle_group)
    elif id_ == 3:
        tP.Monster3('images/monster/purple_slime.png', x, y, player, monster_group, block_group, boom_group, text_group)
    elif id_ == 4:
        tP.Monster4('images/monster/blue_slime.png', x, y, player, monster_group, block_group, boom_group, text_group, make_monster)

def init():
    try:
        global screen, player
        
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        # QtCore.QApplication.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
        
        pygame.mixer.music.load('sound/music/background_music.mp3')
        pygame.mixer.music.play(-1)
        
        if var.terrain == 'sky' or var.terrain == 'mountain':
            for i in range(18):
                random_1 = rd.randint(1, 3)
                cloud1 = Cloud('images/cloud/cloud' + str(random_1) + '.png')
                cloud1.rect.x = rd.randint(0, 500 - cloud1.rect.width)
                cloud1.rect.y = rd.randint(0, rd.randint(0, 500 - cloud1.rect.height))
                cloud1.see()
                cloud_group.add(cloud1)
        
        x_, x, y, k = 1.5, 1.5, 3, 0
        
        if var.terrain == 'sky' or var.terrain == 'mountain':
            for i in range(len(var.map1)):
                x = x_
                y += 1
                for j in var.map1[i]:
                    x += 1
                    k += 1
                    if j == 1:
                        block1 = Block("images/block/砖块.gif", x * 30, y * 30)
                        floor_group.add(block1)
                    elif j == 2:
                        block1 = Block("images/block/砖块7.gif", x * 30, y * 30)
                        block_group.add(block1)
                    elif j == 3:
                        player.set_pos(x * 30, y * 30)
                        block1 = Block("images/block/砖块.gif", x * 30, y * 30)
                        floor_group.add(block1)
        
        elif var.terrain == 'hell':
            for i in range(len(var.map1)):
                x = x_
                y += 1
                for j in var.map1[i]:
                    x += 1
                    k += 1
                    if j == 1:
                        block1 = Block("images/block/砖块4.gif", x * 30, y * 30)
                        floor_group.add(block1)
                    elif j == 2:
                        block1 = Block("images/block/砖块2.gif", x * 30, y * 30)
                        block_group.add(block1)
                    elif j == 3:
                        block1 = Block("images/block/砖块12.gif", x * 30, y * 30)
                        damage_group.add(block1)
                    elif j == 4:
                        player.set_pos(x * 30, y * 30)
                        block1 = Block("images/block/砖块4.gif", x * 30, y * 30)
                        floor_group.add(block1)
        
        thr.Thread(target=func5).start()
        
        kb.add_hotkey('k', weapon1.fight_cut)
        kb.on_press_key('o', func9)
        kb.add_hotkey('spacebar', game_stop)
        
        # thr.Thread(target=updates).start()
        thr.Thread(target=func1).start()
        thr.Thread(target=func2).start()
        thr.Thread(target=func3).start()
        thr.Thread(target=next_b).start()
        thr.Thread(target=func4).start()
        thr.Thread(target=func7).start()
        thr.Thread(target=func8).start()
        # thr.Thread(target=func10).start()
        # thr.Thread(target=func11).start()
        thr.Thread(target=run_debug).start()
        thr.Thread(target=run_command).start()
        thr.Thread(target=buy_win).start()
        thr.Thread(target=settings_win).start()
        thr.Thread(target=add_particles).start()
        thr.Thread(target=exec_app).start()
    except:
        pass

def start():
    global background, screen, clock, font, fail, see, win3
    
    english()
    
    while not exit_:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    for i in range(5):
                        os._exit(0)
            
            for bullet in a_bullet_group:
                bullet.update()
                if not screen.get_rect().collidepoint(bullet.pos):
                    a_bullet_group.remove(bullet)
            
            screen.blit(background, (0, 0))
            
            updates()
            draw()
            
            fps = int(clock.get_fps())
            
            if fps >= 20:
                text_1 = font.render('FPS:' + str(fps), True, (153, 241, 88))
            else:
                text_1 = font.render('FPS:' + str(fps), True, (204, 0, 0))
            
            text_2 = font4.render('第' + str(b) + '波', True, (204, 0, 0))
            
            screen.blit(text_1, (0, 0))
            screen.blit(text_2, (230, 100))
            
            if player.health <= 0:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            for i in range(5):
                                os._exit(0)
                    screen.blit(fail, (0, 120))
                    pygame.display.update()
                    pygame.display.flip()
                    time.sleep(0.1)
            
            if stop:
                screen.blit(stop_, (0, 0))
                if see:
                    screen.blit(font3.render('请按下ctrl以继续游戏', True, (255, 0, 255)), (0, 500 / 2 - 25))
                else:
                    screen.blit(font3.render('请按下空格以继续游戏', True, (255, 0, 255)), (0, 500 / 2 - 25))
            
            pygame.display.update()
            pygame.display.flip()
            clock.tick(50)
        except Exception as e:
            if debug:
                try:
                    win3.write('error', e)
                except Exception as e:
                    print(e)
    
    pygame.quit()
    os._exit()
    return

def start_():
    try:
        set_var()
        init()
        start()
    except:
        pass

if __name__ == '__main__':
    start_()
    # 1566