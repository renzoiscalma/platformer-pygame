import pygame as pg
from Enums import *
from Constants import *
from .Spritesheet import Spritesheet
from .Goal import Goal
from .Platform import Platform

"""
  Class Player. 
"""
class Player(pg.sprite.Sprite):
  def __init__(self):
      super().__init__()
      # load assets of the player
      self.import_character_assets()
      # set initial state of the player to idle
      self.state = PlayerState.IDLE
      # size of player
      self.frame_index = 0
      # animation speed of the player
      self.animation_speed = 0.15
      # set the initial sprite of the player with the current frame index and state (idle and 0 by default)
      self.surf = self.animation_sprites[self.state]["image"][self.frame_index]
      # get the width and height of the surface
      self.rect = self.surf.get_rect()
      # position of player
      self.rect.center = (64 * 3, 64 * 10)
      # current speed of player
      self.velocity = pg.Vector2(0, 0)
      # is the player jumping
      self.jumped = False
      # is the player on the floor
      self.on_floor = False
      # is the player facing right
      self.facing_right = True

  def import_character_assets(self):
    ASSET_SIZE = 32
    character_path = 'Assets/Player/'
    idle_path = character_path + 'Idle (32x32).png'
    fall_path = character_path + 'Fall (32x32).png'
    jump_path = character_path + 'Jump (32x32).png'
    run_path = character_path + 'Run (32x32).png'
		# define dictionary for easy acess of image frames and looping
    self.animation_sprites = {
      PlayerState.IDLE: {
        'frames': 11,
        'path': idle_path,
        'image': [],
        'spritesheet': None
      },
      PlayerState.FALL: {
        'frames': 1,
        'path': fall_path,
        'image': [],
        'spritesheet': None
      },
      PlayerState.JUMP: {
        'frames': 1,
        'path': jump_path,
        'image': [],
        'spritesheet': None
      },
      PlayerState.RUN: {
        'frames': 12,
        'path': run_path,
        'image': [],
        'spritesheet': None
      },
    }
		# for each dictionary key in animation_sprites
    for animation_name in self.animation_sprites:
			# define currently selected value with the key
      anim_sprite = self.animation_sprites[animation_name]
      path = anim_sprite["path"]
      frames = anim_sprite["frames"]
      images = anim_sprite["image"]
      # load the image
      image = pg.image.load(path).convert_alpha()
      # load the image through spritesheet class
      spritesheet = Spritesheet(image)
      # store spritesheet into this animation's spritesheet property
      anim_sprite["spritesheet"] = spritesheet
      # for each frame in the image, store it into images[]
      for frame in range(frames):
        images.append(spritesheet.get_image(ASSET_SIZE, ASSET_SIZE, 1, (0, 0, 0), frame))

  def animate(self):
    animation = self.animation_sprites[self.state]
    self.frame_index += self.animation_speed
    if (self.frame_index >= animation["frames"]):
      self.frame_index = 0
    self.surf = animation["image"][int(self.frame_index)]
    if (not self.facing_right):
      # flip along X axis to face left
      self.surf = pg.transform.flip(self.surf, True, False).convert_alpha()


  def event_direction(self, direction):
    if direction == Direction.LEFT:
       self.velocity.x = -RUN_VELOCITY
    if direction == Direction.RIGHT:
       self.velocity.x = RUN_VELOCITY

  def event_jump(self):
    if self.on_floor and not self.jumped:
      self.velocity.y = -JUMP_VELOCITY
      self.on_floor = False
  """
    Updates the current state of the object, called by the main state
  """
  def update(self, dt, state):
    # if player fell through a hole
    if (self.rect.top >= pg.display.get_surface().get_height()):
      state.game_over()
    # check if going to next screen
    if self.velocity.x > 0 and self.rect.right > pg.display.get_surface().get_width():
      if state.view >= state.MAX_VIEW: # if player is at last view
        self.rect.right = pg.display.get_surface().get_width()
      else:
        state.next_view()              # else go to previous view
        self.rect.x = 2                # place the player on the right most side of the screen
    # check if player can go to previous screen
    if self.velocity.x < 0 and self.rect.x < 0:
      if state.view == 0:           # if player is at first view
        self.rect.left = 0
      else:                         # else increment view
        state.prev_view()
        self.rect.x = pg.display.get_surface().get_width() - 2  # place the player on the left most side of the screen

    # handle x-axis displacements
    dx = (self.velocity.x * dt)
    self.rect.x += dx
    self.handle_horizontal_collisions(state)
    # handle y-axis displacements
    self.velocity.y += FALL_VELOCITY
    dy = (self.velocity.y * dt)
    self.rect.y += dy
    self.handle_vertical_collisions(state)

    self.update_state()
    self.animate()

  def stop(self):
    self.velocity.x = 0

  """
    Handles the horizontal collision, basically avoiding to go through platforms and collect goals
  """
  def handle_horizontal_collisions(self, state):
    # check if colliding with entities (either a goal or a platform)
    for entity in state.get_entities():
      # if collided with a goal
      if isinstance(entity, Goal) and self.rect.colliderect(entity.collideRect) and not entity.collected:
        entity.collect()                            # update goal state
        state.add_collected(entity)                 # mark the goal as collected
      elif isinstance(entity, Platform) and self.rect.colliderect(entity.rect):
        if (self.velocity.x < 0):                   # if player is going left
          self.rect.left = entity.rect.right        # set the player beside the platform
        elif self.velocity.x > 0:                   # if player is going right
          self.rect.right = entity.rect.left        # set the player beside the platform
  """
    Handles the vertical collision, basically avoiding to go through platforms and collect goals
  """
  def handle_vertical_collisions(self, state):
    # check if colliding with entities (either a goal or a platform)
    for entity in state.get_entities():
      # if collided with a goal
      if isinstance(entity, Goal) and self.rect.colliderect(entity.collideRect) and not entity.collected:
        entity.collect()                      # update goal state
        state.add_collected(entity)           # mark the goal as collected
      elif isinstance(entity, Platform) and self.rect.colliderect(entity.rect):
        if self.velocity.y < 0:     # if the player is going up and collided with a platform
          self.rect.top = entity.rect.bottom  # set the player below of the platform
          self.velocity.y = 0                 
        elif self.velocity.y > 0:   # if player is going down and collided with a platform
          self.rect.bottom = entity.rect.top # set the player on top of the platform
          self.velocity.y = 0
          self.on_floor = True
  
  """
    Updates the jumped data member with the value passed
  """
  def set_jumped(self, value):
    self.jumped = value

  """
    Updates the state of the player based on conditions,
    sets if player is idle if not moving, runnning, jumping, or falling
  """
  def update_state(self):
    if self.on_floor and self.velocity.x == 0.0:        # if player is on floor and velocity is 0
      self.state = PlayerState.IDLE
    elif self.on_floor and self.velocity.x is not 0:    # if player is on floor and velocity is not 0
      self.state = PlayerState.RUN
    elif not self.on_floor and self.velocity.y > 0:     # if player is going down
      self.state = PlayerState.FALL
    elif not self.on_floor and self.velocity.y < 0:     # if player is going up
      self.state = PlayerState.JUMP

    if self.velocity.x < 0:                             # if player is going left
      self.facing_right = False
    else:
      self.facing_right = True                          # if player is going right
    