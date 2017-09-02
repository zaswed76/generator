
from gui import tool
class BaseTool(tool.Tool):
    def __init__(self, parent, name, direct, cfg, size=35):
        super().__init__(parent, name, direct, size=35)
        self.cfg = cfg
        self.parent = parent
        self.size = size
        self.__init_ui()

    def __init_ui(self):
        pass