import pygame
import random
import math
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Bounce Count Game!')
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(False)

screen.fill((50, 50, 50))  # RGB for gray
x,y = 400,300
vx,vy = 0,0
circle_radius = 30
pygame.draw.circle(screen,(255, 0, 0), (x,y), circle_radius)
count = 0
absSpeed = 0
growth_flag = False  # To track if the circle has already grown
game_over = False  # Game over flag

# Initialize the font
font = pygame.font.Font(None, 36)  # None uses the default font, 36 is the font size

while True:
    clock.tick(144)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
 # Handle key press events to change velocity
    if not game_over:
        if event.type == pygame.KEYDOWN:  # Only trigger on key press, not hold
            if event.key == pygame.K_LEFT:
                vx = -3
            if event.key == pygame.K_RIGHT:
                vx = 3
            if event.key == pygame.K_UP:
                vy = -3
            if event.key == pygame.K_DOWN:
                vy = 3

        # Update position based on velocity
        x += vx
        y += vy    

        # Check if the circle size reaches the game-over limit
        if circle_radius >= 150:  # Example limit
            game_over = True    

         # Keep the circle within the screen boundaries
        if x < circle_radius +5: 
            x = circle_radius +5
            vx = -vx
            count += 1
            val1 = random.randint(0,255)
            val2 = random.randint(0,255)
            val3 = random.randint(0,255)
        if x > 800 - circle_radius -5: 
            x = 800 - circle_radius -5
            vx = -vx
            count += 1
            val1 = random.randint(0,255)
            val2 = random.randint(0,255)
            val3 = random.randint(0,255)
        if y < circle_radius +5: 
            y = circle_radius +5
            vy = -vy
            count += 1
            val1 = random.randint(0,255)
            val2 = random.randint(0,255)
            val3 = random.randint(0,255)
        if y > 600 - circle_radius -5: 
            y = 600 - circle_radius -5
            vy=-vy
            count += 1
            val1 = random.randint(0,255)
            val2 = random.randint(0,255)
            val3 = random.randint(0,255)

        if count % 10 == 0 and not growth_flag:
            circle_radius = circle_radius * 1.1  # Apply 10% growth
            vx = vx * 1.1
            vy = vy * 1.1
            growth_flag = True  # Set the flag to prevent further growth until the next condition

        if count % 10 != 0:
            growth_flag = False    

        absSpeed =  math.sqrt(vx**2 + vy**2)
        screen.fill((50, 50, 50))  # RGB for gray
        if not game_over:
            if count %2!=0:
            
                pygame.draw.circle(screen, (val1,val2,val3), (x, y), circle_radius)
                message = f"Bounces: {count} radius: {circle_radius:.2f} units speed: {absSpeed:.2f} units"
                text_surface = font.render(message, True, (255, 255, 255))  # White color for the text
                screen.blit(text_surface, (10, 10))  # Position the text at the top-left corner
            else:
            
                pygame.draw.circle(screen,(255, 0, 0), (x,y), circle_radius)
                message = f"Bounces: {count} radius: {circle_radius:.2f} units speed: {absSpeed:.2f} units"  # Example: display bounce count
                text_surface = font.render(message, True, (255, 255, 255))  # White color for the text
                screen.blit(text_surface, (10, 10))  # Position the text at the top-left corner

        else:
            # Game Over screen
            font = pygame.font.Font(None, 28)
            game_over_text = font.render(f"Simulation Over:   final radius: {circle_radius:.2f} Units!   final speed: {absSpeed:.2f} Units!", True, (255, 255, 255))
            screen.blit(game_over_text, (50,300))  # Position the text

        pygame.display.update()
        