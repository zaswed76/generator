import json
import random
import itertools



class PenaltySeq(list):
    def __init__(self):
        super().__init__()

    def append(self, p_object):
        if not p_object in self:
            super().append(p_object)

class Item(int):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self._weight = 0
        self.max_weight = 10
        self.min_weight = 0
        self.min_time = 0.5
        self.penalty_time = 4.0

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w):
        self._weight = w


    def increase_weight(self, time):
        if self.min_time < time > self.penalty_time:
            if self.weight < self.max_weight:
                self.weight += 1

    def reduce_weight(self):
        if self.weight > self.min_weight:
            self.weight -= 1

    def __repr__(self):
        return "item - {}; weight - {}".format(self.item, self.weight)


class Seq:
    def __init__(self, items_weight=None):
        if items_weight is None:
            self.items_weight = dict.fromkeys(range(0, 100), 0)
        else:
            self.items_weight = items_weight
        self.cursor = -1
        self.__seq = []
        self.cycle = None
        self._shuffle = False
        self.penalty = PenaltySeq()
        self._current_item = None

    @property
    def seq(self):
        return self.__seq

    @seq.setter
    def seq(self, seq):
        self.__seq = seq

    # def set_cycle(self):
    #     self.seq = itertools.cycle(self.seq)

    def shuffle(self, key):
        if key:
            self._shuffle = True

            try:
                random.shuffle(self.seq)
            except Exception as er:
                print(er)
        else:
            self._shuffle = False
            self.__seq.sort()

    def get_ten(self, name):
        items = []
        for name in range(name, name + 10):
            item = Item(name)
            item.weight = self.items_weight[name]
            items.append(item)
        return items

    @property
    def get_keys(self):
        return range(0, 100, 10)

    def set_ten(self, name):
        if name == "K":
            return self.get_keys
        else:
            name = int(name)
            assert name % 10 == 0
            return self.get_ten(name)

    @property
    def next(self):
        if self.cycle:
            if self.cursor == len(self.seq) - 2:
                if self._shuffle:
                    self.shuffle(True)
                self.cursor_reset()
            else:
                self.cursor += 1
        else:
            if self.cursor < len(self.seq) - 1:
                self.cursor += 1
        self._current_item = self.seq[self.cursor]
        return self._current_item

    @property
    def current_item(self):
        return self._current_item

    @property
    def past_item(self):
        return self.seq[self.cursor -1]

    @property
    def prev(self):
        if self.cursor > 0:
            self.cursor -= 1
        return self.seq[self.cursor]

    def init_tens(self, **kwargs: dict):
        """

        :param kwargs: словарь {name_ten, bool}
        """

        self.clear()
        self.cursor_reset()
        for name in kwargs:
            if kwargs[name]:  # если кнопка включена
                self.seq.extend(
                    self.set_ten(name))  # добавить в последовательность
        # загружаем на всякий случай если ошибка
        if not self.seq:
            self.seq.extend(self.set_ten(0))

    def clear(self):
        self.seq.clear()

    def cursor_reset(self):
        self.cursor = -1

    def to_penalty(self, obj):
        self.penalty.append(obj)

def load(path):
    with open(path, "r") as f:
        return json.load(f)


def save(path, obj):
    with open(path, "w") as f:
        json.dump(obj, path)

if __name__ == '__main__':
    s = Seq()

    btn_checked = {
        "0": 0,
        "10": 0,
        "20": 1,
        "30": 0,
        "40": 0,
        "50": 0,
        "60": 0,
        "70": 0,
        "80": 0,
        "90": 0,
        "keys": 0
    }
    s.init_tens(**btn_checked)
    print(s.seq)
