# main.py

import arcade as arc
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from game_view import GameView


def main():
    window = arc.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    game_view = GameView()

    window.show_view(game_view) #показываем

    arc.run()


if __name__ == "__main__":
    main()