import os

from PyQt5 import QtCore, QtWidgets, uic

UI_DIR = '../gui/ui'


def set_time():
    set_time_widg = uic.loadUi(
        os.path.join(UI_DIR, "set_time.ui"))
    set_time_widg.setWindowModality(QtCore.Qt.ApplicationModal)
    return set_time_widg
