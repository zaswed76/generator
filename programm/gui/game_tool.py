import sys
from functools import partial

from PyQt5 import QtWidgets, QtGui, QtCore
from gui import tool


class GameButton(tool.Button):
    def __init__(self, layout, name, checkable=False, exclusive=False,
                 icon=None, size=None, icon_size=None):
        super().__init__(layout, name, checkable=False,
                         exclusive=False,
                         icon=None, size=None, icon_size=None)
        self.setCheckable(checkable)
        self.setAutoExclusive(exclusive)


class GameTool(tool.Tool):
    def __init__(self, parent, name, direct, cfg):
        super().__init__(parent, name, direct)
        self.cfg = cfg
        self.parent = parent
        self.__init_ui()

    def __init_ui(self):
        self.add_group(self.group_seq_game)
        self.add_btn(self.exclusive)
        self.add_btn(self.reset)
        self.add_btn(self.all)
        self.add_stretch(1)

    @property
    def reset(self):
        reset = GameButton(self ,"reset_seq")
        reset.clicked.connect(self.parent.controls["seq_tool"])
        reset.setText("R")
        return reset

    @property
    def group_seq_game(self):
        group_seq_game = tool.Group("group_seq_game",
                                    tool.Box(tool.Box.vertical),
                                    exclusive=self.cfg["exclusive"])
        btn_names = self.cfg["btn_checked"]
        btns = self.get_seq_btns(
            btn_names, self, exclusive=self.cfg["exclusive"])
        group_seq_game.addWidgets(btns)

        for name, btn in group_seq_game.btn.items():
            btn.setChecked(self.cfg["btn_checked"][name])

        return group_seq_game

    @property
    def exclusive(self):
        exclusive = GameButton(self, "exclusive", checkable=True)
        exclusive.clicked.connect(self.parent.controls["seq_tool"])
        exclusive.setChecked(self.cfg["exclusive"])
        exclusive.setText("E")
        return exclusive

    @property
    def all(self):
        all = GameButton(self, "all_seq_btns")
        all.clicked.connect(self.parent.controls["seq_tool"])
        all.setText("A")
        return all

    def get_seq_btns(self, btns_names: dict, layout,
                     exclusive=False) -> list:
        btns = []
        for name in btns_names:
            name = str(name)
            btn = GameButton(layout, name, checkable=True,
                             exclusive=exclusive)
            btn.clicked.connect(self.parent.controls["seq_tool"])
            # btn.setChecked(btns_names[name])
            btn.setText(name)
            btns.append(btn)
        return btns

    # def get_active_btn(self):
    #     for btn in self.groups["group_seq_game"].btn.values():
    #         if btn.isChecked():
    #             return




