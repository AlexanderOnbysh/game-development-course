from internal.configurable import Configurable
from pygame.sprite import OrderedUpdates
import pygame


class Menu(Configurable):

    def __init__(self, game):
        super().__init__("Menu", 0, 0)

        self.game = game
        self.components = OrderedUpdates()
        self.clear()
        self.show_main_screen()
        self.visible = True

    def show(self):
        self.visible = True
        self.show_main_screen()

    def clear(self):
        self.components.remove(self.components)
        self.component_next = self.top

    def clicked(self):
        for component in self.components:
            if isinstance(component, MenuButton):
                component.clicked()

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (0, 0))

        self.components.draw(screen)

    def add_button(self, text, callback):
        button = MenuButton(self, "MenuButton", text, 0, self.component_next, callback)
        button.rect.x = (self.rect.width - button.rect.width) / 2

        self.components.add(button)
        self.component_next += button.rect.height
        self.component_next += button.padding

        return button

    def show_main_screen(self):
        self.clear()

        if self.game.level.time > 0:
            self.add_button("Continue", self.hide)
            self.add_button("Restart Game", lambda: self.game.load_level(self.game.level.name))
        else:
            self.add_button("Start Game", self.hide)

        self.add_button("Quit Game", self.game.quit)


class MenuLabel(Configurable):
    def __init__(self, type, text, x, y):
        super().__init__(type, x, y)

        self.text = text
        self.image_template = None
        self.highlighted = False
        self.selected = False
        self.disabled = False
        self.set_image(self.image_s)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        if self.disabled:
            self.set_image(self.image_d)
        elif self.highlighted or self.selected:
            self.set_image(self.image_h)
        else:
            self.set_image(self.image_s)

    def set_text(self, text):
        if self.text != text:
            self.text = text
            
            img = self.image_template
            self.image_template = None
            self.set_image(img)

    def set_image(self, image):
        if self.image_template == image:
            return

        self.image_template = image

        if hasattr(self, "font"):
            self.image = image.copy()
            self.render_text(self.image)
        else:
            self.image = image
           
    def render_text(self, background):
        colour = (self.color_red, self.color_green, self.color_blue)
        rendered = self.font.render(self.text, True, colour)
        dest = ((background.get_rect().width - rendered.get_rect().width) // 2, (background.get_rect().height - rendered.get_rect().height) // 2)
        background.blit(rendered, dest)


class MenuButton(MenuLabel):
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
