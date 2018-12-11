import pygame
from internal.game import Game
from internal.window import Window

if __name__ == '__main__':
    pygame.init()
    window = Window(1280, 768)
    window.set_title("Tower Defense")
    window.set_background(148, 168, 176)
    game = Game(window)
    game.run()
    pygame.quit()
