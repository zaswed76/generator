import random

import itertools
import yaml


class Item:
    global_count = 0
    def __init__(self, value, weight=0, wmax=10, wmin=0):
        self.wmin = wmin
        self.wmax = wmax
        self._value = value
        self._weight = weight
        self.count = 0

    @property
    def value(self):
        self.count += 1
        Item.global_count += 1
        return self._value

    @value.setter
    def value(self, w):
        raise Exception("setter error")

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w):
        self._weight = w

    def increase_weight(self):
        if self.weight < self.wmax:
            self.weight += 1

    def reduce_weight(self):
        if self.weight > self.wmin:
            self.weight -= 1

    # def __str__(self):
    #     return self.value

    def __gt__(self, other):
        return self.value > other.value
    #
    # def __lt__(self, other):
    #     return self.value < other
    #
    # def __ge__(self, other):
    #     return self.value >= other
    #
    # def __le__(self, other):
    #     return self.value <= other

    def __eq__(self, other):

        return self.value == other


class PenaltyList():
    def __init__(self):
        self.lst = []


    def append(self, item):
        self.lst.append(item)

    def extend(self, iterable):
        self.lst.extend(iterable)

    def lst_values(self):
        if self.lst:
            return [x.value for x in self.lst]
        return []

    def __iter__(self):
        return iter(self.lst)

    def __len__(self):
        return len(self.lst)

    def __contains__(self, item):
        return item in self.lst

    def __repr__(self):
        return str(self.lst)


class Seq(dict):
    def __init__(self, seq, items_weight=None):
        super().__init__()
        self._shuffle = False
        self._cycle = False
        self._current_item = None
        self._last_item = None
        self.game_go = False
        if items_weight is None:
            self.items_weight = dict()
        else:
            self.items_weight = items_weight
        self.work_list = []
        self.penalty_list = PenaltyList()
        self.cursor = -1
        self.update({n: Item(n) for n in seq})

    def _get_ten(self, ten):
        if ten == "K":
            lst = [Item(x) for x in range(0, 100, 10)]
        else:
            ten = int(ten)

            lst = [Item(x) for x in range(ten, ten  + 10)]

        return lst

    def clear(self):
        self.work_list.clear()


    def init_tens(self, tens):
        self.work_list.clear()
        for ten in tens:
            self.work_list.extend(self._get_ten(ten))

    def init_penalty_list(self):
        self.work_list.clear()
        self.work_list.extend(self.penalty_list)

    def next(self)->tuple:
        self.game_go = True
        if self._cycle:
            if self.cursor == len(self.work_list) - 2:
                if self.shuffle:
                    self.set_shuffle(True)
                self.cursor_reset()
            else:
                self.cursor += 1
        else:
            if self.cursor < len(self.work_list):
                self.cursor += 1
        try:
            self._current_item = self.work_list[self.cursor]
            self._last_item = self.work_list[self.cursor-1]
        except IndexError:
            self.game_go = False
            if self.shuffle:
                self.set_shuffle(True)
            self.cursor_reset()
        return str(self._current_item.value), self.game_go

    def prev(self):
        if self.cursor > 0:
            self.cursor -= 1
        self._current_item = self.work_list[self.cursor]
        return str(self._current_item.value), self.game_go

    def add_seq(self, seq):
        self.update({n: Item(n) for n in seq})

    @property
    def current_item(self):
        return self._current_item

    @property
    def last_item(self):
        return self._last_item

    @property
    def cycle(self):
        return self._cycle

    @cycle.setter
    def cycle(self, v):
        self._cycle = v

    @property
    def shuffle(self):
        return self._shuffle


    def set_shuffle(self, key):

        if key:
            self._shuffle = True
            try:
                random.shuffle(self.work_list)
            except Exception as er:
                print(er)
        else:
            self._shuffle = False
            self.work_list.sort()


    def cursor_reset(self):
        self.cursor = -1

    def append_penalty(self, name):
        item = Item(name)
        print(not item in self.penalty_list, 555)
        if not item in self.penalty_list and name != "FINISH":

            self.penalty_list.append(item)

    def extend_penalty(self, penalty_lst=None):
        penalty_item_list = [Item(x) for x in penalty_lst]
        self.penalty_list.extend(penalty_item_list)

    def clear_penalty(self):
        self.penalty_list.clear()



def load_yaml(fl):
    with open(fl, "r") as f:
        return yaml.load(f)

def save_yaml(fl, data):
    with open(fl, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


if __name__ == '__main__':
    pass

    f = Seq(range(100))
    f.add_seq([100, 200, 300])
    print(f.work_list)
    f.init_tens([0])

    print(f.work_list)
    f.shuffle = True
    print(f.work_list)





# r = None
# while r not in ("q", "Q"):
#     r = input(">>>\n")
#     if r == "d":
#
#         print(f.next())
#     elif r == "a":
#         print(f.prev())




