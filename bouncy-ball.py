import pygame
import math
from sys import exit

def player_input(vx, vy, ax):
    keys = pygame.key.get_pressed()

    # Horizontal movement
    if keys[pygame.K_LEFT]:
        vx = -3
        ax = -3
    elif keys[pygame.K_RIGHT]:
        vx = 3
        ax = 3
    

    # Vertical movement
    if keys[pygame.K_UP]:
        vy = -3
        vx = 0
    elif keys[pygame.K_DOWN]:
        vy = 3
        vx = 0

    return vx, vy, ax


pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Bouncy ball game!')
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(False)

screen.fill((50, 50, 50))  # RGB for gray
x,y = 400,300 # position
vx,vy = 0,0   # speed
ax,ay = 0,0.5  # acceleration (gravity)
ball_weight = 0.1
circle_radius = 30
bounce_dampening = 0.95  # Reduce velocity on bounce


while True:
    clock.tick(144)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    vx,vy,ax =  player_input(vx,vy,ax)

    # gravity
    vy += ay + ball_weight

    x += vx
    y += vy

     # Bounce on edges
    if y > 600 - circle_radius -5: 
            y = 600 - circle_radius -5
            vy=-vy + ball_weight
    if y < circle_radius +5: 
            y = circle_radius +5
            vy = -vy      
    if x > 800 - circle_radius -5: 
            x = 800 - circle_radius -5
            vx = -vx
    if x < circle_radius +5: 
            x = circle_radius +5
            vx = -vx

    if abs(vy) < 0.5:
        vy = 0
        

    screen.fill((50, 50, 50))  # RGB for gray
    pygame.draw.circle(screen, ('Red'), (x, y), circle_radius)
    
    pygame.display.update()