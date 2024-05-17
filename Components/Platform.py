import pygame as pg
from Components.Spritesheet import Spritesheet
from Enums import *

"""
  class of the platforms for the game. This builds a 64x64 block. 
"""
class Platform(pg.sprite.Sprite):
  # static variables, shared with other platforms.
  surface_types = []

  def __init__(self, width, height, xpos, ypos, type: Platforms):
    super().__init__()
    # assign this object's surface based on the given type
    self.surf = Platform.surface_types[int(type.value)]
    # get the rectangle of the surface and assign it to self.refct
    self.rect = self.surf.get_rect()
    # place the block in the desired position from the parameter
    self.rect.center = (xpos, ypos)
    # assign what type is the platform
    self.type = type

    if (type == Platforms.BLOCK):
      return (255, 0, 0)
    elif (type == Platforms.GROUND):
      return (255, 255, 0)
  
  # need to have update function so when entities are called on update
  def update(self):
    pass
  
  # do not pass self since we want this to be a static function to be called
  def init_surfaces_per_type():
    CELL_SIZE = 16
    PLATFORM_SIZE = 32
    SCALED_PLAT_SIZE = PLATFORM_SIZE * 2
    platform_file = 'Terrain (16x16).png'
    platform_path = 'Assets/Platform/'
    image = pg.image.load(platform_path + platform_file).convert_alpha()
    platform_spritesheet = Spritesheet(image)
    # building blocks for each surface of the platforms, each block is a 16x16 image that is a part of the image,
    # since we're using a spritesheet we have to only get a part of the image that is relevant to the block
    grass_left = platform_spritesheet.get_image(CELL_SIZE, CELL_SIZE, 1, (0, 0, 0), 6)
    grass_center = platform_spritesheet.get_image(CELL_SIZE, CELL_SIZE, 1, (0, 0, 0), 7)
    grass_right = platform_spritesheet.get_image(CELL_SIZE, CELL_SIZE, 1, (0, 0, 0), 8)
    ground_left = platform_spritesheet.get_image(CELL_SIZE, CELL_SIZE, 1, (0, 0, 0), 6, 1)
    ground_center = platform_spritesheet.get_image(CELL_SIZE, CELL_SIZE, 1, (0, 0, 0), 7, 1)
    ground_right = platform_spritesheet.get_image(CELL_SIZE, CELL_SIZE, 1, (0, 0, 0), 8, 1)

    # dict used for which building blocks are used for each platform
    # each platform property will have 4 building blocks
    # if we place the 4 building blocks as grid we come up with a 32x32 block, it is then scaled to become 64x64 
    platform_properties = {
      Platforms.GROUND: [grass_left, grass_right, ground_left, ground_right],
      Platforms.BLOCK: [],  # empty here since it's not really used. we can fill this up if I'm going to use this in the future
                            # i can't not add this here since it should match the Enum
      Platforms.GROUND_GRASS_LEFT: [grass_left, grass_center, ground_left, ground_center],
      Platforms.GROUN_GRASS_RIGHT: [grass_center, grass_right, ground_center, ground_right],
      Platforms.GROUND_GRASS_CENTER: [grass_center, grass_center, ground_center, ground_center],
      Platforms.GROUND_LEFT: [ground_left, ground_center, ground_left, ground_center],
      Platforms.GROUND_CENTER: [ground_center, ground_center, ground_center, ground_center],
      Platforms.GROUND_RIGHT: [ground_center, ground_right, ground_center, ground_right],
      Platforms.GROUND_GRASS_PATCH_LEFT: [],
      Platforms.GROUND_GRASS_PATCH_RIGHT: [],
    }
    # iterate over the property keys in in platform_property dictionary
    for prop_keys in platform_properties:
      # build a block
      platform_surface = pg.Surface((PLATFORM_SIZE, PLATFORM_SIZE))
      properties = platform_properties[prop_keys]
      # if there are properties, build it using the the building blocks 
      # blocks that aren't really needed and has no property will just be skipped
      if len(properties) > 0:
        platform_surface.blit(properties[0], (0, 0))  # get the first 16x16 block and place it at 0,0 coordinate (top left)
        platform_surface.blit(properties[1], (16, 0)) # get the second 16x16 block and place it at 16,0 coordinate (top right)
        platform_surface.blit(properties[2], (0, 16)) # get the 3rd 16x16 block andp place it at 0,16 coordinate (bottom   left)
        platform_surface.blit(properties[3], (16, 16))# get the 4th 16x16 block and place it 16,16 coordinate (bottom right)
        platform_surface = pg.transform.scale(platform_surface, # now that we have all the blocks in the surface, as 32x32 block we scale by 2x, resulting in a 64x64 block
                                              (SCALED_PLAT_SIZE, 
                                              SCALED_PLAT_SIZE))
      # place a block into the static variable
      Platform.surface_types.append(platform_surface)