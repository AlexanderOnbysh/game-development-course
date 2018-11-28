from copy import deepcopy

import pygame
import yaml
from pygame.rect import Rect
from pygame.sprite import Sprite


class Configurable(Sprite):
    Cache = {}

    def __init__(self, name, x, y):
        super().__init__()

        self.name = name
        self.config = self.load_config(name)
        self.apply_config(self.config)

        if hasattr(self, "anim_source"):
            self.anim_change_time = self.anim_rate
            self.anim_index = 0
            self.image = self.anim_source[0]

        if hasattr(self, "image"):
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = Rect(x, y, 32, 32)

    @staticmethod
    def load_config(name):
        if name in Configurable.Cache.keys():
            return Configurable.Cache[name]

        with open(f'configs/{name}.yaml', 'r') as f:
            config = yaml.load(f)

        entries = deepcopy(config)

        for img_fmt in ('image', 'image_s', 'image_h', 'image_d'):
            if img_fmt in config:
                type = config[img_fmt]['type']
                if type == 'img':
                    entries[img_fmt] = pygame.image.load(config[img_fmt]['value']).convert()
                if type == 'aimg':
                    entries[img_fmt] = pygame.image.load(config[img_fmt]['value']).convert_alpha()

        if 'anim_source' in config:
            entries['anim_source'] = [pygame.image.load(config['anim_source'] + str(i) + ".png").convert_alpha()
                                      for i in range(entries["anim_count"])]

        if 'images' in config:
            original = pygame.image.load(config['images']).convert_alpha()
            entries['images'] = [original] + [pygame.transform.rotate(original, angle) for angle in range(5, 361, 5)]

        if 'font' in config:
            entries['font'] = pygame.font.Font(pygame.font.match_font(config['font'], 'font_bold' in entries.keys()), entries['font_size'])

        Configurable.Cache[name] = entries
        return entries

    def apply_config(self, config):
        for name in config.keys():
            setattr(self, name, config[name])
