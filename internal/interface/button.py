import pygame

from .label import InterfaceLabel


class InterfaceButton(InterfaceLabel):
    def __init__(self, type, text, x, y, callback):
        super().__init__(type, text, x, y)

        self.callback = callback
        self.last_pressed = True

    def update(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        self.highlighted = hover and self.callback is not None

        super().update()

    def clicked(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())

        if hover and self.callback is not None:
            self.callback()