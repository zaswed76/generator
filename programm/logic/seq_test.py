
from programm.logic import logic

ITEMS_WEIGHT = "../cfg/items_weight.yaml"

from programm.logic.logic import Seq
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class Widget(QtWidgets.QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.resize(500, 500)
        self.setStyleSheet("color: #6F6F6F")
        font = QtGui.QFont("helvetica", 56)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignCenter)


        self.logic = Seq(range(100))
        # self.logic.shuffle = True
        # self.logic.cycle = True

    def new_game(self):
        self.logic.init_seq([0])
        self.logic.cursor_reset()



    def draw_next(self):
        v, c = self.logic.next()
        if c:
            self.setText(v)
        else:
            self.setText("Finish")

    def draw_prev(self):
        v, c = self.logic.prev()
        self.setText(v)

    def wheelEvent(self, event):
        if event.angleDelta().y() / 120 > 0:
            self.draw_next()
        else:
            self.draw_prev()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_N:
            self.new_game()
            self.draw_next()
        elif e.key() == QtCore.Qt.Key_F:
            self.logic.shuffle = True
            self.logic.cursor_reset()
            self.draw_next()
        elif e.key() == QtCore.Qt.Key_S:
            self.logic.shuffle = False
            self.logic.cursor_reset()
            self.draw_next()
        elif e.key() == QtCore.Qt.Key_C:
            self.logic.cycle = True
            self.logic.cursor_reset()
            self.draw_next()
        else:
            print(e.key())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    main.new_game()
    main.draw_next()
    sys.exit(app.exec_())