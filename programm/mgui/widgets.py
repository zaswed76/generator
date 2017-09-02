import sys
from functools import partial

from PyQt5 import QtWidgets, QtGui, QtCore

_box_margin = (0, 0, 0, 0)
_box_spacing = 0

class Box(QtWidgets.QBoxLayout):
    horizontal = QtWidgets.QBoxLayout.LeftToRight = 0
    vertical = QtWidgets.QBoxLayout.TopToBottom = 2

    def __init__(self, direction, parent=None,
                 margin=_box_margin, spacing=_box_spacing):
        """
        :param direction: Box._horizontal \ Box._vertical
        :param QWidget_parent: QWidget
        :param margin: поле вокруг
        :param spacing: интервал (шаг) между виджетами
        """
        super().__init__(direction, parent)
        self.setDirection(direction)
        self.setContentsMargins(*margin)
        self.setSpacing(spacing)


    def addWidget(self, QWidget, stretch=0, Qt_Alignment=None, Qt_AlignmentFlag=None, *args, **kwargs):
        if self.direction() == Box.horizontal:
            super().addWidget(QWidget, alignment=QtCore.Qt.AlignLeft)
        elif self.direction() == Box.vertical:
            super().addWidget(QWidget, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)