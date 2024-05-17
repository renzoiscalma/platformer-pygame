# acts as the current state of the game, connects
# the player, and other entities and pygame
import pygame as pg
from Components import *
from Constants import *
from Enums import *

"""
  Contains the state of the game, the player, the blocks, and the goals for the game.
"""
class State():
  def __init__(self):
    pg.init()
    # intialize the screen with 1280x768 resolution
    self.screen = pg.display.set_mode((1280, 768))
    # initialize the player class
    self.player = Player()
    # initialize the static data members used for Platform and Goal
    Platform.init_surfaces_per_type()
    Goal.init_surfaces_per_type()
    Goal.init_collected_animation()
    # generate the entities per "view"
    self.entities_per_view = self.generate_entities()
    # current view of the game
    self.view = 0
    # number of goals collected
    self.num_collected = 0
    # max view possible for this world
    self.MAX_VIEW = len(self.entities_per_view) - 1

    # is pygame running?
    self.running = True
    # is the game completed?
    self.completed = False
    # is the player dead?
    self.player_dead = False
    # the delta time for each frame tick
    self.dt = 0
    # initialze the clock for the game
    self.clock = pg.time.Clock()
    # set the font used for the game
    self.font = pg.font.SysFont('Comic Sans MS', 30)


  """
    Main loop for the game, 
      - calls the events handler, 
      - calls the updates function
      - calls the draw function 
      PER FPS TICK
  """
  def main_loop(self):
    while self.running:
      self.events_handler()
      self.update()
      self.draw()
      # limits FPS to 60
      # dt is delta time in seconds since last frame, used for framerate-
      # independent physics.
      self.dt = self.clock.tick(FPS) / 1000
    pg.quit()
    
  """
    The main draw function for the game, fills the screen with the background,
    calls the draw function for each entity, and the draw function for the player
    Also draws the text when the game is completed or when the player is dead
  """
  def draw(self):
    # fill the screen with a color to wipe away anything from last frame
    self.screen.fill("cornflowerblue")
    # draw the player
    self.screen.blit(self.player.surf, self.player.rect)
    # draw the blocks and the goals
    for entity in self.entities_per_view[self.view]:
       if not isinstance(entity, Goal) or not entity.end:
        self.screen.blit(entity.surf, entity.rect)
    # if the game is completed
    if (self.completed):
       game_finished_text = self.font.render("Game Finished!", True, (255, 255, 255))
       # coordinate of the game finished text; half of screen - half of text length
       gf_x = self.screen.get_width() / 2 - game_finished_text.get_rect().width / 2
       # half of height
       gf_y = self.screen.get_height() / 2 - game_finished_text.get_rect().height / 2
       restart_text = self.font.render("Press R to restart", True, (255, 255, 255))
       # coordinate of the restart message; below the game finished text
       rt_x = self.screen.get_width() / 2 - restart_text.get_rect().width / 2
       rt_y = self.screen.get_height() / 2 - restart_text.get_rect().height / 2 + game_finished_text.get_rect().height
       # draw the text
       self.screen.blit(game_finished_text, (gf_x, gf_y))
       self.screen.blit(restart_text, (rt_x, rt_y))

    if (self.player_dead):
       game_over_text = self.font.render("Game Over!", True, (255, 255, 255))
       # coordinate of the game over text; which is at the half of screen - half of text length
       go_x = self.screen.get_width() / 2 - game_over_text.get_rect().width / 2
       # half of height
       go_y = self.screen.get_height() / 2 - game_over_text.get_rect().height / 2
       restart_text = self.font.render("Press R to restart", True, (255, 255, 255))
       # coordinate of teh restart message; below the game over text
       rt_x = self.screen.get_width() / 2 - restart_text.get_rect().width / 2
       rt_y = self.screen.get_height() / 2 - restart_text.get_rect().height / 2 + game_over_text.get_rect().height
       # draw the text
       self.screen.blit(game_over_text, (go_x, go_y))
       self.screen.blit(restart_text, (rt_x, rt_y))
    # display instructions
    direction_text = self.font.render("Press a or d to move or space to jump.", True, (255, 255, 255))
    self.screen.blit(direction_text, (20, 20))
    # display the blitted surfaces
    pg.display.flip()

  """
    Calls the necessary update functions for animations, physics calculation of the main character
  """
  def update(self):
    for entity in self.entities_per_view[self.view]:
       entity.update()
    self.player.update(self.dt, self)

  """
    Handles the keypresses made by the used
  """
  def events_handler(self):
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            self.running = False
    # key actions, get the current key pressed
    keys = pg.key.get_pressed()
    if keys[pg.K_r]: # if key R is pressed, restart
       self.restart()
    if keys[pg.K_a]: # if key a is presed, player moves to left
        self.player.event_direction(Direction.LEFT)
    if keys[pg.K_d]: # if key d is pressed, player moves to right
        self.player.event_direction(Direction.RIGHT)
    if not keys[pg.K_a] and not keys[pg.K_d]: # stop the player if neither keys are pressed
        self.player.stop()
    if keys[pg.K_SPACE]: # make the player jump when space is pressed
       self.player.event_jump()
    if not keys[pg.K_SPACE]: # set jumped to false when space is NOT pressed 
       self.player.set_jumped(False)
  """
    Handles the generation of entities for the entire game,
    Loads from a map file
    Returns a 2d array that represents the platforms, and goal visible for a specific view
  """
  def generate_entities(self):
    # the offset placement of the blocks 
    baseOffset = 32
    # the size of the blocks
    size = 64
    # open World1.dat
    with open("Maps/World1.dat") as world_file:
      entities_per_view = []
      # read the first line to know how many "views" are in the screen
      views_count = world_file.readline().replace("\n", "")
      # loop for view amount of times
      for view in range(int(views_count)):
        # create a sprite group for the specific view
        entities_in_view = pg.sprite.Group()
        # for each row of the view
        # NOTE since the blocks are 64 pixels, and the height of the screen is 768, there will be 
        # 12 blocks per row of the screen. On the other  hand since the screen's width is 1280, 
        # there can be 20 blocks at most per row of the screen (if we divide each row and col by 64)
        for row in range(12):
          # split the line into array so we can easily loop through it
          cols = [*world_file.readline()]
          # for each col(index count) and character in cols array
          for col, entity in enumerate(cols):
            if entity == "G": # if character is G, it's a goal to collect
              # get the coordinates
              x_coor = size * col + baseOffset
              y_coor = size * row + baseOffset
              # add the entity into the entities in view
              entities_in_view.add(Goal(x_coor, y_coor, Goals(view)))
            # else if entity is not X and not a new line, it must be a platform
            elif entity != "X" and entity != "\n":
              # compute the placement of the platform
              x_coor = size * col + baseOffset
              y_coor = size * row + baseOffset
              # add the platform into the entity list for this view
              entities_in_view.add(Platform(size, size, x_coor, y_coor, Platforms(int(entity))))
        # add the entities for this view
        entities_per_view.append(entities_in_view)
        # read the empty next line 
        world_file.readline()
    # return a 2d array that represents the platforms, goal, visible
    return entities_per_view
  
  """
    Returns the current entities based on the view
  """
  def get_entities(self):
     return self.entities_per_view[self.view]
  
  """
    Increments the view data member (when the player goes to the right most side of the screen)
  """
  def next_view(self):
     if self.view < self.MAX_VIEW:
        self.view += 1
  """
    Decrements the view data member (when the player goes to the left most side of the screen)
  """
  def prev_view(self):
     if self.view > 0:
        self.view -= 1
  
  """
    Set the state to completed
  """
  def game_end(self):
     self.completed = True

  """
    Set the state to game over
  """
  def game_over(self):
     self.player_dead = True

  """
    Restart the state for a new game
  """
  def restart(self):
    self.player = Player()
    self.entities_per_view = self.generate_entities()
    self.view = 0
    self.MAX_VIEW = len(self.entities_per_view) - 1
    self.num_collected = 0
    self.player_dead = False
    self.running = True
    self.completed = False
    self.dt = 0
  """
    Increment the number of collected goals
  """
  def add_collected(self, goal):
     self.num_collected += 1
     if self.num_collected > self.MAX_VIEW:
        self.game_end()