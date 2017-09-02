

import sys
from PyQt5 import QtWidgets

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(100, 100)
        self.button = QtWidgets.QPushButton('Button', self)
        self.button.clicked.connect(self.visible_lab)
        self.newLabel = QtWidgets.QLabel(self)
        self.newLabel.setText('Hellow Wrold')
        self.newLabel.move(10, 50)
        self.newLabel.setVisible(False)


    def visible_lab(self):
        self.newLabel.setVisible(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Widget()
    main.show()
    sys.exit(app.exec_())