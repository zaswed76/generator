import os
import sys
from functools import partial
from PyQt5 import QtWidgets, QtGui, QtCore

class ToolButton(QtWidgets.QPushButton):
    def __init__(self, icon, name, checkable=False, exclusive=False):
        super().__init__()
        self.setCheckable(checkable)
        self.setObjectName(name)
        self.setAutoExclusive(exclusive)
        # self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QtCore.QSize(28, 28))
        self.setFixedSize(28, 28)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                       QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)
        self.setCursor(QtCore.Qt.PointingHandCursor)

class GroupBox(QtWidgets.QGroupBox):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        self.setLayout(self.box)

    def addWidget(self, widget):
        self.box.addWidget(widget)

class Tool(QtWidgets.QFrame):
    def __init__(self, parent, height, icon_dir):
        super().__init__(parent)
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        self.icon_dir = icon_dir
        self.parent = parent
        self.setFixedHeight(height)
        self.btn = {}


    def addWidget(self, widget):
        self.box.addWidget(widget)

    def add_actions(self, actions, checkable=False, exclusive=False):
        for act_name in actions:
            icon = os.path.join(self.icon_dir, act_name)
            self.btn[act_name] = ToolButton(icon, act_name, checkable, exclusive)
            self.btn[act_name].clicked.connect(partial(self.press, act_name))
            self.addWidget(self.btn[act_name])

    def add_action(self, act_name, checkable=False, exclusive=False,
                   group=None, method=None ):
        icon = os.path.join(self.icon_dir, act_name)
        self.btn[act_name] = ToolButton(icon, act_name, checkable, exclusive)
        if method is None:
            self.btn[act_name].clicked.connect(partial(self.press, act_name))
        else:
            self.btn[act_name].clicked.connect(partial(self.press, method,
                                                       act_name))
        if group is None:
            self.addWidget(self.btn[act_name])
        else:
            group.addWidget(self.btn[act_name])

    def create_group(self):
        b = GroupBox()
        return b

    def set_group(self, group):
        self.box.addWidget(group)




    def press(self, act, *args):
        self.parent.controll(act, *args)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('settings/style.qss', "r").read())
    main = QtWidgets.QMainWindow()
    main.show()

    icon_dir = r'D:\0SYNC\python_projects\all_cubes\generator\programm\resource\icons'
    tool = Tool(main, 35, icon_dir)
    tool.add_actions(["images"])
    main.addToolBar(tool)
    sys.exit(app.exec_())