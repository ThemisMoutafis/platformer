import pygame
from hero.hero import Hero
from stages.data import stages, grass as gr, current_stage_index as csi

sprite_walk_path = "hero/sprites/WALK.png"
sprite_attack_path = "hero/sprites/ATTACK1.png"
sprite_jump_path = "hero/sprites/JUMP.png"
def stage_transition(x,c,stages):
    if x >= 760:
        c = (c + 1) % len(stages)  # Cycle through stages
        x = 0  # Reset hero position
    return x, c

pygame.init()
screen = pygame.display.set_mode((800, 400),pygame.NOFRAME)
pygame.display.set_caption('Demo version')
# icon = pygame.image.load("path_to_icon.png")
# pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Grass layer
grass = pygame.Surface(gr["surface"]["fill"])
grass.fill(gr["color"]["fill"])  # Dark green

#Stage and hero 
current_stage = stages[csi]
hero = Hero(160,160,'Red',sprite_walk_path,sprite_attack_path,sprite_jump_path)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
         # Pass events to the hero object 
        hero.handle_event(event)

    # Check for stage transition
    hero.x,csi = stage_transition(hero.x,csi,stages)
   
    # Hero logic

    hero.jump_check()
    hero.attack()
    hero.move()

    # Clear screen with current stage background
    current_stage = stages[csi]
    screen.fill(current_stage["color"])
    screen.blit(grass, (0, 350))

    font = pygame.font.SysFont(None, 36)
    stage_text = font.render(f"Stage: {csi+1}", True, (5, 66, 25))  # Black text
    stage_name_text = font.render(f"{stages[csi]["name"]}", True, (5, 66, 25))  # Black text
    screen.blit(stage_name_text, (15, 15))  # Draw the name at the top-left corner
    screen.blit(stage_text, (690, 15))  # Draw the name at the top-left corner

    # Draw hero
    hero.draw(screen)
    pygame.draw.rect(screen, (5, 66, 25), (0, 0, 800, 400), 10)  # Example white border
    pygame.display.flip()
    

    clock.tick(60)