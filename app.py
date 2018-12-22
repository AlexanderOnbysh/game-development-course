import pygame

from internal.game import Game
from internal.window import Window

if __name__ == '__main__':
    pygame.init()
    window = Window((1280, 768))
    window.set_title("Space Defense")
    window.set_background(0, 0, 0)
    game = Game(window)
    game.run()
    pygame.quit()
