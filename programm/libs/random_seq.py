import random
import json


import os


ROOT = os.path.join(os.path.dirname(__file__))

data_file = os.path.join(ROOT, "data", "data.json")

def rand(lenght):
    return [str(random.randint(0, 9)) for _ in range(lenght)]

def generate(lenght):

    d = rand(lenght)
    with open(data_file, "w") as f:
        conf = json.load(f)

def hide():
    print("hide")


def validate():
    repl = input("введите ответ")


df = {1: generate, 2: hide, 3: validate}

def game():
    while True:
        print("""1) генерировать. через пробел - сколько знаков
2) скрыть
3) проверить""")
        repl = input("введите номер")
        if repl.strip().lower() in ["q", "й", "exit", "выход"]:
            print("вы вышли")
            return


if __name__ == '__main__':
    game()