from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

from PyQt5 import QtWidgets, QtGui, QtCore


class GraphicsImage(QtWidgets.QGraphicsObject):
    my_signal = pyqtSignal()

    def __init__(self, pixmap, scene, name):
        super().__init__()
        self.name = name
        self.scene = scene
        self.pixmap = pixmap
        self.pos().x()
        # self.setFlags(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.allow_edit()

        self.setTransformationMode(
            QtCore.Qt.SmoothTransformation)
    def allow_edit(self):
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable | \
            QtWidgets.QGraphicsItem.ItemIsSelectable | \
            QtWidgets.QGraphicsItem.ItemClipsToShape)

    def boundingRect(self):
        return QtCore.QRectF(self.pos().x(), self.pos().y(), self.pixmap.size().width(),
                             self.pixmap.size().height())

    def paint(self, p, *args):
        p.drawPixmap(0, 0, self.pixmap)

    @property
    def width(self):
        return self.pixmap.size().width()

    @property
    def height(self):
        return self.pixmap.size().height()

    def to_center(self):
        w = self.scene.width() / 2 - self.width / 2
        h = self.scene.height() / 2 - self.height / 2
        self.setPos(w, h)

    def mousePressEvent(self, event):
        self.my_signal.emit()


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, geometry, cfg, image_dir, parent=None):
        super().__init__()
        self.image_dir = image_dir
        self.cfg = cfg
        self.parent = parent
        self.setSceneRect(*geometry)

    def draw(self, obj):
        self.addItem(obj)


class View(QtWidgets.QGraphicsView):
    def __init__(self, name, scene, parent, size, *__args):
        super().__init__(*__args)
        self.setObjectName(name)
        self.setScene(scene)
        self.setFixedSize(size[0], size[1])
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

        self.setRubberBandSelectionMode(QtCore.Qt.ContainsItemShape)

