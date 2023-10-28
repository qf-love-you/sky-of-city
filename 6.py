import pygame
import math

pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

print('\a')

class Bullet:
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((7, 2)).convert_alpha()
        self.bullet.fill((255, 255, 255))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 2

    def update(self):
        self.pos = (self.pos[0]+self.dir[0]*self.speed,
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)

bullets = []
pos = (250, 250)
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
    bullets.append(Bullet(*pos))

    for bullet in bullets[:]:
        bullet.update()
        if not window.get_rect().collidepoint(bullet.pos):
            bullets.remove(bullet)

    window.fill(0)
    pygame.draw.circle(window, (0, 255, 0), pos, 10)
    for bullet in bullets:
        bullet.draw(window)
    pygame.display.flip()