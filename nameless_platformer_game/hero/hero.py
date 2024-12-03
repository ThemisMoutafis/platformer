import pygame
from Hero_states import HeroState as state


class Hero:
    def __init__(self, vert, hor, color, sprite_walk_path=None,sprite_attack_path=None,sprite_jump_path=None,sprite_defense_path=None,sprite_idle_path =None) -> None:
        ### hero attributes ###
        self.x = 400
        self.y = 300 
        self.inity = self.y
        self.width = vert
        self.height = hor
        self.speed = 3
        self.gravity = 0.30
        self.velocity = 0
        self.jump_velocity = -8
        self.rect = pygame.Rect(self.x, self.y, vert, hor) 
        self.color = color # if rectangle
        ########################
        ###### initial stuff, bool checks used for logic #########
        self.jumping = False
        self.attacking = False
        self.defending = False
        self.move_right = False
        self.move_left = False
        self.idle = True

        self.state = state.IDLE    ##### toDo , replace all instances of states with the enum State.

        self.flipped = False
        self.attack_animation_done = False 
        self.defense_animation_done = False
        ########################
        ###### frames ##########
        self.walk_frames = []
        self.jump_frames = []
        self.attack_frames = []
        self.defense_frames = []
        self.idle_frames = []
        self.current_walk_frame = 0
        self.jump_current_frame = 0
        self.attack_current_frame = 0
        self.defense_current_frame = 0
        self.idle_current_frame = 0
        self.frame_delay = 3
        self.idle_frame_delay = 6
        self.attack_frame_delay = 3
        self.defense_frame_delay = 5
        self.jump_frame_delay = 12
        self.frame_counter = 0
        ####################################
        # loading sprites #
        self.walk_frames = self.load_frames(sprite_walk_path,8)
        self.attack_frames = self.load_frames(sprite_attack_path,6)
        self.jump_frames = self.load_frames(sprite_jump_path,5)
        self.defense_frames = self.load_frames(sprite_defense_path,6)
        self.idle_frames = self.load_frames(sprite_idle_path,7)

        #####################################
    def set_state(self, state: state):
        self.state = state

    def load_frames(self, sprite_path, frame_number):
        """
        Loads individual frames from a sprite sheet image.

        Args:
            sprite_path (str): The file path to the sprite sheet image.
            frame_number (int): The number of frames to extract from the sprite sheet.

        Returns:
            list: A list of Pygame surfaces, each representing an individual frame.
            Returns an empty list(len = 0) if no path is provided.
        """
        if sprite_path is None:
            return []

        sheet = pygame.image.load(sprite_path)
        
        # Get the width of each frame by dividing the sprite sheet's width by the number of frames
        frame_width = (sheet.get_width() // frame_number)
        
        # The frames should have the original height of the sprite sheet
        frame_height = sheet.get_height()
        
        frames = []
        
        for i in range(frame_number):
            # Extract each frame using the correct dimensions
            frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames

    
    def draw(self, screen):
        """Draw the current frame on the screen, flipping if needed."""
        frame_to_draw = None
        # Choose the appropriate frame based on state
        if self.attacking  and self.attack_frames:
            frame_to_draw = self.attack_frames[self.attack_current_frame]
        elif self.jumping and self.jump_frames:
            frame_to_draw = self.jump_frames[self.jump_current_frame]
        elif self.defending and self.defense_frames:
            frame_to_draw = self.defense_frames[self.defense_current_frame]
        elif (self.move_right or self.move_left) and self.walk_frames:
            frame_to_draw = self.walk_frames[self.current_walk_frame]
        elif self.idle and self.idle_frames:
            frame_to_draw = self.idle_frames[self.idle_current_frame]
        
        # Flip the frame if the character is facing left
        if frame_to_draw:
            if self.flipped:
                frame_to_draw = pygame.transform.flip(frame_to_draw, True, False)

            # Draw the frame
            screen.blit(frame_to_draw, (self.x, self.y))

        # If no frame selected, draw a colored rectangle for the blob (fallback)
        if not frame_to_draw:
            rect_surface = pygame.Surface((self.width, self.height))
            rect_surface.fill(self.color)
            screen.blit(rect_surface, (self.x, self.y))


            
    def handle_event(self, event):
        # Handle key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or (event.key == pygame.K_RIGHT and event.key== pygame.K_d):
                self.move_right = True
                self.attack_flipped = False
                self.idle = False  # Not idle anymore when moving
            if event.key == pygame.K_LEFT or (event.key == pygame.K_LEFT and event.key== pygame.K_d):
                self.move_left = True
                self.attack_flipped = True
                self.idle = False  # Not idle anymore when moving
            if event.key == pygame.K_UP and not self.jumping and self.y == 300:
                self.jumping = True
                self.velocity = self.jump_velocity  # Jump strength
                # self.idle = False  # Not idle when jumping
            if event.key == pygame.K_a and not self.attacking:
                self.attacking = True
                self.attack_flipped = self.move_left
                self.attack_animation_done = False  # Reset animation completion flag
                # self.idle = False  # Not idle when attacking
            if event.key == pygame.K_d and not self.defending:
                if not (self.move_left or self.move_right):
                    self.defending = True
                    self.defense_flipped = self.move_left
                    self.defense_animation_done = False  # Reset animation completion flag
                    # self.idle = False  # Not idle when defending

    # Handle key release events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.move_right = False
            if event.key == pygame.K_LEFT:
                self.move_left = False
            if event.key == pygame.K_UP:
                # Jumping will be stopped by other logic (gravity and landing checks)
                pass
            if event.key == pygame.K_a:
                # Keep attacking until the animation is complete
                pass
            if event.key == pygame.K_d:
                pass

            # If no movement or actions are happening, set idle to True
            if not self.jumping and not self.attacking and not self.defending and not (self.move_right or self.move_left):
                self.idle = True

    def move(self):
    # Lets jumping animation finish first.
        if self.jumping:
            self.jump()
        if self.defending:
            return
        elif self.move_right:
                self.animate_walk()
                self.idle = False
        elif self.move_left:
                self.animate_walk()
                self.idle = False
        elif self.idle:
            self.animate_idle()
        # Apply horizontal movement regardless of jumping
        if self.move_right and self.x < 760:  # Screen boundary check
            self.flipped = False
            self.x += self.speed
        if self.move_left and self.x > -50:
            self.flipped = True
            self.x -= self.speed
    
    def animate_idle(self):
        """Cycles through the frames for animation."""
        if self.idle == True:
            if len(self.idle_frames) > 0:
                self.frame_counter +=1
                if self.frame_counter >= self.frame_delay:
                    self.idle_current_frame += 1
                    if self.idle_current_frame >= len(self.idle_frames):
                        self.idle_current_frame = 0  # Loop back to first frame
                    self.frame_counter = 0  # Reset the counter
    def animate_walk(self):
        """Cycles through the frames for animation."""
        if self.jumping == False:
            if len(self.walk_frames) > 0:
                self.frame_counter +=1
                if self.frame_counter >= self.frame_delay:
                    self.current_walk_frame += 1
                    if self.current_walk_frame >= len(self.walk_frames):
                        self.current_walk_frame = 0  # Loop back to first frame
                    self.frame_counter = 0  # Reset the counter

    def attack(self):
        if self.attacking:
            self.animate_attack()  # Animate attack frames
            if self.attack_current_frame == len(self.attack_frames) - 1:
                # If the attack animation is complete, stop attacking
                self.attacking = False
                self.attack_current_frame = 0  # Reset to first frame
                self.attack_animation_done = True  # Mark animation as complete
                self.idle = True  # Set idle to True once attack is complete

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
    
    def defend(self):
            if self.defending:
                self.move_left = False
                self.move_right = False
                self.idle = False
                self.animate_defense()  # Animate defense frames
                if self.defense_current_frame == len(self.defense_frames) - 1:
                    # If the defense animation is complete, stop defending
                    self.defending = False
                    self.defense_current_frame = 0  # Reset to first frame
                    self.defense_animation_done = True  # Mark animation as complete
                    self.idle = True
    def animate_defense(self):
        """Cycles through the defense frames for animation."""
        if self.defending:
            self.frame_counter += 1
            if self.frame_counter >= self.defense_frame_delay:
                self.defense_current_frame += 1
                if self.defense_current_frame >= len(self.defense_frames):
                    self.defense_current_frame = 0  # Loop back to first frame
                    # Only set animation as complete after finishing the full loop
                    if not self.defense_animation_done:
                        self.defense_animation_done = True  # Mark animation as completed
                self.frame_counter = 0  # Reset the counter


    def jump(self):
        if self.jumping:
            self.y += self.velocity
            self.velocity += self.gravity
            self.animate_jump()  # Apply gravity
            if self.y >= self.inity:  # Collision with ground
                self.y = self.inity
                self.jumping = False
                self.velocity = 0
                self.idle = True
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
            elif self.y >= 300:  # Landed on the ground
                self.jump_current_frame = 4  # Landing
