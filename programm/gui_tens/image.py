#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from functools import partial
NUL_GEOMETRY = 0.0

class Setting:
    rotate_mod = 3
    scale_mod = 0.005

    def get_rotate_mod(self):
        return self.rotate_mod

    def get_scale_mod(self):
        return self.scale_mod

    def set_rotate_mod(self, mod):
        self.rotate_mod = mod

    def set_scale_mod(self, mod):
        self.scale_mod = mod



class ImageItem(QtWidgets.QGraphicsPixmapItem):
    User_rotate = "set_rotate"
    User_increase = "set_scale_increase"
    User_decrease = "set_scale_decrease"
    User_mirror = "mirror"
    User_allow_edit = "allow_edit"
    User_disable_edit = "disable_edit"
    User_ability_change_edit = "ability_change_edit"

    def __init__(self, parent=None, scene=None, press_method=None, path=None, name=None,
                 edit=False, geometry=None, *__args):


        super().__init__(*__args)
        self.setting = Setting()
        self.rotate_mod = self.setting.get_rotate_mod()
        self.scale_mod = self.setting.get_scale_mod()
        self.parent = parent
        self.press_method = press_method
        self.name = name
        self.path = path
        self.edit = edit
        self.geometry = geometry
        if geometry is not None:
            self._x = self.geometry[0][0]
            self._y = self.geometry[0][1]
            self._scale = self.geometry[1]
            self._rotate = self.geometry[2]
            try:
                self._mirror = self.geometry[3]
            except IndexError:
                self._mirror = False
        else:
            self._x = NUL_GEOMETRY
            self._y = NUL_GEOMETRY
            self._scale = NUL_GEOMETRY
            self._rotate = NUL_GEOMETRY
            self._mirror = False

        # self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        # self.setTransformationMode(
        #     QtCore.Qt.SmoothTransformation)

        self.pixmap = self.get_pixmap(self.path)
        self.move_start()
        self.restart_geometry()
        self.draw()

        if self.edit:
            self.allow_edit()

    def __str__(self):
        return self.name

    def get_pixmap(self, path):
        return QtGui.QPixmap(self.path)

    def draw(self):
        self.setPixmap(self.pixmap)

    def allow_edit(self):
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable | \
            QtWidgets.QGraphicsItem.ItemIsSelectable | \
            QtWidgets.QGraphicsItem.ItemClipsToShape)

    # def disable_edit(self):
    #     self.setFlags(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

    # def ability_change_edit(self):
    #     self.edit = not self.edit
    #     if self.edit:
    #         self.allow_edit()
    #     else:
    #         self.disable_edit()

    @property
    def get_geometry(self):
        x, y = self.pos().x, self.pos().y()
        scale = self.scale()
        rotate = self._rotate
        mirror = self._mirror
        return [[x, y], scale, rotate, mirror]

    def mousePressEvent(self, event):
        print(3)
        self.setSelected(True)
        print(self.isSelected())



    def set_geometry_settings(self, x=NUL_GEOMETRY,
                              y=NUL_GEOMETRY,
                              scale=NUL_GEOMETRY,
                              rotate=NUL_GEOMETRY):
        self._x = x
        self._y = y
        self._scale = scale
        self._rotate = rotate

    def restart_geometry(self):
        self.setPos(self._x, self._y)
        self.setScale(self._scale)
        self.setRotation(self._rotate)
        self._load_mirror()

    def _load_mirror(self):
        if self._mirror:
            self.scale(-1, 1)

    @property
    def get_pixmap_size(self):
        width = self.pixmap.size().width()
        height = self.pixmap.size().height()
        return max(width, height)

    def move_start(self):
        size = self.get_pixmap_size
        s = size / 2
        self.setTransformOriginPoint(s, s)

    def set_rotate(self, **kwargs):
        delta = kwargs['delta']
        mod = self.rotate_mod
        if delta < 0:
            mod = -mod
        self._rotate += mod
        self.setRotation(self._rotate)

    def set_scale_increase(self, **kwargs):
        self._scale += self.scale_mod
        self.setScale(self._scale)

    def set_scale_decrease(self, **kwargs):
        self._scale -= self.scale_mod
        self.setScale(self._scale)

    def mirror(self):
        self.prepareGeometryChange()
        self.scale(-1, 1)
        if not self._mirror:
            self.moveBy(self.get_pixmap_size, 0)
            self._mirror = not self._mirror
        else:
            self.moveBy(-self.get_pixmap_size, 0)
            self._mirror = not self._mirror


