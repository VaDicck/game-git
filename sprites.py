import arcade
from constants import *

# Игрок
class Tux(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/images/Gaming_tux.png", scale=SPRITE_SCALING_PLAYER)

        # Физические свойства
        self.change_x = 0
        self.change_y = 0

        self.commits_collected = 0 # Количество собранных коммитов
        self.current_branch = "main"

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

class Platform(arcade.SpriteSolidColor):

    def __init__(self, x, y, width=64, height=32):
        super().__init__(width, height, PLATFORM_COLOR)

        self.center_x = x
        self.center_y = y


class CommitScroll(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("assets/images/Scroll.png", scale=0.05)

        self.center_x = x
        self.center_y = y