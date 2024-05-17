import pygame

"""
	Helper object that returns a subset of an image.
	e.g. If there is an image that is huge, say 500x500,
	we can obtain a nxn image starting from a position. this helps me 
	get a specific part of an image and split them into their own frames,
	opposed to having multiple files of an image.
"""
class Spritesheet():
	def __init__(self, image):
		self.sheet = image

	# returns an image frame from a sprite sheet
	def get_image(self, width, height, scale, colour, frameCol=0, frameRow=0):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frameCol * width, frameRow * height, width, height)))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)
		return image