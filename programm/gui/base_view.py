import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class Item(QtCore.QObject):
    def __init__(self, name, scene):
        super().__init__()


class GraphicsText(QtWidgets.QGraphicsTextItem):
    def __init__(self, name, scene):
        super().__init__()
        self.name = name
        self.scene = scene
        self.setDefaultTextColor(QtGui.QColor('darkgrey'))
        font = QtGui.QFont()
        font.setFamily('helvetica')
        font.setPointSize(156)
        font.setWeight(63)
        self.setFont(font)
        self.setPlainText(name)


    @property
    def width(self):
        return self.sceneBoundingRect().size().width()

    @property
    def height(self):
        return self.sceneBoundingRect().size().height()

    def to_center(self):
        w = self.scene.width() / 2 - self.width / 2
        h = self.scene.height() / 2 - self.height / 2
        self.setPos(w, h)

    def to_right_top(self):
        pw = self.scene.width() / 2
        w = pw + pw / 2 - self.width / 2 + 95
        ph = self.scene.height() / 2
        h = ph - pw / 2 - self.height / 2 - 95
        self.setPos(w, h)


class GraphicsImage(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, path, name, scene):
        super().__init__()
        self.scene = scene
        self.name = name
        self.path = path
        self._pixmap = QtGui.QPixmap(path)
        self.setPixmap(self._pixmap)
        self.setTransformationMode(
            QtCore.Qt.SmoothTransformation)
        self.setFlag(QtWidgets.QGraphicsPixmapItem.ItemIsMovable)


    @property
    def get_pixmap_size(self):
        width = self._pixmap.size().width()
        height = self._pixmap.size().height()
        return max(width, height)

    def move_start(self):
        size = self.get_pixmap_size
        s = size / 2
        self.setTransformOriginPoint(s, s)

    def set_geometry(self, x=0, y=0, scale=1):
        self.setScale(scale)
        self.setPos(x, y)

    @property
    def width(self):
        return self.sceneBoundingRect().size().width()

    @property
    def height(self):
        return self.sceneBoundingRect().size().height()

    def to_center(self):
        w = self.scene.width() / 2 - self.width / 2
        h = self.scene.height() / 2 - self.height / 2
        self.setPos(w, h)

    def to_right_top(self):
        pw = self.scene.width() / 2
        w = pw + pw / 2 - self.width / 2 + 50
        ph = self.scene.height() / 2
        h = ph - pw / 2 - self.height / 2 - 50
        self.setPos(w, h)


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, geometry, cfg, image_dir, parent=None):
        super().__init__()
        self.image_dir = image_dir
        self.cfg = cfg
        self.parent = parent
        self.setSceneRect(*geometry)

    def draw(self, name, fabric):
        self.clear()
        name = str(name)
        if fabric == 'image_mode_btn':
            path = self.path_to_image(name)
            self.obj = GraphicsImage(path, name, self)
        elif fabric == 'text_mode_btn':
            self.obj = GraphicsText(name, self)
        else:
            raise Exception("нет такого режима")
        self.obj.to_center()
        self.addItem(self.obj)

    def draw_help(self, name, fabric):
        name = str(name)
        if fabric == 'image_mode_btn':
            self.help_obj = GraphicsText(name, self)
        elif fabric == 'text_mode_btn':
            path = self.path_to_image(name)
            self.help_obj = GraphicsImage(path, name, self)
        else:
            print("invalid mode")
            return
        self.help_obj.setScale(0.2)
        self.help_obj.to_right_top()
        self.addItem(self.help_obj)

    def draw_finish(self):
        self.clear()
        self.obj = GraphicsText("FINISH", self)
        font = QtGui.QFont("helvetica", 50)
        self.obj.setFont(font)
        self.obj.to_center()
        self.addItem(self.obj)

    def del_help_obj(self):
        self.removeItem(self.help_obj)

    def path_to_image(self, name):
        p = os.path.join(self.image_dir, name + self.cfg["ext"])
        return p

    def mouseReleaseEvent(self, e):
        if self.obj.name != "FINISH":
            pos = self.obj.pos()
            x = pos.x()
            if x > 41:
                self.parent.next_item()



class View(QtWidgets.QGraphicsView):
    def __init__(self, name, scene, parent, size, *__args):
        super().__init__(*__args)
        self.setObjectName(name)
        self.setScene(scene)
        self.setFixedSize(size[0], size[1])

    def wheelEvent(self, event):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    scene = Scene((0, 0, 500, 500))
    main = View(504, 504)
    main.setScene(scene)
    main.show()
    image_pth = r'D:\save\serg\projects\Cube\generator\resource\exemple\cube.png'
    # image_obj = GraphicsObject.make_image(image_pth, 2, scene)
    # image_obj.setScale(3)
    # image_obj.to_center()
    # scene.addItem(image_obj)
