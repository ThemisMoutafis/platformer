import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Interacting Surfaces')
clock = pygame.time.Clock()

# Hero settings
hero_pos = 30
hero_y_pos = 300
hero_speed = 3  # Horizontal movement speed
hero_jump = False
hero_velocity = 0  # Initial vertical velocity
hero_grav = 1  # Gravity strength


# Stages (list of dictionaries)
stages = [
    {"name": "Cozy Yellow", "color": (220, 190, 90)},  # Dark cozy yellow
    {"name": "Baby Blue", "color": (173, 216, 230)},  # Baby blue
    {"name": "Soft Green", "color": (180, 200, 140)},  # Soft greenish beige
    {"name": "Soft Orange", "color": (255, 170, 105)},  # warm gentle orange
]
current_stage_index = 0

# Assets
grass = pygame.Surface((800, 50))
grass.fill((85, 130, 85))  # Dark green

hero = pygame.Surface((10, 50))
hero.fill((255, 0, 0))  # Hero color (red)

hero_move_right = False
hero_move_left = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and hero_y_pos == 300:
                hero_jump = True
                hero_velocity = -15  # Jump strength
            if event.key == pygame.K_RIGHT:
                hero_move_right = True
            if event.key == pygame.K_LEFT:
                hero_move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                hero_move_right = False
            if event.key == pygame.K_LEFT:
                hero_move_left = False

      # Check for stage transition
    if hero_pos >= 790:
        current_stage_index = (current_stage_index + 1) % len(stages)  # Cycle through stages
        hero_pos = 0  # Reset hero position

  # Clear screen with current stage background
    current_stage = stages[current_stage_index]
    screen.fill(current_stage["color"])
    screen.blit(grass, (0, 350))

    font = pygame.font.SysFont(None, 36)
    stage_name_text = font.render(f"Stage: {current_stage_index}", True, (0, 0, 0))  # Black text
    screen.blit(stage_name_text, (10, 10))  # Draw the name at the top-left corner


    # Vertical movement
    if hero_jump:
        hero_y_pos += hero_velocity
        hero_velocity += hero_grav  # Apply gravity
        if hero_y_pos >= 300:  # Collision with ground
            hero_y_pos = 300
            hero_jump = False

    # Horizontal movement
    if hero_move_right and hero_pos < 790:  # Prevent moving past right edge
        hero_pos += hero_speed
    if hero_move_left and hero_pos > 0:  # Prevent moving past left edge
        hero_pos -= hero_speed

    # Draw hero
    screen.blit(hero, (hero_pos, hero_y_pos))
    pygame.display.update()
    clock.tick(60)
