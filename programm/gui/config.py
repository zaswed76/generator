import json
import os


class Config:
    def __init__(self, default_cfg):
        self.default_cfg = default_cfg
        self.conf = {}
        self._current_load_path = ""

    def __load(self, path, mode="r"):
        with open(path, mode) as f:
            return json.load(f)
    @property
    def current_load_path(self):
        return self._current_load_path

    @current_load_path.setter
    def current_load_path(self, pth):
        self._current_load_path = pth

    def load(self, path=None):
        if path is None:
            self.current_load_path = self.default_cfg
        else: self.current_load_path = path
        try: # если указанный в параметре не загрузился
            cfg = self.__load(self.current_load_path)
        except:
            self.current_load_path = self.default_cfg
            cfg = self.__load(self.current_load_path)
        self.conf.update(cfg)


    def save(self, path):
        if os.path.abspath(path) == self.default_cfg:
            raise Exception('нельзя записывать в default')
        else:
            with open(path, "w") as f:
                json.dump(self.conf, f, indent=4)


if __name__ == '__main__':
    c = Config("../cfg/default.json")
    c.load()
    print(c.conf)
    print(c.current_load_path)


