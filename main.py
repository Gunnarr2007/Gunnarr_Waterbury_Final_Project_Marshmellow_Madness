# This file was created by Gunnarr Waterbury

'''
Goals:
make a shooter that is multiplayer maybe vs or a co-op
add respawning mobs and new areas
make the player try and get something 
add dif weapons

will use:

randint 
math 
pygame or other screem 
and other most likely 


Source:
https://www.techwithtim.net/tutorials/python-online-game-tutorial
https://medium.com/@DakaiZhou/generate-random-location-coordinates-within-given-area-with-python-1d6e62b6e382
https://quintagroup.com/cms/python/cocos2d#:~:text=It%20is%20written%20in%20Python%20using%20pyglet%20library.,can%20also%20contain%20other%20sprites.
https://www.youtube.com/watch?v=wicgBgZIUQA&list=PL1P11yPQAo7p_mEAk8Q8FNYVutIc58eXe&index=1

'''

import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Character Game")

# Load background image
background_path = os.path.join(os.path.dirname(__file__), "background.jpg")
if not os.path.exists(background_path):
    print(f"Error: {background_path} not found.")
    pygame.quit()
    sys.exit()

background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (width, height))

# Set up game clock
clock = pygame.time.Clock()

# Define the path to the character image so that it can get displayed
image_path = os.path.join(os.path.dirname(__file__), "character.png")

# Check if the image file exists so that it does not break
if not os.path.exists(image_path):
    print(f"Error: {image_path} not found.")
    pygame.quit()
    sys.exit()

# Create a class for the Player to define everything
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.speed = 5

    def update(self):
        # Update player position based on key input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

# Create a class for Mobs
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = random.uniform(2, 4)

    def update(self):
        # Update mob position, reset if it goes off-screen
        self.rect.y += self.speed
        if self.rect.top > height:
            self.rect.y = 0
            self.rect.x = random.randint(0, width)

# Create a class for Projectiles
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((0, 0, 255))  # Projectile color (blue)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 7

    def update(self):
        # Update projectile position
        self.rect.y -= self.speed

# Create instances of the classes
player = Player()
mobs = pygame.sprite.Group(Mob(random.randint(0, width), random.randint(0, height)))
projectiles = pygame.sprite.Group()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update player
    player.update()

    # Handle player shooting
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        projectile = Projectile(player.rect.centerx, player.rect.top)
        projectiles.add(projectile)

    # Update mobs
    mobs.update()

    # Check for collisions between projectiles and mobs
    collisions = pygame.sprite.groupcollide(projectiles, mobs, True, False)
    for projectile, mob_group in collisions.items():
        for mob in mob_group:
            # Handle the collision (e.g., remove the mob)
            mob.rect.y = 0
            mob.rect.x = random.randint(0, width)

    # Update projectiles
    projectiles.update()

    # Draw background
    screen.blit(background, (0, 0))

    # Draw player
    screen.blit(player.image, player.rect)

    # Draw mobs
    mobs.draw(screen)

    # Draw projectiles
    projectiles.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)