
import os.path as pth

from PyQt5 import QtGui

from gui_tens import graph, image
from mgui import widgets as gui
import sys
from PyQt5 import QtWidgets

IMAGE_DIR = '../resource/image'
EXT = '.png'



class Widget(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(500, 500)


        scene_geometry = (0, 0, 500, 500)
        scene_config = {}
        box = gui.Box(gui.Box.horizontal, self)
        self.scene = graph.Scene(scene_geometry, scene_config, IMAGE_DIR)
        self.view = graph.View('graph_tens', self.scene, self, (504, 504))
        box.addWidget(self.view)

    def draw(self, n):
        p = pth.join(IMAGE_DIR, str(n) + EXT)
        pxm = QtGui.QPixmap(p)
        # print(pxm.size().width())
        obj = image.ImageItem(parent=self, scene=self.scene, path=p, name=n)
        obj.allow_edit()

        self.scene.addItem(obj)
        # obj.to_center()
        obj.setScale(0.4)


    # def add_item(self, name):
    #     name = str(name)
    #     p = pth.join(IMAGE_DIR, name + EXT)
    #     obj = graph.GraphicsImage(p, name, self.scene)
    #     # obj.customSignal.connect(self.press)
    #     self.scene.draw(obj)
    #
    # def add_items(self, names_lst):
    #     for n in names_lst:
    #         self.add_item(n)

    def press(self):
        print(self.sender().name)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('settings/style.qss', "r").read())
    main = Widget()
    main.show()
    main.draw("0")
    main.draw("2")
    sys.exit(app.exec_())