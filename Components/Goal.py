import pygame as pg
from Components.Spritesheet import Spritesheet
from Enums import Goals
"""
	Class Goal is the items to collect per "view"
"""
class Goal(pg.sprite.Sprite):
	# static data members
	surface_types = {} 			# contains the sprites details of a goal type, 
	collected_surfaces = []	# contains the animation for the collected animation
	def __init__(self, xpos, ypos, type):
		super().__init__()
		# assign the surface type based on the enum passed
		self.surf = Goal.surface_types[type]['image'][0]
		# assign the rect based on the surf
		self.rect = self.surf.get_rect()
		# place position of goal in screen, based on passed parameters
		self.rect.center = (xpos, ypos)
		# define collision rectangle for this object
		self.collideRect = pg.Rect((0, 0), (32, 32))
		self.collideRect.center = self.rect.center
		# type of goal
		self.goal_type = type
		# current frame of the animation
		self.frame_index = 0
		# animation speed for this object
		self.animation_speed = 0.2
		# tells if the object is collected
		self.collected = False
		# if object is ready for removal
		self.end = False

	"""
		A static method that intializes the surfaces needed for the collected animation	
	"""
	def init_collected_animation():
		ASSET_SIZE = 32
		collected_frames = 5
		collected_path = 'Assets/Goals/'
		collected_name = 'Collected.png'
		# build path for the animation, and load the spritesheet
		image = pg.image.load(collected_path + collected_name)
		# instantiate the spritesheet object for easy access of per frame surface
		spritesheet = Spritesheet(image)
		# for each frame in the sprite sheet image
		for frame in range(collected_frames):
			# get nth frame of the image
			collected_frame = spritesheet.get_image(ASSET_SIZE, ASSET_SIZE, 2, (0, 0, 0), frame)
			Goal.collected_surfaces.append(collected_frame)
		
	"""
		A static method that initializes the surfaces needed for the goal. (Basically, the fruit shown in the view)
	"""
	def init_surfaces_per_type():
		ASSET_SIZE = 32
		goal_path = 'Assets/Goals/'
		# define dictionary for easy acess of image frames and looping
		Goal.surface_types = {
			Goals.CHERRIES: {
				'frames': 17,
				'path': "Cherries.png",
				'image': [],
				'spritesheet': None
			},
			Goals.KIWI: {
				'frames': 17,
				'path': "Kiwi.png",
				'image': [],
				'spritesheet': None
			},
			Goals.MELON: {
				'frames': 17,
				'path': "Melon.png",
				'image': [],
				'spritesheet': None
			},
		}
		# for each dictionary key in surface_types
		for surface_type in Goal.surface_types:
			# define currently selected value with the key
			type_props = Goal.surface_types[surface_type]
			# load the image
			image = pg.image.load(goal_path + type_props['path']).convert_alpha()
			# make the image into a spritesheet class
			spritesheet = Spritesheet(image)
			# assign spritesheet to spritesheet value
			type_props['spritesheet'] = spritesheet
			# iterate for the amount of frames in the spritesheet
			for frame in range(type_props['frames']):
				# get the specific frame in the spritesheet
				type_props['image'].append(spritesheet.get_image(ASSET_SIZE, ASSET_SIZE, 2, (0, 0, 0), frame))

	# Sets this object to collected and prepares for collected animation
	def collect(self):
		self.collected = True
		self.frame_index = 0
	# Called when main loop is updating
	def update(self):
		self.animate()
	# Update animations for this object
	def animate(self):
		# if this object is collected
		if self.collected:
			# use collected animation
			animations = Goal.collected_surfaces
			# increase frame index based on animation speed (animation speed is float)
			self.frame_index += self.animation_speed
			# if index is not going to overflow
			if (self.frame_index < 5):
				# update surface
				self.surf = animations[int(self.frame_index)]
			else:
				# prepare object to be not shown on the map
				self.end = True
		else:
			# if not collected, repeat animations per frame
			animations = Goal.surface_types[self.goal_type]['image']
			self.frame_index += self.animation_speed
			if (self.frame_index >= 17):
				self.frame_index = 0
			else:
				self.surf = animations[int(self.frame_index)]
		