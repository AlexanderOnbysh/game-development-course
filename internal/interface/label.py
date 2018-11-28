from ..configurable import Configurable


class InterfaceLabel(Configurable):
    def __init__(self, type, text, x, y):
        super().__init__(type, x, y)

        self.text = text
        self.image_template = None
        self.highlighted = False
        self.selected = False
        self.disabled = False
        self.set_image(self.image_selected)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.disabled:
            self.set_image(self.image_d)
        elif self.highlighted or self.selected:
            self.set_image(self.image_highlighted)
        else:
            self.set_image(self.image_selected)

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
        dest = ((background.get_rect().width - rendered.get_rect().width) // 2,
                (background.get_rect().height - rendered.get_rect().height) // 2)
        background.blit(rendered, dest)
