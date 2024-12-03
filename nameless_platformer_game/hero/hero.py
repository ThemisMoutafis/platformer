import pygame

class Hero:
    def __init__(self, vert, hor, color, sprite_walk_path=None,sprite_attack_path=None,sprite_jump_path=None) -> None:
        self.x = 30
        self.y = 230
        self.width = vert
        self.height = hor
        self.speed = 3
        self.gravity = 0.35
        self.velocity = 0
        self.jump_velocity = -11
        self.jumping = False
        self.move_right = False
        self.move_left = False
        self.rect = pygame.Rect(self.x, self.y, vert, hor)
        self.color = color
        self.current_frame = 0
        self.image = None
        self.frames = []
        self.jump_current_frame = 0
        self.jump_frames = []
        self.attack_current_frame = 0
        self.attack_frames = []
        self.flipped = False
        self.attack_flipped = False
        self.frame_delay = 3
        self.attack_frame_delay = 3
        self.jump_frame_delay = 12
        self.frame_counter = 0
        self.attacking = False
        self.attack_animation_done = False 
        
        if sprite_walk_path:
            self.frames = self.load_frames(sprite_walk_path)
        if sprite_attack_path:
            self.attack_frames = self.load_attack_frames(sprite_attack_path)
        if sprite_jump_path:
            self.jump_frames = self.load_jump_frames(sprite_jump_path)


    def load_frames(self, sprite_sheet_path):
        """Loads frames from a sprite sheet."""
        sheet = pygame.image.load(sprite_sheet_path)
        sheet = pygame.transform.scale(sheet, (self.width * 8, self.height))  # Scale to your frame width (8 frames in a row)

        frames = []
        for i in range(8):  # Since there are 6 frames in a row
            frame = sheet.subsurface(pygame.Rect(i * self.width, 0, self.width, self.height))
            frames.append(frame)
        
        return frames

    def load_attack_frames(self, sprite_sheet_path):
        """Loads frames from a sprite sheet."""
        sheet = pygame.image.load(sprite_sheet_path)
        sheet = pygame.transform.scale(sheet, (self.width * 6, self.height))  # Scale to your frame width (6 frames in a row)

        attack_frames = []
        for i in range(6):  # Since there are 6 frames in a row
            frame = sheet.subsurface(pygame.Rect(i * self.width, 0, self.width, self.height))
            attack_frames.append(frame)
        
        return attack_frames
    
    def load_jump_frames(self, sprite_sheet_path):
        """Loads frames from a sprite sheet."""
        sheet = pygame.image.load(sprite_sheet_path)
        sheet = pygame.transform.scale(sheet, (self.width * 5, self.height))  # Scale to your frame width (6 frames in a row)

        jump_frames = []
        for i in range(5):  # Since there are 5 frames in a row
            frame = sheet.subsurface(pygame.Rect(i * self.width, 0, self.width, self.height))
            jump_frames.append(frame)
        
        return jump_frames
    
    def draw(self, screen):
        """Draw the current frame on the screen, flipping if needed."""
        if self.attacking:
            if self.flipped:
                frame_to_draw = pygame.transform.flip(self.attack_frames[self.attack_current_frame], True, False)
            else:
                frame_to_draw = self.attack_frames[self.attack_current_frame]
            screen.blit(frame_to_draw, (self.x, self.y))  # Attack!    
        elif self.jumping:
            if self.flipped:
                frame_to_draw = pygame.transform.flip(self.jump_frames[self.jump_current_frame],True,False)
            else:
                frame_to_draw = self.jump_frames[self.jump_current_frame]
            screen.blit(frame_to_draw, (self.x, self.y))
        elif self.flipped:
            frame_to_draw = pygame.transform.flip(self.frames[self.current_frame], True, False)
            screen.blit(frame_to_draw, (self.x, self.y))
        elif self.frames:
            frame_to_draw = self.frames[self.current_frame]
            screen.blit(frame_to_draw, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        
        

    def handle_event(self, event):
        # Handle key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.move_right = True
                self.attack_flipped = False
            if event.key == pygame.K_LEFT:
                self.move_left = True
                self.attack_flipped = True
            if event.key == pygame.K_UP and not self.jumping and self.y == 230:
                self.jumping = True
                self.velocity = self.jump_velocity  # Jump strength
            if event.key == pygame.K_a and not self.attacking:
                self.attacking = True
                self.attack_flipped = self.move_left
                self.attack_animation_done = False  # Reset animation completion flag



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.move_right = False
            if event.key == pygame.K_LEFT:
                self.move_left = False
             # Do not reset attacking immediately upon key release
            if event.key == pygame.K_a:
                # Keep attacking until the animation is complete
                pass

    def move(self):
    # Handle jumping physics and animation first
        if self.jumping:
            self.jump_check()
        else:
            # Animate walking only if not jumping
            if self.move_right:
                self.animate()
            elif self.move_left:
                self.animate()

        # Apply horizontal movement regardless of jumping
        if self.move_right and self.x < 760:  # Screen boundary check
            self.flipped = False
            self.x += self.speed
        if self.move_left and self.x > -50:
            self.flipped = True
            self.x -= self.speed

        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y

        
    
            
    def animate(self):
        """Cycles through the frames for animation."""
        if self.jumping == False:
            self.frame_counter +=1
            if self.frame_counter >= self.frame_delay:
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0  # Loop back to first frame
                self.frame_counter = 0  # Reset the counter

    def animate_jump(self):
        """Select the appropriate jump frame based on the height and velocity."""
        if self.jumping:
            if self.velocity < -10:  # Strong upward movement
                self.jump_current_frame = 0  # Start of jump
            elif -10 <= self.velocity < -2:  # Slower upward movement
                self.jump_current_frame = 1  # Mid-jump (ascending)
            elif -2 <= self.velocity <= 2:  # Near the peak of the jump
                self.jump_current_frame = 2  # Top of the jump
            elif 2 < self.velocity <= 10:  # Descending
                self.jump_current_frame = 3  # Mid-jump (descending)
            elif self.y >= 230:  # Landed on the ground
                self.jump_current_frame = 4  # Landing

        

    def attack(self):
        if self.attacking:
            self.animate_attack()  # Animate attack frames
            if self.attack_current_frame == len(self.attack_frames) - 1:
                # If the attack animation is complete, stop attacking
                self.attacking = False
                self.attack_current_frame = 0  # Reset to first frame
                self.attack_animation_done = True  # Mark animation as complete

    def animate_attack(self):
        """Cycles through the attack frames for animation."""
        self.frame_counter += 1
        if self.frame_counter >= self.attack_frame_delay:
            self.attack_current_frame += 1
            if self.attack_current_frame >= len(self.attack_frames):
                self.attack_current_frame = 0  # Loop back to first frame
                if self.attack_current_frame == 0 and self.attack_animation_done:
                    self.attack_animation_done = True  # Mark animation as completed
            self.frame_counter = 0  # Reset the counter

    def jump_check(self):
        if self.jumping:
            self.y += self.velocity
            self.velocity += self.gravity
            self.animate_jump()  # Apply gravity
            if self.y >= 230:  # Collision with ground
                self.y = 230
                self.jumping = False
                self.velocity = 0
