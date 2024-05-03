import random

try:
    import math
    import os
    import time, threading as thr
    import pygame, random as rd
    import main
except:
    pass

class Monster1(pygame.sprite.Sprite):
    
    def __init__(self, path, x, y, player, block_group):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 1, y
        self.health = 500
        self.cd = 0
        self.player = player
        self.bullet_group = bullet_group
        self.block_group = block_group
        self.id = 2
    
    def move(self):
        pass
    
    def fight(self, group):
        group.add(Bullet(self.rect.x, self.rect.y, self.player.rect.x, self.player.rect.y))
    
    def hurt(self, health):
        if self.cd == 0:
            
            self.health -= health
            
            if self.health <= 0:
                self.health = -1
                self.kill()
            
            if self.health > 0:
                try:
                    self.cd = 1
                    
                    if self.rect.x > self.player.rect.x:
                        if self.rect.y > self.player.rect.y + 15 - 5:
                            self.rect.x += 20
                            self.rect.y += 5
                            for i in self.block_group:
                                if pygame.sprite.collide_mask(i, self):
                                    self.rect.x -= 20
                                    self.rect.y -= 5
                        elif self.rect.y < self.player.rect.y + 5:
                            self.rect.x += 20
                            self.rect.y -= 5
                            for i in self.block_group:
                                if pygame.sprite.collide_mask(i, self):
                                    self.rect.x -= 20
                                    self.rect.y += 5
                        else:
                            self.rect.x += 20
                            for i in self.block_group:
                                if pygame.sprite.collide_mask(i, self):
                                    self.rect.x -= 20
                    elif self.rect.x < self.player.rect.x:
                        if self.rect.y > self.player.rect.y + 15 - 5:
                            self.rect.x -= 20
                            self.rect.y += 5
                            for i in self.block_group:
                                if pygame.sprite.collide_mask(i, self):
                                    self.rect.x += 20
                                    self.rect.y -= 5
                        elif self.rect.y < self.player.rect.y + 5:
                            self.rect.x -= 20
                            self.rect.y -= 5
                            for i in self.block_group:
                                if pygame.sprite.collide_mask(i, self):
                                    self.rect.x += 20
                                    self.rect.y += 5
                        elif self.player.rect.y - 5 <= self.rect.y <= self.player.rect.y + 5:
                            self.rect.x -= 20
                            for i in self.block_group:
                                if pygame.sprite.collide_mask(i, self):
                                    self.rect.x += 20
                    # time.sleep(0.5)
                    self.cd = 0
                except:
                    pass

class Text(pygame.sprite.Sprite):
    
    def __init__(self, text, x, y, group):
        super().__init__()
        self.image = pygame.font.Font('fonts/font1.ttf', 25).render(text, True, (255, 125, 0))
        # self.image = pygame.image.load(f'images/txt/{text}.png')
        # self.image = pygame.transform.scale(self.image, (30, 15))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        group.add(self)
        
        self.hide()
    
    def hide(self):
        thr.Thread(target=self.hide_).start()
    
    def hide_(self):
        for i in range(255):
            self.image.set_alpha(255 - i)
            time.sleep(0.01)
        
        self.kill()

class Monster2(pygame.sprite.Sprite):
    
    def __init__(self, path, x, y, player, monster_group, block_group, boom_group, text_group, bottle_group):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (31, 30))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 1, y
        self.health = 850
        self.cd = 0
        self.id = 3
        self.isalive = True
        self.monster_group = monster_group
        self.player = player
        self.block_group = block_group
        self.boom_group = boom_group
        self.text_group = text_group
        self.moving = False
        self.bottle_group = bottle_group
        self.monster_group.add(self)
    
    def moves(self):
        self.moving = True
        thr.Thread(target=self.moves_).start()
    
    def moves_(self):
        while True:
            if not main.stop:
                self.move()
            time.sleep(0.05)
    
    def move(self):
        if self.health > 0 and self.isalive == True:
            if self.player.rect.x + 10 > self.rect.x:
                self.rect.x += 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.y + 15 < self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y -= 1
                                time.sleep(0.01)
                        elif self.player.rect.y + 15 > self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y += 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.x -= 1
                                    time.sleep(0.01)
            
            elif self.player.rect.x + 10 < self.rect.x:
                self.rect.x -= 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.y + 15 < self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y -= 1
                                time.sleep(0.01)
                        elif self.player.rect.y + 15 > self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y += 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.y += 1
                                    time.sleep(0.01)
            
            elif self.player.rect.y + 15 < self.rect.y:
                self.rect.y -= 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.x + 10 > self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x += 1
                                time.sleep(0.01)
                        elif self.player.rect.x + 10 < self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x -= 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.x -= 1
                                    time.sleep(0.01)
            
            elif self.player.rect.y + 15 > self.rect.y:
                self.rect.y += 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.x + 10 > self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x += 1
                                time.sleep(0.01)
                        elif self.player.rect.x + 10 < self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x -= 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.x += 1
                                    time.sleep(0.01)
    
    def hurt(self, health, part_sound, part_group):
        if self.cd == 0 and self.isalive == True:
            if rd.randint(0, 2) <= 1:
                
                self.health -= health
                
                if self.health <= 0:
                    self.isalive = False
                    self.health = -1
                    # thr.Thread(target=self.scan).start()
                    for i in range(0, 255, 3):
                        self.image.set_alpha(255 - i)
                        time.sleep(0.01)
                    if rd.randint(0, 3) == 0:
                        part1(self.player, part_sound, (self.rect.x, self.rect.y), self.player.add_part, part_group)
                    if rd.randint(0, 5) == 0:
                        main.add_bottle(self.rect.x, self.rect.y, self.bottle_group, self.player)
                    self.kill()
                
                if self.health > 0:
                    try:
                        self.cd = 1
                        
                        self.image_hurt()
                        
                        thr.Thread(target=self.scan).start()
                        
                        time.sleep(0.5)
                        self.cd = 0
                    except:
                        pass
            else:
                Text('miss', self.rect.x - rd.randint(0, 5), self.rect.y + rd.randint(0, 5), self.text_group)
                self.cd = 1
                self.scan()
                time.sleep(0.5)
                self.cd = 0
    
    def must_hurt(self, health, _, _2):
        if self.cd == 0 and self.isalive == True:
            
            self.health -= health
            
            if self.health <= 0:
                self.isalive = False
                self.health = -1
                # thr.Thread(target=self.scan).start()
                for i in range(0, 255, 3):
                    self.image.set_alpha(255 - i)
                    time.sleep(0.01)
                self.kill()
            
            if self.health > 0:
                try:
                    self.cd = 1
                    
                    self.image_hurt()
                    
                    thr.Thread(target=self.scan).start()
                    
                    time.sleep(0.5)
                    self.cd = 0
                except:
                    pass
    
    def image_hurt(self):
        thr.Thread(target=self.image_hurt_).start()
    
    def image_hurt_(self):
        if self.health > 0:
            self.image = pygame.image.load('images/monster/slime_hurt.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (31, 30))
            self.image = pygame.transform.flip(self.image, True, False)
            time.sleep(0.3)
            self.image = pygame.image.load('images/monster/blue_slime.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (31, 30))
            self.image = pygame.transform.flip(self.image, True, False)
    
    def boom_(self):
        for i in self.boom_group:
            if pygame.sprite.collide_mask(self, i):
                self.must_hurt(8, '', '')
                time.sleep(0.05)
    
    def scan(self):
        if self.rect.x >= self.player.rect.x:
            if self.rect.y > self.player.rect.y + 15 - 5:
                self.rect.x += 20
                self.rect.y += 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
                        self.rect.y -= 5
            elif self.rect.y < self.player.rect.y + 5:
                self.rect.x += 20
                self.rect.y -= 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
                        self.rect.y += 5
            else:
                self.rect.x += 20
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
        elif self.rect.x < self.player.rect.x:
            if self.rect.y > self.player.rect.y + 15 - 5:
                self.rect.x -= 20
                self.rect.y += 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20
                        self.rect.y -= 5
            elif self.rect.y < self.player.rect.y + 5:
                self.rect.x -= 20
                self.rect.y -= 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20
                        self.rect.y += 5
            elif self.player.rect.y - 5 <= self.rect.y <= self.player.rect.y + 5:
                self.rect.x -= 20
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20

class Monster3(pygame.sprite.Sprite):
    
    def __init__(self, path, x, y, player, monster_group, block_group, boom_group, text_group):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 1, y
        self.health = 900
        self.cd = 0
        self.id = 4
        self.isalive = True
        self.move_ = True
        self.monster_group = monster_group
        self.player = player
        self.block_group = block_group
        self.boom_group = boom_group
        self.text_group = text_group
        self.moving = False
        self.monster_group.add(self)
    
    def moves(self):
        self.moving = True
        thr.Thread(target=self.moves_).start()
    
    def moves_(self):
        while True:
            if not main.stop:
                self.move()
            time.sleep(0.05)
    
    def move(self):
        if self.health > 0 and self.isalive == True and self.move_ == True and not main.stop:
            if self.player.rect.x + 40 > self.rect.x:
                self.rect.x += 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.y + 15 < self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y -= 1
                                time.sleep(0.01)
                        elif self.player.rect.y + 15 > self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y += 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.x -= 1
                                    time.sleep(0.01)
            
            elif self.player.rect.x + 40 < self.rect.x:
                self.rect.x -= 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.y + 15 < self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y -= 1
                                time.sleep(0.01)
                        elif self.player.rect.y + 15 > self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y += 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.y += 1
                                    time.sleep(0.01)
            
            elif self.player.rect.y + 15 < self.rect.y:
                self.rect.y -= 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.x + 40 > self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x += 1
                                time.sleep(0.01)
                        elif self.player.rect.x + 40 < self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x -= 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.x -= 1
                                    time.sleep(0.01)
            
            elif self.player.rect.y + 15 > self.rect.y:
                self.rect.y += 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.x + 40 > self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x += 1
                                time.sleep(0.01)
                        elif self.player.rect.x + 40 < self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x -= 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.x += 1
                                    time.sleep(0.01)
                                    
            elif self.player.rect.x + 40 == self.rect.x and self.player.rect.y + 15 == self.rect.y:
                for i in range(6):
                    self.rect.x -= 10
                    time.sleep(0.02)
                
                time.sleep(0.5)

                for i in range(6):
                    self.rect.x += 10
                    time.sleep(0.02)
                
                time.sleep(0.5)
    
    def hurt(self, health, part_sound, part_group):
        if self.cd == 0 and self.isalive == True and not main.stop:
            
            self.health -= health
            
            if self.health <= 0:
                self.isalive = False
                self.health = -1

                for i in range(0, 255, 3):
                    self.image.set_alpha(255 - i)
                    time.sleep(0.01)
                    
                if rd.randint(0, 5) == 0:
                    part1(self.player, part_sound, (self.rect.x, self.rect.y), self.player.add_part, part_group)
                    part1(self.player, part_sound, (self.rect.x, self.rect.y), self.player.add_part, part_group)
                    
                self.kill()
            
            if self.health > 0:
                try:
                    self.cd = 1
                    
                    self.image_hurt()
                    
                    thr.Thread(target=self.scan).start()
                    
                    time.sleep(0.5)
                    self.cd = 0
                except:
                    pass
    
    def must_hurt(self, health):
        if self.cd == 0 and self.isalive == True and not main.stop:
            
            self.health -= health
            
            if self.health <= 0:
                self.isalive = False
                self.health = -1
                # thr.Thread(target=self.scan).start()
                for i in range(0, 255, 3):
                    self.image.set_alpha(255 - i)
                    time.sleep(0.01)
                self.kill()
            
            if self.health > 0:
                try:
                    self.cd = 1
                    
                    self.image_hurt()
                    
                    thr.Thread(target=self.scan).start()
                    
                    time.sleep(0.5)
                    self.cd = 0
                except:
                    pass
    
    def image_hurt(self):
        thr.Thread(target=self.image_hurt_).start()
    
    def image_hurt_(self):
        if self.health > 0 and not main.stop:
            self.image = pygame.image.load('images/monster/slime_hurt.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
            self.image = pygame.transform.flip(self.image, True, False)
            time.sleep(0.3)
            self.image = pygame.image.load('images/monster/purple_slime.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (31, 30))
            self.image = pygame.transform.flip(self.image, True, False)
    
    def boom_(self):
        for i in self.boom_group:
            if pygame.sprite.collide_mask(self, i):
                self.must_hurt(8)
                time.sleep(0.05)
    
    def scan(self):
        if self.rect.x >= self.player.rect.x:
            if self.rect.y > self.player.rect.y + 15 - 5:
                self.rect.x += 20
                self.rect.y += 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
                        self.rect.y -= 5
            elif self.rect.y < self.player.rect.y + 5:
                self.rect.x += 20
                self.rect.y -= 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
                        self.rect.y += 5
            else:
                self.rect.x += 20
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
        elif self.rect.x < self.player.rect.x:
            if self.rect.y > self.player.rect.y + 15 - 5:
                self.rect.x -= 20
                self.rect.y += 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20
                        self.rect.y -= 5
            elif self.rect.y < self.player.rect.y + 5:
                self.rect.x -= 20
                self.rect.y -= 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20
                        self.rect.y += 5
            elif self.player.rect.y - 5 <= self.rect.y <= self.player.rect.y + 5:
                self.rect.x -= 20
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20

class Monster4(pygame.sprite.Sprite):
    
    def __init__(self, path, x, y, player, monster_group, block_group, boom_group, text_group, function):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 1, y
        self.health = 2000
        self.cd = 0
        self.id = 5
        self.s = 0
        self.isalive = True
        self.move_ = True
        self.monster_group = monster_group
        self.player = player
        self.block_group = block_group
        self.boom_group = boom_group
        self.text_group = text_group
        self.function = function
        self.moving = False
        self.monster_group.add(self)
    
    def moves(self):
        self.moving = True
        thr.Thread(target=self.moves_).start()
    
    def moves_(self):
        while True:
            if not main.stop:
                self.move()
            time.sleep(0.05)
    
    def move(self):
        if self.health > 0 and self.isalive == True:
            if self.player.rect.x + 10 > self.rect.x:
                self.rect.x += 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.y + 15 < self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y -= 1
                                time.sleep(0.01)
                        elif self.player.rect.y + 15 > self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y += 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.x -= 1
                                    time.sleep(0.01)
        
            elif self.player.rect.x + 10 < self.rect.x:
                self.rect.x -= 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.y + 15 < self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y -= 1
                                time.sleep(0.01)
                        elif self.player.rect.y + 15 > self.rect.y:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.y += 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.y += 1
                                    time.sleep(0.01)
        
            elif self.player.rect.y + 15 < self.rect.y:
                self.rect.y -= 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.x + 10 > self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x += 1
                                time.sleep(0.01)
                        elif self.player.rect.x + 10 < self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x -= 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.x -= 1
                                    time.sleep(0.01)
        
            elif self.player.rect.y + 15 > self.rect.y:
                self.rect.y += 1
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        if self.player.rect.x + 10 > self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x += 1
                                time.sleep(0.01)
                        elif self.player.rect.x + 10 < self.rect.x:
                            while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                self.rect.x -= 1
                                time.sleep(0.01)
                        else:
                            for i in self.block_group:
                                while pygame.sprite.collide_mask(i, self) and not pygame.sprite.collide_mask(self.player, self):
                                    self.rect.x += 1
                                    time.sleep(0.01)
    
    def hurt(self, health, part_sound, part_group):
        if self.cd == 0 and self.isalive == True and not main.stop:
            
            self.health -= health
            
            if self.s <= 17:
                self.s += 3
            
            if random.randint(1, 3) == 1:
                self.function(self.rect.centerx, self.rect.centery, random.randint(1, 3))
            
            if self.health <= 0:
                self.isalive = False
                self.health = -1
                
                for i in range(0, 255, 3):
                    self.image.set_alpha(255 - i)
                    time.sleep(0.01)
                
                if rd.randint(0, 2) == 0:
                    part1(self.player, part_sound, (self.rect.x, self.rect.y), self.player.add_part, part_group)
                    part1(self.player, part_sound, (self.rect.x, self.rect.y), self.player.add_part, part_group)
                    part1(self.player, part_sound, (self.rect.x, self.rect.y), self.player.add_part, part_group)
                    part1(self.player, part_sound, (self.rect.x, self.rect.y), self.player.add_part, part_group)
                
                self.kill()
            
            if self.health > 0:
                try:
                    self.cd = 1
                    
                    self.image_hurt()
                    
                    thr.Thread(target=self.scan).start()
                    
                    time.sleep(0.5)
                    self.cd = 0
                except:
                    pass
    
    def must_hurt(self, health):
        if self.cd == 0 and self.isalive == True and not main.stop:
            
            self.health -= health
            
            if self.health <= 0:
                self.isalive = False
                self.health = -1
                # thr.Thread(target=self.scan).start()
                for i in range(0, 255, 3):
                    self.image.set_alpha(255 - i)
                    time.sleep(0.01)
                self.kill()
            
            if self.health > 0:
                try:
                    self.cd = 1
                    
                    self.image_hurt()
                    
                    thr.Thread(target=self.scan).start()
                    
                    time.sleep(0.5)
                    self.cd = 0
                except:
                    pass
    
    def image_hurt(self):
        thr.Thread(target=self.image_hurt_).start()
    
    def image_hurt_(self):
        if self.health > 0 and not main.stop:
            self.image = pygame.image.load('images/monster/slime_hurt.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (62-self.s, 60-self.s))
            self.image = pygame.transform.flip(self.image, True, False)
            time.sleep(0.3)
            self.image = pygame.image.load('images/monster/blue_slime.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (62-self.s, 60-self.s))
            self.image = pygame.transform.flip(self.image, True, False)
    
    def boom_(self):
        for i in self.boom_group:
            if pygame.sprite.collide_mask(self, i):
                self.must_hurt(8)
                time.sleep(0.05)
    
    def scan(self):
        if self.rect.x >= self.player.rect.x:
            if self.rect.y > self.player.rect.y + 15 - 5:
                self.rect.x += 20
                self.rect.y += 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
                        self.rect.y -= 5
            elif self.rect.y < self.player.rect.y + 5:
                self.rect.x += 20
                self.rect.y -= 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
                        self.rect.y += 5
            else:
                self.rect.x += 20
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x -= 20
        elif self.rect.x < self.player.rect.x:
            if self.rect.y > self.player.rect.y + 15 - 5:
                self.rect.x -= 20
                self.rect.y += 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20
                        self.rect.y -= 5
            elif self.rect.y < self.player.rect.y + 5:
                self.rect.x -= 20
                self.rect.y -= 5
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20
                        self.rect.y += 5
            elif self.player.rect.y - 5 <= self.rect.y <= self.player.rect.y + 5:
                self.rect.x -= 20
                for i in self.block_group:
                    if pygame.sprite.collide_mask(i, self):
                        self.rect.x += 20

class part1(pygame.sprite.Sprite):
    
    def __init__(self, player, sound_effect, pos, function, group):
        super().__init__()
        self.image = pygame.image.load('images/part/part1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.player = player
        self.sound_effect = sound_effect
        self.func = function
        group.add(self)
    
    def update(self):
        sprite1_center = self.player.rect.center
        sprite2_center = self.rect.center
        
        vector1 = pygame.math.Vector2(sprite1_center)
        vector2 = pygame.math.Vector2(sprite2_center)
        
        distance = vector1.distance_to(vector2)
        
        if pygame.sprite.collide_mask(self, self.player):
            self.sound_effect.play()
            self.func()
            self.kill()
        
        elif distance <= 50:
            direction_vector = pygame.math.Vector2(self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)
            
            velocity_vector = direction_vector.normalize() * 2
            
            self.rect.x += int(velocity_vector.x)
            self.rect.y += int(velocity_vector.y)

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, x1, y1):
        super().__init__()
        self.pos = (x, y)
        mx, my = x1, y1
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        
        self.image = pygame.Surface((14, 4)).convert_alpha()
        self.image.fill((255, 255, 255))
        self.image = pygame.transform.rotate(self.image, angle)
        self.speed = 2
        self.rect = self.image.get_rect()
    
    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed)
        self.rect = self.image.get_rect(center=self.pos)

if __name__ == '__main__':
    screen = pygame.display.set_mode((500, 500))
    
    bullet1 = Bullet(0, 0, 500, 500)
    
    bullet_group = pygame.sprite.Group(bullet1)
    
    while True:
        try:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    for i in range(5):
                        os._exit(0)
            
            for bullet in bullet_group:
                bullet.update()
                if not screen.get_rect().collidepoint(bullet.pos):
                    bullet_group.remove(bullet)
            
            screen.fill(0)
            
            bullet_group.draw(screen)
            
            pygame.display.update()
            pygame.display.flip()
            time.sleep(0.01)
        
        except:
            pass