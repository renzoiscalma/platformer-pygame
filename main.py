# Example file showing a circle moving on screen
import pygame as pg
from state import State

"""
    Runs the main loop of the game.
"""
if __name__ == '__main__':
    gameState = State()
    gameState.main_loop()