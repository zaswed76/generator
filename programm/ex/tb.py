

from tempita import looper
lp = looper([1, 2, 3])

for i in lp:
    print(i.item)