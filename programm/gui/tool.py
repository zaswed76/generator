import sys
from functools import partial

from PyQt5 import QtWidgets, QtGui, QtCore

_box_margin = (0, 0, 0, 0)
_box_spacing = 10

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


class SetBtn(QtWidgets.QPushButton):
    def __init__(self, size, name=None, *__args):
        super().__init__(*__args)
        self.setObjectName(name)
        self.setFixedSize(*size)




class Button(QtWidgets.QPushButton):
    """
    пользовательская кнопка;
    auto_spacing - если size не указан то размер кнопки =
    parent.size - auto_spacing
    """
    auto_spacing = 7
    def __init__(self, layout, name, icon=None, size=None, checkable=False, exclusive=False, icon_size=None):
        """

        :param parent: QtWidgets.QWidget
        :param name: str == objectName
        :param checkable: bool
        :param exclusive: bool
        :param icon: str (path)
        :param size: tuple  < int
        :param icon_size: tuple  < int

         icon_size сработает если указать иконку в пар: icon
         и отключить для этого виджета css стили
        """

        super().__init__()
        self.layout = layout
        self.setCheckable(checkable)
        self.setObjectName(name)
        self.setAutoExclusive(exclusive)
        if icon is not None:
            self.setIcon(QtGui.QIcon(icon))
            self.setIconSize(QtCore.QSize(icon_size[0], icon_size[1]))
        if size is None:  w = h = self.layout.size - Button.auto_spacing
        else: w, h = size
        self.setFixedSize(w, h)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)
        self.setCursor(QtCore.Qt.PointingHandCursor)

        self.setToolTip('{}'.format(self.objectName()))
        QtWidgets.QToolTip.setFont(QtGui.QFont('Verdana', 11))

    def add_setting_btn(self, btn):
        btn.setParent(self)
        par_width = self.size().width()
        btn_width = btn.size().width()
        btn.move(par_width - btn_width, 0)

    def __repr__(self):
        return "{}; name - {}".format(self.__class__, self.objectName())

class Group(QtWidgets.QGroupBox):

    def __init__(self, name, box, spacing=1, exclusive=False):
        """
         контейнер для кнопок; группирует
        :param name: str
        :param spacing: int зазор между кнопками
        """
        super().__init__()
        self.setObjectName(name)
        self.exclusive_flag = exclusive

        self.btn = {}
        self.box = box
        self.box.setSpacing(spacing)
        self.setLayout(self.box)
        self.setStyleSheet("QGroupBox { border: none; }")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def addWidget(self, widget):
        self.btn[widget.objectName()] = widget
        self.box.addWidget(self.btn[widget.objectName()])

    def addWidgets(self, widgets):
        for w in widgets:
            self.addWidget(w)

    def reset(self):
        flag = False
        for btn in self.btn:
            if self.btn[btn].isChecked() and not flag:
                flag = True
                self.btn[btn].setChecked(True)
            else:
                self.btn[btn].setChecked(False)


    def check_all(self):
        if not self.exclusive_flag:
            for btn in self.btn:
                self.btn[btn].setChecked(True)

    def check_exclusive(self, exclusive_checked):

        if exclusive_checked:
            self.exclusive_flag = True
            self.reset()
        else:
            self.exclusive_flag = False
        for btn in self.btn:
            self.btn[btn].setAutoExclusive(self.exclusive_flag)

    def get_btns_checked(self):
        return {n:btn.isChecked() for n, btn in self.btn.items()}

    def __repr__(self):
        return "{}".format(self.btn.keys())

class Tool(QtWidgets.QFrame):
    DirectVertical = "vertical"
    DirectHorizontal = "horizontal"

    def __init__(self, parent, name, direct, size=35):
        """
         панель инструментов
        :param parent: QWidget
        :param name: str == objectName
        :param direct: ToolPanel.DirectVertical or ToolPanel.DirectHorizontal
        :param size: int
        """

        super().__init__(parent)


        self.groups = {}
        self.btn = {}
        self.size = size
        self.parent = parent
        self.setObjectName(str(name))
        self.direct = direct
        if direct == Tool.DirectVertical:
            self.box = Box(Box.vertical, parent=self)
            self.setFixedWidth(size)
        elif direct == Tool.DirectHorizontal:
            self.box = QtWidgets.QHBoxLayout(self)
            self.setFixedHeight(size)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.setToolTip('{}'.format(self.objectName()))
        QtWidgets.QToolTip.setFont(QtGui.QFont('Verdana', 11))

    def add_group(self, widget_group):
        self.groups[widget_group.objectName()] = widget_group
        self.box.addWidget(self.groups[widget_group.objectName()])

    def add_btn(self, widget):
        self.btn[widget.objectName()] = widget
        self.box.addWidget(self.btn[widget.objectName()])

    def add_stretch(self, stretch=0):
        if self.direct == Tool.DirectVertical:
            self.box.addStretch(stretch)
        elif self.direct == Tool.DirectHorizontal:
            self.box.addStretch(stretch)

    def reset_group(self, group_name):
        self.groups[group_name].reset()

    def check_all_group(self, group_name):
        self.groups[group_name].check_all()

    def check_exclusive_group(self, group_name: str, exclusive_checked: bool):
        """

        :param group_name: str
        :param exclusive_checked: bool нажата кнопка или нет
        """

        self.groups[group_name].check_exclusive(exclusive_checked)

    def btns_checked_group(self, group_name):
        return self.groups[group_name].get_btns_checked()

    @property
    def all_btns_checked(self):
        return {n: btn.isChecked() for n, btn in self.all_btns.items() if btn.isCheckable()}

    @property
    def all_btns(self) -> dict:
        btns = {}
        btns.update(self.btn)
        for gr in self.groups:
            btns.update(self.groups[gr].btn)
        return btns

    def set_disabled_btns(self, names_lst, check):
        btns = self.all_btns
        for name in names_lst:
            btns[name].setDisabled(check)

    def set_checked_btns(self, names_lst, check):
        btns = self.all_btns
        for name in names_lst:
            btns[name].setChecked(check)


    def __repr__(self):
        return "{}".format(self.objectName())

class WidgetToolPanel(QtWidgets.QFrame):
    DirectTop = 0
    DirectBottom = -1
    DirectLeft = 2
    DirectRight = 1

    def __init__(self):
        """
         виджет соденжит методы для вствки панелей инструментов
        """
        super().__init__()
        self.tools = {}
        # self.setStyleSheet("background-color: green")
        self.out_box = QtWidgets.QVBoxLayout(self)
        self.out_box.setContentsMargins(0, 0, 0, 0)
        self.out_box.setSpacing(0)

        self.in_box = QtWidgets.QHBoxLayout()
        self.out_box.setContentsMargins(0, 0, 0, 0)
        self.out_box.setSpacing(0)
        self.out_box.addLayout(self.in_box)

        self.stack = QtWidgets.QStackedLayout()
        self.in_box.insertLayout(1, self.stack)

    def set_tool_spacing(self, p_int):
        self.out_box.setSpacing(p_int)

    def add_view(self, widget):
        self.stack.addWidget(widget)

    def set_tool(self, tool_widget, direct):
        self.tools[tool_widget.objectName()] = tool_widget
        if direct in [WidgetToolPanel.DirectTop, WidgetToolPanel.DirectBottom]:
            self.out_box.insertWidget(direct, tool_widget)
        elif direct in [WidgetToolPanel.DirectLeft,
                        WidgetToolPanel.DirectRight]:
            print(direct - 2)
            self.in_box.insertWidget(direct - 2, tool_widget)
        else:
            raise Exception("не правильные параметры - direct")

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_1:
            self.stack.setCurrentIndex(0)
        elif e.key() == QtCore.Qt.Key_2:
            self.stack.setCurrentIndex(1)

    def __repr__(self):
        return "{}".format(self.objectName())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = WidgetToolPanel()
    main.set_tool_spacing(1)
    view = QtWidgets.QFrame()
    view.setStyleSheet("background-color: green")
    view.setFixedSize(500, 500)
    main.add_view(view)

    view2 = QtWidgets.QFrame()
    view2.setStyleSheet("background-color: grey")
    view2.setFixedSize(500, 500)
    main.add_view(view2)

    top_panel = Tool(main, 'top1', Tool.DirectHorizontal)
    top_panel.setStyleSheet("background-color: #D7D7D7")
    main.set_tool(top_panel, WidgetToolPanel.DirectTop)
    btn_group_1 = Group()
    btn_1 = Button("1")
    btn_2 = Button("2")
    btn_3 = Button("3")
    btn_group_1.addWidgets([btn_1, btn_2])
    btn_group_1.addWidget(btn_3)
    top_panel.add_group(btn_group_1)
    main.show()

    # top_panel5 = ToolPanel(main, "right1", ToolPanel.DirectVertical)
    # top_panel5.setStyleSheet("background-color: #848484")
    # main.set_tool(top_panel5, WidgetToolPanel.DirectRight)

    sys.exit(app.exec_())
