import pygame
from pygame.sprite import OrderedUpdates

from .button import Button
from .label import Label
from ..configurable import Configurable


class Interface(Configurable):
    def __init__(self, game):
        super().__init__("interface/interface", 0, 0)

        self.game = game
        self.components = OrderedUpdates()
        self.clear()
        self.show_main_screen()
        self.visible = True

    def show(self):
        self.visible = True
        self.show_main_screen()

    def hide(self):
        self.visible = False
        self.clear()

        self.defence_buttons = [Button("interface/interface_defence_button", self.game.defence_prototypes[i].display_name, (i + 1) * 64, 0, lambda: self.game.select_defence((pygame.mouse.get_pos()[0] - 64) // 64)) for i in range(len(self.game.defence_prototypes))]
        self.components.add(self.defence_buttons)

        self.wave_label = Label("interface/interface_pause_button", "Wave", 448, 0)
        self.lives_label = Label("interface/interface_pause_button", "Lives", 576, 0)
        self.money_label = Label("interface/interface_pause_button", "Money", 704, 0)
        self.score_label = Label("interface/interface_pause_button", "Score", 832, 0)
        self.components.add(self.wave_label)
        self.components.add(self.lives_label)
        self.components.add(self.money_label)
        self.components.add(self.score_label)

        self.components.add(Button("interface/interface_pause_button", "Interface", 1088, 0, self.show))

        self.update()

    def clear(self):
        self.components.remove(self.components)
        self.component_next = self.top

    def update(self):
        if not self.visible:
            self.wave_label.set_text("Wave: " + str(self.game.wave.number))
            self.lives_label.set_text("Lives: " + str(self.game.level.lives))
            self.lives_label.highlighted = (self.game.level.lives < 5)
            self.money_label.set_text("Money: " + str(self.game.level.money))
            self.score_label.set_text("Score: " + str(self.game.level.get_score()))

            for i in range(len(self.defence_buttons)):
                self.defence_buttons[i].disabled = (self.game.defence_prototypes[i].cost > self.game.level.money)
                self.defence_buttons[i].selected = (self.game.defence_type == i)
        
        self.components.update()

    def clicked(self):
        for component in self.components:
            if isinstance(component, Button):
                component.clicked()

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (0, 0))

        self.components.draw(screen)

    def add_button(self, text, callback):
        button = Button("interface/interface_button", text, 0, self.component_next, callback)
        button.rect.x = (self.rect.width - button.rect.width) / 2

        self.components.add(button)
        self.component_next += button.rect.height
        self.component_next += button.padding

        return button

    def add_level_button(self, level):
        button = Button("interface/interface_level_" + level, level, 0, self.component_next, lambda: self.game.load_level(level))
        button.rect.x = (self.rect.width - button.rect.width) / 2
        
        self.components.add(button)
        self.component_next += button.rect.height
        self.component_next += button.padding

    def show_main_screen(self):
        self.clear()

        self.add_button("Start Game", self.hide)
        if self.game.level.time > 0:
            self.add_button("Continue", self.hide)
            self.add_button("Restart Game", lambda: self.game.load_level(self.game.level.name))
        else:
            self.add_button("Start Game", self.hide)

        self.add_button("Change Level", self.show_change_level_screen)
        self.add_button("Quit Game", self.game.quit)

    def show_change_level_screen(self):
        self.clear()
        self.add_button("Back", self.show_main_screen)

        if self.game.level.name != "basic":
            self.add_level_button("basic")

        if self.game.level.name != "path":
            self.add_level_button("path")

        if self.game.level.name != "maze":
            self.add_level_button("maze")
