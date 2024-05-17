from enum import Enum

"""
 Possible states for the player. Used when showing animation
"""
class PlayerState(Enum):
	IDLE = 0
	FALL = 1
	JUMP = 2
	RUN = 3