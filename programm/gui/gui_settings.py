import os

from PyQt5 import QtCore, QtWidgets, uic

UI_DIR = '../gui/ui'

class SetTime(QtWidgets.QDialog):
   def __init__(self, time_interval, *args, **kwargs):
      super().__init__(*args, **kwargs)
      uic.loadUi(
        os.path.join(UI_DIR, "set_time.ui"), self)
      self.setWindowModality(QtCore.Qt.ApplicationModal)
      self.slider.setValue(time_interval)
      # self.btnOk





