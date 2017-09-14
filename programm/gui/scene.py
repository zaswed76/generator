

import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, geometry, cfg, image_dir, parent=None):
        super().__init__()
        self.image_dir = image_dir
        self.cfg = cfg
        self.parent = parent
        self.setSceneRect(*geometry)

