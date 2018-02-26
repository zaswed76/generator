

import sys
from PyQt5 import QtCore


class Timer(QtCore.QTimer):
    def __init__(self):
        super().__init__()