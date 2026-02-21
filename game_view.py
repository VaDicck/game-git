import arcade
from constants import *
from arcade.camera import Camera2D
from sprites import Tux, Platform, CommitScroll


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        self.player = None
        self.platform_list = None
        self.wall_list = None
        self.player_list = None
        self.commit_list = None

        self.physics_engine = None

        self.camera = None

        # Фон
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.setup()

        self.setup_done = True

    def setup(self):

        # Создаём игрока
        self.player = Tux()
        self.player.center_x = 100
        self.player.center_y = 200
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.platform_list = arcade.SpriteList()

        self.commit_list = arcade.SpriteList()

        commit_positions = [
            (200, 300),
            (400, 400),
            (600, 500),
        ]

        for x, y in commit_positions:
            scroll = CommitScroll(x, y)
            self.commit_list.append(scroll)

        # Создаём пол
        for x in range(0, SCREEN_WIDTH, 64):
            platform = Platform(x, 100)
            self.platform_list.append(platform)

        # Создаём несколько платформ для прыжков
        platform_positions = [
            (200, 250, 128, 32),
            (400, 350, 128, 32),
            (600, 450, 128, 32),
        ]

        for x, y, width, height in platform_positions:
            platform = Platform(x, y, width, height)
            self.platform_list.append(platform)

        # Создаём физику
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.platform_list,
            gravity_constant=GRAVITY
        )

        self.camera = Camera2D()

        self.setup_done = True

    def on_draw(self):
        self.clear()

        if not self.setup_done:
            arcade.draw_text(
                "Загрузка...",
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                arcade.color.WHITE, 20, anchor_x="center"
            )
            return

        with self.camera.activate():
            self.platform_list.draw()
            self.commit_list.draw()  # ← новое
            self.player_list.draw()

        arcade.draw_text(
            f"Ветка: {self.player.current_branch} | Коммитов: {self.player.commits_collected}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 16
        )

        arcade.draw_text(
            "← → двигаться | Пробел прыжок",
            SCREEN_WIDTH - 250, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 12
        )

    def on_key_press(self, key, modifiers):
        if not self.setup_done or self.player is None:
            return

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.SPACE or key == arcade.key.W:
            # Прыжок только если на земле
            if self.physics_engine and self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if not self.setup_done or self.player is None:
            return

        if key == arcade.key.LEFT or key == arcade.key.A:
            if self.player.change_x < 0:
                self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if self.player.change_x > 0:
                self.player.change_x = 0

    def on_update(self, delta_time):
        if not self.setup_done or self.physics_engine is None:
            return

        hit_list = arcade.check_for_collision_with_list(
            self.player, self.commit_list
        )

        for scroll in hit_list:
            scroll.remove_from_sprite_lists()
            self.player.commits_collected += 1

        # Двигаем физику
        self.physics_engine.update()

        self.player_list.update()

        self.center_camera_on_player()

    def center_camera_on_player(self):
        if not self.setup_done or self.player is None:
            return

        screen_center_x = self.player.center_x - (SCREEN_WIDTH / 2)
        screen_center_y = self.player.center_y - (SCREEN_HEIGHT / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        self.camera.position = (screen_center_x, screen_center_y)