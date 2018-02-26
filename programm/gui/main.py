import json
import os
import sys
import time
from functools import partial

import yaml
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import QObject
from logic import logic
from gui import (base_view, config, tool,
                 game_tool, alt_view,
                 grid_view, gui_settings,
                 timer)

IMAGE_DIR = '../resource/image'
UI_DIR = '../gui/ui'
IMAGE_DIR_KEY = '../resource/images_key_2'
ICON_DIR = '../resource/icon_2'
DEFAULT_CFG = '../cfg/default.json'
INIT_GAME = '../cfg/init_game.json'
ITEMS_WEIGHT = "../cfg/items_weight.yaml"

def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 'INFO'
    elif mode == QtCore.QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtCore.QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    print('qt_message_handler: line: %d, func: %s(), file: %s' % (
          context.line, context.function, context.file))
    print('  %s: %s\n' % (mode, message))

QtCore.qInstallMessageHandler(qt_message_handler)


def path_to_image(self, name, image_dir, ext):

    return os.path.join(image_dir, name + ext)


class GameToolController(QObject):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName(name)

    def __call__(self, **args):
        sender = self.sender()
        name_btn = sender.objectName()
        try:
            getattr(self, name_btn)(btn=sender)
        except AttributeError:
            self.press_ten(name_btn, sender)

    def reset_seq(self, btn=None):
        self.parent.tools["game"].reset_group(
            "group_seq_game")
        self.parent.new_game()

    def all_seq_btns(self, btn=None):
        self.parent.tools["game"].check_all_group(
            "group_seq_game")
        self.parent.new_game()

    def press_ten(self, name_ten, btn):
        name_view = self.parent.stack.currentWidget().objectName()
        if name_view == "base_game":
            self.parent.new_game()
        elif name_view == "alt_1":
            self.parent.alt_scene.clear()
            self.parent.alt_scene.draw(name_ten, "image_mode_btn")

    def exclusive(self, btn=None):
        self._exclusive(btn=None)
        # self.parent.new_game()


    def _exclusive(self, btn=None):
        name_view = self.parent.stack.currentWidget().objectName()
        if name_view == "base_game":
            exclusive_checked = self.parent.tools["game"].btn[
                    'exclusive'].isChecked()
            if exclusive_checked:
                self.parent.tools["top_tool"].groups["group_games"].btn["alt_1"].setDisabled(False)
            else:
                self.parent.tools["top_tool"].groups["group_games"].btn["alt_1"].setDisabled(True)

            self.parent.tools["game"].check_exclusive_group(
                "group_seq_game", exclusive_checked)



        elif name_view == "alt_1":
            self.parent.tools["game"].check_exclusive_group(
                "group_seq_game", True)
            self.parent.tools["game"].btn['exclusive'].setDisabled(
                True)


class ToolController(QObject):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName(name)

    def __call__(self, **args):
        sender = self.sender()
        name_btn = sender.objectName()
        getattr(self, name_btn)(btn=sender)

    def image_mode_btn(self, **args):
        flag = args['btn'].isChecked()
        self.parent.cfg_base['image_mode_btn'] = flag
        self.parent.cfg_base['text_mode_btn'] = not flag
        self.parent.current_mod = 'image_mode_btn'
        self.parent.new_game()

    def text_mode_btn(self, **args):
        flag = args['btn'].isChecked()
        self.parent.cfg_base['text_mode_btn'] = flag
        self.parent.cfg_base['image_mode_btn'] = not flag
        self.parent.current_mod = 'text_mode_btn'
        self.parent.new_game()

    def cycle(self, **args):
        self.parent.seq.cycle = args['btn'].isChecked()
        self.parent.game_reset()

    def help(self, **args):

        self.parent.help = args['btn'].isChecked()

        if not self.parent.help:

            self.parent.scene.del_help_obj()
        else:
            self.parent.draw_help()

    def test(self, **args):
        print("test")

    def time(self, **args):
        flag = self.parent.tools["top_tool"].btn['time'].isChecked()
        if flag:
            self.parent.penalty_release_flag = False
            time = self.parent.cfg_base["interval_slides"] * 1000
            self.parent.start_timer(time)
            self.parent.games["base_game"].setInteractive(True)

        else:
            try:
                self.parent.penalty_release_flag = True
                self.parent.timer.stop()
                self.parent.games["base_game"].setInteractive(False)
            except AttributeError as er:
                print(er)

    def penalty(self, **args):
        self.parent.start_penalty_list()

    def del_penalty(self, **args):
        self.parent.clear_penalty()

    def check_game(self, **args):
        sender = self.sender()
        id = self.parent.games.index(sender.objectName())
        self.parent.cfg_base['game_id'] = id
        self.parent.check_stack(id)

    def base_game(self, **args):
        print("base")
        disabled_btns = ["all_seq_btns", "reset_seq", "exclusive"]
        self.parent.tools["game"].set_disabled_btns(disabled_btns,
                                                    False)
        self.parent.stack.setCurrentWidget(
            self.parent.games["base_game"])
        self.parent.controls["seq_tool"]._exclusive()


    def grid(self, **args):
        print("grid")
        self.parent.stack.setCurrentWidget(self.parent.games["grid"])

    def alt_1(self, **args):
        btns_checked = self.parent.tools["game"].btns_checked_group(
            "group_seq_game")
        current_ten = [k for k, v in btns_checked.items() if v][0]
        self.parent.alt_scene.clear()
        self.parent.alt_scene.draw(current_ten, "image_mode_btn")

        # print(self.parent.tools["game"].get_active_btn())
        disabled_btns = ["all_seq_btns", "reset_seq", "exclusive"]
        self.parent.tools["game"].set_disabled_btns(disabled_btns, True)
        self.parent.stack.setCurrentWidget(self.parent.games["alt_1"])
        self.parent.controls["seq_tool"].exclusive()

    def restart(self, **args):
        self.parent.new_game()

    def shuffle(self, **args):
        flag = self.parent.tools["top_tool"].btn['shuffle'].isChecked()
        self.parent.seq.set_shuffle(flag)
        self.parent.game_reset()

    def game_panel(self, name):
        self.parent.new_game()

    def set_time(self, **args):
        self.parent.set_time()


class Widget(tool.WidgetToolPanel):
    def __init__(self, *args, **kwargs):

        super().__init__()
        init_game_cfg = kwargs["init_game"]
        default_cfg = kwargs["default_cfg"]
        self.image_dir = kwargs["image_dir"]
        self.image_dir_key = kwargs["image_dir_key"]

        self.__init_config(init_game_cfg, default_cfg)
        self.timer_flag = False
        self.penalty_release_flag = True
        self.timer = timer.Timer()
        self.timer.timeout.connect(self.update_timer)

        self.games = dict()
        self.controls = dict()
        # region main_view
        scene_rect = QtCore.QRectF(0, 0, 500, 500)
        self.scene = base_view.Scene(self, scene_rect)
        self.games["base_game"] = base_view.View("base_game",
                                                 self.scene, self,
                                                 (504, 504))
        self.games["base_game"].setInteractive(False)
        self.add_view(self.games["base_game"])
        # endregion

        # region alt_view
        self.alt_scene = alt_view.Scene((0, 0, 500, 500),
                                        self.cfg_base, self.image_dir_key)
        self.games["alt_1"] = alt_view.View("alt_1", self.alt_scene,
                                            self, (504, 504))
        self.games["alt_1"].setInteractive(False)

        self.add_view(self.games["alt_1"])
        # endregion

        self.grid = grid_view.Scene((0, 0, 500, 500),
                                        self.cfg_base, self.image_dir)
        self.games["grid"] = grid_view.View("grid", self.grid,
                                            self, (504, 504))
        self.add_view(self.games["grid"])

        seq = range(100)
        self.seq = logic.Seq(seq)
        self.seq.extend_penalty(self.cfg.conf["penalty_list"])

        self.tools = {}
        self.mode_names = ["image_mode_btn", "text_mode_btn"]
        self.current_mod = self.get_game_mode()
        self.help = self.cfg_base["help"]
        self.set_start_opt()

    @property
    def current_scene(self) ->QtWidgets.QGraphicsScene:
        return self.stack.currentWidget()

    def set_time(self):
        interval = self.cfg_base["interval_slides"]
        self.set_time_window = gui_settings.SetTime(interval)
        result = self.set_time_window.exec_()
        if result == QtWidgets.QDialog.Accepted:
            interval = self.set_time_window.slider.value()
            self.cfg_base["interval_slides"] = interval
        elif result == QtWidgets.QDialog.Rejected:
            pass

    def set_start_opt(self):
        self.start_flag = False
        self.last_time = None

    def get_game_mode(self):
        for name in self.mode_names:
            if self.cfg_base[name]:
                return name

    def __init_game(self):
        self.check_stack(self.cfg_base["game_id"])

    def __init_config(self, init_game, default_cfg):
        self.cfg = config.Config(default_cfg)
        print(default_cfg)
        print(self.cfg.conf)
        self.init_conf = load_cfg(init_game)
        self.cfg.load(self.init_conf["last_cfg"])
        self.cfg_base = self.cfg.conf['base']
        self.cfg_game_tool = self.cfg.conf['game_tool']

    def check_stack(self, index):
        self.stack.setCurrentIndex(index)

    def ctrl(self, name, args):

        self.controls[name].controll(*args)

    def init_game_tool(self):
        self.tools["game"] = game_tool.GameTool(
            self, "game", tool.Tool.DirectVertical,
            self.cfg_game_tool)
        self.set_tool(self.tools["game"],
                      tool.WidgetToolPanel.DirectRight)

    def init_top_tool(self):
        btn_size = (34, 34)
        # панель
        self.tools["top_tool"] = tool.Tool(self, "top_tool",
                                           tool.Tool.DirectHorizontal)

        # region bottons-mode
        image_mode_btn = tool.Button(self.tools["top_tool"],
                                     "image_mode_btn", checkable=True,
                                     exclusive=True)
        image_mode_btn.clicked.connect(self.controls["top_tool"])

        text_mode_btn = tool.Button(self.tools["top_tool"],
                                    "text_mode_btn", checkable=True,
                                    exclusive=True)
        text_mode_btn.clicked.connect(self.controls["top_tool"])

        group_modes = tool.Group("group_modes",
                                 tool.Box(tool.Box.horizontal),
                                 spacing=2)
        group_modes.addWidgets([image_mode_btn, text_mode_btn])
        self.tools["top_tool"].add_group(group_modes)
        # endregion

        restart = tool.Button(self.tools["top_tool"], "restart")
        restart.clicked.connect(self.controls["top_tool"])
        self.tools["top_tool"].add_btn(restart)

        shuffle = tool.Button(self.tools["top_tool"], "shuffle",
                              checkable=True)
        shuffle.clicked.connect(self.controls["top_tool"])
        self.tools["top_tool"].add_btn(shuffle)

        cycle = tool.Button(self.tools["top_tool"], "cycle",
                            checkable=True)
        cycle.clicked.connect(self.controls["top_tool"])
        self.tools["top_tool"].add_btn(cycle)

        help = tool.Button(self.tools["top_tool"], "help",
                           checkable=True)
        help.clicked.connect(self.controls["top_tool"])
        self.tools["top_tool"].add_btn(help)

        test = tool.Button(self.tools["top_tool"], "test",
                           checkable=True)
        test.clicked.connect(self.controls["top_tool"])
        self.tools["top_tool"].add_btn(test)

        time = tool.Button(self.tools["top_tool"], "time",
                           checkable=True)
        set_time_btn = tool.SetBtn((14, 14), name="set_time")
        set_time_btn.clicked.connect(self.controls["top_tool"])
        time.add_setting_btn(set_time_btn)
        time.clicked.connect(self.controls["top_tool"])
        self.tools["top_tool"].add_btn(time)

        penalty = tool.Button(self.tools["top_tool"], "penalty",
                           checkable=True)
        penalty.clicked.connect(self.controls["top_tool"])
        del_penalty = tool.SetBtn((16, 16), name="del_penalty")
        del_penalty.clicked.connect(self.controls["top_tool"])
        penalty.add_setting_btn(del_penalty)
        self.tools["top_tool"].add_btn(penalty)

        self.tools["top_tool"].add_stretch(1)
        # region games
        base_game = tool.Button(self.tools["top_tool"], "base_game",
                                checkable=True,
                                exclusive=True)
        base_game.clicked.connect(self.controls["top_tool"])
        alt_1 = tool.Button(self.tools["top_tool"], "alt_1",
                            checkable=True, exclusive=True)
        alt_1.clicked.connect(self.controls["top_tool"])
        alt_1.setDisabled(self.cfg_base.get("alt_1_enabled", False))

        grid = tool.Button(self.tools["top_tool"], "grid",
                            checkable=True, exclusive=True)
        grid.clicked.connect(self.controls["top_tool"])
        # grid.setDisabled(self.cfg_base.get("grid", False))

        group_games = tool.Group("group_games",
                                 tool.Box(tool.Box.horizontal),
                                 spacing=2)
        group_games.addWidgets([base_game, alt_1, grid])
        self.tools["top_tool"].add_group(group_games)
        # endregion

        self.tools["top_tool"].add_stretch(1)

        # добавить панель на окно
        self.set_tool(self.tools["top_tool"],
                      tool.WidgetToolPanel.DirectTop)

        image_mode_btn.setChecked(self.cfg_base['image_mode_btn'])
        text_mode_btn.setChecked(self.cfg_base['text_mode_btn'])
        shuffle.setChecked(self.cfg_base['shuffle'])

        # инициировать состояние кнопок
        for name, btn in self.tools["top_tool"].all_btns.items():
            btn.setChecked(self.cfg_base.get(name, False))
            self.tools["top_tool"].btn['time'].setChecked(False)



    def init_controller(self, ctrl):
        self.controls[ctrl.objectName()] = ctrl

    def new_game(self):
        self.seq.cycle = self.tools["top_tool"].btn["cycle"].isChecked()
        btns_checked = self.tools["game"].btns_checked_group(
            "group_seq_game")
        btns_name = [k for k, v in btns_checked.items() if v]
        self.seq.init_tens(btns_name)
        self.seq.set_shuffle(self.tools["top_tool"].btn["shuffle"].isChecked())
        self.game_reset()

    def start_penalty_list(self):
        if self.seq.penalty_list:
            if self.tools["top_tool"].btn["penalty"].isChecked():
                self.seq.init_penalty_list()
                self.seq.set_shuffle(self.tools["top_tool"].btn["shuffle"].isChecked())
                self.game_reset()
            else:
                self.new_game()

    def clear_penalty(self):
        self.seq.clear_penalty()
        self.seq.clear()
        self.new_game()
        self.tools["top_tool"].btn["penalty"].setChecked(False)
        self.tools["top_tool"].btn["penalty"].setDisabled(True)



    def game_reset(self):
        self.seq.cursor_reset()
        self.scene.clear()
        self.next_item()

    def note_time(self):
        self.current_time = time.time()

    def start_timer(self, interval):
        self.timer.start(interval)

    def update_timer(self):
        self.penalty_release_flag = False
        self.next_item()


    def next_item(self):

        item, game_go_flag = self.seq.next()
        scene_items = self.current_scene.items()
        if scene_items:
            scene_item = scene_items[0].name
        else:
            scene_item = None
        if game_go_flag:
            if not self.penalty_release_flag and scene_item:
                self.seq.append_penalty(scene_item)
            path = os.path.join(self.image_dir, item + self.cfg_base["ext"])
            self.scene.draw(item, path, self.current_mod)
            if self.help:
                self.draw_help()
        else:
            if not self.penalty_release_flag:
                self.seq.append_penalty(scene_item)
            self.scene.draw_finish()
            if self.timer.isActive():
                self.timer.stop()
                self.tools["top_tool"].btn['time'].setChecked(False)
                self.games["base_game"].setInteractive(False)

        if self.seq.penalty_list:

            self.tools["top_tool"].btn["penalty"].setDisabled(False)
        else:

            self.tools["top_tool"].btn["penalty"].setDisabled(True)

    def prev_item(self):
        pass
        # item, game_go_flag = self.seq.prev()
        # if game_go_flag:
        #     self.scene.draw(item, self.current_mod)
        #     if self.help:
        #         self.draw_help()

    def draw_help(self):
        item = self.seq.current_item.value
        path = os.path.join(self.image_dir, str(item) + self.cfg_base["ext"])
        self.scene.draw_help(item, path, self.current_mod)

    def keyReleaseEvent(self, e):
        print("release")

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            if not e.isAutoRepeat():
                self.draw_help()
            else:
                pass

    # def keyPressEvent(self, e):
    #     if e.key() == QtCore.Qt.Key_Space:
    #         if not e.isAutoRepeat():
    #             self.draw_help  ()



    # def keyReleaseEvent(self, e):
    #     print( e.key())
    #     print(111)
    #     # if e.key() == QtCore.Qt.Key_Space:
    #     #     if not e.isAutoRepeat():
    #     #         self.scene.del_help_obj()

    def chenge_time(self):
        current = time.time()
        if self.last_time is not None:
            change = current - self.last_time
            self.last_time = current
            return round(change, 1)
        else:
            self.last_time = time.time()
            return 0

    def wheelEvent(self, event):
        if event.angleDelta().y() / 120 > 0:
            self.next_item()
            # self.start_flag = True
            # time = self.chenge_time()
            # print(time)
            # self.seq.past_item.increase_weight(time)
            # self.note_time()
        else:
            self.prev_item()

    def closeEvent(self, *args, **kwargs):
        self.update_cfg()
        self.cfg.save(self.init_conf["last_cfg"])

    def update_cfg(self):
        self.tools["top_tool"].btn["penalty"].setChecked(False)
        btns_checked = self.tools["game"].btns_checked_group(
            "group_seq_game")
        self.cfg_game_tool["btn_checked"].update(btns_checked)

        game_btn_checked = self.tools["game"].all_btns_checked
        for n in game_btn_checked:
            if n in self.cfg_game_tool:
                self.cfg_game_tool[n] = game_btn_checked[n]

        tool_btn_checked = self.tools["top_tool"].all_btns_checked
        for n in tool_btn_checked:
            self.cfg_base[n] = tool_btn_checked[n]


        alt_1_enabled = self.tools["top_tool"].groups["group_games"].btn["alt_1"].isEnabled()
        self.cfg_base["alt_1_enabled"] = not alt_1_enabled

        penalty_list_values = [n.value for n in self.seq.penalty_list]
        self.cfg.conf["penalty_list"].clear()
        self.cfg.conf["penalty_list"].extend(penalty_list_values)



def load_yaml(fl):
    with open(fl, "r") as f:
        return yaml.load(f)


def save_yaml(fl, data):
    with open(fl, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


def load_cfg(path):
    with open(path, "r") as f:
        return json.load(f)


def save(path, obj):
    with open(path, "w") as f:
        json.dump(obj, path)




if __name__ == '__main__':
    
    QtCore.qDebug('something informative')
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open('../css/style.css', "r").read())
    main = Widget()
    main.setObjectName('main_seq_game')
    main.show()

    controller = ToolController(main, "top_tool")
    main.init_controller(controller)
    game_tool_controller = GameToolController(main, "seq_tool")
    main.init_controller(game_tool_controller)
    main.init_top_tool()
    main.init_game_tool()

    main.new_game()

    sys.exit(app.exec_())
