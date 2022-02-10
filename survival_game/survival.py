# Logan Morris
# Python survival tutorial game
# Source: https://realpython.com/pygame-a-primer/
# 31 December 2021

# Import the pygame module
import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen (width height)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a Player object extending Sprite
# Surface drawn on screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
  # Constructor drawing the player object
  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.image.load("jet.png").convert()
    self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.surf.get_rect()
  
  # Move sprite based on keys pressed
  # move_ip is 'move in place'
  def update(self, pressed_keys):
    if pressed_keys[K_UP]:
      self.rect.move_ip(0, -5)
      move_up_sound.play()
    if pressed_keys[K_DOWN]:
      self.rect.move_ip(0, 5)
      move_down_sound.play()
    if pressed_keys[K_LEFT]:
      self.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
      self.rect.move_ip(5, 0)
      
    # Keep the player on screen
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
      self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= SCREEN_HEIGHT:
      self.rect.bottom = SCREEN_HEIGHT

# Enemy object extending Sprite
# Surface drawn on screen is now an attribute of 'enemy'    
class Enemy(pygame.sprite.Sprite):
  # Constructor creating enemies at random positions on the right side of the
  # screen
  def __init__(self):
    super(Enemy, self).__init__()
    self.surf = pygame.image.load("missile.png").convert()
    self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    # Position and speed are randomly generated
    self.rect = self.surf.get_rect(
      center = (
        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        random.randint(0, SCREEN_HEIGHT)
      )
    )
    self.speed = random.randint(5, 20)
    
  # Move the sprite based on speed
  # Remove sprite when it crosses the left side of the screen
  def update(self):
    self.rect.move_ip(-self.speed, 0)
    if self.rect.right < 0:
      self.kill()
      
# Create the Cloud object by extending Sprite using an image
class Cloud(pygame.sprite.Sprite):
  def __init__(self):
    super(Cloud, self).__init__()
    self.surf = pygame.image.load("cloud.png").convert()
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    self.rect = self.surf.get_rect(
      center = (
        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        random.randint(0, SCREEN_HEIGHT)
      )
    )
    
  # Move the cloud at a constant speed
  # Remove the cloud when it passes the left edge of the screen
  def update(self):
    self.rect.move_ip(-5, 0)
    if self.rect.right < 0:
      self.kill()
      
# Setup for sounds with defaults
pygame.mixer.init()
      
# Initialize pygame
pygame.init()

# Create the screen object
# Size is determined by the constants declared above
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create a custom event for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Instantiate an object of the Player class. Currently is just a rectangle
player = Player()

# Create groups to hold enemy sprites as well as all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Loop control variable
running = True

# Control loop
while running:
  for event in pygame.event.get():
    # Was a key pressed?
    if event.type == KEYDOWN:
      # If it was the escape key, end the loop (exit)
      if event.key == K_ESCAPE:
        running = False
    
    # Did the user click the window close button? If yes, exit
    elif event.type == QUIT:
      running = False
      
    # Add a new enemy?
    elif event.type == ADDENEMY:
      # Create a new enemy and add it to the correct sprite groups
      new_enemy = Enemy()
      enemies.add(new_enemy)
      all_sprites.add(new_enemy)
      
    # Add a new cloud?
    elif event.type == ADDCLOUD:
      # Create a new cloud and add it to the correct sprite groups
      new_cloud = Cloud()
      clouds.add(new_cloud)
      all_sprites.add(new_cloud)
      
  # Get the list of keys pressed and check for user input
  pressed_keys = pygame.key.get_pressed()
  
  # Update player position based on key presses
  player.update(pressed_keys)
  
  # Update enemy and cloud positions
  enemies.update()
  clouds.update()
      
  # Set the background to sky blue
  screen.fill((135, 206, 250))

  # Draw all sprites
  for entity in all_sprites:
    screen.blit(entity.surf, entity.rect)
    
  # Check if any enemies have collided with the player
  if pygame.sprite.spritecollideany(player, enemies):
    # Stop any moving sounds and play the collision sound
    move_up_sound.stop()
    move_down_sound.stop()
    collision_sound.play()
    
    # If so, remove the player and stop the loop
    player.kill()
    running = False

  # Update the display
  pygame.display.flip()
  
  # Ensure program maintains a rate of 30fps
  clock.tick(60)
  
# Done! Stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()