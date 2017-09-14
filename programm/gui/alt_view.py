import os
import json
from PyQt5 import QtWidgets, QtGui
from gui import base_view

GEOMETRY_CFG = '../cfg/base_geometry_dict.json'
GEOMETRY_CFG_ALT = '../cfg/alt_geometry.json'


def load_cfg(path):
    with open(path, "r") as f:
        return json.load(f)


def save(path, obj):
    with open(path, "w") as f:
        json.dump(obj, path)





class View(QtWidgets.QGraphicsView):
    def __init__(self, name, scene, parent, size, *__args):
        super().__init__(*__args)
        self.setObjectName(name)
        self.setScene(scene)
        self.setFixedSize(size[0], size[1])
        self.setStyleSheet("background-color: lightgrey")

    def wheelEvent(self, event):
        pass


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, geometry, cfg, image_dir, parent=None):
        super().__init__()
        self.image_dir = image_dir
        self.cfg = cfg
        self.parent = parent
        self.setSceneRect(*geometry)

    def draw(self, name, fabric):
        path = self.path_to_image(name)
        if fabric == 'image_mode_btn':
            obj = base_view.GraphicsImage(path, name, self)
            obj.to_center()
            self.addItem(obj)
        elif fabric == 'text_mode_btn':
            print("fabric == text_mode_btn")
        else:
            raise Exception("нет такого режима")


    def path_to_image(self, name):
        p = os.path.join(self.image_dir, name + self.cfg["ext"])
        return p
