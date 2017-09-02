
import json

class Config:
    def __init__(self, cfg_path):
        self.cfg_path = cfg_path
        self.cfg = self.load()
        self.x = self.cfg.get('x', 1)

    def load(self):
        try:
            with open(self.cfg_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


if __name__ == '__main__':
    cfg = Config('')
    print(cfg.x)



