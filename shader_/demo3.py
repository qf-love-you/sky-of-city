import math
import threading
import time

import pygame
import random

# Initialize pygame
pygame.init()

# Set up the window
size = (500, 500)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Particle Example")

# Set up the clock
clock = pygame.time.Clock()

color = ['red', 'pink', 'orange', 'white']

# Particle list
particles = []

# Main game loop
done = False

fireworks = pygame.sprite.Group()

def scan():
    for i in particles:
        if i.y > screen.get_height() + 5 or i.y < 0 - 5:
            particles.remove(i)
            del i
            continue
        if i.x > screen.get_width() + 5 or i.x < 0 - 5:
            particles.remove(i)
            del i
            continue

def draw_surface():
    for particle in particles:
        particle.draw()
        time.sleep(0.001)

# threading.Thread(target=draw_surface).start()

while not done:
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # Draw particles
    screen.fill((0, 0, 0))
    
    scan()
    
    draw_surface()
    
    fireworks.draw(screen)
    fireworks.update()
    
    for particle in particles:
        particle.update()
    
    # Update the screen
    pygame.display.flip()
    
    clock.tick(500)

# Clean up
pygame.quit()
