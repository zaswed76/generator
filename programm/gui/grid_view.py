
import os
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from gui import base_view

class View(QtWidgets.QGraphicsView):
    def __init__(self, name, scene, parent, size, *__args):
        super().__init__(*__args)
        self.setObjectName(name)
        self.setScene(scene)
        self.setFixedSize(size[0], size[1])
        # self.setStyleSheet("background-color: #C0E5BE")

    def wheelEvent(self, event):
        pass

class ImageGridBtn(QtWidgets.QPushButton):
    def __init__(self, image="", *__args):
        super().__init__(*__args)
        self.setIcon(image)
        self.setIconSize(QtCore.QSize(33, 33))
        s_police = QtWidgets.QSizePolicy.Expanding
        self.setSizePolicy(s_police, s_police)



class Grid(QtWidgets.QFrame):
    def __init__(self, image_dir, cfg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = cfg
        self.image_dir = image_dir
        self.grid_box = QtWidgets.QGridLayout(self)
        self.grid_box.setSpacing(0)
        self.grid_box.setContentsMargins(0, 0, 0, 0)
        self.btns = {}

    def create_grid(self):
        for x in range(10):
            for y in range(10):
                name = str(int("{}{}".format(x, y)))
                path_image = self.path_to_image(name)
                pixm = QtGui.QIcon(path_image)
                self.btns[name] = ImageGridBtn(image=pixm)
                self.grid_box.addWidget(self.btns[name], x, y)


    def path_to_image(self, name):
        p = os.path.join(self.image_dir, name + self.cfg["ext"])
        return p


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, geometry, cfg, image_dir, parent=None):
        super().__init__()
        self.setObjectName("grid")
        self.image_dir = image_dir
        self.cfg = cfg
        self.parent = parent
        self.setSceneRect(*geometry)
        self.grid = Grid(self.image_dir, self.cfg)
        self.grid.create_grid()
        self.grid.setFixedSize(500, 500)
        # self.frame.setStyleSheet("background-color: white")
        self.addWidget(self.grid)

    def draw(self, name, fabric):
        print("draw")


    def path_to_image(self, name):
        p = os.path.join(self.image_dir, name + self.cfg["ext"])
        return p
