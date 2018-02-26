import sys
import os
from PyQt5 import QtWidgets, QtCore
from programm.gui import main as main_mod

ROOT = os.path.join(os.path.dirname(__file__))

CSS_DIR = os.path.join(ROOT, "css")
CFG_DIR = os.path.join(ROOT, "cfg")
INIT_GAME = os.path.join(CFG_DIR, "init_game.json")
DEFAULT_CFG = os.path.join(CFG_DIR, "default.json")
IMAGE_DIR = os.path.join(ROOT, "resource/image")
IMAGE_DIR_KEY = os.path.join(ROOT, "resource/images_key_2")


def main():
    QtCore.qDebug('something informative')
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open(os.path.join(CSS_DIR, "style.css"), "r").read())
    main = main_mod.Widget(init_game=INIT_GAME, default_cfg=DEFAULT_CFG,
                           image_dir=IMAGE_DIR,
                           image_dir_key=IMAGE_DIR_KEY)
    main.setObjectName('main_seq_game')
    main.show()

    controller = main_mod.ToolController(main, "top_tool")
    main.init_controller(controller)
    game_tool_controller = main_mod.GameToolController(main, "seq_tool")
    main.init_controller(game_tool_controller)
    main.init_top_tool()
    main.init_game_tool()

    main.new_game()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()